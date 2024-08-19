import pytest
import rdflib

from respecter.sparql import sparql_query, apply_sparql_query_file

LANGUAGES_DATA_FILE_PATH = "tests/data/languages.ttl"
SPARQL_FILE_PATH = "tests/sparql/languages.sparql"

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

def test_apply_sparql_query():
    graph = load_graph()
    query_results = apply_sparql_query_file(graph, SPARQL_FILE_PATH)
    bindings = query_results.get("results").get("bindings", [])

    assert len(bindings) == 1
    assert bindings[0].get("subject", {}).get("value", "") == "https://example.com/Alice"
