# screens/bunker3.py
import pygame

class BunkerScreen3:
    def __init__(self, screen, font, assets_path, dialogue_path):
        self.screen = screen
        self.font = font
        self.assets_path = assets_path
        self.dialogue_path = dialogue_path

        self.W = screen.get_width()
        self.H = screen.get_height()

        self.COLOR_BG = (5, 5, 15)
        self.COLOR_WALL = (30, 30, 50)
        self.COLOR_LASER = (255, 80, 80)
        self.COLOR_PLAYER = (40, 220, 220)
        self.COLOR_ROCKET = (255, 200, 80)

        pw = int(self.W * 0.026)
        ph = int(self.H * 0.05)
        self.player_speed = max(2, int(self.W * 0.008))

        self.player_start_x = int(self.W * 0.12)
        self.player_start_y = int(self.H * 0.80)

        self.player_rect = pygame.Rect(
            self.player_start_x,
            self.player_start_y,
            pw,
            ph
        )

        self.play_area = pygame.Rect(
            int(self.W * 0.08),
            int(self.H * 0.08),
            int(self.W * 0.84),
            int(self.H * 0.80)
        )

        self.rocket_rect = pygame.Rect(
            int(self.W * 0.78),
            int(self.H * 0.16),
            int(self.W * 0.08),
            int(self.H * 0.16)
        )

        self.lasers = []

        # Corredor inferior: grade de lasers com deslocamentos diferentes
        for i in range(5):
            self.lasers.append({
                "rect": pygame.Rect(
                    int(self.W * (0.18 + i * 0.10)),
                    int(self.H * 0.72),
                    int(self.W * 0.07),
                    int(self.H * 0.012)
                ),
                "axis": "x",
                "speed": (1 if i % 2 == 0 else -1) * int(self.W * 0.0035),
                "blink": True,
                "blink_timer": 0,
                "blink_interval": 25 + i * 4,
                "active": True
            })

        # Duas colunas de lasers verticais alternados
        for xmul in (0.42, 0.58):
            for j in range(3):
                self.lasers.append({
                    "rect": pygame.Rect(
                        int(self.W * xmul),
                        int(self.H * (0.28 + j * 0.14)),
                        int(self.W * 0.012),
                        int(self.H * 0.12)
                    ),
                    "axis": "y",
                    "speed": (1 if j % 2 == 0 else -1) * int(self.H * 0.0032),
                    "blink": True,
                    "blink_timer": 0,
                    "blink_interval": 30 + j * 5,
                    "active": True
                })

        # Laser “muralha” no topo piscando rápido
        self.lasers.append({
            "rect": pygame.Rect(
                int(self.W * 0.18),
                int(self.H * 0.26),
                int(self.W * 0.60),
                int(self.H * 0.012)
            ),
            "axis": "x",
            "speed": -int(self.W * 0.0025),
            "blink": True,
            "blink_timer": 0,
            "blink_interval": 20,
            "active": True
        })

        self.hit_timer = 0
        self.hit_message = "Segurança máxima. Se você chegou até aqui, está quase lá..."

    def reset_player(self):
        self.player_rect.x = self.player_start_x
        self.player_rect.y = self.player_start_y

    def _update_lasers(self):
        for laser in self.lasers:
            if laser["axis"] == "x" and laser["speed"] != 0:
                laser["rect"].x += laser["speed"]
                if laser["rect"].left < self.play_area.left + int(self.W * 0.05) or \
                   laser["rect"].right > self.play_area.right - int(self.W * 0.05):
                    laser["speed"] *= -1

            elif laser["axis"] == "y" and laser["speed"] != 0:
                laser["rect"].y += laser["speed"]
                if laser["rect"].top < self.play_area.top + int(self.H * 0.04) or \
                   laser["rect"].bottom > self.play_area.bottom - int(self.H * 0.04):
                    laser["speed"] *= -1

            if laser["blink"]:
                laser["blink_timer"] += 1
                if laser["blink_timer"] >= laser["blink_interval"]:
                    laser["blink_timer"] = 0
                    laser["active"] = not laser["active"]

    def update(self, keys):
        dx = dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.player_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.player_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.player_speed

        if dx or dy:
            self.player_rect.x += dx
            if not self.play_area.contains(self.player_rect):
                self.player_rect.x -= dx

            self.player_rect.y += dy
            if not self.play_area.contains(self.player_rect):
                self.player_rect.y -= dy

        self._update_lasers()

        hit = any(l["active"] and self.player_rect.colliderect(l["rect"]) for l in self.lasers)
        if hit:
            self.reset_player()
            self.hit_timer = 90

        if self.hit_timer > 0:
            self.hit_timer -= 1

        if self.player_rect.colliderect(self.rocket_rect):
            return "complete"

        return None

    def draw(self):
        self.screen.fill(self.COLOR_BG)
        pygame.draw.rect(self.screen, self.COLOR_WALL, self.play_area, border_radius=12)

        for laser in self.lasers:
            if not laser["active"]:
                faded = pygame.Surface((laser["rect"].width, laser["rect"].height), pygame.SRCALPHA)
                faded.fill((140, 60, 60, 80))
                self.screen.blit(faded, laser["rect"].topleft)
                continue

            pygame.draw.rect(self.screen, self.COLOR_LASER, laser["rect"])
            glow = pygame.Surface((laser["rect"].width, laser["rect"].height), pygame.SRCALPHA)
            glow.fill((255, 100, 100, 130))
            self.screen.blit(glow, laser["rect"].topleft)

        pygame.draw.rect(self.screen, self.COLOR_ROCKET, self.rocket_rect, border_radius=10)
        txt_f = self.font.render("FOGUETE", True, (20, 20, 20))
        self.screen.blit(
            txt_f,
            (self.rocket_rect.centerx - txt_f.get_width() // 2,
             self.rocket_rect.centery - txt_f.get_height() // 2)
        )

        pygame.draw.rect(self.screen, self.COLOR_PLAYER, self.player_rect, border_radius=6)

        instr = self.font.render(
            "Último nível do bunker. Se passar por aqui, você descobre o destino da evacuação...",
            True, (230, 230, 230)
        )
        self.screen.blit(instr, (self.play_area.x, self.play_area.y - instr.get_height() - 10))

        if self.hit_timer > 0:
            msg = self.font.render(self.hit_message, True, (255, 200, 200))
            self.screen.blit(
                msg,
                (self.W // 2 - msg.get_width() // 2,
                 int(self.H * 0.9))
            )

    def click(self):
        return None
