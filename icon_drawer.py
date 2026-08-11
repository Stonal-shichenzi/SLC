folder = [
    {
        "data": [(3, 4), (3, 16), (17, 16), (17, 6), (10, 6), (7, 4)],
        "closed": True
    },
    {
        "data": [(3, 9), (17, 9)],
        "closed": False
    }
]
def draw_element(surface, data: list, colour: tuple, x = 0, y = 0, width = 1):
    import pygame
    def increase(position: tuple, x: int, y: int) -> tuple:
        return (position[0] + x, position[1] + y)
    for i in data:
        if i["closed"]:
            pygame.draw.polygon(surface, colour, map(increase, i["data"]), width)
        else:
            for j in range(len(i["data"]) - 1):
                pygame.draw.line(surface, colour, increase(i["data"][j]), increase(i["data"][j + 1]), width)
def draw_icon_folder(surface, colour: tuple, x = 0, y = 0, width = 1):
    import pygame
    pygame.draw.polygon(surface, colour, ((x + 3, y + 4), (x + 3, y + 16), (x + 17, y + 16), (x + 17, y + 6), (x + 10, y + 6), (x + 7, y + 4)), width)
    pygame.draw.line(surface, colour, (x + 3, y + 9), (x + 17, y + 9), width)