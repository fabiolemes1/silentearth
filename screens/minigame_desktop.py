import pygame
import os
from ui.utils import wrap_text
from ui.dialogue_manager import DialogueManager

class MinigameDesktop:
    def __init__(self, screen, font, assets_path, dialogue_path):
        self.screen = screen
        self.font = font
        self.assets_path = assets_path
        self.dialogue_path = dialogue_path
        
        self.dialogue_manager = DialogueManager(screen, font, assets_path, dialogue_path)
        self.showing_dialogue = False
        self.dialogue_shown = False   # para o primeiro diálogo do arquivo criptografado
        
        self.W = screen.get_width()
        self.H = screen.get_height()
        
        # Colors
        self.BG_COLOR = (0, 100, 150)  # Fallback teal
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
            {"name": "LEMBRETE.txt", "icon": "icon_file", "rect": pygame.Rect(50, 180, 64, 64)},
            {"name": "LIXEIRA", "icon": "icon_trash", "rect": pygame.Rect(50, 310, 64, 64)}
        ]
        
        self.windows = []  # janelas abertas
        self.current_shift = 0  # deslocamento do cifra de César
        self.encrypted_text = "DWHQÇDR: R EXQNHU HVWD QRV FRRUGHQDGDV 78.66, -45.88"
        
    def _load_asset(self, key, filename):
        path = os.path.join(self.assets_path, filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                if key in ("monitor_border", "desktop_bg"):
                    img = pygame.transform.smoothscale(img, (self.W, self.H))
                elif key.startswith("icon_"):
                    img = pygame.transform.smoothscale(img, (64, 64))
                self.assets[key] = img
            except:
                self.assets[key] = None
        else:
            self.assets[key] = None

    def update(self):
        if self.showing_dialogue:
            self.dialogue_manager.update()

    def draw(self):
        # 1. Desktop Background
        if self.assets["desktop_bg"]:
            self.screen.blit(self.assets["desktop_bg"], (0, 0))
        else:
            self.screen.fill(self.BG_COLOR)
        
        # 2. Ícones
        for icon in self.icons:
            icon_img = self.assets.get(icon["icon"])
            if icon_img:
                self.screen.blit(icon_img, icon["rect"])
            else:
                pygame.draw.rect(self.screen, self.ICON_COLOR, icon["rect"])
            
            label = self.font.render(icon["name"], True, (255, 255, 255))
            label_bg = pygame.Surface((label.get_width() + 4, label.get_height() + 4))
            label_bg.fill((0, 0, 0))
            label_bg.set_alpha(100)
            
            lbl_x = icon["rect"].centerx - label.get_width() // 2
            lbl_y = icon["rect"].bottom + 5
            
            self.screen.blit(label_bg, (lbl_x - 2, lbl_y - 2))
            self.screen.blit(label, (lbl_x, lbl_y))
            
        # 3. Barra de tarefas
        pygame.draw.rect(self.screen, (192, 192, 192), (0, self.H - 40, self.W, 40))
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.H - 40), (self.W, self.H - 40))
        
        pygame.draw.rect(self.screen, (150, 150, 150), (5, self.H - 35, 80, 30))
        start_txt = self.font.render("Iniciar", True, (0, 0, 0))
        self.screen.blit(start_txt, (15, self.H - 30))
        
        # 4. Janelas
        for win in self.windows:
            self.draw_window(win)
            
        # 5. Moldura do monitor
        if self.assets["monitor_border"]:
            self.screen.blit(self.assets["monitor_border"], (0, 0))

        # 6. Diálogo sobreposto (somente textbox, sem mexer no fundo)
        if self.showing_dialogue:
            self.dialogue_manager.draw_textbox()

    def draw_window(self, win):
        # Janela normal ou decoder
        if win.get("type") == "DECODER":
            self.draw_decoder_window(win)
            return

        pygame.draw.rect(self.screen, self.WINDOW_BG, win["rect"])
        pygame.draw.rect(self.screen, (0, 0, 0), win["rect"], 2)
        
        # Barra de título
        title_bar = pygame.Rect(win["rect"].x, win["rect"].y, win["rect"].width, 30)
        pygame.draw.rect(self.screen, self.TITLE_BAR_COLOR, title_bar)
        
        title_txt = self.font.render(win["title"], True, (255, 255, 255))
        self.screen.blit(title_txt, (win["rect"].x + 10, win["rect"].y + 5))
        
        # Botão fechar
        close_btn = pygame.Rect(win["rect"].right - 25, win["rect"].y + 5, 20, 20)
        pygame.draw.rect(self.screen, (192, 192, 192), close_btn)
        pygame.draw.line(self.screen, (0,0,0), close_btn.topleft, close_btn.bottomright)
        pygame.draw.line(self.screen, (0,0,0), close_btn.bottomleft, close_btn.topright)
        
        # Conteúdo
        content_rect = pygame.Rect(
            win["rect"].x + 10,
            win["rect"].y + 40,
            win["rect"].width - 20,
            win["rect"].height - 50
        )
        pygame.draw.rect(self.screen, (255, 255, 255), content_rect)
        
        lines = wrap_text(win["content"], self.font, content_rect.width - 20)
        y_offset = content_rect.y + 10
        for line in lines:
            line_surf = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(line_surf, (content_rect.x + 10, y_offset))
            y_offset += line_surf.get_height() + 5

    def draw_decoder_window(self, win):
        # Barra de título
        title_bar = pygame.Rect(win["rect"].x, win["rect"].y, win["rect"].width, 30)
        pygame.draw.rect(self.screen, self.TITLE_BAR_COLOR, title_bar)
        
        title_txt = self.font.render("DECODIFICADOR DE TEXTO", True, (255, 255, 255))
        self.screen.blit(title_txt, (win["rect"].x + 10, win["rect"].y + 5))
        
        # Botão fechar
        close_btn = pygame.Rect(win["rect"].right - 25, win["rect"].y + 5, 20, 20)
        pygame.draw.rect(self.screen, (192, 192, 192), close_btn)
        pygame.draw.line(self.screen, (0,0,0), close_btn.topleft, close_btn.bottomright)
        pygame.draw.line(self.screen, (0,0,0), close_btn.bottomleft, close_btn.topright)
        
        # Área de conteúdo
        content_rect = pygame.Rect(
            win["rect"].x + 10,
            win["rect"].y + 40,
            win["rect"].width - 20,
            win["rect"].height - 50
        )
        pygame.draw.rect(self.screen, (240, 240, 240), content_rect)
        
        # Texto cifrado
        enc_label = self.font.render("TEXTO CIFRADO:", True, (100, 100, 100))
        self.screen.blit(enc_label, (content_rect.x + 10, content_rect.y + 10))
        
        enc_lines = wrap_text(self.encrypted_text, self.font, content_rect.width - 20)
        y = content_rect.y + 35
        for line in enc_lines:
            surf = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(surf, (content_rect.x + 10, y))
            y += surf.get_height() + 2
            
        # Separador
        y += 20
        pygame.draw.line(self.screen, (150, 150, 150),
                         (content_rect.x + 10, y),
                         (content_rect.right - 10, y))
        y += 20
        
        # Controles de deslocamento
        ctrl_y = y
        shift_label = self.font.render(f"DESLOCAMENTO: {self.current_shift}", True, (0, 0, 0))
        self.screen.blit(shift_label, (content_rect.centerx - shift_label.get_width()//2, ctrl_y))
        
        btn_w = 40
        btn_h = 40
        self.btn_minus = pygame.Rect(content_rect.centerx - 80, ctrl_y + 30, btn_w, btn_h)
        self.btn_plus  = pygame.Rect(content_rect.centerx + 40, ctrl_y + 30, btn_w, btn_h)
        
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_minus)
        pygame.draw.rect(self.screen, (0, 0, 0), self.btn_minus, 2)
        minus_txt = self.font.render("-", True, (0, 0, 0))
        self.screen.blit(minus_txt, (self.btn_minus.centerx - minus_txt.get_width()//2,
                                     self.btn_minus.centery - minus_txt.get_height()//2))
        
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_plus)
        pygame.draw.rect(self.screen, (0, 0, 0), self.btn_plus, 2)
        plus_txt = self.font.render("+", True, (0, 0, 0))
        self.screen.blit(plus_txt, (self.btn_plus.centerx - plus_txt.get_width()//2,
                                    self.btn_plus.centery - plus_txt.get_height()//2))
        
        y = ctrl_y + 90
        
        # Visualização decodificada
        dec_label = self.font.render("VISUALIZAÇÃO:", True, (100, 100, 100))
        self.screen.blit(dec_label, (content_rect.x + 10, y))
        
        decoded = self.caesar_cipher(self.encrypted_text, -self.current_shift)
        dec_lines = wrap_text(decoded, self.font, content_rect.width - 20)
        y += 25
        for line in dec_lines:
            color = (0, 100, 0) if self.current_shift == 3 else (100, 0, 0)
            surf = self.font.render(line, True, color)
            self.screen.blit(surf, (content_rect.x + 10, y))
            y += surf.get_height() + 2
            
        # Botão confirmar
        y += 20
        self.btn_confirm = pygame.Rect(content_rect.centerx - 60, content_rect.bottom - 50, 120, 40)
        pygame.draw.rect(self.screen, (0, 120, 0), self.btn_confirm)
        pygame.draw.rect(self.screen, (0, 0, 0), self.btn_confirm, 2)
        conf_txt = self.font.render("CONFIRMAR", True, (255, 255, 255))
        self.screen.blit(conf_txt, (self.btn_confirm.centerx - conf_txt.get_width()//2,
                                    self.btn_confirm.centery - conf_txt.get_height()//2))

    def caesar_cipher(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                offset = 65 if char.isupper() else 97
                result += chr((ord(char) - offset + shift) % 26 + offset)
            elif char.isdigit():
                result += str((int(char) + shift) % 10)
            else:
                result += char
        return result

    def click(self):
        # Se está mostrando diálogo (encrypted_message ou decoding_success)
        if self.showing_dialogue:
            action = self.dialogue_manager.click()
            if action == "END" or action == "success":
                self.showing_dialogue = False
                if action == "success":
                    # sinalizar para o main.py que pode ir para o bunker
                    return "success"
            return

        mx, my = pygame.mouse.get_pos()
        
        # Checar janelas (de cima pra baixo)
        for i in range(len(self.windows) - 1, -1, -1):
            win = self.windows[i]
            
            close_btn = pygame.Rect(win["rect"].right - 25, win["rect"].y + 5, 20, 20)
            if close_btn.collidepoint((mx, my)):
                self.windows.pop(i)
                return
                
            title_bar = pygame.Rect(win["rect"].x, win["rect"].y, win["rect"].width, 30)
            if title_bar.collidepoint((mx, my)):
                # trazer janela pra frente
                self.windows.append(self.windows.pop(i))
                return
                
            if win["rect"].collidepoint((mx, my)) and win.get("type") == "DECODER":
                # Botões do decoder
                if hasattr(self, "btn_minus") and self.btn_minus.collidepoint((mx, my)):
                    self.current_shift = (self.current_shift - 1) % 26
                elif hasattr(self, "btn_plus") and self.btn_plus.collidepoint((mx, my)):
                    self.current_shift = (self.current_shift + 1) % 26
                elif hasattr(self, "btn_confirm") and self.btn_confirm.collidepoint((mx, my)):
                    if self.current_shift == 3:
                        # Carrega o diálogo de sucesso (decoding_success.json)
                        self.dialogue_manager.load_dialogue("decoding_success.json")
                        self.showing_dialogue = True
                return

        # Ícones na área de trabalho
        for icon in self.icons:
            if icon["rect"].collidepoint((mx, my)):
                self.open_window(icon["name"])
                
    def open_window(self, name):
        content = "Pasta vazia."
        title = name
        
        if name == "COORDENADAS_BUNKER.txt":
            content = ""  # tratado pela janela DECODER
            title = "DECODIFICADOR"
            if not self.dialogue_shown:
                self.dialogue_manager.load_dialogue("encrypted_message.json")
                self.showing_dialogue = True
                self.dialogue_shown = True
        elif name == "LEMBRETE.txt":
            content = "Lembrete: O General César adorava o número 3.\n\nIsso deve ser útil para decifrar os arquivos criptografados do sistema."
        elif name == "LIXEIRA":
            content = "A lixeira está vazia."
            
        win_w = int(self.W * 0.8)
        win_h = int(self.H * 0.8)
        win_x = (self.W - win_w) // 2
        win_y = (self.H - win_h) // 2
        
        new_window = {
            "title": title,
            "rect": pygame.Rect(win_x, win_y, win_w, win_h),
            "content": content,
            "type": "DECODER" if name == "COORDENADAS_BUNKER.txt" else "NORMAL"
        }
        self.windows.append(new_window)

    def handle_event(self, event):
        if self.showing_dialogue:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "exit"
        return None
