# screens/bunker2.py
import pygame

class BunkerScreen2:
    def __init__(self, screen, font, assets_path, dialogue_path):
        self.screen = screen
        self.font = font
        self.assets_path = assets_path
        self.dialogue_path = dialogue_path

        self.W = screen.get_width()
        self.H = screen.get_height()

        self.COLOR_BG = (8, 8, 18)
        self.COLOR_WALL = (35, 35, 55)
        self.COLOR_LASER = (240, 60, 60)
        self.COLOR_PLAYER = (40, 220, 220)
        self.COLOR_ROCKET = (230, 160, 40)

        pw = int(self.W * 0.028)
        ph = int(self.H * 0.055)
        self.player_speed = max(2, int(self.W * 0.0075))

        self.player_start_x = int(self.W * 0.10)
        self.player_start_y = int(self.H * 0.80)

        self.player_rect = pygame.Rect(
            self.player_start_x,
            self.player_start_y,
            pw,
            ph
        )

        # área mais estreita (corredores mais apertados)
        self.play_area = pygame.Rect(
            int(self.W * 0.10),
            int(self.H * 0.10),
            int(self.W * 0.80),
            int(self.H * 0.78)
        )

        self.rocket_rect = pygame.Rect(
            int(self.W * 0.78),
            int(self.H * 0.18),
            int(self.W * 0.07),
            int(self.H * 0.14)
        )

        self.lasers = []

        # Corredor inferior: série de lasers curtos alternados
        for i in range(4):
            self.lasers.append({
                "rect": pygame.Rect(
                    int(self.W * (0.18 + i * 0.12)),
                    int(self.H * 0.70),
                    int(self.W * 0.08),
                    int(self.H * 0.012)
                ),
                "axis": "x",
                "speed": (1 if i % 2 == 0 else -1) * int(self.W * 0.003),
                "blink": True,
                "blink_timer": 0,
                "blink_interval": 30 + i * 5,
                "active": True
            })

        # “Parede” de lasers verticais no meio
        for i in range(3):
            self.lasers.append({
                "rect": pygame.Rect(
                    int(self.W * 0.45 + i * 0.05),
                    int(self.H * 0.28),
                    int(self.W * 0.012),
                    int(self.H * 0.40)
                ),
                "axis": "y",
                "speed": int(self.H * 0.003) * (1 if i % 2 == 0 else -1),
                "blink": False,
                "blink_timer": 0,
                "blink_interval": 0,
                "active": True
            })

        # Laser horizontal perto do topo piscando rápido
        self.lasers.append({
            "rect": pygame.Rect(
                int(self.W * 0.20),
                int(self.H * 0.32),
                int(self.W * 0.55),
                int(self.H * 0.012)
            ),
            "axis": "x",
            "speed": -int(self.W * 0.002),
            "blink": True,
            "blink_timer": 0,
            "blink_interval": 25,
            "active": True
        })

        self.hit_timer = 0
        self.hit_message = "Os protocolos de segurança aqui são muito mais rígidos..."

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
                faded.fill((120, 50, 50, 80))
                self.screen.blit(faded, laser["rect"].topleft)
                continue
            pygame.draw.rect(self.screen, self.COLOR_LASER, laser["rect"])
            glow = pygame.Surface((laser["rect"].width, laser["rect"].height), pygame.SRCALPHA)
            glow.fill((255, 90, 90, 110))
            self.screen.blit(glow, laser["rect"].topleft)

        pygame.draw.rect(self.screen, self.COLOR_ROCKET, self.rocket_rect, border_radius=8)
        txt_f = self.font.render("FOGUETE", True, (20, 20, 20))
        self.screen.blit(
            txt_f,
            (self.rocket_rect.centerx - txt_f.get_width() // 2,
             self.rocket_rect.centery - txt_f.get_height() // 2)
        )

        pygame.draw.rect(self.screen, self.COLOR_PLAYER, self.player_rect, border_radius=6)

        instr = self.font.render(
            "Bunker interno: caminhos mais estreitos e lasers alternados. Cuidado!",
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
