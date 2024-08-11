from abc import ABC, abstractmethod

from src.umlars_translator.core.model.abstract.uml_elements import IUmlElement


class IUmlDiagram(ABC):
    @abstractmethod
    def add_element(self, element: IUmlElement) -> None:
        ...


class IUmlClassDiagram(IUmlDiagram):
    ...


class IUmlSequenceDiagram(IUmlDiagram):
    ...

