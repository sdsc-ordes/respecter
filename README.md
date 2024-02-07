# respecter
ReSpecter is a tool which turns a RDF serialization of an ontology into a ReSpec styled HTML page using Jinja templates.

# Installation

Create a virtual environment and install the dependencies with 

```sh
pip3 install -r requirements.txt
```

# Example

The script `example.py` reads the results of a SPARQL query and uses it to fill the template `template/example.html`. You can test it by running

```sh
python3 example.py
```

A new file named `output.html` will be created with the result of the SPARQL queries displayed in the different sections.