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
from src.umlars_translator.core.model.abstract.uml_elements import IUmlPackage
from src.umlars_translator.core.deserialization.exceptions import (
    InvalidFormatException,
)
from src.umlars_translator.core.model.umlars_model.uml_model_builder import (
    UmlModelBuilder,
)
from src.umlars_translator.core.model.constants import UmlVisibilityEnum


LIBRARY_MODEL_FILE_PATH = "tests/core/deserializer/formats/ea_xmi/test_data/ea_xmi_class_library.xml"


FILES_WITH_EA_XMI_FORMAT = [
    "tests/core/deserializer/formats/ea_xmi/test_data/ea_xmi_class_basic.xml",
    LIBRARY_MODEL_FILE_PATH,
    "tests/core/deserializer/formats/ea_xmi/test_data/ea_xmi_car-model-xmi-21.xml",
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
            file_paths_list=FILES_WITH_EA_XMI_FORMAT
        )
    )


@pytest.fixture
def ea_xmi_library_data_source():
    return InputProcessor().accept_input(file_path=LIBRARY_MODEL_FILE_PATH)


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

def test_when_deserialize_library_file_then_correct_model_created(
    umlars_model_builder, ea_xmi_library_data_source, ea_xmi_deserialization_strategy_factory
):
    # Deserialize the model from the XMI data source
    strategy = ea_xmi_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    model = strategy.retrieve_model(ea_xmi_library_data_source)
    
    # Assertions to check if the created model is an instance of IUmlModel
    assert isinstance(model, IUmlModel)
    assert model.name == "EA_Model"
    
    # Assertions to check if the root package is correctly deserialized
    root_package = model.elements.packages[0]
    assert isinstance(root_package, IUmlPackage)
    assert root_package.name == "Basic Class Diagram with Attributes and Operations"
    
    # Assertions to check if classes are correctly deserialized
    class_a = next(c for c in root_package.elements.classes if c.name == "Class A")
    assert class_a is not None
    assert class_a.visibility == UmlVisibilityEnum.PUBLIC
    
    class_b = next(c for c in root_package.elements.classes if c.name == "Class B")
    assert class_b is not None
    assert class_b.visibility == UmlVisibilityEnum.PUBLIC
    
    class_c = next(c for c in root_package.elements.classes if c.name == "Class C")
    assert class_c is not None
    assert class_c.visibility == UmlVisibilityEnum.PUBLIC
    
    # Assertions to check if attributes of Class A are correctly deserialized
    attribute_a = next(attr for attr in class_a.attributes if attr.name == "Attribute A")
    assert attribute_a is not None
    assert attribute_a.visibility == UmlVisibilityEnum.PRIVATE
    
    attribute_b = next(attr for attr in class_a.attributes if attr.name == "Attribute B")
    assert attribute_b is not None
    assert attribute_b.visibility == UmlVisibilityEnum.PRIVATE
    
    # Assertions to check if operations of Class A are correctly deserialized
    operation_a = next(op for op in class_a.operations if op.name == "Operation A")
    assert operation_a is not None
    assert operation_a.visibility == UmlVisibilityEnum.PUBLIC
    
    operation_b = next(op for op in class_a.operations if op.name == "Operation B")
    assert operation_b is not None
    assert operation_b.visibility == UmlVisibilityEnum.PUBLIC
    
    # Assertions to check if associations are correctly deserialized
    association_a = next(assoc for assoc in root_package.elements.associations if assoc.name == "Association A")
    assert association_a is not None
    assert association_a.visibility == UmlVisibilityEnum.PUBLIC
    
    association_b = next(assoc for assoc in root_package.elements.associations if assoc.name == "Association B")
    assert association_b is not None
    assert association_b.visibility == UmlVisibilityEnum.PUBLIC
    
    # Assertions to check if ends of Association A are correctly deserialized
    assert association_a.end1.role == "role a"
    assert association_a.end2.role == "role b"
    
    # Assertions to check if ends of Association B are correctly deserialized
    assert association_b.end1.role == "role a"
    assert association_b.end2.role == "role c"
    
    # # Assertions to check if Class B and Class C have correct links
    # class_b_link = next(link for link in class_b.links if link.association.name == "Association A")
    # assert class_b_link is not None
    
    # class_c_link = next(link for link in class_c.links if link.association.name == "Association B")
    # assert class_c_link is not None
