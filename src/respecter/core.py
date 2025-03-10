# respecter
# Copyright 2022 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from jinja2 import Environment, FileSystemLoader
import json
import rdflib
import os
from respecter.models import Ontology, Class, Property, Enumeration
from respecter.helpers import (
    extract_classes,
    extract_enumerations,
    extract_properties,
    format_classes,
    format_properties,
    group_format_enumerations,
)
from respecter.sparql import apply_sparql_query_file, SparqlConfig
from typing import List

# Define the SPARQL query to retrieve the concepts
ONTOLOGY_SPARQL = "sparql_queries/sparql_query_ontology.sparql"


def fetch_ontology(ontology_file_path, sparql_config_file_path, debug=False):
    """
    Fetch the ontology from the RDF file and the SPARQL query.
    """
    # Load the turtle file
    graph = rdflib.Graph()
    graph.parse(ontology_file_path)
    
    
    # Load the SPARQL query

    sparql_config = SparqlConfig(sparql_config_file_path)
    
    concepts_query = sparql_config.build_concepts_query()
    

    # Save the query to a file (for debugging)
    if debug:
        os.makedirs("debug", exist_ok=True)
        filename = "debug/sparql_query_file.sparql"
        with open(filename, "w") as file:
            # Load the SPARQL query
            file.write(concepts_query)
            print(f"SPARQL query saved to file: {filename}")

    ontology_query_result = apply_sparql_query_file(graph, ONTOLOGY_SPARQL)
    concepts_query_result = graph.query(concepts_query).serialize(format="json")
    concepts_query_result = json.loads(concepts_query_result)
    

    enumerations_query = sparql_config.build_enumerations_query()
    enumerations_query_result = graph.query(enumerations_query).serialize(format="json")
    enumerations_query_result = json.loads(enumerations_query_result)

    ontology_metadata = ontology_query_result.get("results", {}).get("bindings", [])
    
    concepts_data = concepts_query_result.get("results", {}).get("bindings", [])
    enumerations_data = enumerations_query_result.get("results", {}).get("bindings", [])

    concepts = extract_classes(
        concepts_data,
        qname=graph.qname,
        current_ontology_url=sparql_config.get_uri_base()
        
        + sparql_config.get_uri_separator(),
    )
    properties = extract_properties(
        concepts_data,
        qname=graph.qname,
        current_ontology_url=sparql_config.get_uri_base()
        + sparql_config.get_uri_separator(),
    )
    enumerations = extract_enumerations(
        enumerations_data,
        qname=graph.qname,
        current_ontology_url=sparql_config.get_uri_base()
        + sparql_config.get_uri_separator(),
    )
    ontology = Ontology()
    ontology.import_from_rdf(ontology_metadata[0])
   
    return ontology, concepts, properties, enumerations

def fix_prefixes(rendered_html):
    """
    Fixes a bug caused by rdflib replacing the prefix "schema" with "schema1".
    """
    if "schema1" in rendered_html:
        rendered_html = rendered_html.replace("schema1", "schema")
    return rendered_html

def render_template(
    ontology: Ontology,
    concepts: List[Class],
    properties: List[Property],
    enumerations: List[Enumeration],
):
    grouped_enumerations = group_format_enumerations(enumerations)
    environment = Environment(loader=FileSystemLoader("templates"))
    template = environment.get_template("example.html")
    # Render the template
    rendered_html = template.render(
        concepts=format_classes(concepts),
        ontology=ontology.to_dict(),
        properties=format_properties(properties),
        grouped_enumerations=grouped_enumerations,
    )
    rendered_html = fix_prefixes(rendered_html)
    return rendered_html
