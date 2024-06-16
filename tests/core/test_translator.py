from pytest import fixture

from umlars_translator.core.translator import ModelTranslator
from umlars_translator.core.model.uml_model import UmlModel

# test_when_given_ea_data_deserialization_successful


@fixture
def translator() -> ModelTranslator:
    return ModelTranslator()


@fixture
def ea_data() -> str:
    return """<xmi:XMI xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1">
    <xmi:Documentation exporter="Enterprise Architect" exporterVersion="6.5" exporterID="1628"/>
    <uml:Model xmi:type="uml:Model" name="unit model" visibility="public">
    </uml:Model>
    <xmi:Extension extender="Enterprise Architect" extenderID="6.5">
        <diagrams>
            <diagram xmi:id="EAID_273DF9F0_0D33_42c1_A84B_86493AF661DD">
                <model package="EAPK_53FD35CE_1AC8_4eb3_837B_A43049AEA5FE" localID="1" owner="EAPK_53FD35CE_1AC8_4eb3_837B_A43049AEA5FE"/>
                <properties name="diagram1" type="Logical"/>
                <elements>
                </elements>
            </diagram>
        </diagrams>
    </xmi:Extension>
</xmi:XMI>
    """


def test_when_given_ea_format_deserialization_successful(ea_data, translator) -> None:
    # Given
    # When
    result = translator.translate(ea_data)

    # Then
    assert isinstance(result, UmlModel)
