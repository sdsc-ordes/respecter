"""
This script is only an example of how Jinja2 and Respec can be used to generate an HTML document from a SPARQL query.
This code is not meant to be reused as is, but rather to be used as a starting point for a more complex and complete implementation.
"""

from jinja2 import Environment, FileSystemLoader
import json
import rdflib

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

title = "My Ontology"
author = "John Doe"
url = "https://www.example.com"
abstract = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec odio. Fusce risus nisl, viverra et, tempor et, pretium in, sapien."
introduction = "This is my introduction."
note = "This is a note"


# Load SPARQL query results

with open("data/result.json", "r") as f:
    results = json.load(f)

sections = results.get("results", {}).get("bindings", [])

# # SPARQL query

# SPARQL = """
# PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX dct: <http://purl.org/dc/terms/>
# PREFIX dcat: <https://www.w3.org/TR/vocab-dcat-2/#>
# SELECT ?g ?concept ?prefLabel ?definition
# WHERE{
#     GRAPH ?g {
#       {
#             ?concept skos:prefLabel ?prefLabel .
#             OPTIONAL {
#                 ?concept skos:definition ?definition
#             }
#         }
#         FILTER(!isblank(?concept))
#         FILTER (?g=<https://swissdatacustodian.ch/doc/ontology/contractshapes#>)#||?g=<https://swissdatacustodian.ch/doc/ontology/contractcontrolledlists#>)
#     }
# }
# """

# g = rdflib.Graph()
# g.parse("data/data.ttl", format="turtle")
# results = g.query(SPARQL)
# sections = results.bindings  # ??

sections = format_sections(sections)

# Render template

environment = Environment(loader=FileSystemLoader("templates"))
template = environment.get_template("example.html")

rendered_html = template.render(
    abstract=abstract,
    introduction=introduction,
    note=note,
    sections=sections,
    title=title,
    author=author,
    url=url,
)

# Write rendered template to file
with open("output.html", "w") as f:
    f.write(rendered_html)
