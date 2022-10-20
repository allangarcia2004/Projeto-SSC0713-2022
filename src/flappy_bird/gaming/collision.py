from pygame import Rect, Vector2


def collided_circle_rect(circle_center: Vector2, circle_radius: float, rectangle: Rect):
    collision_edge_x = circle_center.x
    collision_edge_y = circle_center.y

    if circle_center.x < rectangle.left:
        collision_edge_x = rectangle.left
    elif circle_center.x > rectangle.right:
        collision_edge_x = rectangle.right

    if circle_center.y < rectangle.top:
        collision_edge_y = rectangle.top
    elif circle_center.y > rectangle.bottom:
        collision_edge_y = rectangle.bottom

    distance_x = circle_center.x - collision_edge_x
    distance_y = circle_center.y - collision_edge_y
    distance_sq = distance_x ** 2 + distance_y ** 2

    if distance_sq <= circle_radius ** 2:
        return True
    return False
