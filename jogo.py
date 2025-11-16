import pgzero
import random
import math
from pygame import Rect


WIDTH = 512
HEIGHT = 320

GHOST_IMAGES = ['tile_0121', 'tile_0108']

HERO_FRAMES = {
    "up": ["player_walk_behind0", "player_walk_behind1"],
    "down": ["player_walk0", "player_walk1"],
    "left": ["player_walk_left0", "player_walk_left1"],
    "right": ["player_walk_right0", "player_walk_right1"]
}

HERO_IDLE = ["player_idle1", "player_idle2", "player_idle3"]

HERO_ATTACK = {
    "up": "player_attack_up0",
    "down": "player_attack_down0",
    "left": "player_attack_left0",
    "right": "player_attack_right0"
}

menu = True
running = False
game_over = False
sound_on = True

start_button = Rect(WIDTH // 2 - 90, HEIGHT // 2 - 36, 180, 40)
music_button = Rect(WIDTH // 2 - 90, HEIGHT // 2 + 12, 180, 34)
exit_button  = Rect(WIDTH // 2 - 90, HEIGHT // 2 + 56, 180, 34)

enemies = []
attack = []

frame_counter = 0
score = 0
survival_seconds = 0
min_enemies = 4


class Hero:
    def __init__(self):
        self.facing = "down"
        self.frame_index = 0
        self.idle_index = 0

        self.frame_timer = 0
        self.idle_timer = 0

        self.is_moving = False
        self.speed = 2.6

        self.actor = Actor(HERO_IDLE[0])
        self.actor.pos = (WIDTH // 2, HEIGHT // 2)
        self.actor.scale = 2.0

        self.attack_cooldown = 0
        self.attack_timer = 0
        self.hp = 3

    def update(self):
        dx = 0
        dy = 0

        if keyboard.left:
            dx = -self.speed
            self.facing = "left"
        elif keyboard.right:
            dx = self.speed
            self.facing = "right"

        if keyboard.up:
            dy = -self.speed
            self.facing = "up"
        elif keyboard.down:
            dy = self.speed
            self.facing = "down"

        self.is_moving = (dx != 0 or dy != 0)

        nx = self.actor.x + dx
        ny = self.actor.y + dy

        if 8 < nx < WIDTH - 8:
            self.actor.x = nx
        if 8 < ny < HEIGHT - 8:
            self.actor.y = ny

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1

    def animate(self):
        if self.attack_timer > 0:
            self.actor.image = HERO_ATTACK[self.facing]
            return

        if self.is_moving:
            self.frame_timer += 1
            if self.frame_timer > 5:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(HERO_FRAMES[self.facing])
            self.actor.image = HERO_FRAMES[self.facing][self.frame_index]
        else:
            self.idle_timer += 1
            if self.idle_timer > 17:
                self.idle_timer = 0
                self.idle_index = (self.idle_index + 1) % len(HERO_IDLE)
            self.actor.image = HERO_IDLE[self.idle_index]

    def draw(self):
        self.actor.draw()


class Enemy:
    def __init__(self):
        img = random.choice(GHOST_IMAGES)
        self.actor = Actor(img)
        self.actor.x = random.randint(32, WIDTH - 32)
        self.actor.y = random.randint(32, HEIGHT - 32)
        self.actor.scale = 1.6

        self.speed = random.uniform(0.3, 0.9)

        self.patrol_center = (self.actor.x, self.actor.y)
        self.patrol_radius = random.randint(30, 80)
        self.target = (self.actor.x, self.actor.y)

        self.change_timer = random.randint(50, 150)
        self.frame_timer = 0

    def pick_target(self):
        ang = random.random() * math.tau
        r = random.random() * self.patrol_radius

        tx = self.patrol_center[0] + math.cos(ang) * r
        ty = self.patrol_center[1] + math.sin(ang) * r

        tx = max(20, min(WIDTH - 20, tx))
        ty = max(20, min(HEIGHT - 20, ty))

        self.target = (tx, ty)

    def update(self):
        self.change_timer -= 1
        if self.change_timer <= 0:
            self.change_timer = random.randint(70, 180)
            self.pick_target()

        dx = self.target[0] - self.actor.x
        dy = self.target[1] - self.actor.y
        dist = math.hypot(dx, dy)

        if dist > 0.5:
            self.actor.x += (dx / dist) * self.speed
            self.actor.y += (dy / dist) * self.speed

    def animate(self):
        self.frame_timer = (self.frame_timer + 1) % 60
        bob = 1.0 + math.sin(self.frame_timer / 8) * 0.06
        self.actor.scale = 1.4 * bob

    def draw(self):
        self.actor.draw()


class Attack:
    def __init__(self, x, y, direction):
        self.lifetime = 12

        offs = {
            "up": (0, -34),
            "down": (0, 34),
            "left": (-34, 0),
            "right": (34, 0)
        }

        dx, dy = offs.get(direction, (0, 0))
        self.rect = Rect(int(x + dx - 12), int(y + dy - 12), 24, 24)

    def update(self):
        self.lifetime -= 1

    def draw(self):
        screen.draw.filled_rect(self.rect, (255, 255, 120))
        screen.draw.rect(self.rect, (200, 160, 0))

    def active(self):
        return self.lifetime > 0


#inicializa personagens
hero = Hero()
for _ in range(4):
    enemies.append(Enemy())


def toggle_sound():
    global sound_on
    sound_on = not sound_on
    try:
        music.set_volume(1.0 if sound_on else 0.0)
        if sound_on:
            music.play('menu_music' if menu else 'game_music')
        else:
            music.stop()
    except:
        pass


def start_game():
    global menu, running, game_over, score, survival_seconds

    menu = False
    running = True
    game_over = False
    survival_seconds = 0
    score = 0

    attack.clear()

    hero.actor.pos = (WIDTH // 2, HEIGHT // 2)
    hero.hp = 3

    enemies.clear()
    for _ in range(4):
        enemies.append(Enemy())

    try:
        music.play('game_music')
        music.set_volume(1.0 if sound_on else 0.0)
        sounds.sound_menu_click.play()
    except:
        pass



def check_attack_hit(a, e):
    try:
        ew = int(getattr(e.actor, "width", 32) * getattr(e.actor, "scale", 1.0))
        er = Rect(e.actor.x - ew // 2, e.actor.y - ew // 2, ew, ew)
        return a.rect.colliderect(er)
    except:
        cx = a.rect.x + a.rect.w // 2
        cy = a.rect.y + a.rect.h // 2
        return math.hypot(e.actor.x - cx, e.actor.y - cy) < 24


def update():
    global frame_counter, survival_seconds, running, menu, game_over, score

    if menu or not running or game_over:
        return

    frame_counter += 1
    survival_seconds += 1 / 60

    hero.update()
    for e in enemies:
        e.update()

    for atk in attack[:]:
        atk.update()
        if not atk.active():
            attack.remove(atk)
            continue

        for e in enemies[:]:
            if check_attack_hit(atk, e):
                try:
                    sounds.sound_hurt.play()
                except:
                    pass
                enemies.remove(e)
                score += 1
                break

    hx, hy = hero.actor.x, hero.actor.y
    hw = int(getattr(hero.actor, "width", 32) * hero.actor.scale * 0.5)
    hrect = Rect(hx - hw // 2, hy - hw // 2, hw, hw)

    for e in enemies:
        ew = int(getattr(e.actor, "width", 32) * e.actor.scale * 0.6)
        erect = Rect(e.actor.x - ew // 2, e.actor.y - ew // 2, ew, ew)
        if erect.colliderect(hrect):
            running = False
            game_over = True
            try:
                music.stop()
            except:
                pass
            break

    while len(enemies) < min_enemies:
        enemies.append(Enemy())

    if frame_counter % 6 == 0:
        hero.animate()
        for e in enemies:
            e.animate()


def draw_button(rect, text, size=26):
    screen.draw.filled_rect(rect, (40, 40, 50))
    screen.draw.text(text, center=rect.center, fontsize=size, color=(255, 255, 255))

    x, y, w, h = rect
    b = (100, 100, 120)
    screen.draw.line((x, y), (x + w, y), b)
    screen.draw.line((x + w, y), (x + w, y + h), b)
    screen.draw.line((x + w, y + h), (x, y + h), b)
    screen.draw.line((x, y + h), (x, y), b)


def draw_menu():
    try:
        screen.blit('menu_background', (0, 0))
    except:
        screen.clear()

    cx = WIDTH // 2
    cy = HEIGHT // 2 - 100

    screen.draw.text("Deserto Assombrado", center=(cx + 2, cy + 2), fontsize=42, color=(0, 0, 0))
    screen.draw.text("Deserto Assombrado", center=(cx, cy), fontsize=42, color=(220, 20, 20))

    draw_button(start_button, "JOGAR")
    draw_button(music_button, "MUSICA: LIGADO" if sound_on else "MUSICA: DESLIGADO", size=20)
    draw_button(exit_button, "SAIR", size=20)


def draw_game_over():
    overlay = Rect(0, 0, WIDTH, HEIGHT)
    screen.draw.filled_rect(overlay, (30, 0, 0))

    cx = WIDTH // 2
    cy = HEIGHT // 2 - 30

    screen.draw.text("FIM DE JOGO", center=(cx + 3, cy + 3), fontsize=56, color=(0, 0, 0))
    screen.draw.text("FIM DE JOGO", center=(cx, cy), fontsize=56, color=(220, 20, 20))

    screen.draw.text(f"PONTOS: {score}", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=28)
    screen.draw.text("ENTER - Menu Principal", center=(WIDTH // 2, HEIGHT // 2 + 62), fontsize=18)


def draw():
    screen.clear()

    if menu:
        draw_menu()
        return

    screen.blit('game_map', (0, 0))

    for e in enemies:
        e.draw()
    for atk in attack:
        atk.draw()

    hero.draw()

    screen.draw.text(f"PONTOS: {score}", (8, HEIGHT - 52), fontsize=20)
    screen.draw.text(f"TEMPO: {int(survival_seconds)}s", (8, HEIGHT - 32), fontsize=18)

    if game_over:
        draw_game_over()

def on_mouse_down(pos):
    global menu, running

    if not menu:
        return

    if start_button.collidepoint(pos):
        start_game()

    elif music_button.collidepoint(pos):
        toggle_sound()
        try:
            sounds.sound_menu_click.play()
        except:
            pass

    elif exit_button.collidepoint(pos):
        try:
            sounds.sound_menu_click.play()
        except:
            pass
        quit()



def on_key_down(key):
    global menu, running, game_over

    if running and not game_over:
        if key == keys.SPACE and hero.attack_cooldown <= 0:
            attack.append(Attack(hero.actor.x, hero.actor.y, hero.facing))
            hero.attack_cooldown = 24
            hero.attack_timer = 12
            try:
                sounds.sword_attack.play()
            except:
                pass

    if game_over and key == keys.RETURN:
        menu = True
        running = False
        game_over = False
        try:
            music.play('menu_music')
            music.set_volume(1.0 if sound_on else 0.0)
        except:
            pass

try:
    music.play('menu_music')
    music.set_volume(1.0 if sound_on else 0.0)
except:
    pass
