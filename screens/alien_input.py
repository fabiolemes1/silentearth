import pygame
import time

class AlienInput:
    def __init__(self, state):
        self.state = state
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.bg_color = (10, 0, 20) # Dark Purple
        self.accent_color = (0, 255, 255) # Cyan
        self.error_color = (255, 0, 0) # Red
        
        self.input_text = ""
        self.message = "ENTER DESTINATION COORDINATES"
        self.message_color = self.accent_color
        self.solved = False
        self.cursor_blink = 0
        
        self.target_coords = ["45.12, -93.21", "45.12,-93.21", "45.12 -93.21"]

    def handle_input(self, events):
        if self.solved:
            for ev in events:
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                     # Transition to End Game / Next Level
                     self.state["current"] = "menu" # Placeholder: Back to menu for now
            return

        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    self.validate_input()
                elif ev.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    self.message = "ENTER DESTINATION COORDINATES"
                    self.message_color = self.accent_color
                elif ev.key == pygame.K_ESCAPE:
                    # Optional: Go back to desktop? Or is this a one-way trip?
                    # Let's allow going back to desktop to check files again
                    self.state["current"] = "desktop"
                else:
                    if len(self.input_text) < 20:
                        self.input_text += ev.unicode

    def validate_input(self):
        # Normalize input (remove spaces for easier matching if desired, but let's stick to list)
        if self.input_text.strip() in self.target_coords:
            self.solved = True
            self.message = "TARGET LOCKED. INITIATING TRANSPORT..."
            self.message_color = (0, 255, 0)
        else:
            self.message = "INVALID COORDINATES. SCANNING..."
            self.message_color = self.error_color
            self.input_text = ""

    def draw(self, screen):
        screen.fill(self.bg_color)
        w, h = screen.get_width(), screen.get_height()
        
        # Draw Border
        pygame.draw.rect(screen, self.accent_color, (20, 20, w-40, h-40), 2, border_radius=15)
        
        # Header
        header = self.font.render("ALIEN NAVIGATION SYSTEM v9.0", True, self.accent_color)
        screen.blit(header, (w//2 - header.get_width()//2, 50))
        
        # Message
        msg = self.font.render(self.message, True, self.message_color)
        screen.blit(msg, (w//2 - msg.get_width()//2, h//2 - 50))
        
        # Input Box
        input_rect = pygame.Rect(w//2 - 200, h//2, 400, 50)
        pygame.draw.rect(screen, (20, 20, 40), input_rect, border_radius=5)
        pygame.draw.rect(screen, self.accent_color, input_rect, 2, border_radius=5)
        
        # Input Text
        self.cursor_blink += 1
        cursor = "|" if (self.cursor_blink // 30) % 2 == 0 else ""
        txt = self.font.render(self.input_text + cursor, True, (255, 255, 255))
        screen.blit(txt, (input_rect.x + 10, input_rect.y + 10))
        
        # Instructions
        if not self.solved:
            instr = self.small_font.render("[ENTER] SUBMIT   [ESC] RETURN TO TERMINAL", True, (100, 100, 150))
            screen.blit(instr, (w//2 - instr.get_width()//2, h - 60))
        else:
            instr = self.small_font.render("PRESS [ENTER] TO ENGAGE HYPERDRIVE", True, (0, 255, 0))
            screen.blit(instr, (w//2 - instr.get_width()//2, h - 60))
