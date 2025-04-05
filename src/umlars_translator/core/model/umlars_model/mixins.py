import uuid
from typing import TYPE_CHECKING, Optional
from typing import Optional

if TYPE_CHECKING:
    from umlars_translator.core.model.umlars_model.uml_model import UmlModel
    from umlars_translator.core.model.umlars_model.uml_model_builder import UmlModelBuilder


class RegisteredInBuilderMixin:
    def __init__(self, id: Optional[str] = None, builder: Optional['UmlModelBuilder'] = None):
        self._id = id or str(uuid.uuid4())
        self.builder = builder
        if builder:
            builder.register_if_not_present(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        old_id = self.id
        self._id = str(new_id)
        if self.builder:
            self.builder.register_if_not_present(self, old_id=old_id)

    @property
    def builder(self) -> Optional['UmlModelBuilder']:
        return self._builder

    @builder.setter
    def builder(self, new_builder: 'UmlModelBuilder'):
        self._builder = new_builder


class RegisteredInModelMixin(RegisteredInBuilderMixin):
    def __init__(self, id: Optional[str] = None, model: Optional['UmlModel'] = None, builder: Optional['UmlModelBuilder'] = None):
        super().__init__(id=id, builder=builder)
        self.model = model
        self.builder = builder

    @property
    def builder(self) -> Optional['UmlModelBuilder']:
        builder = self._builder
        if builder is None and self._model:
            builder = self._model.builder

        return builder

    @builder.setter
    def builder(self, new_builder: 'UmlModelBuilder'):
        self._builder = new_builder
        if new_builder:
            self._model = new_builder.model

    @property
    def model(self) -> Optional['UmlModel']:
        model = self._model
        if model is None and self._builder:
            model = self._builder.model
        return model

    @model.setter
    def model(self, new_model: 'UmlModel'):
        self._model = new_model
        if new_model:
            self._builder = new_model.builder
