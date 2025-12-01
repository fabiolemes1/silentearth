import pygame
import os
from ui.utils import wrap_text

class MinigameDesktop:
    def __init__(self, screen, font, assets_path):
        self.screen = screen
        self.font = font
        self.assets_path = assets_path
        
        self.W = screen.get_width()
        self.H = screen.get_height()
        
        # Colors
        self.BG_COLOR = (0, 100, 150) # Fallback teal
        self.ICON_COLOR = (255, 255, 255)
        self.WINDOW_BG = (200, 200, 200)
        self.TITLE_BAR_COLOR = (0, 0, 128)
        
        # Load Assets (with fallbacks)
        self.assets = {}
        self._load_asset("monitor_border", "monitor_border.png")
        self._load_asset("desktop_bg", "desktop_bg.png")
        self._load_asset("icon_folder", "icon_folder.png")
        self._load_asset("icon_file", "icon_file.png")
        self._load_asset("icon_trash", "icon_trash.png")
        
        # Icons setup
        self.icons = [
            {"name": "COORDENADAS_BUNKER.txt", "icon": "icon_file", "rect": pygame.Rect(50, 50, 64, 64)},
            {"name": "LEMBRETE_SENHA.txt", "icon": "icon_file", "rect": pygame.Rect(50, 180, 64, 64)},
            {"name": "LIXEIRA", "icon": "icon_trash", "rect": pygame.Rect(50, 310, 64, 64)}
        ]
        
        self.windows = [] # List of open windows
        
    def _load_asset(self, key, filename):
        path = os.path.join(self.assets_path, filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                if key == "monitor_border" or key == "desktop_bg":
                    img = pygame.transform.smoothscale(img, (self.W, self.H))
                elif key.startswith("icon_"):
                    img = pygame.transform.smoothscale(img, (64, 64))
                self.assets[key] = img
            except:
                self.assets[key] = None
        else:
            self.assets[key] = None

    def update(self):
        pass

    def draw(self):
        # 1. Desktop Background
        if self.assets["desktop_bg"]:
            self.screen.blit(self.assets["desktop_bg"], (0, 0))
        else:
            self.screen.fill(self.BG_COLOR)
        
        # 2. Icons
        for icon in self.icons:
            # Draw Icon Image or Placeholder
            icon_img = self.assets.get(icon["icon"])
            if icon_img:
                self.screen.blit(icon_img, icon["rect"])
            else:
                pygame.draw.rect(self.screen, self.ICON_COLOR, icon["rect"])
            
            # Draw Label (with background for readability)
            label = self.font.render(icon["name"], True, (255, 255, 255))
            label_bg = pygame.Surface((label.get_width() + 4, label.get_height() + 4))
            label_bg.fill((0, 0, 0))
            label_bg.set_alpha(100)
            
            lbl_x = icon["rect"].centerx - label.get_width()//2
            lbl_y = icon["rect"].bottom + 5
            
            self.screen.blit(label_bg, (lbl_x - 2, lbl_y - 2))
            self.screen.blit(label, (lbl_x, lbl_y))
            
        # 3. Taskbar
        pygame.draw.rect(self.screen, (192, 192, 192), (0, self.H - 40, self.W, 40))
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.H - 40), (self.W, self.H - 40))
        
        # Start Button
        pygame.draw.rect(self.screen, (150, 150, 150), (5, self.H - 35, 80, 30))
        start_txt = self.font.render("Iniciar", True, (0, 0, 0))
        self.screen.blit(start_txt, (15, self.H - 30))
        
        # 4. Windows
        for win in self.windows:
            self.draw_window(win)
            
        # 5. Monitor Border (Overlay)
        if self.assets["monitor_border"]:
            self.screen.blit(self.assets["monitor_border"], (0, 0))

    def draw_window(self, win):
        # Window Frame
        pygame.draw.rect(self.screen, self.WINDOW_BG, win["rect"])
        pygame.draw.rect(self.screen, (0, 0, 0), win["rect"], 2)
        
        # Title Bar
        title_bar = pygame.Rect(win["rect"].x, win["rect"].y, win["rect"].width, 30)
        pygame.draw.rect(self.screen, self.TITLE_BAR_COLOR, title_bar)
        
        title_txt = self.font.render(win["title"], True, (255, 255, 255))
        self.screen.blit(title_txt, (win["rect"].x + 10, win["rect"].y + 5))
        
        # Close Button
        close_btn = pygame.Rect(win["rect"].right - 25, win["rect"].y + 5, 20, 20)
        pygame.draw.rect(self.screen, (192, 192, 192), close_btn)
        pygame.draw.line(self.screen, (0,0,0), close_btn.topleft, close_btn.bottomright)
        pygame.draw.line(self.screen, (0,0,0), close_btn.bottomleft, close_btn.topright)
        
        # Content Area
        content_rect = pygame.Rect(win["rect"].x + 10, win["rect"].y + 40, win["rect"].width - 20, win["rect"].height - 50)
        pygame.draw.rect(self.screen, (255, 255, 255), content_rect)
        
        # Text Content (Wrapped)
        lines = wrap_text(win["content"], self.font, content_rect.width - 20)
        y_offset = content_rect.y + 10
        for line in lines:
            line_surf = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(line_surf, (content_rect.x + 10, y_offset))
            y_offset += line_surf.get_height() + 5

    def click(self):
        mx, my = pygame.mouse.get_pos()
        
        # Check windows (top to bottom)
        for i in range(len(self.windows) - 1, -1, -1):
            win = self.windows[i]
            
            # Close button
            close_btn = pygame.Rect(win["rect"].right - 25, win["rect"].y + 5, 20, 20)
            if close_btn.collidepoint((mx, my)):
                self.windows.pop(i)
                return
                
            # Title bar (bring to front)
            title_bar = pygame.Rect(win["rect"].x, win["rect"].y, win["rect"].width, 30)
            if title_bar.collidepoint((mx, my)):
                self.windows.append(self.windows.pop(i))
                return
                
            # Click inside window (consume click)
            if win["rect"].collidepoint((mx, my)):
                return

        # Check icons
        for icon in self.icons:
            if icon["rect"].collidepoint((mx, my)):
                self.open_window(icon["name"])
                
    def open_window(self, name):
        content = "Pasta vazia."
        title = name
        
        if name == "COORDENADAS_BUNKER.txt":
            content = "MENSAGEM CRIPTOGRAFADA:\n\nKHOO ZRUOG -> HELLO WORLD\n\nCOORDENADAS: 45.33, -12.55\n\n(Use a Cifra de César com deslocamento 3 para decifrar a mensagem real se necessário, mas as coordenadas já estão visíveis aqui para facilitar o teste.)"
        elif name == "LEMBRETE_SENHA.txt":
            content = "Lembrete: O General César adorava o número 3.\n\nIsso deve ser útil para decifrar os arquivos criptografados do sistema."
        elif name == "LIXEIRA":
            content = "A lixeira está vazia."
            
        # Center the window
        win_w = int(self.W * 0.8)
        win_h = int(self.H * 0.7)
        win_x = (self.W - win_w) // 2
        win_y = (self.H - win_h) // 2
        
        new_window = {
            "title": title,
            "rect": pygame.Rect(win_x, win_y, win_w, win_h),
            "content": content
        }
        self.windows.append(new_window)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "exit"
        return None
