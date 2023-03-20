import numpy as np

def vector2(x, y):
    return np.array((x, y), dtype=np.float64)

def tvector2(tuple):
    return np.array(tuple, dtype=np.float64)


def square_norm(v):
    return np.inner(v, v)


def manhattan_norm(v):
    return sum((abs(x) for x in v))


def point_rect_distance(point, rect):
    dx = abs(point[0] - rect.centerx) - rect.width
    dy = abs(point[1] - rect.centery) - rect.height
    return np.sqrt(max(dx, 0.0) ** 2 + max(dy, 0.0) ** 2) + min(max(dx, dy), 0.0)


def circle_rect_distance(circle, rect):
    return point_rect_distance(circle[:2], rect) - circle[2]


def circle_rect_collision(circle, rect):
    dx = abs(circle[0] - rect.centerx)
    dy = abs(circle[1] - rect.centery)

    w = rect.width / 2
    h = rect.height / 2

    if dx > w + circle[2] or dy > h + circle[2]:
        return False
    if dx <= w or dy <= h:
        return True

    return circle_rect_distance(circle, rect) <= 0.0


def circle_rect_collision_vector(circle, rect):
    closest_x = (
        rect.left
        if circle[0] < rect.left
        else rect.right
        if circle[0] > rect.right
        else circle[0]
    )
    closest_y = (
        rect.top
        if circle[1] < rect.top
        else rect.bottom
        if circle[1] > rect.bottom
        else circle[1]
    )

    v = np.array([circle[0] - closest_x, circle[1] - closest_y])
    l = np.linalg.norm(v)

    return np.zeros(2) if circle[2] < l or l == 0.0 else v / l * (circle[2] - l)


def rotate_vector(v, alpha):
    alpha = np.deg2rad(alpha)
    transformation = np.array(
        [[np.cos(alpha), -np.sin(alpha)], [np.sin(alpha), np.cos(alpha)]]
    )
    return np.dot(transformation, v)


def rotate_vector_rad(v, alpha):
    transformation = np.array(
        [[np.cos(alpha), -np.sin(alpha)], [np.sin(alpha), np.cos(alpha)]]
    )
    return np.dot(transformation, v)
