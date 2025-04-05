from pytest import fixture

from umlars_translator.core.translator import ModelTranslator
from umlars_translator.core.deserialization.input_processor import InputProcessor


CAR_MODEL_FILE_PATH = "tests/core/deserializer/formats/ea_xmi/test_data/ea_car_model_xmi21-with-sequence.xml"


@fixture
def translator() -> ModelTranslator:
    return ModelTranslator()


@fixture
def ea_xmi_car_data_source():
    return InputProcessor().accept_input(file_path=CAR_MODEL_FILE_PATH)


def test_when_given_ea_format_deserialization_successful(ea_xmi_car_data_source, translator) -> None:
    # Given
    # When
    result = translator.translate(data_sources=[ea_xmi_car_data_source])

    # Then
    assert isinstance(result, str)
