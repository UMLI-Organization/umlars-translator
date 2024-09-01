import pytest

from kink import di

from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_deserialization_strategy import (
    StarumlMDJDeserializationStrategy,
)
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_model_processing_pipeline import (
    RootPipe, UmlModelPipe,
)
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_format_detection_pipeline import (
    StarumlMDJDetectionPipe,
)
from src.umlars_translator.core.deserialization.input_processor import InputProcessor
from src.umlars_translator.core.model.abstract.uml_model import IUmlModel
from src.umlars_translator.core.model.abstract.uml_elements import (
    IUmlClass, IUmlAttribute, IUmlOperation, IUmlInterface, IUmlEnumeration, 
    IUmlDataType, IUmlPrimitiveType, IUmlAssociation, IUmlAssociationEnd, 
    IUmlGeneralization, IUmlRealization
)
from src.umlars_translator.core.model.umlars_model.uml_model_builder import (
    UmlModelBuilder,
)
from src.umlars_translator.core.model.constants import UmlVisibilityEnum, UmlAssociationDirectionEnum, UmlPrimitiveTypeKindEnum

CAR_MODEL_FILE_PATH = "tests/core/deserializer/formats/staruml_mdj/test_data/staruml-car-model-with-sequence.mdj"

FILES_WITH_MDJ_FORMAT = [
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
def staruml_mdj_deserialization_strategy_factory():
    class StarumlMDJDeserializationStrategyFactory:
        def create_strategy(self, model_builder):
            return StarumlMDJDeserializationStrategy(model_builder=model_builder)

    return StarumlMDJDeserializationStrategyFactory()

@pytest.fixture
def staruml_mdj_class_data_sources():
    return list(
        InputProcessor().accept_multiple_inputs(
            file_paths_list=FILES_WITH_MDJ_FORMAT
        )
    )

def test_build_processing_pipe(
    umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    pipe = strategy._build_processing_pipe()
    assert isinstance(pipe, RootPipe)

def test_build_format_detection_pipe(
    umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
        model_builder=umlars_model_builder
    )
    detection_pipe = strategy._build_format_detection_pipe()
    assert isinstance(detection_pipe, StarumlMDJDetectionPipe)

def test_when_retrieve_model_from_mdj_then_return_model(
    staruml_mdj_class_data_sources,
    umlars_model_builder,
    staruml_mdj_deserialization_strategy_factory,
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)
        assert isinstance(model, IUmlModel)

        # Test the name of the model
        assert model.name == "Model"

def test_when_deserialize_car_model_file_then_correct_classes_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_classes = {
        "Person": {"visibility": UmlVisibilityEnum.PACKAGE},
        "Car": {"visibility": UmlVisibilityEnum.PUBLIC},
        "Driver": {"visibility": UmlVisibilityEnum.PUBLIC},
        "Wheel": {"visibility": UmlVisibilityEnum.PUBLIC},
    }

    assert isinstance(model.elements.classes, list)
    assert len(model.elements.classes) == 4

    for cls in model.elements.classes:
        assert isinstance(cls, IUmlClass)
        assert cls.name in expected_classes
        assert cls.visibility == expected_classes[cls.name]["visibility"]

def test_when_deserialize_car_model_file_then_correct_interfaces_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_interfaces = {
        "Movable": {"visibility": UmlVisibilityEnum.PUBLIC},
    }

    for iface in model.elements.interfaces:
        assert isinstance(iface, IUmlInterface)
        assert iface.name in expected_interfaces
        assert iface.visibility == expected_interfaces[iface.name]["visibility"]

def test_when_deserialize_car_model_file_then_correct_enumerations_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

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
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

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
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_primitives = {
        "String": UmlPrimitiveTypeKindEnum.STRING,
        "Boolean": UmlPrimitiveTypeKindEnum.BOOLEAN,
        "Real": UmlPrimitiveTypeKindEnum.REAL,
    }

    for primitive in model.elements.primitive_types:
        assert isinstance(primitive, IUmlPrimitiveType)
        assert primitive.name in expected_primitives
        assert primitive.kind == expected_primitives[primitive.name]

def test_when_deserialize_car_model_file_then_correct_associations_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_associations = {
        "car_ownership": {"direction": UmlAssociationDirectionEnum.BIDIRECTIONAL},
    }

    for association in model.elements.associations:
        assert isinstance(association, (IUmlAssociation, IUmlDirectedAssociation))
        assert association.name in expected_associations
        assert association.direction == expected_associations[association.name]["direction"]

def test_when_deserialize_car_model_file_then_correct_operations_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_operations = {
        "Car": ["drive"],
        "Person": ["move"],
    }

    for cls in model.elements.classes:
        if cls.name in expected_operations:
            operation_names = [op.name for op in cls.operations]
            assert all(op in operation_names for op in expected_operations[cls.name])
            assert all(isinstance(op, IUmlOperation) for op in cls.operations)

def test_when_deserialize_car_model_file_then_correct_operation_parameters_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_parameters = {
        "drive": ["driver"],
        "isFlat": ["return"]
    }

    for cls in model.elements.classes:
        for operation in cls.operations:
            if operation.name in expected_parameters:
                parameter_names = [param.name for param in operation.parameters]
                assert all(param in parameter_names for param in expected_parameters[operation.name])

def test_when_deserialize_car_model_file_then_correct_generalizations_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_generalizations = ["Driver -> Person"]

    generalizations = [f"{gen.specific.name} -> {gen.general.name}" for gen in model.elements.generalizations]
    assert all(gen in expected_generalizations for gen in generalizations)
    assert all(isinstance(gen, IUmlGeneralization) for gen in model.elements.generalizations)

def test_when_deserialize_car_model_file_then_correct_realizations_created(
    staruml_mdj_class_data_sources, umlars_model_builder, staruml_mdj_deserialization_strategy_factory
):
    for data_source in staruml_mdj_class_data_sources:
        strategy = staruml_mdj_deserialization_strategy_factory.create_strategy(
            model_builder=umlars_model_builder
        )
        model = strategy.retrieve_model(data_source)

    expected_realizations = ["Car -> Movable", "Person -> Movable"]

    realizations = [f"{realization.client.name} -> {realization.supplier.name}" for realization in model.elements.realizations]
    assert all(realization in expected_realizations for realization in realizations)
    assert all(isinstance(realization, IUmlRealization) for realization in model.elements.realizations)
