class Widget:
    
    def __init__(self, x: int, y: int, texto: str, pantalla, font_size: int = 25):
        self.x = x
        self.y = y
        self.texto = texto
        self.pantalla = pantalla
        self.font_size = font_size
    
    def draw(self):
        self.pantalla.blit(self.image, (self.rect.x, self.rect.y))
