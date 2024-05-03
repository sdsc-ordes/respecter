import json
import yaml
from dataclasses import dataclass, field


@dataclass
class SparqlConfig:
    """
    Class to store the configuration metadata.

    Args:
        config_file_path (str): Path to the YAML file containing SPARQL predicate definitions.

    Attributes:
        types (dict): A dictionary of types.
        predicates (dict): A dictionary of predicates.
    """

    types: dict = field(default_factory=dict)
    predicates: dict = field(default_factory=dict)

    def __init__(self, config_file_path):
        """
        Initialize the SparqlConfig class.

        Args:
            config_file_path (str): Path to the YAML file containing SPARQL predicate definitions.

        Raises:
            ValueError: If the "type" or "predicate" elements are not found in the config file.
        """
        with open(config_file_path, "r") as f:
            _yaml_config = yaml.load(f, Loader=yaml.FullLoader)
        if "type" not in _yaml_config:
            raise ValueError('Element "type" not found in config file')
        if "predicate" not in _yaml_config:
            raise ValueError('Element "predicate" not found in config file')

        self.types = _yaml_config["type"]
        self.predicates = _yaml_config["predicate"]

    def get_type(self, type_name):
        """
        Get the type URI from the config file.
        """
        if type_name not in self.types:
            raise ValueError(f"Type {type_name} not found in config file")
        return self.types.get(type_name)

    def get_predicate(self, predicate_name):
        """
        Get the predicate URI from the config file.
        """
        if predicate_name not in self.predicates:
            raise ValueError(f"Predicate {predicate_name} not found in config file")
        return self.predicates.get(predicate_name)

def build_enumerations_query(config_file_path: str) -> str:
    """
    Builds a SPARQL query string for enumerations based on a YAML configuration file.

    Args:
        config_file_path (str): Path to the YAML file containing SPARQL predicate definitions.

    Returns:
        str: The complete SPARQL query string for enumerations.
    """

    config = SparqlConfig(config_file_path)

    enumerations_query = (
        """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <https://www.w3.org/TR/vocab-dcat-2/#>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX vann: <http://purl.org/vocab/vann/>
        prefix schema: <http://schema.org/>
        prefix sd: <https://w3id.org/okn/o/sd#>
        prefix bio: <https://bioschemas.org/>
        prefix spe: <https://openschemas.github.io/spec-container/specifications/>
        prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix sh:   <http://www.w3.org/ns/shacl#>
        prefix xsd:  <http://www.w3.org/2001/XMLSchema#> 
        prefix shsh: <http://www.w3.org/ns/shacl-shacl#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix dcterms: <http://purl.org/dc/terms/> 
        prefix ex: <https://epfl.ch/example/> 
        prefix md4i: <http://w3id.org/nfdi4ing/metadata4ing#>

        SELECT DISTINCT ?enumerationValue ?enumerationLabel ?enumerationDefinition ?property ?propertyLabel ?group ?groupLabel
        WHERE { {
        ?propertyShape a sh:PropertyShape .
                ?propertyShape sh:path ?property.
                OPTIONAL{
                    ?property """ + config.get_predicate("label") + """ ?propertyLabel}
        { 
            ?propertyShape sh:class ?group .
            ?group rdfs:subClassOf """ + config.get_type("enumeration") + """ .
            ?enumerationValue a ?group .
                    ?group """ + config.get_predicate("label") + """ ?groupLabel .
                    OPTIONAL{?enumerationValue """ + config.get_predicate("definition") + """ ?enumerationDefinition .}
                    OPTIONAL{?enumerationValue """ + config.get_predicate("label") + """ ?enumerationLabel.}
        }
        UNION
        {
            ?propertyShape sh:or/rdf:rest*/rdf:first/sh:class ?enumerationType2 .
            ?enumerationType2 rdfs:subClassOf """ + config.get_type("enumeration") + """.
            ?enumerationValue a ?enumerationType2 .
                    OPTIONAL{?enumerationValue """ + config.get_predicate("label") +""" ?enumerationDefinition .}
                        OPTIONAL{?enumerationValue """ + config.get_predicate("label") +""" ?enumerationLabel.}
                        
        }
        }
            BIND(coalesce(?enumerationType1, ?enumerationType2) as ?range)
            ?range """+ config.get_predicate("label") + """ ?rangeLabel.
            ?range """+ config.get_predicate("definition") + """ ?rangeDefinition.
        }
        """
        )

    return enumerations_query


def build_concepts_query(config_file_path: str) -> str:
    """
    Builds a SPARQL query string for concepts based on a YAML configuration file.

    Args:
        config_file_path (str): Path to the YAML file containing SPARQL predicate definitions.

    Returns:
        str: The complete SPARQL query string for concepts.
    """

    config = SparqlConfig(config_file_path)

    sparql_query = (
        """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <https://www.w3.org/TR/vocab-dcat-2/#>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX vann: <http://purl.org/vocab/vann/>
        prefix schema: <http://schema.org/>
        prefix sd: <https://w3id.org/okn/o/sd#>
        prefix bio: <https://bioschemas.org/>
        prefix spe: <https://openschemas.github.io/spec-container/specifications/>
        prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix sh:   <http://www.w3.org/ns/shacl#>
        prefix xsd:  <http://www.w3.org/2001/XMLSchema#> 
        prefix shsh: <http://www.w3.org/ns/shacl-shacl#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix dcterms: <http://purl.org/dc/terms/> 
        prefix ex: <https://epfl.ch/example/> 
        prefix md4i: <http://w3id.org/nfdi4ing/metadata4ing#>
        
        SELECT ?domain ?classLabel ?classDefinition ?property ?propertyLabel ?propertyDefinition ?range ?example
        WHERE{
        
        ?nodeshape sh:property ?propertyShape .
        
        

        ?property a """
        + config.get_type("property")
        + """.
        ?property """
        + config.get_predicate("definition")
        + """ ?propertyDefinition.
        ?property """
        + config.get_predicate("label")
        + """ ?propertyLabel.

        ?propertyShape a sh:PropertyShape .
        ?propertyShape sh:path ?property .

        OPTIONAL {?property skos:example ?example}
        OPTIONAL {?propertyShape sh:datatype ?datatype}
        OPTIONAL {?propertyShape sh:class ?classRestriction}
        OPTIONAL {?propertyShape sh:or/rdf:rest*/rdf:first ?option .
                ?option ?pred ?thing .}
        OPTIONAL {?nodeshape sh:property ?property .}
        OPTIONAL{?nodeshape sh:targetClass ?domain1 .}
        BIND(COALESCE(?domain1,?nodeshape) as ?domain).
        ?domain """
        + config.get_predicate("label")
        + """ ?classLabel .
        ?domain """
        + config.get_predicate("definition")
        + """ ?classDefinition.
        BIND(COALESCE(?thing,?classRestriction,?datatype) AS ?range)}
        """
        )

    return sparql_query

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
