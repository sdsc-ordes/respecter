from importlib import resources

CONFIG = resources.read_text("respecter", "data/config.yaml")
QUERY = resources.read_text("respecter", "data/queries/ontology_metadata.sparql")
TEMPLATE = resources.read_text("respecter", "data/template.html")
