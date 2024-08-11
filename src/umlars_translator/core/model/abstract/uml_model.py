from abc import ABC

from src.umlars_translator.core.utils.visitor import IVisitable, IVisitor


# TODO: add accept to the other elements
class IUmlModel(IVisitable, ABC):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_model(self)