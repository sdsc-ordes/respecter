import click
import typer
from typing import Optional
from core import fetch_ontology, render_template

__version__ = (
    "0.0.1"  # TODO: Move this to __init__.py and use poetry to manage the version
)
app = typer.Typer(add_completion=False)


# Used to autogenerate docs with sphinx-click
@click.group()
def cli():
    """Command line group"""
    pass


def version_callback(value: bool):
    if value:
        print(f"ReSpecter, version {__version__}")
        # Exits successfully
        raise typer.Exit()


@app.command()
def main(
    ontology: str = typer.Argument(
        help="Path to the ontology RDF file.",
    ),
    sparql_config_path: Optional[str] = typer.Option(
        "config/sparql_config.yaml",
        "--sparql-config",
        show_choices=True,
        help="Path to the SPARQL configuration file.",
    ),
    debug: Optional[bool] = typer.Option(
        False, "--debug", help="Enable debugging mode."
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Display version and exit",
        callback=version_callback,
    ),
):
    """
    Turns a RDF serialization of an ontology into a ReSpec styled HTML page
    """
    ontology, concepts, properties = fetch_ontology(
        ontology_file_path=ontology,
        sparql_config_file_path=sparql_config_path,
        debug=debug,
    )
    template = render_template(ontology, concepts, properties)

    with open("output.html", "w") as f:
        f.write(template)


if __name__ == "__main__":
    app()
