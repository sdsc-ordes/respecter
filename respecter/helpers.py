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
from models import Class, Property, Enumeration, EnumerationGroup
from typing import Dict, List


def format_classes(classes):
    """
    Format the classes to be used in the template.
    """
    return [class_.to_dict() for class_ in classes.values()]


def format_enumerations(enumerations: List[Enumeration]):
    """
    Format the enumerations to be used in the template.
    """
    return [enumeration.to_dict() for enumeration in enumerations]


def format_properties(properties):
    """
    Format the properties to be used in the template.
    """
    return [property.to_dict() for property in properties.values()]


def format_value(value, qname=None):
    """
    Format the value to be used in the template.
    """
    # FIXME: the following section is a hack to have a working example.
    # This should be done differently and follow the Respec syntax for URLs.
    if value.get("type") == "uri":
        if qname:
            value_string = qname(value["value"])
        else:
            value_string = value["value"]
        return '<a href="' + value["value"] + '">' + value_string + "</a>"
    elif value.get("type") == "literal":
        return value["value"]
    elif value.get("type") == None:
        # Display a warning message
        print("Warning: missing value encountered.")
        print(value)
        return ""
    else:  # FIXME: handle other types
        # Display a warning message
        print(
            "Warning: unknown type '"
            + value.get("type")
            + "' for value '"
            + value.get("value")
            + "'"
        )
        return value["value"]


def extract_properties(rdf_properties, qname):
    """
    Extract the properties from the RDF data.
    """
    properties = dict()
    for property in rdf_properties:
        label = property.get("propertyLabel", "")["value"]
        if label not in properties:
            properties[label] = Property()

        current_property = properties[label]
        current_property.label = label
        current_property.definition = format_value(
            property.get("propertyDefinition", {}), qname=qname
        )

        current_property.property = format_value(
            property.get("property", {}), qname=qname
        )
        current_property.add_domain(
            format_value(property.get("domain", {}), qname=qname)
        )
        current_property.add_range(format_value(property.get("range", {}), qname=qname))

        properties[label] = current_property
    return properties


def extract_classes(rdf_classes, qname):
    """
    Extract the classes from the RDF data.
    """
    classes = dict()
    for rdf_class in rdf_classes:
        label = rdf_class.get("classLabel", {}).get("value", "")
        if label not in classes:
            classes[label] = Class()

        current_class = classes[label]
        current_class.label = label
        current_class.definition = format_value(
            rdf_class.get("classDefinition", {}), qname=qname
        )
        current_class.term = format_value(rdf_class.get("domain", {}), qname=qname)
        current_class.add_property(
            format_value(rdf_class.get("property", {}), qname=qname)
        )

        classes[label] = current_class
    return classes


def extract_enumerations(rdf_enumerations, qname):
    """
    Extract the enumerations from the RDF data.
    """
    enumerations = dict()
    for rdf_enumeration in rdf_enumerations:
        label = rdf_enumeration.get("enumerationLabel", {}).get("value", "")
        if label not in enumerations:
            enumerations[label] = Enumeration()

        current_enumeration = enumerations[label]
        current_enumeration.label = label
        current_enumeration.definition = format_value(
            rdf_enumeration.get("enumerationDefinition", {}), qname=qname
        )
        current_enumeration.term = format_value(
            rdf_enumeration.get("enumerationValue", {}), qname=qname
        )
        current_enumeration.term = format_value(
            rdf_enumeration.get("enumerationValue", {}), qname=qname
        )
        current_enumeration.add_property(
            format_value(rdf_enumeration.get("property", {}), qname=qname)
        )
        group_label = format_value(rdf_enumeration.get("groupLabel", {}), qname=qname)
        group_term = format_value(rdf_enumeration.get("group", {}), qname=qname)
        enumeration_group = EnumerationGroup(label=group_label, term=group_term)
        current_enumeration.add_enumeration_group(enumeration_group)

        enumerations[label] = current_enumeration
    return enumerations


def group_format_enumerations(enumerations: Dict[str, Enumeration]):
    """
    Group the enumerations by the group term.
    """
    grouped_enumerations = dict()
    for _, enumeration in enumerations.items():
        for enumeration_group in enumeration.enumeration_group:
            if enumeration_group.term not in grouped_enumerations:
                grouped_enumerations[enumeration_group.term] = {
                    "term": enumeration_group.term,
                    "label": enumeration_group.label,
                    "enumerations": [],
                }
            grouped_enumerations[enumeration_group.term]["enumerations"].append(
                enumeration
            )
    for group_label, group_data in grouped_enumerations.items():
        enumerations = group_data["enumerations"]
        sorted_enumerations = sorted(enumerations)
        print(sorted_enumerations)
        grouped_enumerations[group_label]["enumerations"] = format_enumerations(
            sorted_enumerations
        )
    return grouped_enumerations
