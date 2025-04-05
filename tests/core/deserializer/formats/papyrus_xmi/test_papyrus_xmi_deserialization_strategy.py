import pytest

from kink import di

from umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_deserialization_strategy import (
    PapyrusXmiImportParsingStrategy,
)
from umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_model_processing_pipeline import (
    UmlModelPipe,
)
from umlars_translator.core.deserialization.formats.papyrus_xmi.papyrus_xmi_format_detection_pipeline import (
    PapyrusXmiDetectionPipe,
)
from umlars_translator.core.deserialization.input_processor import InputProcessor
from umlars_translator.core.model.abstract.uml_model import IUmlModel
from umlars_translator.core.model.abstract.uml_diagrams import IUmlDiagrams, IUmlClassDiagram, IUmlSequenceDiagram
from umlars_translator.core.model.abstract.uml_elements import IUmlPackage, IUmlModelElements, IUmlClass, IUmlAttribute, IUmlOperation, IUmlInterface, IUmlEnumeration, IUmlDataType, IUmlPrimitiveType, IUmlAssociation, IUmlDirectedAssociation, IUmlAssociationEnd, IUmlLifeline, IUmlMessage, IUmlGeneralization, IUmlRealization
from umlars_translator.core.deserialization.exceptions import (
    InvalidFormatException,
)
from umlars_translator.core.model.umlars_model.uml_model_builder import (
    UmlModelBuilder,
)
from umlars_translator.core.model.constants import UmlVisibilityEnum, UmlAssociationDirectionEnum, UmlPrimitiveTypeKindEnum


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
    return UmlModelBuilder()


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


def test_build_processing_pipe(
    umlars_model_builder, papyrus_xmi_deserialization_strategy_factory
):
    strategy = papyrus_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    pipe = strategy._build_processing_pipe()
    assert isinstance(pipe, UmlModelPipe)


def test_build_uml_model_processing_pipe(
    umlars_model_builder, papyrus_xmi_deserialization_strategy_factory
):
    strategy = papyrus_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    root_pipe = strategy._build_processing_pipe()
    assert isinstance(root_pipe, UmlModelPipe)


def test_build_format_detection_pipe(
    umlars_model_builder, papyrus_xmi_deserialization_strategy_factory
):
    strategy = papyrus_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    detection_pipe = strategy._build_format_detection_pipe()
    assert isinstance(detection_pipe, PapyrusXmiDetectionPipe)


def test_when_retrieve_model_from_papyrus_xmi_then_return_model(
    payprus_uml_car_model_data_source,
    umlars_model_builder,
    papyrus_xmi_deserialization_strategy_factory,
):
    strategy = papyrus_xmi_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
    
    model = strategy.retrieve_model(payprus_uml_car_model_data_source)
    assert isinstance(model, IUmlModel)


def test_when_retrieve_model_from_other_format_then_raise_exception(
    other_format_data_source,
    umlars_model_builder,
    papyrus_xmi_deserialization_strategy_factory,
):
    strategy = papyrus_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    with pytest.raises(InvalidFormatException):
        strategy.retrieve_model(other_format_data_source)


def test_when_retrieve_model_from_other_xmi_then_raise_exception(
    other_xmi_data_source, umlars_model_builder, papyrus_xmi_deserialization_strategy_factory
):
    strategy = papyrus_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    with pytest.raises(InvalidFormatException):
        strategy.retrieve_model(other_xmi_data_source)

