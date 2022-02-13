import random, sys, pygame
from settings import *
from support import import_folder

pygame.init()
pygame.display.set_caption('Blackjack')


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'playing'
        self.players = 1
        self.values = list(range(2, 11)) + "Jack Queen King Ace".split()
        self.suits = "♥⯁♠♣"
        self.deck = [f'{v} {s}' for s in self.suits for v in self.values]
        random.shuffle(self.deck)
        self.hand_value = []
        self.hand = self.deck[:2]
        self.deck = self.deck[2:]
        self.num = 0

        self.p1_turn = True
        self.dealer_turn = False

        global card
        global suit

        self.load()
        self.import_card_assets()

    def run(self):
        while self.running:
            self.pos = pygame.mouse.get_pos()
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
                self.calculate_value()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ############### HELPER FUNCTIONS ###############

    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        pos[0] = pos[0] - text_size[0] / 2
        pos[1] = pos[1] - text_size[1] / 2
        screen.blit(text, pos)

    def load(self):
        self.bg = pygame.image.load('assets/Background.jpg').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.hit_button = pygame.image.load('assets/button_hit.png').convert_alpha()
        self.hit_button_rect = self.hit_button.get_rect()
        self.hit_button_rect.center = ((WIDTH / 2) - 150, 600)
        self.stand_button = pygame.image.load('assets/button_stand.png').convert_alpha()
        self.stand_button_rect = self.stand_button.get_rect()
        self.stand_button_rect.center = ((WIDTH / 2) + 150, 600)

    def deal_card(self):
        return self.deck.pop()

    def deal_hand(self):
        self.hand = []
        for i in range(2):
            self.hand.append(self.deal_card())
            self.deck.pop()
            self.calculate_value()
        return self.hand

    def hit(self):
        value = (self.calculate_value())
        if len(self.hand) >= 2 and value < 21:
            self.hand.append(self.deal_card())
        else:
            print("You busted retard... no more hitting")
        return self.hand, self.deck.pop()

    def stay(self):
        value = (self.calculate_value())
        if value < 21:
            print('stayed')
        else:
            print("You busted retard... you can't stay anymore")

    def calculate_value(self):
        value = 0
        aces = 0
        for card in self.hand:
            if card[0] == "A":
                aces += 1
            elif card[0] in ["J", "Q", "K"]:
                value += 10
            else:
                value += int(card.split()[0])
                # FIX ACES
        while aces > 0 and value + 11 <= 21 and len(self.hand) >= 2:
            value += 11
            aces -= 1
            if aces == 2:
                value = 12
                aces -= 2
        while aces > 0 and value + 1 < 21:
            value += 1
            aces -= 1
        return value

    def import_card_assets(self):
        self.card_path = 'assets/cards/'
        self.cards = {'clubs': [], 'spades': [], 'hearts': [], 'diamonds': []}

        for card in self.cards.keys():
            self.full_path = self.card_path + card
            self.cards[card] = import_folder(self.full_path)

    def playing_update(self):
        pass

    ############### INTRO FUNCTIONS ###############

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        pygame.display.update()

    ############### PLAYING FUNCTIONS ###############

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # HIT BUTTON
                    if self.hit_button_rect.collidepoint(self.pos):
                        value = (self.calculate_value())
                        if value < 21:
                            self.hit()
                            self.calculate_value()
                    # STAY BUTTON
                    if self.stand_button_rect.collidepoint(self.pos):
                        self.stay()

    def playing_draw(self):
        self.screen.blit(self.bg, (0, 0))
        value = (self.calculate_value())

        card_n = 0
        for card in self.hand:
            mapping = {"2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "1": "ten", "A": "ace", "J": "jack", "Q": "queen", "K": "king"}

            self.num = mapping[card[0]]

            if card.split()[1] == "♠":
                suit = "spades"
                self.img = pygame.image.load(
                    "assets/cards/" + suit + "/" + self.num + "-" + suit + ".webp").convert_alpha()
                self.img = pygame.transform.scale(self.img, (100, 100))
                self.screen.blit(self.img, ((WIDTH / 3 - 100 * len(self.cards) / 2) + 100 * card_n, 250))

            if card.split()[1] == "⯁":
                suit = "diamonds"
                self.img = pygame.image.load(
                    "assets/cards/" + suit + "/" + self.num + "-" + suit + ".webp").convert_alpha()
                self.img = pygame.transform.scale(self.img, (100, 100))
                self.screen.blit(self.img, ((WIDTH / 3 - 100 * len(self.cards) / 2) + 100 * card_n, 250))

            if card.split()[1] == "♣":
                suit = "clubs"
                self.img = pygame.image.load(
                    "assets/cards/" + suit + "/" + self.num + "-" + suit + ".webp").convert_alpha()
                self.img = pygame.transform.scale(self.img, (100, 100))
                self.screen.blit(self.img, ((WIDTH / 3 - 100 * len(self.cards) / 2) + 100 * card_n, 250))

            if card.split()[1] == "♥":
                suit = "hearts"
                self.img = pygame.image.load(
                    "assets/cards/" + suit + "/" + self.num + "-" + suit + ".webp").convert_alpha()
                self.img = pygame.transform.scale(self.img, (100, 100))
                self.screen.blit(self.img, ((WIDTH / 3 - 100 * len(self.cards) / 2) + 100 * card_n, 250))
            card_n += 1

        if value > 21:
            self.draw_text("BUST", self.screen, [(WIDTH / 2) - 25, 450], 50, 5, "black")
        if value == 21:
            self.draw_text("BLACKJACK", self.screen, [(WIDTH / 2) - 25, 450], 50, 5, "black")

        self.screen.blit(self.hit_button, self.hit_button_rect)
        self.screen.blit(self.stand_button, self.stand_button_rect)
        self.draw_text("Blackjack", self.screen, [WIDTH / 2, 50], 100, 10, "black")
        pygame.display.flip()
        pygame.display.update()
