from pygame import Surface, Vector2


class WorldSharedData:
    def __init__(self, gravity: float, horizontal_speed: int, screen_size: Vector2, screen: Surface):
        self.gravity = gravity
        self.horizontal_velocity = horizontal_speed
        self.screen_size = screen_size
        self.screen = screen
