"""
This script is only an example of how Jinja2 and Respec can be used to generate an HTML document from a SPARQL query.
This code is not meant to be reused as is, but rather to be used as a starting point for a more complex and complete implementation.
"""

from jinja2 import Environment, FileSystemLoader
import json
import rdflib
import pandas as pd
# Define functions


def format_sections(sections):
    """
    Format the sections to be used in the template.
    """
    output = []
    for section in sections:
        current_section = {}
        for key in section:
            if section[key]["type"] == "uri":
                # FIXME: the following section is a hack to have a working example.
                # This should be done differently and follow the Respec syntax for URLs.
                current_section[key] = (
                    '<a href="'
                    + section[key]["value"]
                    + '">'
                    + section[key]["value"]
                    + "</a>"
                )
            elif section[key]["type"] == "literal":
                current_section[key] = section[key]["value"]
        output.append(current_section)
    return output


# Hardcoded variables

# Execute SPARQL query and retrieve results

# Load the turtle file
graph = rdflib.Graph()
graph.parse("C:/Users/franken/respecter/data/data.ttl", format="turtle")

# Load the SPARQL query
f = open("C:/Users/franken/respecter/data/sparql_query.sparql", "r")
query = f.read()

# Load the SPARQL query
f2 = open("C:/Users/franken/respecter/data/sparql_query2.sparql", "r")
query2 = f2.read()

qres = graph.query(query)
qres = qres.serialize(format="json")
qres = json.loads(qres)
qres2 = graph.query(query2)
qres2 = qres2.serialize(format="json")
qres2 = json.loads(qres2)

sections = qres.get("results", {}).get("bindings", [])
ont_sections = qres2.get("results", {}).get("bindings", [])
sections = format_sections(sections)

# Render template
contributors = ont_sections[0].get("contributors", "")["value"]
contributors = contributors.split("\n")
creators = ont_sections[0].get("creators", "")["value"]
creators = creators.split("\n")
environment = Environment(loader=FileSystemLoader("templates"))
template = environment.get_template("example.html")

print(sections)

ont_sections=ont_sections[0]
rendered_html = template.render(
    abstract=ont_sections.get("abstract", "")["value"],
    introduction=ont_sections.get("description", "")["value"],
    sections=sections,
    title=ont_sections.get("title", "")["value"],
    contributors = contributors,
    creators = creators,
    publishDate = ont_sections.get("modified", "")["value"],
)

# Write rendered template to file
with open("output.html", "w") as f:
    f.write(rendered_html)
