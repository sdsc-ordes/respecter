from jinja2 import Environment, FileSystemLoader
import json
import rdflib
import os
from models import Ontology, Class, Property, Enumeration
from helpers import (
    extract_classes,
    extract_enumerations,
    extract_properties,
    format_classes,
    format_properties,
    format_enumerations,
    group_format_enumerations,
)
from sparql import (
    apply_sparql_query_file,
    build_concepts_query,
    build_enumerations_query,
)
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

    concepts_query = build_concepts_query(sparql_config_file_path)

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

    enumerations_query = build_enumerations_query(sparql_config_file_path)
    enumerations_query_result = graph.query(enumerations_query).serialize(format="json")
    enumerations_query_result = json.loads(enumerations_query_result)

    ontology_metadata = ontology_query_result.get("results", {}).get("bindings", [])
    concepts_data = concepts_query_result.get("results", {}).get("bindings", [])
    enumerations_data = enumerations_query_result.get("results", {}).get("bindings", [])

    concepts = extract_classes(concepts_data, qname=graph.qname)
    properties = extract_properties(concepts_data, qname=graph.qname)
    enumerations = extract_enumerations(enumerations_data, qname=graph.qname)

    ontology = Ontology()
    ontology.import_from_rdf(ontology_metadata[0])

    return ontology, concepts, properties, enumerations


def render_template(
    ontology: Ontology,
    concepts: List[Class],
    properties: List[Property],
    enumerations: List[Enumeration],
):
    grouped_enumerations = group_format_enumerations(enumerations)
    print(grouped_enumerations)
    environment = Environment(loader=FileSystemLoader("templates"))
    template = environment.get_template("example.html")
    # Render the template
    rendered_html = template.render(
        concepts=format_classes(concepts),
        ontology=ontology.to_dict(),
        properties=format_properties(properties),
        grouped_enumerations=grouped_enumerations,
    )

    return rendered_html
