import pytest
from src.umlars_translator.core.serialization.umlars_model.json_serializer import UmlToPydanticSerializer
from src.umlars_translator.core.model.umlars_model.uml_elements import (
    UmlClass,
    UmlAttribute,
    UmlOperation,
    UmlParameter,
    UmlAssociation,
    UmlAssociationEnd,
    UmlGeneralization,
    UmlDependency,
    UmlRealization,
    UmlPrimitiveType,
    UmlInterface,
    UmlEnumeration,
    UmlDataType,
    UmlMessage,
    UmlInteraction,
    UmlLifeline,
    UmlCombinedFragment,
    UmlOperand,
    UmlInteractionUse,
    UmlOccurrenceSpecification,
    UmlPackage,
    UmlModelElements,
)
from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel
from src.umlars_translator.app.dtos.uml_model import (
    UmlClass as PydanticUmlClass,
    UmlAttribute as PydanticUmlAttribute,
    UmlOperation as PydanticUmlOperation,
    UmlParameter as PydanticUmlParameter,
    UmlAssociation as PydanticUmlAssociation,
    UmlAssociationEnd as PydanticUmlAssociationEnd,
    UmlGeneralization as PydanticUmlGeneralization,
    UmlDependency as PydanticUmlDependency,
    UmlRealization as PydanticUmlRealization,
    UmlPrimitiveType as PydanticUmlPrimitiveType,
    UmlInterface as PydanticUmlInterface,
    UmlEnumeration as PydanticUmlEnumeration,
    UmlDataType as PydanticUmlDataType,
    UmlMessage as PydanticUmlMessage,
    UmlInteraction as PydanticUmlInteraction,
    UmlLifeline as PydanticUmlLifeline,
    UmlCombinedFragment as PydanticUmlCombinedFragment,
    UmlOperand as PydanticUmlOperand,
    UmlInteractionUse as PydanticUmlInteractionUse,
    UmlOccurrenceSpecification as PydanticUmlOccurrenceSpecification,
    UmlPackage as PydanticUmlPackage,
    UmlModelElements as PydanticUmlModelElements,
    UmlModel as PydanticUmlModel,
)

# Fixtures for common test objects
@pytest.fixture
def uml_class():
    return UmlClass(id="class1", name="TestClass", visibility="public")


@pytest.fixture
def uml_attribute():
    return UmlAttribute(id="attr1", name="attribute1", visibility="public", type=None)


@pytest.fixture
def uml_operation():
    return UmlOperation(id="op1", name="operation1", visibility="public")


@pytest.fixture
def uml_model(uml_class, uml_attribute, uml_operation):
    uml_class.attributes.append(uml_attribute)
    uml_class.operations.append(uml_operation)
    elements = UmlModelElements(classes=[uml_class])
    return UmlModel(id="model1", name="TestModel", elements=elements, diagrams=None)


# Test Serializer for UmlClass
def test_uml_class_serialization(uml_class):
    serializer = UmlToPydanticSerializer()
    pydantic_class = serializer.visit_uml_class(uml_class)
    
    assert isinstance(pydantic_class, PydanticUmlClass)
    assert pydantic_class.id == uml_class.id
    assert pydantic_class.name == uml_class.name
    assert pydantic_class.visibility == uml_class.visibility


# Test Serializer for UmlAttribute
def test_uml_attribute_serialization(uml_attribute):
    serializer = UmlToPydanticSerializer()
    pydantic_attribute = serializer.visit_uml_attribute(uml_attribute)
    
    assert isinstance(pydantic_attribute, PydanticUmlAttribute)
    assert pydantic_attribute.id == uml_attribute.id
    assert pydantic_attribute.name == uml_attribute.name
    assert pydantic_attribute.visibility == uml_attribute.visibility


# Test Serializer for UmlOperation
def test_uml_operation_serialization(uml_operation):
    serializer = UmlToPydanticSerializer()
    pydantic_operation = serializer.visit_uml_operation(uml_operation)
    
    assert isinstance(pydantic_operation, PydanticUmlOperation)
    assert pydantic_operation.id == uml_operation.id
    assert pydantic_operation.name == uml_operation.name
    assert pydantic_operation.visibility == uml_operation.visibility


# Test Serializer for UmlModel
def test_uml_model_serialization(uml_model):
    serializer = UmlToPydanticSerializer()
    pydantic_model = serializer.serialize(uml_model)
    
    assert isinstance(pydantic_model, str)
    assert "TestModel" in pydantic_model
    assert "TestClass" in pydantic_model
    assert "attribute1" in pydantic_model
    assert "operation1" in pydantic_model

# TODO: Add more test cases for each UML element type...

