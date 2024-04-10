import yaml

# Define the SPARQL prefixes
prefixes = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcat: <https://www.w3.org/TR/vocab-dcat-2/#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
"""


with open("/Users/ossey/code/python/respec/respecter/config/sparql_config.yaml", "r") as f:
    # Load the configuration
    config= yaml.load(f, Loader=yaml.FullLoader)
    print(f"configuration: {config}")


  # Access the definition predicate URI from the config (assuming the key is "definitionPredicate")
definition_Predicate = config["definitionPredicate"]
label_Predicate = config["labelPredicate"]
property_Predicate = config["propertyPredicate"]
print(definition_Predicate)


# SPARQL SELECT clause
select_clause = 'SELECT ?concept ?definition ?label ?type (GROUP_CONCAT(?properties; separator="\\n") as ?Properties)'

# SPARQL WHERE clause template
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

# SPARQL GROUP BY clause
group_by_clause = "GROUP BY ?concept ?definition ?label ?example ?type"

# SPARQL Combined clauses
sparql_query = f"{prefixes}\n{select_clause}\n{where_clause_template}\n{group_by_clause}"

filename = "sparql_query_file.sparql" 

with open(filename, "w") as f:
  f.write(sparql_query)

print(f"SPARQL query saved to file: {filename}")