
import random
import sys
 
import pygame
 
# ---------------------------------------------------------------- Configuracion
WIDTH, HEIGHT = 800, 600   # Tamano de pantalla (usado en todo el juego)
FPS = 60                   # Fotogramas por segundo (control con Clock)
 
PURPLE = (138, 79, 255)
BG = (22, 22, 42)
WHITE = (240, 240, 240)
RED = (255, 107, 107)
YELLOW = (255, 214, 90)
GREEN = (120, 230, 180)
 
PLAYER_SIZE = 40
PLAYER_SPEED = 7
START_LIVES = 3
LEVEL_TIME_MS = 10_000     # Cada 10 s sube el nivel
INVINCIBLE_MS = 1_200      # Tiempo de invulnerabilidad tras un golpe
 
 
def draw_text(screen, text, size, color, center=None, topleft=None):
    font = pygame.font.SysFont("arial", size, bold=True)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = center
    if topleft:
        rect.topleft = topleft
    screen.blit(surf, rect)
 
 
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dodge & Collect")
        self.clock = pygame.time.Clock()
        self.state = "welcome"   # welcome | playing | gameover
        self.reset()
 
    # ------------------------------------------------------------------ Estado
    def reset(self):
        self.player = pygame.Rect(
            WIDTH // 2 - PLAYER_SIZE // 2,
            HEIGHT - PLAYER_SIZE - 20,
            PLAYER_SIZE,
            PLAYER_SIZE,
        )
        self.enemies = []   # cada enemigo: [rect, velocidad]
        self.coins = []
        self.score = 0
        self.lives = START_LIVES
        self.level = 1
        self.level_start = pygame.time.get_ticks()
        self.last_hit = -INVINCIBLE_MS
        self.spawn_timer = 0
        self.coin_timer = 0
 
    # ------------------------------------------------------------- Dificultad
    def enemy_speed(self):
        return 3 + self.level * 0.8
 
    def spawn_interval(self):
        return max(250, 900 - self.level * 80)   # ms entre enemigos
 
    def update_difficulty(self):
        now = pygame.time.get_ticks()
        if now - self.level_start >= LEVEL_TIME_MS:
            self.level += 1
            self.level_start = now
 
    # ------------------------------------------------------------------ Logica
    def spawn_enemy(self):
        w = random.randint(30, 70)
        h = random.randint(30, 50)
        rect = pygame.Rect(random.randint(0, WIDTH - w), -h, w, h)
        speed = self.enemy_speed() + random.uniform(-0.5, 1.0)
        self.enemies.append([rect, speed])
 
    def spawn_coin(self):
        rect = pygame.Rect(random.randint(10, WIDTH - 30), -20, 20, 20)
        self.coins.append(rect)
 
    def update_playing(self, dt):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        self.player.x += dx * PLAYER_SPEED
        self.player.y += dy * PLAYER_SPEED
        self.player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
 
        self.update_difficulty()
 
        # Aparicion de enemigos y monedas
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval():
            self.spawn_timer = 0
            self.spawn_enemy()
        self.coin_timer += dt
        if self.coin_timer >= 1800:
            self.coin_timer = 0
            self.spawn_coin()
 
        now = pygame.time.get_ticks()
 
        # Mover enemigos y comprobar colisiones
        for enemy in self.enemies[:]:
            rect, speed = enemy
            rect.y += speed
            if rect.top > HEIGHT:            # esquivado -> +1 punto
                self.enemies.remove(enemy)
                self.score += 1
            elif rect.colliderect(self.player):
                self.enemies.remove(enemy)
                if now - self.last_hit >= INVINCIBLE_MS:
                    self.lives -= 1
                    self.last_hit = now
                    if self.lives <= 0:
                        self.state = "gameover"
 
        # Monedas: +10 puntos
        for coin in self.coins[:]:
            coin.y += 4
            if coin.colliderect(self.player):
                self.coins.remove(coin)
                self.score += 10
            elif coin.top > HEIGHT:
                self.coins.remove(coin)
 
    # ----------------------------------------------------------------- Dibujo
    def draw_welcome(self):
        self.screen.fill(BG)
        draw_text(self.screen, "DODGE & COLLECT", 56, PURPLE, center=(WIDTH // 2, 170))
        draw_text(self.screen, "Esquiva los bloques rojos y recoge las monedas", 24, WHITE, center=(WIDTH // 2, 260))
        draw_text(self.screen, "Muevete con las flechas o WASD", 22, GREEN, center=(WIDTH // 2, 310))
        draw_text(self.screen, "Monedas: +10   |   Esquivar: +1   |   Tienes 3 vidas", 20, YELLOW, center=(WIDTH // 2, 350))
        draw_text(self.screen, "Pulsa cualquier tecla para empezar", 28, WHITE, center=(WIDTH // 2, 450))
 
    def draw_playing(self):
        self.screen.fill(BG)
        now = pygame.time.get_ticks()
 
        for rect, _ in self.enemies:
            pygame.draw.rect(self.screen, RED, rect, border_radius=6)
        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW, coin.center, coin.width // 2)
 
        # Parpadeo del jugador mientras es invulnerable
        invincible = now - self.last_hit < INVINCIBLE_MS
        if not invincible or (now // 100) % 2 == 0:
            pygame.draw.rect(self.screen, PURPLE, self.player, border_radius=6)
 
        # HUD
        draw_text(self.screen, f"Puntos: {self.score}", 26, WHITE, topleft=(15, 10))
        draw_text(self.screen, f"Vidas: {self.lives}", 26, RED, topleft=(15, 44))
        draw_text(self.screen, f"Nivel: {self.level}", 26, GREEN, topleft=(WIDTH - 130, 10))
 
    def draw_gameover(self):
        self.screen.fill(BG)
        draw_text(self.screen, "GAME OVER", 64, RED, center=(WIDTH // 2, 190))
        draw_text(self.screen, f"Puntuacion final: {self.score}", 36, YELLOW, center=(WIDTH // 2, 290))
        draw_text(self.screen, f"Nivel alcanzado: {self.level}", 26, WHITE, center=(WIDTH // 2, 340))
        draw_text(self.screen, "R - Jugar de nuevo", 28, GREEN, center=(WIDTH // 2, 430))
        draw_text(self.screen, "ESC - Salir", 28, WHITE, center=(WIDTH // 2, 475))
 
    # --------------------------------------------------------------- Bucle
    def quit(self):
        pygame.quit()
        sys.exit()
 
    def run(self):
        while True:
            dt = self.clock.tick(FPS)   # ms desde el ultimo frame; limita a FPS
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                    elif self.state == "welcome":
                        self.reset()
                        self.state = "playing"
                    elif self.state == "gameover" and event.key == pygame.K_r:
                        self.reset()
                        self.state = "playing"
 
            if self.state == "welcome":
                self.draw_welcome()
            elif self.state == "playing":
                self.update_playing(dt)
                self.draw_playing()
            else:
                self.draw_gameover()
 
            pygame.display.flip()
 
 
if __name__ == "__main__":
    Game().run()
 