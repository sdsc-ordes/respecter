# respecter
respecter is a CLI tool which turns a RDF serialization of an ontology into a ReSpec styled HTML page using Jinja templates. The generated HTML page contains an overview of the classes, properties and enumeration types in your ontology, and creates links between them based on the SHACL shapes present in the ontology.
respecter is supposed to make it easier for non-RDF aware humans to browse through concepts in an ontology, and refer to specific concepts using URL's. Similar tooling exists ([pyLODE](https://github.com/RDFLib/pyLODE), [Widoco](https://github.com/dgarijo/Widoco) ) but does not allow for the configurationability and SHACL support which respecter does, or does not provide nicely structured w3c ReSpec style html. 

# Installation

Create a virtual python environment and install the dependencies from requirements.txt with:
```sh
pip install git+https://github.com/sdsc-ordes/respecter
```

## Development setup

We use [just](https://github.com/casey/just) as a command runner and [uv](https://github.com/astral-sh/uv) as a python package manager. You can get into a development environment with a dedicated venv using:

```sh
just dev
```

# Usage
Edit the `config/sparql_config.yaml` file in order to specify which URI's you want to use for fetching semantic information inside your ontology. These URI's will be used in the SPARQL query to fetch the data from your ontology.

The script `respecter/cli.py` can then be used to generate a ReSpec styled HTML page from an ontology serialized in RDF. 

The following command will generate a ReSpec styled HTML page from the ontology `custodian.ttl` and save it under the name `custodian.html`:

```sh
respecter examples/custodian.ttl --output custodian.html
```

To know more about the available options, run:

```sh
respecter --help
```
# Copyright
Copyright © 2024 Swiss Data Science Center (SDSC), www.datascience.ch. All rights reserved. The SDSC operates as a 'Société Simple' (einfache Gesellschaft) under Swiss law, jointly established and legally represented by the École Polytechnique Fédérale de Lausanne (EPFL) and the Eidgenössische Technische Hochschule Zürich (ETH Zürich). This copyright encompasses all materials, software, documentation, and other content created and developed by the SDSC.
# License Information
The respecter software is distributed as open-source under the Apache-2.0 license. Details about the license can be found in the LICENSE file included within the distribution package.
# Ethical Use and Legal Compliance Disclaimer
Please note that this software should not be used to harm any individual or entity. Users and developers must adhere to ethical guidelines and use the software responsibly and legally.
