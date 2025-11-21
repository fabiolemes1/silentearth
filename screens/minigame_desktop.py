import pygame
import os

class MinigameDesktop:
    def __init__(self, state):
        self.state = state
        self.font = pygame.font.SysFont("arial", 14)
        self.title_font = pygame.font.SysFont("arial", 16, bold=True)
        self.path_font = pygame.font.SysFont("arial", 18)
        self.bg_color = (240, 240, 240) # Light grey background for explorer
        
        # Game State
        self.found_encrypted = False
        self.dialog = None # Current dialog (dict or None)
        self.file_overlay = None # Current open file (dict or None)

        # File System
        self.fs = {
            "Documents": {
                "type": "folder",
                "content": {
                    "Personal.txt": {"type": "file", "content": "My favorite month is March."},
                    "History.png": {"type": "image", "path": "julius_caesar.png"}
                }
            },
            "Secret": {
                "type": "folder",
                "content": {
                    "Bunker_Coords.txt": {"type": "file", "content": "Khoor! DV FRRUGV VDR: 45.12, -93.21"} # Hello! AS COORDS SAO: ... (Shift +3)
                }
            }
        }
        
        # Navigation State
        self.path_stack = [] # List of (name, content_dict) tuples. Empty means root.
        self.current_content = self.fs # Start at root

        # Assets
        self.assets_path = os.path.join(os.getcwd(), "assets")

    def get_current_path_string(self):
        if not self.path_stack:
            return "Computer"
        return "Computer > " + " > ".join([p[0] for p in self.path_stack])

    def navigate_to(self, name, content):
        self.path_stack.append((name, content))
        self.current_content = content["content"]

    def navigate_up(self):
        if self.path_stack:
            self.path_stack.pop()
            if self.path_stack:
                self.current_content = self.path_stack[-1][1]["content"]
            else:
                self.current_content = self.fs

    def open_file(self, name, file_data):
        # Check for triggers
        if name == "Bunker_Coords.txt":
            self.found_encrypted = True
        
        if name == "History.png":
            if self.found_encrypted:
                self.show_dialog("Hint", "This man looks familiar... maybe a leader?")
        
        if name == "Personal.txt":
            if self.found_encrypted:
                self.show_dialog("Hint", "March... the third month?")

        # Open Overlay
        self.file_overlay = {
            "title": name,
            "type": file_data["type"],
            "content": file_data.get("content", ""),
            "path": file_data.get("path", ""),
            "rect": pygame.Rect(100, 50, 600, 400) # Centered large window
        }

    def show_dialog(self, title, msg):
        self.dialog = {
            "title": title,
            "msg": msg,
            "rect": pygame.Rect(250, 250, 300, 150)
        }

    def handle_input(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    # Close overlay/dialog if open, else disconnect
                    if self.dialog:
                        self.dialog = None
                    elif self.file_overlay:
                        self.file_overlay = None
                    else:
                        self.state["current"] = "alien_input"

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    # 1. Handle Dialog
                    if self.dialog:
                        close_rect = pygame.Rect(self.dialog["rect"].right - 25, self.dialog["rect"].top + 5, 20, 20)
                        if close_rect.collidepoint(mouse_pos):
                            self.dialog = None
                        return # Modal blocks

                    # 2. Handle File Overlay
                    if self.file_overlay:
                        # Close button
                        close_rect = pygame.Rect(self.file_overlay["rect"].right - 25, self.file_overlay["rect"].top + 5, 20, 20)
                        if close_rect.collidepoint(mouse_pos):
                            self.file_overlay = None
                        return # Modal blocks

                    # 3. Handle Top Bar (Back Button)
                    if self.path_stack:
                        back_rect = pygame.Rect(10, 10, 40, 30)
                        if back_rect.collidepoint(mouse_pos):
                            self.navigate_up()
                            return

                    # 4. Handle Icons in Grid
                    idx = 0
                    start_x, start_y = 50, 80
                    for name, data in self.current_content.items():
                        ix, iy = (idx % 6) * 100 + start_x, (idx // 6) * 100 + start_y
                        icon_rect = pygame.Rect(ix, iy, 80, 80)
                        
                        if icon_rect.collidepoint(mouse_pos):
                            if data["type"] == "folder":
                                self.navigate_to(name, data)
                            else:
                                self.open_file(name, data)
                        idx += 1

    def draw(self, screen):
        screen.fill(self.bg_color)
        w, h = screen.get_width(), screen.get_height()

        # --- Top Bar ---
        pygame.draw.rect(screen, (220, 220, 220), (0, 0, w, 50))
        pygame.draw.line(screen, (180, 180, 180), (0, 50), (w, 50))

        # Back Button
        if self.path_stack:
            back_rect = pygame.Rect(10, 10, 40, 30)
            pygame.draw.rect(screen, (200, 200, 200), back_rect, border_radius=5)
            pygame.draw.polygon(screen, (50, 50, 50), [(35, 15), (15, 25), (35, 35)]) # Arrow

        # Path Text
        path_str = self.get_current_path_string()
        path_surf = self.path_font.render(path_str, True, (50, 50, 50))
        screen.blit(path_surf, (60, 15))

        # --- Main Content Area (Grid) ---
        idx = 0
        start_x, start_y = 50, 80
        for name, data in self.current_content.items():
            ix, iy = (idx % 6) * 100 + start_x, (idx // 6) * 100 + start_y
            icon_rect = pygame.Rect(ix, iy, 80, 80)
            
            # Hover effect
            if icon_rect.collidepoint(pygame.mouse.get_pos()) and not self.dialog and not self.file_overlay:
                pygame.draw.rect(screen, (200, 220, 255), icon_rect, border_radius=5)

            # Icon Graphic
            color = (255, 200, 100) if data["type"] == "folder" else (200, 200, 255)
            pygame.draw.rect(screen, color, icon_rect.inflate(-30, -40).move(0, -10))
            
            # Label
            lbl = self.font.render(name, True, (0, 0, 0))
            if lbl.get_width() > 78:
                 lbl = self.font.render(name[:8]+"..", True, (0,0,0))
            screen.blit(lbl, (icon_rect.centerx - lbl.get_width()//2, icon_rect.bottom - 20))
            
            idx += 1

        # --- File Overlay ---
        if self.file_overlay:
            # Dim background
            s = pygame.Surface((w, h))
            s.set_alpha(100)
            s.fill((0,0,0))
            screen.blit(s, (0,0))
            
            rect = self.file_overlay["rect"]
            # Window Body
            pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=5)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2, border_radius=5)
            
            # Title Bar
            title_bar = pygame.Rect(rect.left, rect.top, rect.width, 30)
            pygame.draw.rect(screen, (230, 230, 230), title_bar, border_top_left_radius=5, border_top_right_radius=5)
            pygame.draw.line(screen, (200, 200, 200), (rect.left, rect.top+30), (rect.right, rect.top+30))
            
            t = self.title_font.render(self.file_overlay["title"], True, (50, 50, 50))
            screen.blit(t, (title_bar.x + 10, title_bar.y + 5))
            
            # Close Button
            close_rect = pygame.Rect(rect.right - 30, rect.top + 5, 20, 20)
            pygame.draw.rect(screen, (200, 50, 50), close_rect, border_radius=3)
            t = self.font.render("X", True, (255,255,255))
            screen.blit(t, (close_rect.x + 5, close_rect.y + 2))
            
            # Content
            content_rect = rect.inflate(-20, -50).move(0, 20)
            
            if self.file_overlay["type"] == "image":
                try:
                    img_path = os.path.join(self.assets_path, self.file_overlay["path"])
                    if os.path.exists(img_path):
                        img = pygame.image.load(img_path)
                        scale = min(content_rect.width / img.get_width(), content_rect.height / img.get_height())
                        new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
                        img = pygame.transform.smoothscale(img, new_size)
                        screen.blit(img, (content_rect.centerx - img.get_width()//2, content_rect.centery - img.get_height()//2))
                    else:
                        t = self.font.render("[Image Not Found]", True, (255, 0, 0))
                        screen.blit(t, (content_rect.x, content_rect.y))
                except:
                    t = self.font.render("[Error Loading Image]", True, (255, 0, 0))
                    screen.blit(t, (content_rect.x, content_rect.y))
            else:
                lines = self.file_overlay["content"].split('\n')
                for i, line in enumerate(lines):
                    t = self.font.render(line, True, (0, 0, 0))
                    screen.blit(t, (content_rect.x, content_rect.y + i*20))

        # --- Dialog ---
        if self.dialog:
            # Dim background (darker)
            s = pygame.Surface((w, h))
            s.set_alpha(150)
            s.fill((0,0,0))
            screen.blit(s, (0,0))
            
            rect = self.dialog["rect"]
            pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=10)
            
            t = self.title_font.render(self.dialog["title"], True, (0,0,0))
            screen.blit(t, (rect.x + 10, rect.y + 10))
            
            words = self.dialog["msg"].split(' ')
            lines = []
            curr_line = ""
            for w in words:
                if self.font.size(curr_line + w)[0] < 280:
                    curr_line += w + " "
                else:
                    lines.append(curr_line)
                    curr_line = w + " "
            lines.append(curr_line)
            
            for i, line in enumerate(lines):
                t = self.font.render(line, True, (50, 50, 50))
                screen.blit(t, (rect.x + 10, rect.y + 40 + i*20))
            
            close_rect = pygame.Rect(rect.right - 25, rect.top + 5, 20, 20)
            pygame.draw.rect(screen, (200, 50, 50), close_rect, border_radius=3)
            t = self.font.render("X", True, (255,255,255))
            screen.blit(t, (close_rect.x + 5, close_rect.y + 2))
