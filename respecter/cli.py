import click
import typer
import os
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
        typer.echo(f"ReSpecter, version {__version__}")
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
    output: Optional[str] = typer.Option(
        "output.html",
        "--output",
        help="Path to the output HTML file.",
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
    ontology, concepts, properties, enumerations = fetch_ontology(
        ontology_file_path=ontology,
        sparql_config_file_path=sparql_config_path,
        debug=debug,
    )
    template = render_template(ontology, concepts, properties, enumerations)

    # Write rendered template to file
    if os.path.exists(output):
        click.confirm(
            f"The file {output} already exists. Do you want to overwrite it?",
            abort=True,
        )
    with open(output, "w") as f:
        f.write(template)
    typer.echo(f"HTML page saved to {output}")


if __name__ == "__main__":
    app()
