import pygame
import time

class MinigamePassword:
    def __init__(self, state):
        self.state = state
        self.font = pygame.font.SysFont("consolas", 20)
        self.bg_color = (10, 10, 10)
        self.text_color = (0, 255, 0)
        self.input_text = ""
        self.history = [
            "FBI SECURE TERMINAL v4.0.1",
            "SYSTEM RECOVERY MODE",
            "--------------------------",
            "ENTER PASSWORD TO ACCESS MAINFRAME",
            "Type 'help' for available commands.",
            ""
        ]
        self.files = {
            "notes.txt": "Lembrete: A senha é o ano do 'Grande Evento' + o código do meu distintivo (123).",
            "log.txt": "Erro de sistema em 2032. Dados corrompidos.",
            "badge_info.txt": "Agente Smith. Distintivo #123."
        }
        self.password = "2032123"
        self.solved = False
        self.cursor_blink = 0
        self.prompt = "> "

    def handle_input(self, events):
        if self.solved:
            for ev in events:
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                     # Transition back or to next stage
                     self.state["current"] = "desktop"
            return

        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    self.process_command(self.input_text)
                    self.input_text = ""
                elif ev.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += ev.unicode

    def process_command(self, cmd_str):
        cmd_str = cmd_str.strip()
        self.history.append(self.prompt + cmd_str)
        
        parts = cmd_str.split()
        if not parts:
            return

        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            self.history.append("AVAILABLE COMMANDS:")
            self.history.append("  ls            - List files")
            self.history.append("  cat [file]    - Read file content")
            self.history.append("  login [pass]  - Attempt login")
            self.history.append("  exit          - Exit terminal")
        elif cmd == "ls":
            for f in self.files:
                self.history.append(f"  {f}")
        elif cmd == "cat":
            if not args:
                self.history.append("Usage: cat [filename]")
            elif args[0] in self.files:
                self.history.append(f"--- {args[0]} ---")
                self.history.append(self.files[args[0]])
                self.history.append("----------------")
            else:
                self.history.append(f"File not found: {args[0]}")
        elif cmd == "login":
            if not args:
                self.history.append("Usage: login [password]")
            elif args[0] == self.password:
                self.history.append("ACCESS GRANTED.")
                self.history.append("LOADING DESKTOP ENVIRONMENT...")
                self.solved = True
            else:
                self.history.append("ACCESS DENIED.")
        elif cmd == "exit":
            self.state["current"] = "menu"
        else:
            self.history.append(f"Unknown command: {cmd}")

        # Keep history manageable
        if len(self.history) > 20:
            self.history = self.history[-20:]

    def draw(self, screen):
        screen.fill(self.bg_color)
        
        line_height = 25
        start_y = 20
        
        # Draw history
        for i, line in enumerate(self.history):
            text_surf = self.font.render(line, True, self.text_color)
            screen.blit(text_surf, (20, start_y + i * line_height))

        # Draw current input line
        if not self.solved:
            self.cursor_blink += 1
            cursor = "_" if (self.cursor_blink // 30) % 2 == 0 else ""
            input_line = f"{self.prompt}{self.input_text}{cursor}"
            text_surf = self.font.render(input_line, True, self.text_color)
            screen.blit(text_surf, (20, start_y + len(self.history) * line_height))
        else:
            # Auto transition after a brief delay or wait for enter
            # For now, let's wait for enter as per previous logic, but change action
            msg = "PRESS ENTER TO ENTER DESKTOP..."
            text_surf = self.font.render(msg, True, self.text_color)
            screen.blit(text_surf, (20, start_y + len(self.history) * line_height + 20))

