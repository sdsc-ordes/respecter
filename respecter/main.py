"""
This script is only an example of how Jinja2 and Respec can be used to generate an HTML document from a SPARQL query.
This code is not meant to be reused as is, but rather to be used as a starting point for a more complex and complete implementation.
"""

from jinja2 import Environment, FileSystemLoader
import json
import rdflib
import os
from models import Ontology
from helpers import format_classes, format_properties
from sparql import apply_sparql_query_file, build_sparql_query

# Constants

# Define the SPARQL query to retrieve the concepts
ONTOLOGY_SPARQL = "sparql/sparql_query_ontology.sparql"
DEBUG = False


# Define functions


# Execute SPARQL query and retrieve results

# Load the turtle file
graph = rdflib.Graph()
graph.parse("data/data_new.ttl", format="turtle")
# Load the SPARQL query

config_file_path = "config/sparql_config.yaml"
concepts_query = build_sparql_query(config_file_path)

# Save the query to a file (for debugging)
if DEBUG:
    os.makedirs("debug", exist_ok=True)
    filename = "debug/sparql_query_file.sparql"
    with open(filename, "w") as file:
        # Load the SPARQL query
        file.write(concepts_query)
        print(f"SPARQL query saved to file: {filename}")


# Load the SPARQL query
with open(ONTOLOGY_SPARQL, "r") as file:
    ont_query = file.read()

concepts_query_result = graph.query(concepts_query)
concepts_query_result = concepts_query_result.serialize(format="json")
concepts_query_result = json.loads(concepts_query_result)
ontology_query_result = apply_sparql_query_file(graph, ONTOLOGY_SPARQL)

ontology_metadata = ontology_query_result.get("results", {}).get("bindings", [])
ontology_data = concepts_query_result.get("results", {}).get("bindings", [])

concepts = format_classes(ontology_data, qname=graph.qname)
properties = format_properties(ontology_data, qname=graph.qname)


ontology = Ontology()
ontology.import_from_rdf(ontology_metadata[0])

# Render template

environment = Environment(loader=FileSystemLoader("templates"))
template = environment.get_template("example.html")

# Render the template
rendered_html = template.render(
    concepts=concepts,
    ontology=ontology.to_dict(),
    properties=properties,
)

# Write rendered template to file
with open("output.html", "w") as f:
    f.write(rendered_html)
