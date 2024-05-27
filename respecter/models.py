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
    fragment_identifier: str = ""
    range: set = field(default_factory=set)

    def add_domain(self, domain):
        self.domain.add(domain)

    def add_range(self, range):
        self.range.add(range)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "FragmentIdentifier": self.fragment_identifier,
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
    fragment_identifier: str = ""
    term: str = ""
    property: set = field(default_factory=set)

    def add_property(self, property):
        self.property.add(property)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "FragmentIdentifier": self.fragment_identifier,
            "Term": self.term,
            "Property": ", ".join(self.property),
        }


@dataclass
class EnumerationGroup:
    """
    Class to store the enumeration group metadata.
    """

    label: str = ""
    definition: str = ""
    fragment_identifier: str = ""
    term: str = ""

    def to_string(self):
        return f"{self.term}"

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "FragmentIdentifier": self.fragment_identifier,
            "Term": self.term,
        }

    def __hash__(self) -> int:
        return hash(self.term)  # TODO: Check if this is correct


@dataclass
class Enumeration:
    """
    Class to store the enumeration instances metadata.
    """

    label: str = ""
    definition: str = ""
    enumeration_group: set = field(default_factory=set)
    fragment_identifier: str = ""
    property: set = field(default_factory=set)
    term: str = ""

    def add_property(self, property):
        self.property.add(property)

    def add_enumeration_group(self, enumeration_group: EnumerationGroup):
        """
        Add a group to the enumeration.
        Parameters:
            group (EnumerationGroup): The group to add to the enumeration.
        """
        self.enumeration_group.add(enumeration_group)

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
            "FragmentIdentifier": self.fragment_identifier,
            "Term": self.term,
            "Groups": ", ".join([g.to_string() for g in self.enumeration_group]),
            "Property": ", ".join(self.property),
        }

    def __lt__(self, other):
        """Used to sort the enumerations by label."""
        return self.label < other.label
