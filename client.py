import pygame
from network import Network

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("RPS Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 180
        self.height = 100
        self.font = pygame.font.SysFont("arialrounded", 40, bold=True)

    def draw(self, win, dim=False):
        if dim:
            rect_color = (100, 100, 100)
            text_color = (180, 180, 180)
        else:
            rect_color = self.color
            text_color = (255, 255, 255)

        pygame.draw.rect(win, rect_color, (self.x, self.y, self.width, self.height), border_radius=15)
        text = self.font.render(self.text, True, text_color)
        win.blit(text, (
            self.x + self.width // 2 - text.get_width() // 2,
            self.y + self.height // 2 - text.get_height() // 2
        ))

    def click(self, pos):
        x1, y1 = pos
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

btns = [
    Button("Rock", 50, 500, (52, 152, 219)),
    Button("Paper", 250, 500, (46, 204, 113)),
    Button("Scissors", 450, 500, (231, 76, 60))
]

def redrawWindow(win, game, p, phase, my_choices):
    win.fill((30, 30, 30))
    title_font = pygame.font.SysFont("arialrounded", 50, bold=True)
    small_font = pygame.font.SysFont("arialrounded", 35)

    if not game or not game.connected():
        text = title_font.render("Waiting for opponent...", True, (255, 255, 255))
        win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    else:
        if phase == 1:
            text = title_font.render("Pick 2 moves:", True, (255, 255, 255))
        elif phase == 2:
            text = title_font.render("Commit to 1 move:", True, (255, 255, 255))
        else:
            winner = game.winner()
            if winner == -1:
                result = "It's a Tie!"
            elif winner == p:
                result = "You Won!"
            else:
                result = "You Lost!"
            text = title_font.render(result, True, (255, 255, 255))

        win.blit(text, (width // 2 - text.get_width() // 2, 50))

        if phase >= 2:
            vs = small_font.render(f"P1: {game.p1Choices}  VS  P2: {game.p2Choices}", True, (200, 200, 200))
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

        # Always trust server to switch phase:
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
import pygame
from network import Network

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("RPS Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 180
        self.height = 100
        self.font = pygame.font.SysFont("arialrounded", 40, bold=True)

    def draw(self, win, dim=False):
        if dim:
            rect_color = (100, 100, 100)
            text_color = (180, 180, 180)
        else:
            rect_color = self.color
            text_color = (255, 255, 255)

        pygame.draw.rect(win, rect_color, (self.x, self.y, self.width, self.height), border_radius=15)
        text = self.font.render(self.text, True, text_color)
        win.blit(text, (
            self.x + self.width // 2 - text.get_width() // 2,
            self.y + self.height // 2 - text.get_height() // 2
        ))

    def click(self, pos):
        x1, y1 = pos
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

btns = [
    Button("Rock", 50, 500, (52, 152, 219)),
    Button("Paper", 250, 500, (46, 204, 113)),
    Button("Scissors", 450, 500, (231, 76, 60))
]

def redrawWindow(win, game, p, phase, my_choices):
    win.fill((30, 30, 30))
    title_font = pygame.font.SysFont("arialrounded", 50, bold=True)
    small_font = pygame.font.SysFont("arialrounded", 35)

    if not game or not game.connected():
        text = title_font.render("Waiting for opponent...", True, (255, 255, 255))
        win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    else:
        if phase == 1:
            text = title_font.render("Pick 2 moves:", True, (255, 255, 255))
        elif phase == 2:
            text = title_font.render("Commit to 1 move:", True, (255, 255, 255))
        else:
            winner = game.winner()
            if winner == -1:
                result = "It's a Tie!"
            elif winner == p:
                result = "You Won!"
            else:
                result = "You Lost!"
            text = title_font.render(result, True, (255, 255, 255))

        win.blit(text, (width // 2 - text.get_width() // 2, 50))

        if phase >= 2:
            vs = small_font.render(f"P1: {game.p1Choices}  VS  P2: {game.p2Choices}", True, (200, 200, 200))
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

        # Always trust server to switch phase:
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
