from utils.observable import Observable


class Hp(Observable):
    def __init__(self, max_hp):
        super().__init__()
        self.max_hp = max_hp
        self.hp = max_hp

    def setup(self, entity):
        self.entity = entity

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def reduce(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.entity.on_death()
        self.notify_listeners(self)

    def increase(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        self.notify_listeners(self)
