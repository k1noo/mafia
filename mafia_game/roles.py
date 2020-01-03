

class BaseRole(object):
    def get_name(self):
        raise NotImplementedError

    def action(self):
        pass


class Villager(BaseRole):
    def get_name(self):
        return "villager"


class Mafia(BaseRole):
    def get_name(self):
        return "mafia"


class Healer(BaseRole):
    def get_name(self):
        return "healer"


class Detective(BaseRole):
    def get_name(self):
        return "detective"

