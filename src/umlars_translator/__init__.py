from src.umlars_translator.bootstrap import bootstrap_di as main_bootstrap_di
from src.umlars_translator.core.model.bootstrap import bootstrap_di as model_bootstrap_di
from src.umlars_translator.core.bootstrap import bootstrap_di as core_bootstrap_di


main_bootstrap_di()

# TODO: move from here
core_bootstrap_di()
model_bootstrap_di()
