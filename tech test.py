import pygame


class Utilities:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Arial", 30)
        self.TEXT_COLOUR = (255, 255, 255)

        self.BUTTONS_PER_ROW = 2
        self.BUTTON_ROWS = 4
        self.BUTTON_COLOUR = (100, 100, 100)
        self.BUTTON_BORDER_RADIUS = 10

        # as a fraction of the screen to allow for resizing
        self.HORIZONTAL_BUTTON_SPACING = 1 / 10
        self.VERTICAL_BUTTON_SPACING = 1 / 20
        self.BUTTON_WIDTH = 1 / 6
        self.BUTTON_HEIGHT = 1 / 8
        self.HORIZONTAL_OFFSET = self.HORIZONTAL_BUTTON_SPACING
        self.VERTICAL_OFFSET = 1 / 4

    def render_button_text(self, rect: pygame.Rect, text: str, surface: pygame.Surface):

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

        self.render_button_text(button_rect, text, surface)

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
        if button_index >= self.BUTTONS_PER_ROW * self.BUTTON_ROWS:
            return -1

        return button_index


def main() -> None:

    pygame.init()
    pygame.font.init()

    DRINK_NAMES = ["Lemon Tea", "Chocolate", "Coffee"]

    WINDOW_SIZE = WIDTH, HEIGHT = 1600, 900
    BACKGROUND_COLOUR = (55, 0, 55)
    MAX_FPS = 60
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Hot Drinks Machine")
    clock = pygame.time.Clock()
    utilities = Utilities()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                relative_position = (
                    position[0] / screen.get_size()[0],
                    position[1] / screen.get_size()[1],
                )
                button_index = utilities.get_drink_button_pressed(relative_position)
                if button_index >= 0 and button_index < len(DRINK_NAMES):
                    print(DRINK_NAMES[button_index])

        screen.fill(BACKGROUND_COLOUR)

        index = 0
        for drink_name in DRINK_NAMES:
            utilities.draw_button(index, screen, drink_name)
            index += 1
        while index < utilities.BUTTON_ROWS * utilities.BUTTONS_PER_ROW:
            utilities.draw_button(index, screen)
            index += 1

        pygame.display.flip()
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
