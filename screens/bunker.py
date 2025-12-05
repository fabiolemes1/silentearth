# screens/bunker.py
import pygame

class BunkerScreen:
    def __init__(self, screen, font, assets_path, dialogue_path):
        self.screen = screen
        self.font = font
        self.assets_path = assets_path
        self.dialogue_path = dialogue_path

        self.W = screen.get_width()
        self.H = screen.get_height()

        # Cores
        self.COLOR_BG = (10, 10, 20)      # fundo do bunker
        self.COLOR_WALL = (40, 40, 60)
        self.COLOR_LASER = (220, 40, 40)
        self.COLOR_PLAYER = (40, 220, 220)
        self.COLOR_ROCKET = (230, 160, 40)

        # Player
        pw = int(self.W * 0.03)
        ph = int(self.H * 0.06)
        self.player_speed = max(2, int(self.W * 0.007))  # velocidade proporcional

        self.player_start_x = int(self.W * 0.12)
        self.player_start_y = int(self.H * 0.78)

        self.player_rect = pygame.Rect(
            self.player_start_x,
            self.player_start_y,
            pw,
            ph
        )

        # Área jogável (como se fossem as paredes do bunker)
        self.play_area = pygame.Rect(
            int(self.W * 0.08),
            int(self.H * 0.12),
            int(self.W * 0.84),
            int(self.H * 0.76)
        )

        # Foguete (objetivo)
        rw = int(self.W * 0.08)
        rh = int(self.H * 0.16)
        self.rocket_rect = pygame.Rect(
            int(self.W * 0.78),
            int(self.H * 0.18),
            rw,
            rh
        )

        # ============================
        # LASERS – FASE 1 (difícil, mas não absurdo)
        # ============================
        self.lasers = []

        # Laser horizontal inferior (se move pra esquerda/direita)
        self.lasers.append({
            "rect": pygame.Rect(
                int(self.W * 0.18),
                int(self.H * 0.63),
                int(self.W * 0.45),
                int(self.H * 0.012)
            ),
            "axis": "x",
            "speed": int(self.W * 0.003),
            "blink": False,
            "blink_timer": 0,
            "blink_interval": 0,
            "active": True
        })

        # Laser horizontal intermediário piscando
        self.lasers.append({
            "rect": pygame.Rect(
                int(self.W * 0.25),
                int(self.H * 0.50),
                int(self.W * 0.58),
                int(self.H * 0.012)
            ),
            "axis": "x",
            "speed": -int(self.W * 0.0025),
            "blink": True,
            "blink_timer": 0,
            "blink_interval": 45,   # ~0.75s ligado/desligado
            "active": True
        })

        # Laser vertical à esquerda (fixo)
        self.lasers.append({
            "rect": pygame.Rect(
                int(self.W * 0.40),
                int(self.H * 0.28),
                int(self.W * 0.012),
                int(self.H * 0.30)
            ),
            "axis": "y",
            "speed": 0,
            "blink": False,
            "blink_timer": 0,
            "blink_interval": 0,
            "active": True
        })

        # Laser vertical à direita, piscando e se movendo
        self.lasers.append({
            "rect": pygame.Rect(
                int(self.W * 0.58),
                int(self.H * 0.40),
                int(self.W * 0.012),
                int(self.H * 0.34)
            ),
            "axis": "y",
            "speed": int(self.H * 0.003),
            "blink": True,
            "blink_timer": 0,
            "blink_interval": 35,
            "active": True
        })

        # Feedback de dano
        self.hit_timer = 0
        self.hit_message = "Você foi atingido pelos lasers! Tentando novamente..."

    def reset_player(self):
        self.player_rect.x = self.player_start_x
        self.player_rect.y = self.player_start_y

    def _update_lasers(self):
        for laser in self.lasers:
            # Movimento
            if laser["axis"] == "x" and laser["speed"] != 0:
                laser["rect"].x += laser["speed"]
                if laser["rect"].left < self.play_area.left + int(self.W * 0.08) or \
                   laser["rect"].right > self.play_area.right - int(self.W * 0.08):
                    laser["speed"] *= -1

            elif laser["axis"] == "y" and laser["speed"] != 0:
                laser["rect"].y += laser["speed"]
                if laser["rect"].top < self.play_area.top + int(self.H * 0.06) or \
                   laser["rect"].bottom > self.play_area.bottom - int(self.H * 0.06):
                    laser["speed"] *= -1

            # Piscar
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

        # Colisão
        hit = False
        for laser in self.lasers:
            if not laser["active"]:
                continue
            if self.player_rect.colliderect(laser["rect"]):
                hit = True
                break

        if hit:
            self.reset_player()
            self.hit_timer = 90

        if self.hit_timer > 0:
            self.hit_timer -= 1

        # Objetivo
        if self.player_rect.colliderect(self.rocket_rect):
            return "complete"

        return None

    def draw(self):
        self.screen.fill(self.COLOR_BG)
        pygame.draw.rect(self.screen, self.COLOR_WALL, self.play_area, border_radius=12)

        # lasers
        for laser in self.lasers:
            if not laser["active"]:
                faded = pygame.Surface((laser["rect"].width, laser["rect"].height), pygame.SRCALPHA)
                faded.fill((100, 40, 40, 80))
                self.screen.blit(faded, laser["rect"].topleft)
                continue
            pygame.draw.rect(self.screen, self.COLOR_LASER, laser["rect"])
            glow = pygame.Surface((laser["rect"].width, laser["rect"].height), pygame.SRCALPHA)
            glow.fill((255, 80, 80, 90))
            self.screen.blit(glow, laser["rect"].topleft)

        # Foguete
        pygame.draw.rect(self.screen, self.COLOR_ROCKET, self.rocket_rect, border_radius=8)
        txt_f = self.font.render("FOGUETE", True, (20, 20, 20))
        self.screen.blit(
            txt_f,
            (self.rocket_rect.centerx - txt_f.get_width() // 2,
             self.rocket_rect.centery - txt_f.get_height() // 2)
        )

        # Player
        pygame.draw.rect(self.screen, self.COLOR_PLAYER, self.player_rect, border_radius=6)

        instr = self.font.render(
            "Use W, A, S, D para se mover. Evite os lasers e alcance o foguete.",
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
