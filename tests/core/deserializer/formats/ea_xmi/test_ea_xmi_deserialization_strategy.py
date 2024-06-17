import pytest

from umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_deserialization_strategy import (
    EaXmiImportParsingStrategy,
)
from umlars_translator.core.deserialization.formats.ea_xmi.ea_xmi_pipeline import (
    RootPipe,
    UmlModelPipe,
    ExtensionPipe,
    EaXmiDetectionPipe,
)
from umlars_translator.core.deserialization.input_processor import InputProcessor
from umlars_translator.core.model.uml_model import UmlModel
from umlars_translator.core.deserialization.exceptions import (
    UnsupportedFormatException,
    InvalidFormatException,
)


FILES_WITH_EA_XMI_FORMAT = [
    # "tests/core/deserializer/formats/ea_xmi/test_data/ea_xmi_class_basic.xml",
    # "tests/core/deserializer/formats/ea_xmi/test_data/ea_xmi_class_library.xml",
    "tests/core/deserializer/formats/ea_xmi/test_data/ea_xmi_car-model-xmi-21.xml",
]


@pytest.fixture
def ea_xmi_class_data_sources():
    return list(
        InputProcessor().accept_multiple_inputs(
            file_paths_list=FILES_WITH_EA_XMI_FORMAT
        )
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


def test_build_processing_pipe():
    strategy = EaXmiImportParsingStrategy()
    pipe = strategy._build_processing_pipe()
    assert isinstance(pipe, RootPipe)


def test_build_uml_model_processing_pipe():
    strategy = EaXmiImportParsingStrategy()
    root_pipe = strategy._build_processing_pipe()
    uml_model_pipe = strategy._build_uml_model_processing_pipe(root_pipe)
    assert isinstance(uml_model_pipe, UmlModelPipe)


def test_build_extension_processing_pipe():
    strategy = EaXmiImportParsingStrategy()
    root_pipe = strategy._build_processing_pipe()
    extension_pipe = strategy._build_extension_processing_pipe(root_pipe)
    assert isinstance(extension_pipe, ExtensionPipe)


def test_build_format_detection_pipe():
    strategy = EaXmiImportParsingStrategy()
    detection_pipe = strategy._build_format_detection_pipe()
    assert isinstance(detection_pipe, EaXmiDetectionPipe)


def test_when_retrieve_model_from_ea_xmi_then_return_model(ea_xmi_class_data_sources):
    for data_source in ea_xmi_class_data_sources:
        strategy = EaXmiImportParsingStrategy()
        model = strategy.retrieve_model(data_source)
        assert isinstance(model, UmlModel)


def test_when_retrieve_model_from_other_format_then_raise_exception(
    other_format_data_source,
):
    strategy = EaXmiImportParsingStrategy()
    with pytest.raises(UnsupportedFormatException):
        strategy.retrieve_model(other_format_data_source)


def test_when_retrieve_model_from_other_xmi_then_raise_exception(other_xmi_data_source):
    strategy = EaXmiImportParsingStrategy()
    with pytest.raises(InvalidFormatException):
        strategy.retrieve_model(other_xmi_data_source)
