# respecter
# Copyright 2022 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
    prefixes: dict = field(default_factory=dict)

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
        if "prefix" not in _yaml_config:
            raise ValueError('Element "prefix" not found in config file')
        

        self.types = _yaml_config["type"]
        self.predicates = _yaml_config["predicate"]
        self.prefixes = _yaml_config["prefix"]

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
    
    def get_prefixes(self):
        """
        Get the prefixes from the config file.
        """
        prefixes = ""
        for prefix, uri in self.prefixes.items():
            prefixes += f"PREFIX {prefix}: {uri}\n"
        return prefixes

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
        
        config.get_prefixes()
        +
        """

        SELECT DISTINCT ?enumerationValue ?enumerationLabel ?enumerationDefinition ?property ?propertyLabel ?group ?groupLabel
        WHERE { {
        ?propertyShape a sh:PropertyShape .
                ?propertyShape sh:path ?property.
                OPTIONAL{
                    ?property """
        + config.get_predicate("label")
        + """ ?propertyLabel}
        { 
            ?propertyShape sh:class ?group .
            ?group rdfs:subClassOf """
        + config.get_type("enumeration")
        + """ .
            ?enumerationValue a ?group .
                    ?group """
        + config.get_predicate("label")
        + """ ?groupLabel .
                    OPTIONAL{?enumerationValue """
        + config.get_predicate("definition")
        + """ ?enumerationDefinition .}
        OPTIONAL{?enumerationValue """
        + config.get_predicate("label")
        + """ ?enumerationLabel.}
        }
        UNION
        {
        ?propertyShape sh:or/rdf:rest*/rdf:first/sh:class ?group .
        ?group rdfs:subClassOf """
        + config.get_type("enumeration")
        + """ .
        ?enumerationValue a ?group .
        ?group """
        + config.get_predicate("label")
        + """ ?groupLabel.
        OPTIONAL{?enumerationValue """
        + config.get_predicate("definition")
        + """ ?enumerationDefinition .}
        OPTIONAL{?enumerationValue """
        + config.get_predicate("label")
        + """ ?enumerationLabel.}
                        
        }
        }    
        }
        """
    )
    print(enumerations_query)
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
        config.get_prefixes()
        +
        """
                
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
