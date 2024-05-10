from jinja2 import Environment, FileSystemLoader
import json
import rdflib
import os
from models import Ontology, Class, Property, Enumeration
from helpers import format_classes, format_properties, format_enumerations
from sparql import apply_sparql_query_file, build_sparql_query
from typing import List

# Define the SPARQL query to retrieve the concepts
ONTOLOGY_SPARQL = "sparql/sparql_query_ontology.sparql"
ENUMERATIONS_SPARQL = "sparql/sparql_query_enumerations.sparql"


def fetch_ontology(ontology_file_path, sparql_config_file_path, debug=False):
    """
    Fetch the ontology from the RDF file and the SPARQL query.
    """
    # Load the turtle file
    graph = rdflib.Graph()
    graph.parse(ontology_file_path, format="turtle")  # TODO: accept other formats
    # Load the SPARQL query

    concepts_query = build_sparql_query(sparql_config_file_path, "concepts")

    # Save the query to a file (for debugging)
    if debug:
        os.makedirs("debug", exist_ok=True)
        filename = "debug/sparql_query_file.sparql"
        with open(filename, "w") as file:
            # Load the SPARQL query
            file.write(concepts_query)
            print(f"SPARQL query saved to file: {filename}")

    concepts_query_result = graph.query(concepts_query)
    concepts_query_result = concepts_query_result.serialize(format="json")
    concepts_query_result = json.loads(concepts_query_result)

    enumerations_query = build_sparql_query(sparql_config_file_path, "enumerations")
    enumerations_query_result = graph.query(enumerations_query)
    enumerations_query_result = enumerations_query_result.serialize(format="json")
    enumerations_query_result = json.loads(enumerations_query_result)
    enumerations_data = enumerations_query_result.get("results", {}).get("bindings", [])

    ontology_query_result = apply_sparql_query_file(graph, ONTOLOGY_SPARQL)

    ontology_metadata = ontology_query_result.get("results", {}).get("bindings", [])
    ontology_data = concepts_query_result.get("results", {}).get("bindings", [])

    concepts = format_classes(ontology_data, qname=graph.qname)
    properties = format_properties(ontology_data, qname=graph.qname)
    enumerations = format_enumerations(enumerations_data, qname=graph.qname)

    ontology = Ontology()
    ontology.import_from_rdf(ontology_metadata[0])

    return ontology, concepts, properties, enumerations


def render_template(
    ontology: Ontology,
    concepts: List[Class],
    properties: List[Property],
    enumerations: List[Enumeration],
):
    # Render template

    environment = Environment(loader=FileSystemLoader("templates"))
    template = environment.get_template("example.html")
    # Render the template
    rendered_html = template.render(
        concepts=concepts,
        ontology=ontology.to_dict(),
        properties=properties,
        enumerations=enumerations,
    )

    return rendered_html
