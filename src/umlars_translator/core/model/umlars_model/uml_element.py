from dataclasses import dataclass, field
from typing import List, Optional, Union, ClassVar, TYPE_CHECKING
from enum import Enum
import uuid

from dataclass_wizard import property_wizard, JSONWizard
if TYPE_CHECKING:
    from src.umlars_translator.core.model.umlars_model.uml_model_builder import UmlModelBuilder
    from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel


@dataclass
class UmlElement(JSONWizard, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    builder: Optional['UmlModelBuilder'] = field(default=None, repr=False, init=True)
    model: Optional['UmlModel'] = field(default=None, repr=False, init=True)

    @classmethod
    def element_name(cls) -> str:
        try:
            return cls.__ELEMENT_NAME
        except AttributeError:
            return cls.__name__

    @property
    def id(self):
        try:
            return self._id
        except AttributeError:
            return None

    @id.setter
    def id(self, new_id: str) -> None:
        old_id = self.id
        self._id = new_id
        if self.builder:
            self.builder.register_if_not_present(self, old_id)

    @property
    def builder(self) -> Optional['UmlModelBuilder']:
        try:
            builder = self._builder
            self._model = builder.model
        except AttributeError:
            try:
                builder = self._model.builder
                self._builder = builder
            except AttributeError:
                return None
        
        return builder

    @builder.setter
    def builder(self, new_builder: 'UmlModelBuilder'):
        self._builder = new_builder
        if new_builder:
            self._model = new_builder.model

    @property
    def model(self) -> Optional['UmlModel']:
        try:
            model = self._model
            self._builder = model.builder
        except AttributeError:
            try:
                model = self._builder.model
                self._model = model
            except AttributeError:
                return None
        
        return model
        
    @model.setter
    def model(self, new_model: 'UmlModel'):
        self._model = new_model
        if new_model:
            self._builder = new_model.builder

@dataclass(kw_only=True)
class UmlNamedElement(UmlElement):
    name: Optional[str] = None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, new_name: Optional[str]):
        self._name = new_name

