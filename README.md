# ReSpecter

ReSpecter is a tool which turns a RDF serialization of an ontology into a ReSpec styled HTML page using Jinja templates.

# Installation

Create a virtual environment and install the dependencies with 

```sh
pip3 install -r requirements.txt
```

# Usage

The script `respecter/cli.py` can be used to generate a ReSpec styled HTML page from an ontology serialized in RDF. 

The following command will generate a ReSpec styled HTML page from the ontology `custodian.ttl` and save it under the name `custodian.html`:

```sh
python3 respecter/cli.py examples/custodian.ttl --output custodian.html
```

To know more about the available options, run:

```sh
python3 respecter/cli.py --help
```