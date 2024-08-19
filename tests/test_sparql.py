import pytest
import rdflib

from respecter.sparql import sparql_query, apply_sparql_query_file


SAMPLE_RDF = """
<https://example.com/Alice> a <https://schema.org/Person> ;
    <https://schema.org/knowsLanguage> "English" .
<https://example.com/Bob> a <https://schema.org/Person> ;
    <https://schema.org/knowsLanguage> "French" .

<https://example.com/SDSC> a <https://schema.org/Organization> ;
    <https://schema.org/knowsLanguage> "English" .
"""

SAMPLE_SPARQL = """
SELECT ?subject WHERE {
    ?subject a <https://schema.org/Person> .
    ?subject <https://schema.org/knowsLanguage> "English" .
}
"""

def test_sparql_query():
    graph = rdflib.Graph()
    graph.parse(data=SAMPLE_RDF, format="ttl")
    query_results = sparql_query(graph, SAMPLE_SPARQL)
    
    bindings = query_results.get("results").get("bindings", []) 
    
    assert len(bindings) == 1
    assert bindings[0].get("subject", {}).get("value", "") == "https://example.com/Alice"

