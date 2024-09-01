from enum import Enum


class UmlAssociationTypeEnum(str, Enum):
    ASSOCIATION = "association"
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"


class UmlInteractionOperatorEnum(str, Enum):
    ALT = "alt"
    BREAK = "break"
    CRITICAL = "critical"
    ELSE = "else"
    IGNORE = "ignore"
    LOOP = "loop"
    PAR = "par"
    STRICT = "strict"
    NEG = "neg"
    ASSERT = "assert"
    REF = "ref"
    SEQ = "seq"
    SD = "sd"
    OPT = "opt"

class UmlParameterDirectionEnum(str, Enum):
    IN = "in"
    OUT = "out"
    INOUT = "inout"
    RETURN = "return"

class UmlMessageSortEnum(str, Enum):
    SYNCH_CALL = "synchCall"
    ASYNCH_CALL = "asynchCall"
    REPLY = "reply"
    CREATE = "create"
    DELETE = "delete"


class UmlMessageKindEnum(str, Enum):
    COMPLETE = "complete"
    LOST = "lost"
    FOUND = "found"
    UNKNOWN = "unknown"


class UmlVisibilityEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    PACKAGE = "package"


class UmlMultiplicityEnum(str, Enum):
    ZERO_OR_ONE = "0..1"
    ONE = "1"
    ZERO_OR_MORE = "0..*"
    ONE_OR_MORE = "1..*"


# TODO: new deserialized type has to supply mapping of primitive types
class UmlPrimitiveTypeKindEnum(str, Enum):
    """Enum class for primitive types"""

    STRING = "String"
    INTEGER = "Integer"
    FLOAT = "Float"
    CHAR = "Char"
    BOOLEAN = "Boolean"
    REAL = "Real"
    UNLIMITED_NATURAL = "UnlimitedNatural"
    VOID = "Void"
    ANY = "Any"


class UmlAssociationDirectionEnum(str, Enum):
    DIRECTED = "directed"
    BIDIRECTIONAL = "bidirectional"


class UmlDiagramType(str, Enum):
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


class UmlElementType(str, Enum):
    """Enum class for UML element types"""

    PACKAGE = "Package"
    CLASS = "Class"
    INTERFACE = "Interface"
    ENUMERATION = "Enumeration"
    PRIMITIVE_TYPE = "PrimitiveType"
    DATA_TYPE = "DataType"
    SIGNAL = "Signal"
    ARTIFACT = "Artifact"
    COMPONENT = "Component"
    COLLABORATION = "Collaboration"
    NODE = "Node"
    USE_CASE = "UseCase"
    ACTOR = "Actor"
    ACTIVITY = "Activity"
    STATE = "State"
    INTERACTION = "Interaction"
    INTERACTION_FRAGMENT = "InteractionFragment"
    LIFELINE = "Lifeline"
    MESSAGE = "Message"
    EXECUTION_SPECIFICATION = "ExecutionSpecification"
    INTERACTION_USE = "InteractionUse"
    DEPLOYMENT_SPECIFICATION = "DeploymentSpecification"
    DEPLOYMENT_TARGET = "DeploymentTarget"
    DEPLOYMENT = "Deployment"
    ARTIFACT_INSTANCE = "ArtifactInstance"
    COMPONENT_INSTANCE = "ComponentInstance"
    NODE_INSTANCE = "NodeInstance"
    ACTOR_INSTANCE = "ActorInstance"
    USE_CASE_INSTANCE = "UseCaseInstance"
    STATE_MACHINE = "StateMachine"
    STATE_MACHINE_STATE = "StateMachineState"
    ASSOCIATION = "Association"
    DEPENDENCY = "Dependency"
    GENERALIZATION = "Generalization"
    REALIZATION = "Realization"
