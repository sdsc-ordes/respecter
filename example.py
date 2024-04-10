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
CONCEPTS_SPARQL = "data/sparql_query_concepts.sparql"
ONTOLOGY_SPARQL = "data/sparql_query_ontology.sparql"

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
    definition: str = ""
    property: str = ""
    domain: set = field(default_factory=set)
    range: set = field(default_factory=set)

    def add_domain(self, domain):
        self.domain.add(domain)

    def add_range(self, range):
        self.range.add(range)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "Property": self.property,
            "Domain": ", ".join(self.domain),
            "Range": ", ".join(self.range),
        }


@dataclass
class Class:
    """
    Class to store the class metadata.
    """

    label: str = ""
    definition: str = ""
    term: str = ""
    property: set = field(default_factory=set)

    def add_property(self, property):
        self.property.add(property)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "Term": self.term,
            "Property": ", ".join(self.property),
        }


# Define functions


def format_value(value, qname=None):
    """
    Format the value to be used in the template.
    """
    # FIXME: the following section is a hack to have a working example.
    # This should be done differently and follow the Respec syntax for URLs.
    if value["type"] == "uri":
        if qname:
            value_string = qname(value["value"])
        else:
            value_string = value["value"]
        return '<a href="' + value["value"] + '">' + value_string + "</a>"
    elif value["type"] == "literal":
        return value["value"]
    else:  # FIXME: handle other types
        return value["value"]


def extract_properties(rdf_properties, qname):
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
        current_property.definition = format_value(
            property.get("propertyDefinition", {}), qname=qname
        )

        current_property.property = format_value(
            property.get("property", {}), qname=qname
        )
        current_property.add_domain(
            format_value(property.get("domain", {}), qname=qname)
        )
        current_property.add_range(format_value(property.get("range", {}), qname=qname))

        properties[label] = current_property
    return properties


def format_properties(rdf_properties, qname):
    """
    Format the properties to be used in the template.
    """
    properties = extract_properties(rdf_properties, qname)
    return [property.to_dict() for property in properties.values()]


def extract_classes(rdf_classes, qname):
    """
    Extract the classes from the RDF data.
    """
    classes = dict()
    for rdf_class in rdf_classes:
        label = rdf_class.get("classLabel", {}).get("value", "")
        if label not in classes:
            classes[label] = Class()

        current_class = classes[label]
        current_class.label = label
        current_class.definition = format_value(
            rdf_class.get("classDefinition", {}), qname=qname
        )
        current_class.term = format_value(rdf_class.get("domain", {}), qname=qname)
        current_class.add_property(
            format_value(rdf_class.get("property", {}), qname=qname)
        )

        classes[label] = current_class
    return classes


def format_classes(rdf_classes, qname):
    """
    Format the classes to be used in the template.
    """
    classes = extract_classes(rdf_classes, qname)
    return [class_.to_dict() for class_ in classes.values()]


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
