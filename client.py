import pygame
from network import Network

pygame.font.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("가위 바위 보, 하나 빼기")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 120
        self.height = 70
        self.font = pygame.font.SysFont("AppleGothic", 26, bold=True)

    def draw(self, win, dim=False):
        if dim:
            rect_color = (50, 50, 50)
            text_color = (120, 120, 120)
        else:
            rect_color = self.color
            text_color = (255, 255, 255)

        pygame.draw.rect(win, rect_color, (self.x, self.y, self.width, self.height), border_radius=25)
        text = self.font.render(self.text, True, text_color)
        win.blit(text, (
            self.x + self.width // 2 - text.get_width() // 2,
            self.y + self.height // 2 - text.get_height() // 2
        ))

    def click(self, pos):
        x1, y1 = pos
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

# Squid Game neon colors for buttons
btns = [
    Button("가위", 35, 300, (3,122,118)),      # teal
    Button("바위", 185, 300, (3,122,118)),     # purple
    Button("보", 335, 300, (3,122,118))         # red
]


def redrawWindow(win, game, p, phase, my_choices):
    # Squid Game inspired hot pink background
    win.fill((244,71,134)
)

    title_font = pygame.font.SysFont("AppleGothic", 36)
    small_font = pygame.font.SysFont("AppleGothic", 22)

    if not game or not game.connected():
        text = title_font.render("Waiting for Opponent...", True, (0, 0, 0))
        win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    else:
        if phase == 1:
            text = title_font.render("가위 바위 보!", True, (0, 0, 0))
        elif phase == 2:
            text = title_font.render("하나 빼기!", True, (0, 0, 0))
        else:
            winner = game.winner()
            if winner == -1:
                result = "무승부!"
            elif winner == p:
                result = "승!"
            else:
                result = "패!"
            text = title_font.render(result, True, (0, 0, 0))

        win.blit(text, (width // 2 - text.get_width() // 2, 50))

        if phase >= 2:
            vs = small_font.render(f"P1: {game.p1Choices}  VS  P2: {game.p2Choices}", True, (20, 20, 20))
            win.blit(vs, (width // 2 - vs.get_width() // 2, 150))

        for btn in btns:
            if phase == 1:
                btn.draw(win, dim=(btn.text in my_choices))
            elif phase == 2:
                if btn.text in my_choices:
                    btn.draw(win)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player_str = n.getP()
    if player_str is None:
        print("Could not connect to server. Exiting.")
        return

    player = int(player_str)
    phase = 1
    my_choices = []
    result_shown_time = None

    while run:
        clock.tick(60)
        game = n.send("get")
        if not game:
            print("Connection lost. Exiting.")
            break

        if phase == 1 and game.both_chosen_two():
            phase = 2
        if phase == 2 and game.both_committed():
            phase = 3
            result_shown_time = pygame.time.get_ticks()

        if phase == 3 and result_shown_time:
            elapsed = pygame.time.get_ticks() - result_shown_time
            if elapsed > 3000:
                n.send("reset")
                my_choices = []
                phase = 1
                result_shown_time = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos):
                        if phase == 1 and btn.text not in my_choices and len(my_choices) < 2:
                            n.send(f"add:{btn.text}")
                            my_choices.append(btn.text)
                        elif phase == 2 and btn.text in my_choices:
                            n.send(f"commit:{btn.text}")

        redrawWindow(win, game, player, phase, my_choices)

if __name__ == "__main__":
    main()
