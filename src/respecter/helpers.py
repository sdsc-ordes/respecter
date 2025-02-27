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
from respecter.models import Class, Property, Enumeration, EnumerationGroup
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

def format_uri_value(value, qname=None, current_ontology_url=None):
    if current_ontology_url and value.startswith(current_ontology_url):
        value_uri = value.replace(current_ontology_url, "#")
    else:
        value_uri = value
    if qname:
        value_string = qname(value)
    else:
        value_string = value
    return '<a href="' + value_uri + '">' + value_string + "</a>"


def format_value(item, qname=None, current_ontology_url=None):
    """
    Format the value to be used in the template.
    """
    # FIXME: the following section is a hack to have a working example.
    # This should be done differently and follow the Respec syntax for URLs.
    
    if item.get("type") == "uri":
        return format_uri_value(item.get("value", ""), qname=qname, current_ontology_url=current_ontology_url)
    elif item.get("type") == "literal":
        return item["value"]
    elif item.get("type") == None:
        # Display a warning message
        print("Warning: missing value encountered.", file=sys.stderr)
        return ""
    else:  # FIXME: handle other types
        # Display a warning message
        print(
            "Warning: unknown type '"
            + item.get("type")
            + "' for value '"
            + item.get("value")
            + "'"
        )
        return item["value"]


def extract_fragment_identifier(uri_reference: str, separator="#"):
    """
    Extract the fragment identifier from the URI reference.

    Args:
        uri_reference: The URI reference.
        separator: The separator to use to split the URI reference.

    Returns:
        The fragment identifier.

    Examples:
        >>> extract_fragment_identifier("https://example.com#fragment")
        "fragment"
    """
    if separator in uri_reference:
        return uri_reference.split(separator)[-1]
    return ""


def extract_properties(rdf_properties, qname, current_ontology_url=None):
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
            property.get("propertyDefinition", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        current_property.fragment_identifier = extract_fragment_identifier(  # TODO: refactor this to use the separator from the sparql config
            property.get("property", {}).get("value", "")
        )
        current_property.property = format_value(
            property.get("property", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        current_property.add_domain(
            format_value(
                property.get("domain", {}),
                qname=qname,
                current_ontology_url=current_ontology_url,
            )
        )
        current_property.add_range(
            format_value(
                property.get("range", {}),
                qname=qname,
                current_ontology_url=current_ontology_url,
            )
        )
        properties[label] = current_property
    return properties


def extract_classes(rdf_classes, qname, current_ontology_url=None):
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
            rdf_class.get("classDefinition", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        current_class.fragment_identifier = extract_fragment_identifier(  # TODO: refactor this to use the separator from the sparql config
            rdf_class.get("domain", {}).get("value", "")
        )
        current_class.term = format_value(
            rdf_class.get("domain", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        current_class.add_property(
            format_value(
                rdf_class.get("property", {}),
                qname=qname,
                current_ontology_url=current_ontology_url,
            )
        )

        classes[label] = current_class
    return classes


def extract_enumerations(rdf_enumerations, qname, current_ontology_url=None):
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
            rdf_enumeration.get("enumerationDefinition", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        current_enumeration.fragment_identifier = extract_fragment_identifier(  # TODO: refactor this to use the separator from the sparql config
            rdf_enumeration.get("enumerationValue", {}).get("value", "")
        )
        current_enumeration.term = format_value(
            rdf_enumeration.get("enumerationValue", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        current_enumeration.add_property(
            format_value(
                rdf_enumeration.get("property", {}),
                qname=qname,
                current_ontology_url=current_ontology_url,
            )
        )
        group_label = format_value(
            rdf_enumeration.get("groupLabel", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        group_term = format_value(
            rdf_enumeration.get("group", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        group_fragment_identifier = extract_fragment_identifier(  # TODO: refactor this to use the separator from the sparql config
            rdf_enumeration.get("group", {}).get("value", "")                                         
        )
        group_definition = format_value(
            rdf_enumeration.get("groupDefinition", {}),
            qname=qname,
            current_ontology_url=current_ontology_url,
        )
        enumeration_group = EnumerationGroup(label=group_label, term=group_term, fragment_identifier=group_fragment_identifier, definition=group_definition)
        current_enumeration.add_enumeration_group(enumeration_group)

        enumerations[label] = current_enumeration
        
    return enumerations


def group_format_enumerations(enumerations: Dict[str, Enumeration]):
    """
    Group the enumerations by the group term.

    Args:
        enumerations: A dictionary of enumerations.

    Returns:
        A dictionary of grouped enumerations.

    Dictionary format:
    {
        "term": str,
        "label": str,
        "enumerations": List[Dict[str, str]]
    }
    """
    grouped_enumerations = dict()
    for _, enumeration in enumerations.items():
        for enumeration_group in enumeration.enumeration_group:
            if enumeration_group.term not in grouped_enumerations:
                grouped_enumerations[enumeration_group.term] = {
                    "term": enumeration_group.term,
                    "label": enumeration_group.label,
                    "FragmentIdentifier": enumeration_group.fragment_identifier,
                    "enumerations": [],
                }
            grouped_enumerations[enumeration_group.term]["enumerations"].append(
                enumeration
            )
            
            
    for group_label, group_data in grouped_enumerations.items():
        enumerations = group_data["enumerations"]
        sorted_enumerations = sorted(enumerations)
        grouped_enumerations[group_label]["enumerations"] = format_enumerations(
            sorted_enumerations
        )
    return grouped_enumerations
