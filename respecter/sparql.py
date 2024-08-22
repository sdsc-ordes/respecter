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
        if "ontology" not in _yaml_config:
            raise ValueError('Element "ontology" not found in config file')

        self.types = _yaml_config["type"]
        self.predicates = _yaml_config["predicate"]
        self.ontology = _yaml_config["ontology"]

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

    def build_enumerations_query(self,config_file_path) -> str:
        """
        Builds a SPARQL query string for enumerations.

        Returns:
            str: The complete SPARQL query string for enumerations.
        """
        
        with open(config_file_path, "r") as f:
            _yaml_config = yaml.load(f, Loader=yaml.FullLoader)
        
        prefixes = _yaml_config["prefix"]
        
        enumerations_query = (
        """
        """
        )
         
        for prefix_key, prefix_value in prefixes.items():# Construct the SPARQL query with placeholders for prefixes
            enumerations_query += f"PREFIX {prefix_key}: {prefix_value}\n"

        enumerations_query += (
            """   
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

    def build_concepts_query(self, config_file_path) -> str:
        """
        Builds a SPARQL query string for concepts.

        Returns:
            str: The complete SPARQL query string for concepts.
        """
        
        with open(config_file_path, "r") as f:
            _yaml_config = yaml.load(f, Loader=yaml.FullLoader)
        
        prefixes = _yaml_config["prefix"]
        
        sparql_query = (
        """
        """
        )
         
        for prefix_key, prefix_value in prefixes.items():# Construct the SPARQL query with placeholders for prefixes
            sparql_query += f"PREFIX {prefix_key}: {prefix_value}\n"

        sparql_query += (
            """
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


