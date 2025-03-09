import pygame
from math import pi


class Utilities:
    def __init__(self, max_fps: int) -> None:
        # holding most constants and variable in the self
        # this is to stop having to passthrough/global the variables
        # this also makes it earier to change constants
        self.font = pygame.font.SysFont("Arial", 30)
        self.TEXT_COLOUR = (255, 255, 255)

        self.MACHINE_COLOUR = (155, 155, 155)
        self.WINDOW_COLOUR = (200, 200, 200)
        self.MUG_COLOUR = (50, 100, 200)
        self.SCREEN_COLOUR = (100, 100, 100)

        self.WATER_COLOUR = (150, 200, 255)
        self.BOILING_WATER_COLOUR = (200, 255, 255)
        self.CHOCOLATE_COLOUR = (100, 80, 50)
        self.TEA_COLOUR = (120, 100, 70)
        self.LEMON_TEA_COLOUR = (160, 140, 70)
        self.COFFEE_COLOUR = self.TEA_COLOUR
        self.MILKY_COFFEE_COLOUR = (160, 140, 110)

        self.FILL_TIME = 2.5 * max_fps

        self.BUTTONS_PER_ROW = 2
        self.BUTTON_ROWS = 4
        self.BUTTON_COLOUR = (0, 100, 200)
        self.BUTTON_BORDER_RADIUS = 10

        # as a fraction of the screen to allow for resizing
        self.HORIZONTAL_BUTTON_SPACING = 1 / 10
        self.VERTICAL_BUTTON_SPACING = 1 / 20
        self.BUTTON_WIDTH = 1 / 6
        self.BUTTON_HEIGHT = 1 / 8
        self.HORIZONTAL_OFFSET = self.HORIZONTAL_BUTTON_SPACING
        self.VERTICAL_OFFSET = 1 / 4

        self.drink = ""
        self.animation_frame = 0

    def render_text(self, rect: pygame.Rect, text: str, surface: pygame.Surface):

        words = [word for word in text.split(" ")]
        space = self.font.size(" ")[0]
        max_width = rect.width

        x = self.BUTTON_BORDER_RADIUS
        y = self.BUTTON_BORDER_RADIUS
        for word in words:
            word_surface = self.font.render(word, 0, self.TEXT_COLOUR)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = self.BUTTON_BORDER_RADIUS
                y += word_height
            surface.blit(word_surface, (rect.topleft[0] + x, rect.topleft[1] + y))
            x += word_width + space

        return surface

    def draw_button(
        self, button_number: int, surface: pygame.Surface, text: str = ""
    ) -> None:
        # button number indexes from 0 and fills lines before moving to the next
        surface_width = surface.get_width()
        surface_height = surface.get_height()

        rect_width = self.BUTTON_WIDTH * surface_width
        rect_height = self.BUTTON_HEIGHT * surface_height

        horizontal_index = button_number % self.BUTTONS_PER_ROW
        rect_x = (
            self.HORIZONTAL_OFFSET * surface_width
            + self.HORIZONTAL_BUTTON_SPACING * horizontal_index * surface_width
            + rect_width * horizontal_index
        )

        vertical_index = button_number // self.BUTTONS_PER_ROW
        rect_y = (
            self.VERTICAL_OFFSET * surface_height
            + self.VERTICAL_BUTTON_SPACING * vertical_index * surface_height
            + rect_height * vertical_index
        )

        button_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        pygame.draw.rect(
            surface,
            self.BUTTON_COLOUR,
            button_rect,
            border_radius=self.BUTTON_BORDER_RADIUS,
        )

        self.render_text(button_rect, text, surface)

    def get_drink_button_pressed(
        self, relative_mouse_position: tuple[float, float]
    ) -> int:
        click_location = [0, 0]
        click_location[0] = relative_mouse_position[0] - self.HORIZONTAL_OFFSET
        click_location[1] = relative_mouse_position[1] - self.VERTICAL_OFFSET

        button_total_width = self.HORIZONTAL_BUTTON_SPACING + self.BUTTON_WIDTH
        horizontal_index = -1
        while click_location[0] > 0:

            # check if click is in the space between buttons
            if (
                click_location[0] > self.BUTTON_WIDTH
                and click_location[0] < button_total_width
            ):
                horizontal_index = -1
            else:
                horizontal_index += 1

            click_location[0] -= button_total_width

        button_total_height = self.VERTICAL_BUTTON_SPACING + self.BUTTON_HEIGHT
        vertical_index = -1
        while click_location[1] > 0:

            # check if click is in the space between buttons
            if (
                click_location[1] > self.BUTTON_HEIGHT
                and click_location[1] < button_total_height
            ):
                vertical_index = -1
            else:
                vertical_index += 1

            click_location[1] -= button_total_height

        if vertical_index == -1 or horizontal_index == -1:
            return -1

        button_index = self.BUTTONS_PER_ROW * vertical_index + horizontal_index
        if (
            button_index >= self.BUTTONS_PER_ROW * self.BUTTON_ROWS
            or horizontal_index >= self.BUTTONS_PER_ROW
        ):
            return -1

        return button_index

    def get_machine_padding(self, surface: pygame.Surface):
        # makes the machine visual scale to the lower of x/y to keep in bounds and square
        size = surface.get_size()
        scale = min(size[0] / 1600, size[1] / 900)

        machine_size = scale * 500
        horizontal_padding = size[0] * 0.6
        vertical_padding = size[1] * 0.25

        return machine_size, horizontal_padding, vertical_padding

    def draw_window_liquid(
        self,
        surface: pygame.Surface,
        colour: tuple[int, int, int],
        fill_amount: float,
    ):

        machine_size, horizontal_padding, vertical_padding = self.get_machine_padding(
            surface
        )

        pygame.draw.rect(
            surface,
            colour,
            pygame.rect.Rect(
                (
                    horizontal_padding + machine_size * 0.6,
                    vertical_padding
                    + machine_size * 0.35
                    + max(1 - fill_amount, 0) * machine_size * 0.5,
                ),
                (
                    machine_size * 0.3,
                    machine_size * 0.5 * fill_amount,
                ),
            ),
        )

    def draw_spout_liquid(
        self,
        surface: pygame.Surface,
        colour: tuple[int, int, int],
        fill_amount: float,
    ):

        machine_size, horizontal_padding, vertical_padding = self.get_machine_padding(
            surface
        )

        pygame.draw.rect(
            surface,
            colour,
            pygame.rect.Rect(
                (
                    horizontal_padding + machine_size * 0.225,
                    vertical_padding
                    + machine_size * 0.4
                    + max(fill_amount * 2 - 1, 0) * machine_size * 0.2,
                ),
                (
                    machine_size * 0.05,
                    machine_size * 0.2 * (1 - abs(fill_amount * 2 - 1)),
                ),
            ),
        )

    def colour_interpolate(
        self,
        colour_1: tuple[int, int, int],
        colour_2: tuple[int, int, int],
        distance: float,
    ):
        r = colour_1[0] + (colour_2[0] - colour_1[0]) * distance
        g = colour_1[1] + (colour_2[1] - colour_1[1]) * distance
        b = colour_1[2] + (colour_2[2] - colour_1[2]) * distance

        return (r, g, b)

    def draw_machine(self, surface: pygame.Surface):

        machine_size, horizontal_padding, vertical_padding = self.get_machine_padding(
            surface
        )

        # main body of machine
        # top arm
        pygame.draw.rect(
            surface,
            self.MACHINE_COLOUR,
            pygame.rect.Rect(
                (horizontal_padding, vertical_padding), (machine_size, machine_size / 3)
            ),
        )
        # main body
        pygame.draw.rect(
            surface,
            self.MACHINE_COLOUR,
            pygame.rect.Rect(
                (horizontal_padding + machine_size / 2, vertical_padding),
                (machine_size / 2, machine_size),
            ),
        )
        # bottom platform
        pygame.draw.rect(
            surface,
            self.MACHINE_COLOUR,
            pygame.rect.Rect(
                (horizontal_padding, vertical_padding + machine_size * 9 / 10),
                (machine_size, machine_size / 10),
            ),
        )
        # spout
        pygame.draw.rect(
            surface,
            self.MACHINE_COLOUR,
            pygame.rect.Rect(
                (
                    horizontal_padding + machine_size / 5,
                    vertical_padding + machine_size / 3,
                ),
                (machine_size / 10, machine_size / 10),
            ),
        )
        # mug body
        pygame.draw.rect(
            surface,
            self.MUG_COLOUR,
            pygame.rect.Rect(
                (
                    horizontal_padding + machine_size / 10,
                    vertical_padding + machine_size * 0.6,
                ),
                (machine_size * 0.3, machine_size * 0.3),
            ),
        )
        # mug arm
        pygame.draw.arc(
            surface,
            self.MUG_COLOUR,
            pygame.rect.Rect(
                (
                    horizontal_padding,
                    vertical_padding + machine_size * 0.65,
                ),
                (machine_size * 0.2, machine_size * 0.2),
            ),
            pi / 2,
            pi * 3 / 2,
            int(machine_size / 50),
        )
        # liquid window
        pygame.draw.rect(
            surface,
            self.WINDOW_COLOUR,
            pygame.rect.Rect(
                (
                    horizontal_padding + machine_size * 0.6,
                    vertical_padding + machine_size * 0.35,
                ),
                (machine_size * 0.3, machine_size * 0.5),
            ),
        )

        # machine screen
        screen_rect = pygame.rect.Rect(
            (
                horizontal_padding + machine_size * 0.05,
                vertical_padding + machine_size * 0.05,
            ),
            ((machine_size * 0.9, machine_size * 0.25)),
        )
        pygame.draw.rect(surface, self.SCREEN_COLOUR, screen_rect)

        # animate the window, screen and spout
        # if no drink active display a message
        if self.drink == "":
            self.render_text(screen_rect, "Please choose a drink :)", surface)
            return 0

        self.animation_frame += 1

        # fill with water, all drinks need it so placed before selection
        if self.animation_frame < self.FILL_TIME:
            # filling with water
            self.render_text(screen_rect, "Filling with water", surface)
            self.draw_window_liquid(
                surface,
                self.WATER_COLOUR,
                self.animation_frame / self.FILL_TIME,
            )

        elif self.animation_frame < self.FILL_TIME * 2:
            # boiling the water
            self.render_text(screen_rect, "Boiling water", surface)
            boiled_amount = self.animation_frame / self.FILL_TIME - 1
            colour = self.colour_interpolate(
                self.WATER_COLOUR, self.BOILING_WATER_COLOUR, boiled_amount
            )
            self.draw_window_liquid(surface, colour, 1)

        else:
            match self.drink:
                case "Chocolate":
                    if self.animation_frame < self.FILL_TIME * 3:
                        self.render_text(screen_rect, "Mixing in chocolate", surface)
                        chocolate_amount = self.animation_frame / self.FILL_TIME - 2
                        colour = self.colour_interpolate(
                            self.BOILING_WATER_COLOUR,
                            self.CHOCOLATE_COLOUR,
                            chocolate_amount,
                        )
                        self.draw_window_liquid(surface, colour, 1)
                    elif self.animation_frame < self.FILL_TIME * 4:
                        self.render_text(screen_rect, "Dispensing", surface)
                        dispensed_amount = self.animation_frame / self.FILL_TIME - 3
                        window_fill_amount = max(1 - dispensed_amount * 2, 0)
                        self.draw_window_liquid(
                            surface, self.CHOCOLATE_COLOUR, window_fill_amount
                        )
                        self.draw_spout_liquid(
                            surface, self.CHOCOLATE_COLOUR, dispensed_amount
                        )
                    elif self.animation_frame < self.FILL_TIME * 5:
                        self.render_text(
                            screen_rect, "Enjoy your hot chocolate :)", surface
                        )
                    else:
                        self.animation_frame = 0
                        return 0

                case "Lemon Tea":
                    if self.animation_frame < self.FILL_TIME * 3:
                        self.render_text(screen_rect, "Brewing tea", surface)
                        tea_amount = self.animation_frame / self.FILL_TIME - 2
                        colour = self.colour_interpolate(
                            self.BOILING_WATER_COLOUR,
                            self.TEA_COLOUR,
                            tea_amount,
                        )
                        self.draw_window_liquid(surface, colour, 1)
                    elif self.animation_frame < self.FILL_TIME * 4:
                        self.render_text(screen_rect, "Adding lemon", surface)
                        lemon_amount = self.animation_frame / self.FILL_TIME - 3
                        colour = self.colour_interpolate(
                            self.TEA_COLOUR,
                            self.LEMON_TEA_COLOUR,
                            lemon_amount,
                        )
                        self.draw_window_liquid(surface, colour, 1)
                    elif self.animation_frame < self.FILL_TIME * 5:
                        self.render_text(screen_rect, "Dispensing", surface)
                        dispensed_amount = self.animation_frame / self.FILL_TIME - 4
                        window_fill_amount = max(1 - dispensed_amount * 2, 0)
                        self.draw_window_liquid(
                            surface, self.LEMON_TEA_COLOUR, window_fill_amount
                        )
                        self.draw_spout_liquid(
                            surface, self.LEMON_TEA_COLOUR, dispensed_amount
                        )
                    elif self.animation_frame < self.FILL_TIME * 6:
                        self.render_text(
                            screen_rect, "Enjoy your lemon tea :)", surface
                        )
                    else:
                        self.animation_frame = 0
                        return 0
                case "Coffee":
                    if self.animation_frame < self.FILL_TIME * 3:
                        self.render_text(screen_rect, "Brewing coffee", surface)
                        coffee_amount = self.animation_frame / self.FILL_TIME - 2
                        colour = self.colour_interpolate(
                            self.BOILING_WATER_COLOUR,
                            self.COFFEE_COLOUR,
                            coffee_amount,
                        )
                        self.draw_window_liquid(surface, colour, 1)
                    elif self.animation_frame < self.FILL_TIME * 4:
                        self.render_text(screen_rect, "Adding sugar and milk", surface)
                        milk_amount = self.animation_frame / self.FILL_TIME - 3
                        colour = self.colour_interpolate(
                            self.COFFEE_COLOUR,
                            self.MILKY_COFFEE_COLOUR,
                            milk_amount,
                        )
                        self.draw_window_liquid(surface, colour, 1)
                    elif self.animation_frame < self.FILL_TIME * 5:
                        self.render_text(screen_rect, "Dispensing", surface)
                        dispensed_amount = self.animation_frame / self.FILL_TIME - 4
                        window_fill_amount = max(1 - dispensed_amount * 2, 0)
                        self.draw_window_liquid(
                            surface, self.MILKY_COFFEE_COLOUR, window_fill_amount
                        )
                        self.draw_spout_liquid(
                            surface, self.MILKY_COFFEE_COLOUR, dispensed_amount
                        )
                    elif self.animation_frame < self.FILL_TIME * 6:
                        self.render_text(screen_rect, "Enjoy your coffee :)", surface)
                    else:
                        self.animation_frame = 0
                        return 0
                case _:
                    print(f"no drink with name {self.drink} :(")
        return 1


def main() -> None:

    pygame.init()
    pygame.font.init()

    DRINK_NAMES = ["Lemon Tea", "Chocolate", "Coffee"]

    WINDOW_SIZE = (1600, 900)
    BACKGROUND_COLOUR = (255, 255, 255)
    MAX_FPS = 60
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Hot Drinks Machine")
    clock = pygame.time.Clock()
    utilities = Utilities(MAX_FPS)

    state = "buttons"
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "buttons":
                    position = pygame.mouse.get_pos()
                    relative_position = (
                        position[0] / screen.get_size()[0],
                        position[1] / screen.get_size()[1],
                    )
                    button_index = utilities.get_drink_button_pressed(relative_position)
                    if (
                        button_index >= 0
                        and button_index < len(DRINK_NAMES)
                        and state == "buttons"
                    ):
                        utilities.drink = DRINK_NAMES[button_index]
                        state = "brewing"

        screen.fill(BACKGROUND_COLOUR)

        index = 0
        for drink_name in DRINK_NAMES:
            utilities.draw_button(index, screen, drink_name)
            index += 1
        while index < utilities.BUTTON_ROWS * utilities.BUTTONS_PER_ROW:
            utilities.draw_button(index, screen)
            index += 1

        brewing_index = utilities.draw_machine(screen)
        if brewing_index == 0:
            state = "buttons"
            utilities.drink = ""

        pygame.display.flip()
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
