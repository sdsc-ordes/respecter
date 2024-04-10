"""
This script is only an example of how Jinja2 and Respec can be used to generate an HTML document from a SPARQL query.
This code is not meant to be reused as is, but rather to be used as a starting point for a more complex and complete implementation.
"""

from jinja2 import Environment, FileSystemLoader
import json
import rdflib
from dataclasses import dataclass, field

# Constants

# Define the SPARQL query to retrieve the concepts
CONCEPTS_SPARQL = "data/sparql_query.sparql"
ONTOLOGY_SPARQL = "data/sparql_ont_query.sparql"
PROPERTIES_SPARQL = "data/prop_query.sparql"

# Define Classes


@dataclass
class Ontology:
    """
    Class to store the ontology metadata.
    """

    title: str = ""
    introduction: str = ""
    abstract: str = ""
    publishDate: str = ""
    contributors: list = field(default_factory=list)
    creators: list = field(default_factory=list)

    def to_dict(self):
        return {
            "title": self.title,
            "introduction": self.introduction,
            "abstract": self.abstract,
            "publishDate": self.publishDate,
            "contributors": self.contributors,
            "creators": self.creators,
        }

    def import_from_rdf(self, rdf_ontology):
        self.title = rdf_ontology.get("title", {}).get("value", "")
        self.introduction = rdf_ontology.get("description", {}).get("value", "")
        self.abstract = rdf_ontology.get("abstract", {}).get("value", "")
        self.publishDate = rdf_ontology.get("modified", {}).get("value", "")
        self.contributors = (
            rdf_ontology.get("contributors", {}).get("value", "").split("\n")
        )
        self.creators = rdf_ontology.get("creators", {}).get("value", "").split("\n")


@dataclass
class Property:
    """
    Class to store the property metadata.
    """

    label: str = ""
    description: str = ""
    property: str = ""
    domains: set = field(default_factory=set)
    ranges: set = field(default_factory=set)

    def add_domain(self, domain):
        self.domains.add(domain)

    def add_range(self, range):
        self.ranges.add(range)

    def to_dict(self):
        return {
            "label": self.label,
            "description": self.description,
            "property": self.property,
            "domains": ", ".join(self.domains),
            "ranges": ", ".join(self.ranges),
        }


# Define functions


def format_value(value):
    """
    Format the value to be used in the template.
    """
    # FIXME: the following section is a hack to have a working example.
    # This should be done differently and follow the Respec syntax for URLs.
    if value["type"] == "uri":
        return '<a href="' + value["value"] + '">' + value["value"] + "</a>"
    elif value["type"] == "literal":
        return value["value"]
    else:  # FIXME: handle other types
        return value["value"]


def format_section(sections):
    """
    Format the sections to be used in the template.
    """
    output = []
    for section in sections:
        current_section = {}
        for key in section:
            current_section[key] = format_value(section[key])
        output.append(current_section)
    return output


def extract_properties(rdf_properties):
    """
    Extract the properties from the RDF data.
    """
    properties = dict()
    for property in rdf_properties:
        label = property.get("propertyLabel", "")["value"]
        if label not in properties:
            properties[label] = Property()

        current_property = properties[label]
        current_property.label = label
        current_property.description = format_value(
            property.get("propertyDefinition", {})
        )

        current_property.property = format_value(property.get("property", {}))
        current_property.add_domain(format_value(property.get("domain", {})))
        current_property.add_range(format_value(property.get("range", {})))

        properties[label] = current_property
    return properties


def format_properties(rdf_properties):
    """
    Format the properties to be used in the template.
    """
    properties = extract_properties(rdf_properties)
    return [property.to_dict() for property in properties.values()]


def format_class(rdf_class):
    """
    Format the class to be used in the template.
    """
    return NotImplementedError


def sparql_query(graph, query):
    """
    Execute a SPARQL query on a graph and return the results.
    """
    query_result = graph.query(query)
    query_result = query_result.serialize(format="json")
    query_result = json.loads(query_result)
    return query_result


def apply_sparql_query_file(graph, sparql_filename):
    """
    Execute a SPARQL query on a graph and return the results.
    """
    # Load the SPARQL query
    with open(sparql_filename, "r") as f:
        query = f.read()
    return sparql_query(graph, query)


def debug_sparql_query(file):
    """
    Load the results of a SPARQL query from a file.
    """
    with open(file, "r") as f:
        return json.load(f)


# Execute SPARQL query and retrieve results

# Load the turtle file
graph = rdflib.Graph()
graph.parse("data/respec-ontology-shapes.ttl", format="turtle")

# Execute the SPARQL query
concepts_query_result = apply_sparql_query_file(graph, CONCEPTS_SPARQL)
ont_query_result = apply_sparql_query_file(graph, ONTOLOGY_SPARQL)
properties_result = debug_sparql_query("data/prop_result.json")
# properties_result = apply_sparql_query_file(graph, PROPERTIES_SPARQL)

classes_section = concepts_query_result.get("results", {}).get("bindings", [])
ont_section = ont_query_result.get("results", {}).get("bindings", [])
properties_section = properties_result.get("results", {}).get("bindings", [])

concepts = format_section(classes_section)
properties = format_properties(properties_section)

ontology = Ontology()
ontology.import_from_rdf(ont_section[0])

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
