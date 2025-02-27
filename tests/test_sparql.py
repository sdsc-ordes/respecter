from pathlib import Path
import pytest
import rdflib

from respecter.sparql import sparql_query, SparqlConfig

LANGUAGES_DATA_FILE_PATH = Path("tests/data/languages.ttl")
SPARQL_FILE_PATH = Path("tests/sparql/languages.sparql")
SPARQL_CONFIG_FILE_PATH = Path("tests/config/sparql_config.yaml")

SAMPLE_SPARQL = """
SELECT ?subject WHERE {
    ?subject a <https://schema.org/Person> .
    ?subject <https://schema.org/knowsLanguage> "English" .
}
"""

def load_graph():
    graph = rdflib.Graph()
    graph.parse(LANGUAGES_DATA_FILE_PATH, format="ttl")
    return graph

def test_sparql_query():
    graph = load_graph()
    query_results = sparql_query(graph, SAMPLE_SPARQL)
    bindings = query_results.get("results").get("bindings", []) 
    
    assert len(bindings) == 1
    assert bindings[0].get("subject", {}).get("value", "") == "https://example.com/Alice"

def test_load_sparql_config():
    sparql_config = SparqlConfig.from_path(SPARQL_CONFIG_FILE_PATH)
    assert sparql_config.get_uri_base() == "https://example.com"
    assert sparql_config.get_uri_separator() == "/"
    assert sparql_config.get_type("class") == "<http://www.w3.org/2000/01/rdf-schema#Class>"
    assert sparql_config.get_type("property") == "<http://www.w3.org/1999/02/22-rdf-syntax-ns#Property>"
    assert sparql_config.get_type("enumeration") == "<https://epfl.ch/example/EnumerationType>"
    assert sparql_config.get_predicate("definition") == "<http://www.w3.org/2000/01/rdf-schema#comment>"
    assert sparql_config.get_predicate("example") == "<http://www.w3.org/2004/02/skos/core#example>"
    assert sparql_config.get_predicate("label") == "<http://www.w3.org/2000/01/rdf-schema#label>"
