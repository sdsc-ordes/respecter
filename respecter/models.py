from dataclasses import dataclass, field


@dataclass
class Ontology:
    """
    Class to store the ontology metadata.
    """

    title: str = ""
    introduction: str = ""
    abstract: str = ""
    publish_date: str = ""
    contributors: list = field(default_factory=list)
    creators: list = field(default_factory=list)

    def to_dict(self):
        return {
            "title": self.title,
            "introduction": self.introduction,
            "abstract": self.abstract,
            "publish_date": self.publish_date,
            "contributors": self.contributors,
            "creators": self.creators,
        }

    def import_from_rdf(self, rdf_ontology):
        self.title = rdf_ontology.get("title", {}).get("value", "")
        self.introduction = rdf_ontology.get("description", {}).get("value", "")
        self.abstract = rdf_ontology.get("abstract", {}).get("value", "")
        self.publish_date = rdf_ontology.get("modified", {}).get("value", "")
        self.contributors = (
            rdf_ontology.get("contributors", {}).get("value", "").split("\n")
        )
        self.creators = rdf_ontology.get("creators", {}).get("value", "").split("\n")


@dataclass
class Property:
    """
    Class to store the property metadata.
    """

    label: str = ""
    definition: str = ""
    property: str = ""
    domain: set = field(default_factory=set)
    range: set = field(default_factory=set)

    def add_domain(self, domain):
        self.domain.add(domain)

    def add_range(self, range):
        self.range.add(range)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "Property": self.property,
            "Domain": ", ".join(self.domain),
            "Range": ", ".join(self.range),
        }


@dataclass
class Class:
    """
    Class to store the class metadata.
    """

    label: str = ""
    definition: str = ""
    term: str = ""
    property: set = field(default_factory=set)

    def add_property(self, property):
        self.property.add(property)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "Term": self.term,
            "Property": ", ".join(self.property),
        }
    
@dataclass
class Enumeration:
    """
    Class to store the enumeration instances metadata.
    """

    label: str = ""
    definition: str = ""
    term: str = ""
    group: set = field(default_factory=set)
    property: set = field(default_factory=set)

    def add_property(self, property):
        self.property.add(property)
    
    def add_group(self, group):
        self.group.add(group)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "Term": self.term,
            "Group": ", ".join(self.group),
            "Property": ", ".join(self.property),
        }
        