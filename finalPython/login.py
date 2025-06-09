import pygame
import sys
from auth import UserAuth

pygame.init()
pygame.font.init()

# Constants
WINDOW_SIZE = (400, 300)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)

# Initialize window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Iniciar Sesión - Dale dale daleeee")

# Font
font = pygame.font.Font("assets/font.otf", 20)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False

    def draw(self):
        color = BLUE if self.is_hovered else GRAY
        pygame.draw.rect(window, color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class InputBox:
    def __init__(self, x, y, width, height, text='', is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_password = is_password
        self.active = False
        self.color = BLACK

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect, 2)
        display_text = '*' * len(self.text) if self.is_password else self.text
        text_surface = font.render(display_text, True, self.color)
        window.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

def main():
    auth = UserAuth()
    
    # Create UI elements
    username_box = InputBox(100, 70, 200, 30)
    password_box = InputBox(100, 140, 200, 30, is_password=True)
    login_button = Button(100, 200, 90, 40, "Entrar")
    register_button = Button(210, 200, 90, 40, "Registrar")
    
    message = ""
    message_color = BLACK

    while True:
        window.fill(WHITE)
        
        # Draw labels
        username_label = font.render("Usuario:", True, BLACK)
        password_label = font.render("Contraseña:", True, BLACK)
        window.blit(username_label, (100, 45))
        window.blit(password_label, (100, 115))
        
        # Draw message if any
        if message:
            msg_surface = font.render(message, True, message_color)
            window.blit(msg_surface, (100, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            username_box.handle_event(event)
            password_box.handle_event(event)
            
            if login_button.handle_event(event):
                result = auth.login(username_box.text, password_box.text)
                if result["status"] == "success":
                    return username_box.text  # Return username on successful login
                message = result["message"]
                message_color = (255, 0, 0) if result["status"] == "error" else (0, 255, 0)
            
            if register_button.handle_event(event):
                result = auth.register(username_box.text, password_box.text)
                message = result["message"]
                message_color = (255, 0, 0) if result["status"] == "error" else (0, 255, 0)

        username_box.draw()
        password_box.draw()
        login_button.draw()
        register_button.draw()
        
        pygame.display.flip()

if __name__ == "__main__":
    main() 