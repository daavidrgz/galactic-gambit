def add_border(surface, color):
    temp_data = surface.copy()
    w = surface.get_width()
    h = surface.get_height()

    def check_alpha(x, y, l):
        if x < 0 or y < 0 or x >= w or y >= h: return False
        return temp_data.get_at((x, y))[3] >= l
    
    for x in range(w):
        for y in range(h):
            if not check_alpha(x, y, 250):
                if check_alpha(x+1, y, 1) or check_alpha(x, y+1, 1) or check_alpha(x-1, y, 1) or check_alpha(x, y-1, 1):
                    surface.set_at((x, y), color)