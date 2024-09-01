import pytest

from kink import di

from src.umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_deserialization_strategy import (
    PapyrusXmiImportParsingStrategy,
)
from src.umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_model_processing_pipeline import (
    UmlModelPipe,
)
from src.umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_format_detection_pipeline import (
    PapyrusXmiDetectionPipe,
)
from src.umlars_translator.core.deserialization.input_processor import InputProcessor
from src.umlars_translator.core.model.abstract.uml_model import IUmlModel
from src.umlars_translator.core.model.abstract.uml_diagrams import IUmlDiagrams, IUmlClassDiagram, IUmlSequenceDiagram
from src.umlars_translator.core.model.abstract.uml_elements import IUmlPackage, IUmlModelElements, IUmlClass, IUmlAttribute, IUmlOperation, IUmlInterface, IUmlEnumeration, IUmlDataType, IUmlPrimitiveType, IUmlAssociation, IUmlDirectedAssociation, IUmlAssociationEnd, IUmlLifeline, IUmlMessage, IUmlGeneralization, IUmlRealization
from src.umlars_translator.core.deserialization.exceptions import (
    InvalidFormatException,
)
from src.umlars_translator.core.model.umlars_model.uml_model_builder import (
    UmlModelBuilder,
)
from src.umlars_translator.core.model.constants import UmlVisibilityEnum, UmlAssociationDirectionEnum, UmlPrimitiveTypeKindEnum
from src.umlars_translator.core.deserialization.deserializer import ModelDeserializer


CAR_MODEL_FILE_PATH_NOTATION = "tests/core/deserializer/formats/papyrus_xmi/test_data/eclipse-papyrus-car-model-with-sequence.notation"
CAR_MODEL_FILE_PATH_UML = "tests/core/deserializer/formats/papyrus_xmi/test_data/eclipse-papyrus-car-model-with-sequence.uml"


FILES_WITH_PAPYRUS_XMI_FORMAT = [
    CAR_MODEL_FILE_PATH_NOTATION,
    CAR_MODEL_FILE_PATH_UML,
]


@pytest.fixture(autouse=True)
def clear_cache():
    yield
    di.clear_cache()


@pytest.fixture
def umlars_model_builder():
    builder = UmlModelBuilder()
    yield builder
    builder.clear()


@pytest.fixture
def umlars_deserializer():
    builder = UmlModelBuilder()
    deserializer = ModelDeserializer(model_builder=builder)
    yield deserializer
    deserializer.clear()


@pytest.fixture
def papyrus_xmi_deserialization_strategy_factory():
    class PapyrusXmiDeserializationStrategyFactory:
        def create_strategy(self, model_builder):
            return PapyrusXmiImportParsingStrategy(model_builder=model_builder)

    return PapyrusXmiDeserializationStrategyFactory()


@pytest.fixture
def papyrus_xmi_class_data_sources():
    return list(
        InputProcessor().accept_multiple_inputs(
            file_paths_list=FILES_WITH_PAPYRUS_XMI_FORMAT
        )
    )


@pytest.fixture
def payprus_uml_car_model_data_source():
    return InputProcessor().accept_input(
        file_path=CAR_MODEL_FILE_PATH_UML
    )


@pytest.fixture
def other_xmi_data_source():
    return InputProcessor().accept_input(
        """<?xml version="1.0" encoding="windows-1252"?>
<xmi:XMI xmlns:xmi="http://schema.eclipse.com/spec/XMI/2.1" xmlns:uml="http://schema.eclipse.com/spec/UML/2.1" xmi:version="2.1">
    <xmi:Documentation exporter-name="Not Enterprise Architect" exporterVersion="6.5" exporterID="1628"/>
    <uml:Model xmi:type="uml:Model" name="EA_Model" visibility="public">
        <packagedElement xmi:type="uml:Package" xmi:id="EAPK_53FD35CE_1AC8_4eb3_837B_A43049AEA5FE" name="Basic Class Diagram with Attributes and Operations" visibility="public">
            <packagedElement xmi:type="uml:Class" xmi:id="EAID_2" name="EA_Class" visibility="public"/>
        </packagedElement>
    </uml:Model>
</xmi:XMI>"""
    )


@pytest.fixture
def other_format_data_source():
    return InputProcessor().accept_input(
        """
                {
                    Exporter : Imaginary Exporter,
                    UML_MODEL: {
                        name: "Imaginary Model",
                        classes: [
                            {name: "Imaginary Class", type: "class", visibility: "public"}
                        ]
                    }
                }
            """
    )



def test_when_deserialize_car_model_file_then_correct_model_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    assert isinstance(model, IUmlModel)
    assert model.name == "eclipse-papyrus-car-model-with-sequence"
    assert model.visibility == UmlVisibilityEnum.PUBLIC
    assert isinstance(model.elements, IUmlModelElements)
    assert isinstance(model.diagrams, IUmlDiagrams)


def test_when_deserialize_car_model_file_then_correct_classes_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = ModelDeserializer(model_builder=UmlModelBuilder()).deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_classes = {
        "Car": {"visibility": UmlVisibilityEnum.PUBLIC},
        "Driver": {"visibility": UmlVisibilityEnum.PUBLIC},
        "Person": {"visibility": UmlVisibilityEnum.PACKAGE},
        "Wheel": {"visibility": UmlVisibilityEnum.PUBLIC},
    }

    assert isinstance(model.elements.classes, list)
    assert len(model.elements.classes) == 4

    for cls in model.elements.classes:
        assert isinstance(cls, IUmlClass)
        assert cls.name in expected_classes
        assert cls.visibility == expected_classes[cls.name]["visibility"]
        assert isinstance(cls.attributes, list)
        assert all(isinstance(attr, IUmlAttribute) for attr in cls.attributes)
        assert isinstance(cls.operations, list)
        assert all(isinstance(op, IUmlOperation) for op in cls.operations)


def test_when_deserialize_car_model_file_then_correct_interfaces_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = ModelDeserializer(model_builder=UmlModelBuilder()).deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_interfaces = {
        "Movable": {"visibility": UmlVisibilityEnum.PACKAGE},
    }

    for iface in model.elements.interfaces:
        assert isinstance(iface, IUmlInterface)
        assert iface.name in expected_interfaces
        assert iface.visibility == expected_interfaces[iface.name]["visibility"]


def test_when_deserialize_car_model_file_then_correct_enumerations_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_enums = {
        "Gender": {
            "visibility": UmlVisibilityEnum.PUBLIC,
        },
    }

    assert isinstance(model.elements.enumerations, list)
    assert len(model.elements.enumerations) == 1

    for enum in model.elements.enumerations:
        assert isinstance(enum, IUmlEnumeration)
        assert enum.name in expected_enums
        assert enum.visibility == expected_enums[enum.name]["visibility"]


def test_when_deserialize_car_model_file_then_correct_datatypes_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_datatypes = {
        "Datetime": {"visibility": UmlVisibilityEnum.PUBLIC},
    }

    assert isinstance(model.elements.data_types, list)
    assert len(model.elements.data_types) == 1

    for datatype in model.elements.data_types:
        assert isinstance(datatype, IUmlDataType)
        assert datatype.name in expected_datatypes
        assert datatype.visibility == expected_datatypes[datatype.name]["visibility"]


def test_when_deserialize_car_model_file_then_correct_primitive_types_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_primitives = {
        "EAJava_boolean": UmlPrimitiveTypeKindEnum.BOOLEAN,
        "EAJava_void": UmlPrimitiveTypeKindEnum.VOID,
        "EAJava_double": UmlPrimitiveTypeKindEnum.REAL,
        "EAJava_char": UmlPrimitiveTypeKindEnum.CHAR,
        "EAJava_float": UmlPrimitiveTypeKindEnum.FLOAT,
    }

    for primitive in model.elements.primitive_types:
        assert isinstance(primitive, IUmlPrimitiveType)
        assert primitive.name in expected_primitives
        assert primitive.kind == expected_primitives[primitive.name]


def test_when_deserialize_car_model_file_then_correct_associations_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    # TODO: Maybe model should be changed -> so that UmlAggregation is actually Bidirectional
    # Now this test passes, because there is no way to determine in the builder that we are deserializing an aggregation or composition
    expected_associations = {
        "car_ownership": {"direction": UmlAssociationDirectionEnum.BIDIRECTIONAL},
        None: {"direction": UmlAssociationDirectionEnum.BIDIRECTIONAL},
    }

    for association in model.elements.associations:
        assert isinstance(association, (IUmlAssociation, IUmlDirectedAssociation))
        assert association.name in expected_associations
        assert association.direction == expected_associations[association.name]["direction"]


def test_when_deserialize_car_model_file_then_correct_attributes_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_attributes = {
        "Car": ["yearOfProduction"],
    }

    for cls in model.elements.classes:
        if cls.name in expected_attributes:
            attribute_names = [attr.name for attr in cls.attributes]
            assert all(attr in attribute_names for attr in expected_attributes[cls.name])
            assert all(isinstance(attr, IUmlAttribute) for attr in cls.attributes)


def test_when_deserialize_car_model_file_then_correct_operations_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_operations = {
        "Car": ["canDrive", "changeWheels", "drive"],
    }

    for cls in model.elements.classes:
        if cls.name in expected_operations:
            operation_names = [op.name for op in cls.operations]
            assert all(op in operation_names for op in expected_operations[cls.name])
            assert all(isinstance(op, IUmlOperation) for op in cls.operations)


def test_when_deserialize_car_model_file_then_correct_association_ends_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_ends = {
        "car_ownership": ["owner", "car"],
    }

    for association in model.elements.associations:
        if association.name in expected_ends:
            association_end_names = [end.role for end in (association.end1, association.end2)]
            assert all(end in association_end_names for end in expected_ends[association.name])
            assert all(isinstance(end, IUmlAssociationEnd) for end in (association.end1, association.end2))


def test_when_deserialize_car_model_file_then_correct_lifelines_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_lifelines = ["userDriver", "car", "driver", "newWheel", "wheel"]

    lifeline_names = [lifeline.name for lifeline in model.elements.interactions[0].lifelines]
    assert all(lifeline in lifeline_names for lifeline in expected_lifelines)
    assert all(isinstance(lifeline, IUmlLifeline) for lifeline in model.elements.interactions[0].lifelines)


def test_when_deserialize_car_model_file_then_correct_messages_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_messages = ["changeWheels", "driving", "stop", "start"]

    message_names = [message.name for message in model.elements.interactions[0].messages]
    assert all(message in message_names for message in expected_messages)
    assert all(isinstance(message, IUmlMessage) for message in model.elements.interactions[0].messages)


def test_when_deserialize_car_model_file_then_correct_diagrams_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_diagrams = ["Starter Class Diagram", "changeWheelsSequence", "Driving Seq Diag"]

    diagram_names = [diag.name for diag in model.diagrams.class_diagrams]
    assert all(diag in diagram_names for diag in expected_diagrams)


def test_when_deserialize_car_model_file_then_correct_generalizations_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_generalizations = ["Person -> Driver"]

    generalizations = [f"{gen.specific.name} -> {gen.general.name}" for gen in model.elements.generalizations]
    assert all(gen in expected_generalizations for gen in generalizations)
    assert all(isinstance(gen, IUmlGeneralization) for gen in model.elements.generalizations)


def test_when_deserialize_car_model_file_then_correct_realizations_created(
    umlars_model_builder, papyrus_xmi_class_data_sources, umlars_deserializer
):

    model = umlars_deserializer.deserialize(
        data_sources=papyrus_xmi_class_data_sources,
        )

    expected_realizations = ["Driver -> Movable"]

    realizations = [f"{realization.client.name} -> {realization.supplier.name}" for realization in model.elements.realizations]
    assert all(realization in expected_realizations for realization in realizations)
    assert all(isinstance(realization, IUmlRealization) for realization in model.elements.realizations)
