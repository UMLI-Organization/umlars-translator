from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, Annotated
import uuid

from dataclass_wizard import property_wizard, json_field, JSONWizard, json_key


if TYPE_CHECKING:
    from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel
    from src.umlars_translator.core.model.umlars_model.uml_model_builder import UmlModelBuilder


@dataclass
class RegisteredInBuilderMixin(JSONWizard, metaclass=property_wizard):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    builder: Annotated[Optional['UmlModelBuilder'], json_key('', dump=False)] = json_field('', default=None, repr=False, init=True, dump=False, hash=False)
    """
    Annotation is used to prevent the builder attribute from being serialized. It should be achievable with the dump=False argument in json_field, 
    but some internal processing converts JSONField type into normal dataclass Field type, which does not support the dump argument.
    """

    @property
    def id(self):
        try:
            return self._id
        except AttributeError:
            self._id = None
            return None

    @id.setter
    def id(self, new_id: str) -> None:
        old_id = self.id
        self._id = new_id
        if self.builder:
            self.builder.register_if_not_present(self, old_id=old_id)

    @property
    def builder(self) -> Optional['UmlModelBuilder']:
        try:
            return self._builder
        except AttributeError:
            self._builder = None
            return None

    @builder.setter
    def builder(self, new_builder: 'UmlModelBuilder'):
        self._builder = new_builder


# TODO: decide if use JSONSerializable / JSONWizard here
@dataclass
class RegisteredInModelMixin(RegisteredInBuilderMixin, metaclass=property_wizard):
    model: Optional['UmlModel'] = json_field('', default=None, repr=False, init=True, dump=False, hash=False)
    builder: Annotated[Optional['UmlModelBuilder'], json_key('', dump=False)] = json_field('', default=None, repr=False, init=True, dump=False, hash=False)
    """
    Duplicated builder attribute required to override the one from RegisteredInBuilderMixin while using dataclass-wizard
    """

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


@dataclass
class NamedElementMixin(metaclass=property_wizard):
    name: Optional[str] = None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, new_name: Optional[str]):
        self._name = new_name
