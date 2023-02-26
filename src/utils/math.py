import numpy as np

def point_rect_distance(point, rect):
    dx = abs(point[0] - rect.centerx) - rect.width
    dy = abs(point[1] - rect.centery) - rect.height
    return np.sqrt(max(dx, 0.0)**2 + max(dy, 0.0)**2) + min(max(dx, dy), 0.0)

def circle_rect_distance(circle, rect):
    return point_rect_distance(circle[:2], rect) - circle[2]

def circle_rect_collision(circle, rect):
    dx = abs(circle[0] - rect.centerx)
    dy = abs(circle[1] - rect.centery)

    w = rect.width / 2
    h = rect.height / 2

    if dx > w + circle[2] or dy > h + circle[2]: return False
    if dx <= w or dy <= h: return True

    return circle_rect_distance(circle, rect) <= 0.0