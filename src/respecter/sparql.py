from pathlib import Path
import json
import yaml
from dataclasses import dataclass, field
from respecter import defaults

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
    ontology: dict = field(default_factory=dict)


    @classmethod
    def default(cls):
        """
        Initialize the SparqlConfig class with default values.
        """
        return cls.parse(defaults.CONFIG)


    @classmethod
    def from_path(cls, config_path: Path):
        """
        Initialize the SparqlConfig class.

        Args:
            config_file_path (str): Path to the YAML file containing SPARQL predicate definitions.

        Raises:
            ValueError: If the "type" or "predicate" elements are not found in the config file.
        """
        with open(config_path, "r") as f:
            return cls.parse(f.read())


    @classmethod
    def parse(cls, config: str):
        """
        Initialize the SparqlConfig class.
        Args:
            config (str): A YAML string containing the config data.
        """
        _yaml_config = yaml.load(config, Loader=yaml.FullLoader)
        return cls(
            types=_yaml_config["type"], 
            predicates=_yaml_config["predicate"],
            ontology=_yaml_config["ontology"],
        )

    def get_uri_base(self):
        """
        Get the ontology URI from the config file.
        """
        return self.ontology.get("uri_base")

    def get_uri_separator(self):
        """
        Get the ontology URI separator from the config file.
        """
        return self.ontology.get("separator")

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

    def build_enumerations_query(self) -> str:
        """
        Builds a SPARQL query string for enumerations.

        Returns:
            str: The complete SPARQL query string for enumerations.
        """

        enumerations_query = (
            """
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat: <https://www.w3.org/TR/vocab-dcat-2/#>
            PREFIX vann: <http://purl.org/vocab/vann/>
            prefix schema: <http://schema.org/>
            prefix sd: <https://w3id.org/okn/o/sd#>
            prefix bio: <https://bioschemas.org/>
            prefix spe: <https://openschemas.github.io/spec-container/specifications/>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            prefix xsd:  <http://www.w3.org/2001/XMLSchema#> 
            prefix shsh: <http://www.w3.org/ns/shacl-shacl#> 
            prefix dcterms: <http://purl.org/dc/terms/> 
            prefix ex: <https://epfl.ch/example/> 
            prefix md4i: <http://w3id.org/nfdi4ing/metadata4ing#>

            SELECT DISTINCT ?enumerationValue ?enumerationLabel ?enumerationDefinition ?property ?propertyLabel ?group ?groupLabel ?groupDefinition
            WHERE { {
            ?propertyShape a sh:PropertyShape .
                    ?propertyShape sh:path ?property.
                    OPTIONAL{
                        ?property """
            + self.get_predicate("label")
            + """ ?propertyLabel}
            { 
                ?propertyShape sh:class ?group .
                ?group rdfs:subClassOf """
            + self.get_type("enumeration")
            + """ .
                ?enumerationValue a ?group .
                        ?group """
            + self.get_predicate("label")
            + """ ?groupLabel .
            ?group """
            + self.get_predicate("definition")
            + """ ?groupDefinition .
                        OPTIONAL{?enumerationValue """
            + self.get_predicate("definition")
            + """ ?enumerationDefinition .}
                        OPTIONAL{?enumerationValue """
            + self.get_predicate("label")
            + """ ?enumerationLabel.}
            }
            UNION
            {
                ?propertyShape sh:or/rdf:rest*/rdf:first/sh:class ?group .
                ?group rdfs:subClassOf """
            + self.get_type("enumeration")
            + """.
                ?enumerationValue a ?group .
                ?group """
            + self.get_predicate("definition")
            + """ ?groupDefinition .
            ?group """
            + self.get_predicate("label")
            + """ ?groupLabel .
                        OPTIONAL{?enumerationValue """
            + self.get_predicate("label")
            + """ ?enumerationDefinition .}
                            OPTIONAL{?enumerationValue """
            + self.get_predicate("label")
            + """ ?enumerationLabel.}
            }
            }
            }
            """
        )

        return enumerations_query

    def build_concepts_query(self) -> str:
        """
        Builds a SPARQL query string for concepts.

        Returns:
            str: The complete SPARQL query string for concepts.
        """

        sparql_query = (
            """
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat: <https://www.w3.org/TR/vocab-dcat-2/#>
            PREFIX vann: <http://purl.org/vocab/vann/>
            prefix schema: <http://schema.org/>
            prefix sd: <https://w3id.org/okn/o/sd#>
            prefix bio: <https://bioschemas.org/>
            prefix spe: <https://openschemas.github.io/spec-container/specifications/>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            prefix xsd:  <http://www.w3.org/2001/XMLSchema#> 
            prefix shsh: <http://www.w3.org/ns/shacl-shacl#> 
            prefix dcterms: <http://purl.org/dc/terms/> 
            prefix ex: <https://epfl.ch/example/> 
            prefix md4i: <http://w3id.org/nfdi4ing/metadata4ing#>
            prefix sdc:  <https://swissdatacustodian.ch/doc/ontology#>
            prefix dpv:  <https://w3id.org/dpv#> 
            
            SELECT ?domain ?classLabel ?classDefinition ?property ?propertyLabel ?propertyDefinition ?range ?example
            WHERE{
            
            ?nodeshape sh:property ?propertyShape .

            ?property a """
            + self.get_type("property")
            + """.
            ?property """
            + self.get_predicate("definition")
            + """ ?propertyDefinition.
            ?property """
            + self.get_predicate("label")
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
            + self.get_predicate("label")
            + """ ?classLabel .
            ?domain """
            + self.get_predicate("definition")
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


