import Math


class Ammo:
    g = -9.81

    def __init__(self, velocity=3) -> None:
        self.velocity = velocity
        self.x = None
        self.y = None

    def travel(self, x, y, aim_angle):
        self.x = x
        self.y = y
        starting_angle = aim_angle


class Tank:
    def __init__(self, x, y, health=100, amount=30, aim_angle=30) -> None:
        self.health = health
        self.ammo = Ammo()
        self.ammo_amount = amount
        self.aim_angle = aim_angle
        self.velocity = 0
        self.x = x
        self.y = y

    def fire(self):
        if self.ammo_amount > 0:
            self.ammo_amount -= 1
            self.ammo.travel(self.x, self.y, self.aim_angle)
