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
import click
import typer
import os
from typing import Optional
from typing_extensions import Annotated
from .core import fetch_ontology, render_template

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
    ontology: Annotated[str, typer.Argument(
        help="Path to the ontology RDF file.",
    )],
    config_path: Annotated[Optional[str], typer.Option(
        "--config",
        show_choices=True,
        help="Path to the YAML configuration file.",
    )] = "config/sparql_config.yaml",
    debug: Annotated[bool, typer.Option(
        "--debug", help="Enable debugging mode."
    )] = False,
    output: Annotated[str, typer.Option(
        "--output",
        help="Path to the output HTML file.",
    )] = "output.html",
    version: Annotated[Optional[bool], typer.Option(
        "--version",
        help="Display version and exit",
        callback=version_callback,
    )] = None,
):
    """
    Turns a RDF serialization of an ontology into a ReSpec styled HTML page
    """
    breakpoint()
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
    with open(output, "w", encoding="utf-8") as f:
        f.write(template)
    typer.echo(f"HTML page saved to {output}")


if __name__ == "__main__":
    app()
