from pytest import fixture

from umlars_translator.core.model.umlars_model.uml_elements import (
    UmlElement,
    UmlNamedElement,
    UmlPrimitiveType,
    UmlClass,
    UmlInterface,
    UmlAttribute,
    UmlOperation,
    UmlGeneralization,
    UmlDependency,
    UmlAssociationEnd,
    UmlAggregation,
    UmlComposition,
    UmlLifeline,
    UmlMessage,
    UmlInteraction,
    UmlPackage,
    UmlParameter,
    UmlOccurrenceSpecification
)
from umlars_translator.core.model.constants import UmlPrimitiveTypeKindEnum


@fixture
def uml_element() -> UmlElement:
    return UmlElement()


@fixture
def uml_named_element() -> UmlNamedElement:
    return UmlNamedElement()


@fixture
def uml_primitive_type() -> UmlPrimitiveType:
    return UmlPrimitiveType(kind=UmlPrimitiveTypeKindEnum.INTEGER)


@fixture
def uml_class() -> UmlClass:
    return UmlClass()


@fixture
def interface() -> UmlInterface:
    return UmlInterface()


@fixture
def uml_attribute() -> UmlAttribute:
    return UmlAttribute(name="attribute", type=uml_class)


@fixture
def uml_operation() -> UmlOperation:
    return UmlOperation(name="operation")


@fixture
def uml_generalization() -> UmlGeneralization:
    return UmlGeneralization()


@fixture
def uml_dependency() -> UmlDependency:
    return UmlDependency()


@fixture
def uml_association_end() -> UmlAssociationEnd:
    return UmlAssociationEnd(element=uml_class)


@fixture
def uml_aggregation(uml_association_end) -> UmlAggregation:
    return UmlAggregation(end1=uml_association_end, end2=uml_association_end)


@fixture
def uml_composition(uml_association_end) -> UmlComposition:
    return UmlComposition(end1=uml_association_end, end2=uml_association_end)


@fixture
def uml_lifeline_factory() -> UmlLifeline:
    return lambda represents: UmlLifeline(represents=represents)


@fixture
def uml_message_factory() -> UmlMessage:
    return lambda sender, receiver: UmlMessage(send_event=sender, receive_event=receiver)

@fixture
def uml_interaction() -> UmlInteraction:
    return UmlInteraction()


@fixture
def uml_package() -> UmlPackage:
    return UmlPackage()


def test_uml_element_id(uml_element):
    assert isinstance(uml_element.id, str)


def test_uml_named_element_name(uml_named_element):
    uml_named_element.name = "name"
    assert uml_named_element.name == "name"
    

def test_uml_primitive_type_kind(uml_primitive_type):
    assert uml_primitive_type.kind == UmlPrimitiveTypeKindEnum.INTEGER


def test_uml_class_super_classes(uml_class):
    # Given
    super_classes = [UmlClass()]
    uml_class.super_classes = super_classes

    # When
    assigned_super_classes = uml_class.super_classes

    # Then
    assert assigned_super_classes == super_classes


def test_interface_operations(interface):
    # Given
    operations = [UmlOperation()]
    interface.operations = operations

    # When
    assigned_operations = interface.operations

    # Then
    assert assigned_operations == operations


def test_uml_attribute_type(uml_attribute):
    # Given
    attribute_type = UmlClass()
    uml_attribute.type = attribute_type

    # When
    assigned_type = uml_attribute.type

    # Then
    assert assigned_type == attribute_type


def test_uml_operation_parameters(uml_operation):
    # Given
    parameters = [UmlParameter()]
    uml_operation.parameters = parameters

    # When
    assigned_parameters = uml_operation.parameters

    # Then
    assert assigned_parameters == parameters


def test_uml_generalization_specific(uml_generalization):
    # Given
    specific = UmlClass()
    uml_generalization.specific = specific

    # When
    assigned_specific = uml_generalization.specific

    # Then
    assert assigned_specific == specific


def test_uml_dependency_client(uml_dependency):
    # Given
    client = UmlClass(name="client")
    uml_dependency.client = client

    # When
    assigned_client = uml_dependency.client

    # Then
    assert assigned_client == client


def test_uml_association_end_end(uml_association_end):
    # Given
    end = UmlClass(name="client")
    uml_association_end.end = end

    # When
    assigned_end = uml_association_end.end

    # Then
    assert assigned_end == end



def test_uml_aggregation_end1(uml_aggregation):
    # Given
    end1 = UmlAssociationEnd(element=UmlClass())
    uml_aggregation.source = end1

    # When
    assigned_end1 = uml_aggregation.end1

    # Then
    assert assigned_end1 == end1


def test_uml_composition_end2(uml_composition):
    # Given
    end2 = UmlAssociationEnd(element=UmlClass())
    uml_composition.target = end2

    # When
    assigned_end2 = uml_composition.end2

    # Then
    assert assigned_end2 == end2


def test_uml_lifeline_represents(uml_lifeline_factory):
    # Given
    represents = UmlClass()
    uml_lifeline = uml_lifeline_factory(represents) 

    # When
    assigned_represents = uml_lifeline.represents

    # Then
    assert assigned_represents == represents


def test_uml_message_sender(uml_message_factory, uml_lifeline_factory):
    # Given
    sender_class = UmlClass('sender')
    receiver_class = UmlClass('receiver')
    sender = uml_lifeline_factory(sender_class)
    receiver = uml_lifeline_factory(receiver_class)
    send_event = UmlOccurrenceSpecification(covered=sender)
    receive_event = UmlOccurrenceSpecification(covered=receiver)

    uml_message = uml_message_factory(send_event, receive_event)

    # When
    assigned_sender = uml_message.send_event.covered
    assigned_receiver = uml_message.receive_event.covered

    # Then
    assert assigned_sender == sender
    assert assigned_receiver == receiver
    assert assigned_sender.represents == sender_class
    assert assigned_receiver.represents == receiver_class


def test_uml_interaction_lifelines(uml_interaction, uml_lifeline_factory):
    # Given
    lifelines = [uml_lifeline_factory(UmlClass())]
    uml_interaction.lifelines = lifelines

    # When
    assigned_lifelines = uml_interaction.lifelines

    # Then
    assert assigned_lifelines == lifelines


def test_uml_package_elements(uml_package):
    # Given
    elements = [UmlElement()]
    uml_package.elements = elements

    # When
    assigned_elements = uml_package.elements

    # Then
    assert assigned_elements == elements