import pytest

from helpers import extract_fragment_identifier, format_value


def test_extract_fragment_identifier():
    assert extract_fragment_identifier("https://example.com/respecter", "/") == "respecter"
    assert extract_fragment_identifier("https://example.com#respecter", "#") == "respecter"

def test_format_value():
    assert format_value({"type": "uri", "value": "https://example.com/respecter"}, 
                        current_ontology_url="https://example.com/") == '<a href="#respecter">https://example.com/respecter</a>'
    assert format_value({"type": "uri", "value": "https://example.com/respecter"},
                        current_ontology_url="https://my-other-example.com/") == '<a href="https://example.com/respecter">https://example.com/respecter</a>'
    assert format_value({"type": "litteral", "value": "Respecter"}) == "Respecter"
