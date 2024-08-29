import pytest
from unittest.mock import Mock
from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel
from src.umlars_translator.core.model.umlars_model.uml_elements import (
    UmlClass, UmlInterface, UmlDataType, UmlEnumeration, UmlPrimitiveType, UmlAttribute, UmlOperation,
    UmlLifeline, UmlAssociation, UmlAssociationEnd, UmlAggregation, UmlComposition, UmlRealization,
    UmlGeneralization, UmlDependency, UmlParameter, UmlMessage, UmlInteraction, UmlOccurrenceSpecification,
    UmlInteractionUse, UmlCombinedFragment, UmlOperand
)
from src.umlars_translator.core.model.umlars_model.uml_diagrams import UmlDiagram
from src.umlars_translator.core.model.constants import UmlVisibilityEnum, UmlMultiplicityEnum
from src.umlars_translator.core.model.umlars_model.uml_model_builder import UmlModelBuilder

# Fixtures
@pytest.fixture
def logger_mock():
    """Fixture for creating a mock logger."""
    return Mock()

@pytest.fixture
def builder(logger_mock):
    """Fixture for initializing UmlModelBuilder with a mock logger."""
    return UmlModelBuilder(core_logger=logger_mock)

# Tests
def test_construct_uml_model(builder):
    builder.construct_uml_model(name="TestModel", visibility=UmlVisibilityEnum.PUBLIC)
    model = builder.build()

    assert model.name == "TestModel"
    assert model.visibility == UmlVisibilityEnum.PUBLIC

def test_construct_uml_class(builder):
    builder.construct_uml_class(id="class1", name="Class1")
    model = builder.build()

    uml_class = model.elements.classes[0]
    assert uml_class.id == "class1"
    assert uml_class.name == "Class1"

def test_construct_uml_interface(builder):
    builder.construct_uml_interface(id="interface1", name="Interface1")
    model = builder.build()

    uml_interface = model.elements.interfaces[0]
    assert uml_interface.id == "interface1"
    assert uml_interface.name == "Interface1"

# Test for construct_uml_association_end
def test_construct_uml_association_end(builder):
    # Step 1: Construct the UML class that will be connected by the association end
    builder.construct_uml_class(id="class1", name="Class1")

    # Step 2: Construct the association that the end will belong to
    builder.construct_uml_association(id="assoc1", name="Association1")

    # Step 3: Construct the association end and bind it to the association
    builder.construct_uml_association_end(
        id="end1", 
        element_id="class1", 
        role="endRole", 
        multiplicity=UmlMultiplicityEnum.ONE, 
        navigability=True, 
        association_id="assoc1"
    )

    # Step 4: Build the model
    model = builder.build()

    # Verify the association end was created correctly
    association_end = model.builder.get_instance_by_id("end1")
    assert association_end is not None, "UmlAssociationEnd was not created."
    assert association_end.role == "endRole"
    assert association_end.multiplicity == UmlMultiplicityEnum.ONE
    assert association_end.navigability is True
    assert association_end.element.id == "class1"

    # Verify the association was created and the end was added correctly
    association = next((assoc for assoc in model.elements.associations if assoc.id == "assoc1"), None)
    assert association is not None, "UmlAssociation was not created."
    assert any(end.id == "end1" for end in (association.end1, association.end2)), "UmlAssociationEnd was not bound to UmlAssociation."

def test_construct_uml_association_end_with_delayed_assignment(builder):
    # Step 1: Construct the association end with a delayed assignment
    builder.construct_uml_association_end(
        id="end1", 
        element_id="class1",  # Element not yet available
        role="endRole", 
        multiplicity=UmlMultiplicityEnum.ONE, 
        navigability=True, 
        association_id="assoc1"  # Association not yet available
    )

    # Step 2: Construct the class and association later
    builder.construct_uml_class(id="class1", name="Class1")
    builder.construct_uml_association(id="assoc1", name="Association1")

    # Step 3: Build the model
    model = builder.build()

    # Verify that the delayed assignments were correctly handled
    association_end = model.builder.get_instance_by_id("end1")
    assert association_end is not None, "UmlAssociationEnd was not created."
    assert association_end.element is not None, "Delayed assignment for element was not handled."
    assert association_end.element.id == "class1"

    # Verify the association is bound correctly after the delayed assignment
    association = next((assoc for assoc in model.elements.associations if assoc.id == "assoc1"), None)
    assert association is not None, "UmlAssociation was not created."
    assert any(end.id == "end1" for end in (association.end1, association.end2)), "Delayed binding of UmlAssociationEnd to UmlAssociation was not handled."

#TODO def test_delayed_assignment(builder):
#     # Construct an UmlAttribute with delayed type assignment
#     builder.construct_uml_attribute(id="attr1", name="Attribute1", type_id="type1")

#     # Construct UmlPrimitiveType later
#     builder.construct_uml_primitive_type(id="type1", name="int")

#     model = builder.build()
#     attribute = model.elements.attributes[0]

#     assert attribute.id == "attr1"
#     assert attribute.name == "Attribute1"
#     assert attribute.type.id == "type1"
#     assert attribute.type.name == "int"

def test_construct_uml_dependency_with_delayed_assignment(builder):
    # Construct UmlDependency with delayed assignments
    builder.construct_uml_dependency(client_id="client1", supplier_id="supplier1")

    # Construct elements later
    builder.construct_uml_class(id="client1", name="ClientClass")
    builder.construct_uml_interface(id="supplier1", name="SupplierInterface")

    model = builder.build()
    dependency = model.elements.dependencies[0]

    assert dependency.client.id == "client1"
    assert dependency.supplier.id == "supplier1"

def test_clear_model(builder):
    builder.construct_uml_class(id="class1", name="Class1")
    builder.clear()

    model = builder.build()
    assert len(model.elements.classes) == 0

def test_method_chaining(builder):
    builder.construct_uml_class(id="class1", name="Class1").construct_uml_interface(id="interface1", name="Interface1")
    model = builder.build()

    assert len(model.elements.classes) == 1
    assert len(model.elements.interfaces) == 1
    assert model.elements.classes[0].name == "Class1"
    assert model.elements.interfaces[0].name == "Interface1"

# def test_bind_element_to_diagram(builder):
#     builder.construct_uml_class(id="class1", name="Class1")
#     builder.construct_uml_package(id="package1", name="Package1")
#     builder.bind_element_to_diagram(element_id="class1", diagram_id="package1")

#     model = builder.build()
#     package = model.elements.packages[0]

#     assert any(e.id == "class1" for e in package.elements)
