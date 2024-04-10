import yaml

def build_sparql_query(config_file_path):
    
    """
    Builds a SPARQL query string based on a YAML configuration file.

    Args:
        config_file_path (str): Path to the YAML file containing SPARQL predicate definitions.

    Returns:
        str: The complete SPARQL query string.
    """
  
  
    # Define the SPARQL prefixes
    prefixes = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX dcat: <https://www.w3.org/TR/vocab-dcat-2/#>
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    """


    with open(config_file_path, "r") as f:
        # Load the configuration
        config= yaml.load(f, Loader=yaml.FullLoader)
        print(f"configuration: {config}")
        
    # Definition predicate URI from the config
    definition_Predicate = config["definitionPredicate"]
    label_Predicate = config["labelPredicate"]
    property_Predicate = config["propertyPredicate"]


    # SPARQL clauses
    select_clause = 'SELECT ?concept ?definition ?label ?type (GROUP_CONCAT(?properties; separator="\\n") as ?Properties)'

    where_clause_template = """
    WHERE {
        {
                ?concept a rdfs:Class.
            OPTIONAL {?concept """ + definition_Predicate + """ ?definition}  # Replaced placeholder with variable
            OPTIONAL {?concept """ + label_Predicate + """  ?label}
            OPTIONAL {?concept """ + property_Predicate + """  ?properties}
        
            }
            FILTER(!isblank(?concept))
    }
    """

    group_by_clause = "GROUP BY ?concept ?definition ?label ?example ?type"

    #  SPARQL Combined clauses
    sparql_query = f"{prefixes}\n{select_clause}\n{where_clause_template}\n{group_by_clause}"
    
    return sparql_query
    
