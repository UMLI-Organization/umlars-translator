import pytest

from kink import di

from src.umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_deserialization_strategy import (
    EaXmiImportParsingStrategy,
)
from src.umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_model_processing_pipeline import (
    RootPipe,
    UmlModelPipe,
    ExtensionPipe,
)
from src.umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_format_detection_pipeline import (
    EaXmiDetectionPipe,
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


CAR_MODEL_FILE_PATH = "tests/core/deserializer/formats/ea_xmi/test_data/ea_car_model_xmi21-with-sequence.xml"


FILES_WITH_PAPYRUS_XMI_FORMAT = [
    CAR_MODEL_FILE_PATH,
]


@pytest.fixture(autouse=True)
def clear_cache():
    yield
    di.clear_cache()


@pytest.fixture
def umlars_model_builder():
    return UmlModelBuilder()


@pytest.fixture
def ea_xmi_deserialization_strategy_factory():
    class EaXmiDeserializationStrategyFactory:
        def create_strategy(self, model_builder):
            return EaXmiImportParsingStrategy(model_builder=model_builder)

    return EaXmiDeserializationStrategyFactory()


@pytest.fixture
def ea_xmi_class_data_sources():
    return list(
        InputProcessor().accept_multiple_inputs(
            file_paths_list=FILES_WITH_PAPYRUS_XMI_FORMAT
        )
    )


@pytest.fixture
def ea_xmi_car_data_source():
    return InputProcessor().accept_input(file_path=CAR_MODEL_FILE_PATH)


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


def test_build_processing_pipe(
    umlars_model_builder, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    pipe = strategy._build_processing_pipe()
    assert isinstance(pipe, RootPipe)


def test_build_uml_model_processing_pipe(
    umlars_model_builder, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    root_pipe = strategy._build_processing_pipe()
    uml_model_pipe = strategy._build_uml_model_processing_pipe(root_pipe)
    assert isinstance(uml_model_pipe, UmlModelPipe)


def test_build_extension_processing_pipe(
    umlars_model_builder, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    root_pipe = strategy._build_processing_pipe()
    extension_pipe = strategy._build_extension_processing_pipe(root_pipe)
    assert isinstance(extension_pipe, ExtensionPipe)


def test_build_format_detection_pipe(
    umlars_model_builder, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    detection_pipe = strategy._build_format_detection_pipe()
    assert isinstance(detection_pipe, EaXmiDetectionPipe)


def test_when_retrieve_model_from_ea_xmi_then_return_model(
    ea_xmi_class_data_sources,
    umlars_model_builder,
    ea_xmi_deserialization_strategy_factory,
):
    for data_source in ea_xmi_class_data_sources:
        strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)
        assert isinstance(model, IUmlModel)


def test_when_retrieve_model_from_other_format_then_raise_exception(
    other_format_data_source,
    umlars_model_builder,
    ea_xmi_deserialization_strategy_factory,
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    with pytest.raises(InvalidFormatException):
        strategy.retrieve_model(other_format_data_source)


def test_when_retrieve_model_from_other_xmi_then_raise_exception(
    other_xmi_data_source, umlars_model_builder, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    with pytest.raises(InvalidFormatException):
        strategy.retrieve_model(other_xmi_data_source)


def test_when_create_new_strategy_deserialization_successfull(
    other_xmi_data_source,
    ea_xmi_class_data_sources,
    umlars_model_builder,
    ea_xmi_deserialization_strategy_factory,
):
    for data_source in ea_xmi_class_data_sources:
        strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)
        assert isinstance(model, IUmlModel)

    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    with pytest.raises(InvalidFormatException):
        strategy.retrieve_model(other_xmi_data_source)


def test_when_reuse_strategy_deserialization_successfull(
    other_xmi_data_source,
    ea_xmi_class_data_sources,
    umlars_model_builder,
    ea_xmi_deserialization_strategy_factory,
):
    for data_source in ea_xmi_class_data_sources:
        strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source, clear_afterwards=True)
        assert isinstance(model, IUmlModel)

    with pytest.raises(InvalidFormatException):
        strategy.retrieve_model(other_xmi_data_source)


def test_when_deserialize_car_model_file_then_correct_model_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    assert isinstance(model, IUmlModel)
    assert model.name == "EA_Model"
    assert model.visibility == UmlVisibilityEnum.PUBLIC
    assert model.metadata == {
        "exporter": "Enterprise Architect",
        "exporterVersion": "6.5",
        "exporterID": "1628",
    }
    assert isinstance(model.elements, IUmlModelElements)
    assert isinstance(model.diagrams, IUmlDiagrams)


def test_when_deserialize_car_model_file_then_correct_classes_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

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


def test_when_deserialize_car_model_file_then_correct_packages_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    package_names = [pkg.name for pkg in model.elements.packages]
    assert isinstance(model.elements.packages, list)
    assert all(isinstance(pkg, IUmlPackage) for pkg in model.elements.packages)
    assert "CarModelPackage" in package_names


def test_when_deserialize_car_model_file_then_correct_interfaces_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_interfaces = {
        "Movable": {"visibility": UmlVisibilityEnum.PUBLIC},
    }

    for iface in model.elements.interfaces:
        assert isinstance(iface, IUmlInterface)
        assert iface.name in expected_interfaces
        assert iface.visibility == expected_interfaces[iface.name]["visibility"]


def test_when_deserialize_car_model_file_then_correct_enumerations_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

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
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

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
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

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
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

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
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_attributes = {
        "Car": ["yearOfProduction"],
    }

    for cls in model.elements.classes:
        if cls.name in expected_attributes:
            attribute_names = [attr.name for attr in cls.attributes]
            assert all(attr in attribute_names for attr in expected_attributes[cls.name])
            assert all(isinstance(attr, IUmlAttribute) for attr in cls.attributes)


def test_when_deserialize_car_model_file_then_correct_operations_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_operations = {
        "Car": ["canDrive", "changeWheels", "drive"],
    }

    for cls in model.elements.classes:
        if cls.name in expected_operations:
            operation_names = [op.name for op in cls.operations]
            assert all(op in operation_names for op in expected_operations[cls.name])
            assert all(isinstance(op, IUmlOperation) for op in cls.operations)


def test_when_deserialize_car_model_file_then_correct_association_ends_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_ends = {
        "car_ownership": ["owner", "car"],
    }

    for association in model.elements.associations:
        if association.name in expected_ends:
            association_end_names = [end.role for end in (association.end1, association.end2)]
            assert all(end in association_end_names for end in expected_ends[association.name])
            assert all(isinstance(end, IUmlAssociationEnd) for end in (association.end1, association.end2))


def test_when_deserialize_car_model_file_then_correct_lifelines_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_lifelines = ["userDriver", "car", "driver", "newWheel", "wheel"]

    lifeline_names = [lifeline.name for lifeline in model.elements.interactions[0].lifelines]
    assert all(lifeline in lifeline_names for lifeline in expected_lifelines)
    assert all(isinstance(lifeline, IUmlLifeline) for lifeline in model.elements.interactions[0].lifelines)


def test_when_deserialize_car_model_file_then_correct_messages_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_messages = ["changeWheels", "driving", "stop", "start"]

    message_names = [message.name for message in model.elements.interactions[0].messages]
    assert all(message in message_names for message in expected_messages)
    assert all(isinstance(message, IUmlMessage) for message in model.elements.interactions[0].messages)


def test_when_deserialize_car_model_file_then_correct_diagrams_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_diagrams = ["Starter Class Diagram", "changeWheelsSequence", "Driving Seq Diag"]

    diagram_names = [diag.name for diag in model.diagrams.class_diagrams]
    assert all(diag in diagram_names for diag in expected_diagrams)


def test_when_deserialize_car_model_file_then_correct_generalizations_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_generalizations = ["Person -> Driver"]

    generalizations = [f"{gen.specific.name} -> {gen.general.name}" for gen in model.elements.generalizations]
    assert all(gen in expected_generalizations for gen in generalizations)
    assert all(isinstance(gen, IUmlGeneralization) for gen in model.elements.generalizations)


def test_when_deserialize_car_model_file_then_correct_realizations_created(
    umlars_model_builder, ea_xmi_car_data_source, ea_xmi_deserialization_strategy_factory
):
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_car_data_source)

    expected_realizations = ["Driver -> Movable"]

    realizations = [f"{realization.client.name} -> {realization.supplier.name}" for realization in model.elements.realizations]
    assert all(realization in expected_realizations for realization in realizations)
    assert all(isinstance(realization, IUmlRealization) for realization in model.elements.realizations)
