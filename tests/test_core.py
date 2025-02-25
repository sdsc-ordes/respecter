import pytest

from respecter.core import fix_prefixes

def test_fix_prefixes():
    input_html = """
    ex:Bob a schema1:Person
    """
    expected_html = """
    ex:Bob a schema:Person
    """
    assert fix_prefixes(input_html) == expected_html
