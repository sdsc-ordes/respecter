from importlib import resources


def _read_resource(path: str):
    data = (
        resources.files("respecter").joinpath(path).open("r", encoding="utf-8").read()
    )
    return data


CONFIG = _read_resource("data/config.yaml")
QUERY = _read_resource("data/queries/ontology_metadata.sparql")
TEMPLATE = _read_resource("data/template.html")
