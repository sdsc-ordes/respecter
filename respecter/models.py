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
class EnumerationGroup:
    """
    Class to store the enumeration group metadata.
    """

    label: str = ""
    definition: str = ""
    term: str = ""

    def to_string(self):
        return f"{self.term}"

    def to_dict(self):
        return {
            "Label": self.label,
            "Definition": self.definition,
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
    term: str = ""
    enumeration_group: set = field(default_factory=set)
    property: set = field(default_factory=set)

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
            "Term": self.term,
            "Groups": ", ".join([g.to_string() for g in self.enumeration_group]),
            "Property": ", ".join(self.property),
        }

    def __lt__(self, other):
        """Used to sort the enumerations by label."""
        return self.label < other.label
