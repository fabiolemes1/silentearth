import pygame
import sys

class MinigamePassword:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.input_text = ""
        self.message = "ENTER PASSWORD:"
        self.active = True
        self.blink_timer = 0
        self.show_cursor = True
        
        # Colors
        self.BG_COLOR = (10, 20, 10)  # Dark green/black
        self.TEXT_COLOR = (50, 255, 50)  # Retro green
        self.ERROR_COLOR = (255, 50, 50) # Red
        
        self.state = "typing" # typing, success, error
        self.timer = 0

    def update(self):
        self.blink_timer += 1
        if self.blink_timer > 30:
            self.show_cursor = not self.show_cursor
            self.blink_timer = 0
            
        if self.state == "success":
            self.timer += 1
            if self.timer > 60: # Wait 1 second
                return "success"
                
        if self.state == "error":
            self.timer += 1
            if self.timer > 60:
                self.state = "typing"
                self.input_text = ""
                self.message = "ENTER PASSWORD:"
                self.timer = 0
                
        return None

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        # Draw border
        pygame.draw.rect(self.screen, self.TEXT_COLOR, (50, 50, self.screen.get_width()-100, self.screen.get_height()-100), 2)
        
        # Draw message
        msg_surf = self.font.render(self.message, True, self.TEXT_COLOR if self.state != "error" else self.ERROR_COLOR)
        self.screen.blit(msg_surf, (100, 100))
        
        # Draw input
        if self.state == "typing":
            txt_surf = self.font.render(f"> {self.input_text}" + ("_" if self.show_cursor else ""), True, self.TEXT_COLOR)
            self.screen.blit(txt_surf, (100, 150))
            
    def handle_event(self, event):
        if self.state != "typing":
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.upper() == "METEORO":
                    self.state = "success"
                    self.message = "ACCESS GRANTED"
                else:
                    self.state = "error"
                    self.message = "ACCESS DENIED"
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            else:
                if len(self.input_text) < 15 and event.unicode.isprintable():
                    self.input_text += event.unicode.upper()
        return None
