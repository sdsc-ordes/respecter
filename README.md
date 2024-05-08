# respecter
ReSpecter is a CLI tool which turns a RDF serialization of an ontology into a ReSpec styled HTML page using Jinja templates. The generated HTML page contains an overview of the classes, properties and enumeration types in your ontology, and creates links between them based on the SHACL shapes present in the ontology.
ReSpecter is supposed to make it easier for non-RDF aware humans to browse through concepts in an ontology, and refer to specific concepts using URL's. Similar tooling exists ([pyLODE](https://github.com/RDFLib/pyLODE), [Widoco](https://github.com/dgarijo/Widoco) but does not allow for the configurationability and SHACL support which ReSpecter does, or does not provide nicely structured w3c ReSpec style html. 

# Installation

Create a virtual python environment and install the dependencies with 

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
