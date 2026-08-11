class definition_of_colours():
    def __init__(self, object_colour: tuple, background_colour: tuple) -> None:
        self.object_colour = object_colour
        self.background_colour = background_colour
black = definition_of_colours((0, 0, 0), (0, 0, 0))
dark_blue = definition_of_colours((0, 0, 170), (0, 0, 42))
dark_green = definition_of_colours((0, 170, 0), (0, 42, 0))
dark_aqua = definition_of_colours((0, 170, 170), (0, 42, 42))
dark_red = definition_of_colours((170, 0, 0), (42, 0, 0))
dark_purple = definition_of_colours((170, 0, 170), (42, 0, 42))
gold = definition_of_colours((255, 170, 0), (64, 42, 0))
gray = definition_of_colours((170, 170, 170), (42, 42, 42))
dark_gray = definition_of_colours((85, 85, 85), (21, 21, 21))
blue = definition_of_colours((85, 85, 255), (21, 21, 63))
green = definition_of_colours((85, 255, 85), (21, 63, 21))
aqua = definition_of_colours((85, 255, 255), (21, 63, 63))
red = definition_of_colours((255, 85, 85), (63, 21, 21))
light_purple = definition_of_colours((255, 85, 255), (63, 21, 63))
yellow = definition_of_colours((255, 255, 85), (63, 63, 21))
white = definition_of_colours((255, 255, 255), (63, 63, 63))