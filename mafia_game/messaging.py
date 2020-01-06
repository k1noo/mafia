from enum import auto, Enum, unique


class MessagePrioritiesEnum(Enum):
    CTRL = 0
    GAME_PLAY = 1


class BaseMessage(object):
    priority = 0
    game_token = None

    def __cmp__(self, other):
        return self.priority < other.priority


class CtrlMessage(BaseMessage):
    def __init__(self, game_token):
        self.game_token = game_token
        self.priority = MessagePrioritiesEnum.CTRL.value


class PlayerCtrlMessage(CtrlMessage):
    @unique
    class Type(Enum):
        REGISTER = auto()
        LEAVE = auto()

    def __init__(self, game_token, player_id, msg_type: Type):
        super().__init__(game_token)
        self.player_id = player_id
        self.type = msg_type


class GameSessionCtrlMessage(CtrlMessage):
    @unique
    class Type(Enum):
        INIT = auto()
        RUN = auto()
        STOP = auto()
        RESTART = auto()

    def __init__(self, msg_type: Type, game_token=None):
        super().__init__(game_token)
        self.type = msg_type


class GamePlayMessage(BaseMessage):
    def __init__(self, game_token):
        self.game_token = game_token
        self.priority = MessagePrioritiesEnum.GAME_PLAY.value


class DayGamePlayMessage(GamePlayMessage):
    @unique
    class Type(Enum):
        VOTE = auto()
        LAST_WORD = auto()
        HANG = auto()

    def __init__(self, game_token, msg_type: Type):
        super().__init__(game_token)
        self.type = msg_type


class NightGamePlayMessage(GamePlayMessage):
    @unique
    class Type(Enum):
        ROLE_ACTION = auto()
        MAFIA_VOTE = auto()
        KILL = auto()

    def __init__(self, game_token, msg_type: Type):
        super().__init__(game_token)
        self.type = msg_type
