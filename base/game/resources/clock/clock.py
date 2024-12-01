import pygame
import time


class Clock:
    def __init__(self, pantalla, duration=10, max_radius=200):
        """
        Inicializa el cronómetro circular.

        :param pantalla: Objeto pantalla donde se dibujará el cronómetro.
        :param duration: Duración del cronómetro en segundos.
        :param max_radius: Radio máximo del círculo del cronómetro.
        """
        self.pantalla = pantalla
        self.duration = duration
        self.max_radius = max_radius
        self.center = (pantalla.get_width() // 2, pantalla.get_height() // 2)
        self.start_time = time.time()
        self.finished = False

    def update(self):
        """
        Actualiza el estado del cronómetro.
        """
        if self.finished:
            return

        elapsed_time = time.time() - self.start_time
        remaining_time = max(self.duration - elapsed_time, 0)

        if remaining_time <= 0:
            self.finished = True

    def draw(self):
        """
        Dibuja el cronómetro circular en la pantalla.
        """
        if self.finished:
            return

        elapsed_time = time.time() - self.start_time
        remaining_time = max(self.duration - elapsed_time, 0)

        # Calcular el radio proporcional al tiempo restante
        radius = int((remaining_time / self.duration) * self.max_radius)

        # Dibujar el círculo proporcional
        pygame.draw.circle(self.pantalla, pygame.Color(
            'blue'), self.center, radius)

        # Mostrar tiempo restante
        font = pygame.font.SysFont('Verdana', 50)
        time_text = font.render(
            f'{int(remaining_time)}', True, pygame.Color('white'))
        text_rect = time_text.get_rect(center=self.center)
        self.pantalla.blit(time_text, text_rect)

    def reset(self, duration=None):
        """
        Reinicia el cronómetro.

        :param duration: Nueva duración del cronómetro. Si es None, usa la duración original.
        """
        self.duration = duration if duration is not None else self.duration
        self.start_time = time.time()
        self.finished = False

    def is_finished(self):
        """
        Verifica si el cronómetro ha terminado.

        :return: True si el cronómetro ha llegado a cero, False en caso contrario.
        """
        return self.finished
