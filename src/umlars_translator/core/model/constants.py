from enum import Enum


class DiagramType(Enum):
    """Enum class for diagram types"""
    CLASS = "Class"
    USE_CASE = "UseCase"
    ACTIVITY = "Activity"
    SEQUENCE = "Sequence"
    STATE = "State"
    COMPONENT = "Component"
    DEPLOYMENT = "Deployment"
    OBJECT = "Object"
    COMMUNICATION = "Communication"
    TIMING = "Timing"
    INTERACTION_OVERVIEW = "InteractionOverview"
    CUSTOM = "Custom"
    NONE = "None"