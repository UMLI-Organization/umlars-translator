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
def uml_association(uml_class):
    end1 = UmlAssociationEnd(id="end1", element=uml_class)
    end2 = UmlAssociationEnd(id="end2", element=uml_class)
    return UmlAssociation(id="assoc1", name="association1", end1=end1, end2=end2)


@pytest.fixture
def uml_generalization(uml_class):
    return UmlGeneralization(id="gen1", specific=uml_class, general=uml_class)


@pytest.fixture
def uml_dependency(uml_class):
    return UmlDependency(id="dep1", client=uml_class, supplier=uml_class)


@pytest.fixture
def uml_realization(uml_class, uml_interface):
    return UmlRealization(id="real1", client=uml_class, supplier=uml_interface)


@pytest.fixture
def uml_interface():
    return UmlInterface(id="interface1", name="TestInterface", visibility="public")


@pytest.fixture
def uml_enumeration():
    return UmlEnumeration(id="enum1", name="TestEnumeration", literals=["LITERAL1"])


@pytest.fixture
def uml_data_type():
    return UmlDataType(id="datatype1", name="TestDataType")


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


# Test Serializer for UmlAssociation
def test_uml_association_serialization(uml_association):
    serializer = UmlToPydanticSerializer()
    pydantic_association = serializer.visit_uml_association(uml_association)
    
    assert isinstance(pydantic_association, PydanticUmlAssociation)
    assert pydantic_association.id == uml_association.id
    assert pydantic_association.name == uml_association.name
    assert pydantic_association.end1.id == uml_association.end1.id
    assert pydantic_association.end2.id == uml_association.end2.id


# Test Serializer for UmlGeneralization
def test_uml_generalization_serialization(uml_generalization):
    serializer = UmlToPydanticSerializer()
    pydantic_generalization = serializer.visit_uml_generalization(uml_generalization)
    
    assert isinstance(pydantic_generalization, PydanticUmlGeneralization)
    assert pydantic_generalization.id == uml_generalization.id
    assert pydantic_generalization.specific.idref == uml_generalization.specific.id
    assert pydantic_generalization.general.idref == uml_generalization.general.id


# Test Serializer for UmlDependency
def test_uml_dependency_serialization(uml_dependency):
    serializer = UmlToPydanticSerializer()
    pydantic_dependency = serializer.visit_uml_dependency(uml_dependency)
    
    assert isinstance(pydantic_dependency, PydanticUmlDependency)
    assert pydantic_dependency.id == uml_dependency.id
    assert pydantic_dependency.client.idref == uml_dependency.client.id
    assert pydantic_dependency.supplier.idref == uml_dependency.supplier.id


# Test Serializer for UmlRealization
def test_uml_realization_serialization(uml_realization):
    serializer = UmlToPydanticSerializer()
    pydantic_realization = serializer.visit_uml_realization(uml_realization)
    
    assert isinstance(pydantic_realization, PydanticUmlRealization)
    assert pydantic_realization.id == uml_realization.id
    assert pydantic_realization.client.idref == uml_realization.client.id
    assert pydantic_realization.supplier.idref == uml_realization.supplier.id


# Test Serializer for UmlInterface
def test_uml_interface_serialization(uml_interface):
    serializer = UmlToPydanticSerializer()
    pydantic_interface = serializer.visit_uml_interface(uml_interface)
    
    assert isinstance(pydantic_interface, PydanticUmlInterface)
    assert pydantic_interface.id == uml_interface.id
    assert pydantic_interface.name == uml_interface.name
    assert pydantic_interface.visibility == uml_interface.visibility


# Test Serializer for UmlEnumeration
def test_uml_enumeration_serialization(uml_enumeration):
    serializer = UmlToPydanticSerializer()
    pydantic_enumeration = serializer.visit_uml_enumeration(uml_enumeration)
    
    assert isinstance(pydantic_enumeration, PydanticUmlEnumeration)
    assert pydantic_enumeration.id == uml_enumeration.id
    assert pydantic_enumeration.name == uml_enumeration.name
    assert pydantic_enumeration.literals == uml_enumeration.literals


# Test Serializer for UmlDataType
def test_uml_data_type_serialization(uml_data_type):
    serializer = UmlToPydanticSerializer()
    pydantic_data_type = serializer.visit_uml_data_type(uml_data_type)
    
    assert isinstance(pydantic_data_type, PydanticUmlDataType)
    assert pydantic_data_type.id == uml_data_type.id
    assert pydantic_data_type.name == uml_data_type.name


# Test Serializer for UmlModel
def test_uml_model_serialization(uml_model):
    serializer = UmlToPydanticSerializer()
    pydantic_model = serializer.serialize(uml_model)
    
    assert isinstance(pydantic_model, str)
    assert "TestModel" in pydantic_model
    assert "TestClass" in pydantic_model
    assert "attribute1" in pydantic_model
    assert "operation1" in pydantic_model
