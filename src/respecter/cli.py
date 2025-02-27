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
import sys
from pathlib import Path
import click
import typer
from typing import Optional
from typing_extensions import Annotated
from respecter.core import fetch_ontology, render_template
from respecter.sparql import SparqlConfig
from respecter import defaults

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
def run(
    ontology_path: Annotated[Path, typer.Argument(
        help="Path to the ontology RDF file.",
        exists=True,
        dir_okay=False,
        show_default=False,
    )],
    config_path: Annotated[Path, typer.Option(
        "--config",
        help="Path to the YAML configuration file.",
        show_default=False,
        exists=True,
        dir_okay=False,
    )],
    debug: Annotated[bool, typer.Option(
        "--debug", help="Enable debugging mode."
    )] = False,
    output: Annotated[Optional[Path], typer.Option(
        "--output",
        help="Path to the output HTML file. If not provided, the output will be printed to stdout.",
        exists=False,
        dir_okay=False,
    )] = None,
    version: Annotated[Optional[bool], typer.Option(
        "--version",
        help="Display version and exit",
        callback=version_callback,
    )] = None,
):
    """
    Turns a RDF serialization of an ontology into a ReSpec styled HTML page
    """
    config = SparqlConfig.from_path(config_path)
    ontology, concepts, properties, enumerations = fetch_ontology(
        ontology_path=ontology_path,
        config=config,
        debug=debug,
    )
    docs = render_template(ontology, concepts, properties, enumerations)
    # Write rendered template to file
    sink = open(output, "w") if output else sys.stdout
    typer.echo(docs, file=sink)

@app.command()
def generate_config(
        interactive: Annotated[bool, typer.Option(
        "-i", 
        "--interactive",
        help="Populate the configuration file interactively.",
        show_default=False,
    )] = False
):
    """
    Generate an example configuration file.
    """
    config = SparqlConfig.parse(defaults.CONFIG)
    
    if interactive:
        config.ontology['uri'] = typer.prompt("URI base of the ontology")
        config.ontology['separator'] = typer.prompt(
            "Separator character for the ontology URI", default="#",
        )

        for field in ['class', 'property', 'enumeration']:
            default = config.types[field]
            config.types[field] = typer.prompt(
                f"Type used for {field}", default=default,
            )
        for field in ['definition', 'label', 'example']:
            default = config.types[field]
            config.predicates[field] = typer.prompt(
                f"Predicate used for {field}", default=default,
            )

    typer.echo(config.dump())
    
    

typer_cli = typer.main.get_command(app)
cli.add_command(typer_cli, "cli")

# Called when respecter is called without a subcommand
@app.callback()
def callback(
        version: Annotated[bool, typer.Option("--version", callback=version_callback)] = False
):
    """respecter generates a ReSpec styled HTML page from an ontology RDF file."""
    ...

if __name__ == "__main__":
    app()
