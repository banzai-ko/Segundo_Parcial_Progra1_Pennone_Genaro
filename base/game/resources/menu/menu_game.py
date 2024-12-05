
import random
from typing import Callable

import pygame as pg
from tabulate import tabulate
from settings import SettingsLoader
from game.resources.timer import GameTimer
from game.resources.questions import Questions
from game.resources.menu import Menu
from game.resources.bar import AnimatedBar
from game.resources.player import Player
from game.resources.debugger import Debugger
from game.resources.widgets import (
    Button, AnswerButton, TextTitle, Banner, Logo, Wildcard
)

config = SettingsLoader()
debug = Debugger()

SCREEN = config.screen
questions_path = config.base_dir + config.get_key('QUESTIONS_FILE')
questions = Questions(questions_path)
questions.load_file()


class MenuGame(Menu):
    """
    _summary_ Clase Juego Principal

    Arguments:
        Menu -- El desarrolllo de la dinámica del juego se maneja en esta clase
    """

    def __init__(self, name, pantalla, x, y, active, level_num, music_path):
        super().__init__(name, pantalla, x, y, active, level_num, music_path)
        # Game state
        self.index = 0
        self.puntaje = 0
        self.start = False
        self.loop = True

        # Display setup
        self.surface = pg.image.load(
            config.base_dir + config.get_key('GAME_BACKGROUND')).convert_alpha()
        self.surface = pg.transform.scale(self.surface, SCREEN)
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.pantalla = pantalla

        # Lists and containers
        self.public_answers = []
        self.widgets_list = []
        self.public_banner = []
        self.wildcards_used_list = [0, 0, 0]

        # UI Elements
        self.button_back = Button(
            x=120,
            y=SCREEN[1]//2+300,
            texto='VOLVER AL MENU',
            pantalla=pantalla,
            on_click=self.click_back,
            on_click_param='form_main_menu'
        )
        self.generate_play_button('JUGAR')

        # Game elements
        self.public = 14
        self.game_question = None
        self.answer_a = None
        self.answer_b = None
        self.marcador_puntaje = None
        self.next_button = None

        # Timer setup
        self.first_time = pg.time.get_ticks()
        self.clock = pg.time.Clock()
        self.level_timer = 15
        self.segundos = 15
        self.jugador = Player.get_player()
        self.contador_texto = TextTitle(
            x=800, y=20, texto=f'Tiempo: {self.level_timer}', pantalla=self.pantalla, font_size=20
        )
        self.logo = Logo(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 100,
            pantalla=pantalla,
            texto='', font_size=0,
            key='PYTHON_LOGO')

        self. button_blue = Button(
            x=349,
            y=576,
            texto='',
            pantalla=pantalla,
            on_click=self.game_logic,
            on_click_param='blue')

        self.button_red = Button(
            x=845,
            y=576,
            texto='',
            pantalla=pantalla,
            on_click=self.game_logic,
            on_click_param='red'
        )

        self.show([self.button_back, self.contador_texto, self.logo])

        self.music_update()
        self.bar_graph = None

    def actualizar_timer(self) -> None:  # Mover clase Timer
        if self.level_timer > 0 and self.start:
            tiempo_actual = pg.time.get_ticks()
            if tiempo_actual - self.first_time >= 1000:
                self.level_timer -= 1
                self.first_time = tiempo_actual

    def set_marcador_puntaje(self, puntaje: int) -> None:
        self.hide([self.marcador_puntaje])
        self.marcador_puntaje = TextTitle(
            x=100,
            y=20,
            texto='Puntaje: ' + str(puntaje),
            pantalla=self.pantalla,
            font_size=30
        )
        self.show([self.marcador_puntaje])

    def generate_play_button(self, texto: str) -> None:
        """
        _summary_ Genera botón de Play

        Arguments:
            texto --  Texto del botón
        """
        self.play_button = Button(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 200,
            texto=texto,
            pantalla=self.pantalla,
            on_click=self.start_game,
            on_click_param='play')
        self.widgets_list.append(self.play_button)

    def start_game(self, show: str) -> None:
        """
        PLAY - Entry point

        Arguments:
            show -- Mensaje para informar en consola cuando comienza el juego
        """
        self.index = 0
        self.puntaje = 0
        self.set_marcador_puntaje(0)
        print(f'Estado Juego: {show}')
        self.generate_public_answers()
        self.start = True
        self.hide([self.play_button])
        self.next_question("START GAME")
        [self.next, self.half, self.change] = self.set_wildcards()
        self.remove_element(None, 'banner')
        self.bar_graph = self.create_animated_bar(
            self.public_answers)
        self.bar_graph.set_active(False)
        self.set_wildcards_used('NONE')
        self.hide([self.next_button])

    def game_logic(self, answer):
        """
        _summary_ Lógica central del juego

        Arguments:
            answer --  Respuesta del USUARIO.
        """
        valid = self.check_response(
            answer, self.get_public_answers_result()
        )
        self.show_public_answers(self.pantalla)

        if (not valid):
            self.game_over()

        else:
            if self.index < 11:
                self.set_next_button()
                self.increment_puntaje()
                valid = False
            else:
                self.win()

    def check_response(self, answer: str, public_answer: str) -> bool:
        """
        _summary_: Verfica respuesta correcta

        Arguments:
            answer --  Respuesta del usuario
            public_answer --  Respuesta correcta

        Returns:

        """
        if (not answer == public_answer):
            print(f'PERDISTE, RESPUESTA CORRECTA: {public_answer}')
            return False

        print('SUMA PUNTAJE, SIGUIENTE PREGUNTA >>>')
        return True

    def set_next_button(self) -> None:

        print('SIGUIENTE PREGUNTA >>>')
        self.next_button = AnswerButton(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 20,
            texto='CORRECTO!, Siguiente pregunta',
            pantalla=self.pantalla,
            on_click=self.next_question,
            on_click_param='Next Question >>>'
        )
        self.start = False
        self.level_timer = 15
        self.show([self.next_button])
        self.hide([self.game_question, self.answer_a,
                  self.answer_b])
        if self.bar_graph is not None:
            self.bar_graph.set_active(True)

    def next_question(self, show) -> None:
        """
        _summary_: Obtiene la siguiente pregunta y actualiza la vista
        """
        print(show)
        self.start = True
        self.hide([self.game_question, self.answer_a,
                  self.answer_b, self.next_button])
        self.index += 1
        self.generate_public_answers()

        question, answers = self.get_question_and_answers()
        debug.show(question, answers,
                   self.get_public_answers_result(), self.index, self.puntaje, self.public_answers)
        # Pregunta
        self.game_question = self.set_text(question, self.pantalla)

        # Respuesta Roja
        self.answer_a = self.set_answer(
            answers[0], 'left', self.game_logic, 'red', self.pantalla)

        # Respuesta Azul
        self.answer_b = self.set_answer(
            answers[1], 'right', self.game_logic, 'blue', self.pantalla)

        #  AnimatedBarGraph
        if self.bar_graph is not None:
            self.bar_graph.set_active(False)
        self.remove_element(None, 'banner')

    def create_animated_bar(self, data: list,) -> AnimatedBar:
        self.bg_image = pg.image.load(
            config.base_dir +
            config.get_key('BAR_GRAPH')).convert_alpha()
        bar_graph = AnimatedBar(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2,
            texto='',
            pantalla=self.pantalla,
            data=data,
            image=self.bg_image
        )

        return bar_graph

    def set_text(self, question: str, pantalla: pg.Surface) -> TextTitle:
        """
        _summary_ Crea el objeto pregunta

        Arguments:
            question --  Pregunta
            pantalla --  Objeto pantalla

        Returns:
             Objeto tñitulo
        """
        game_question = TextTitle(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 300,
            texto=question,
            pantalla=pantalla,
            font_size=55
        )
        self.show([game_question])
        return game_question

    def set_answer(
        self, answer: str,
        position: str,
        function: Callable[[str], None],
        param: str,
        pantalla: pg.Surface
    ) -> AnswerButton:
        """
        _summary_ Crea el objeto Respuesta Genérica

        Arguments:
            answer --  Respuesta, texto
            position --  Posición del botón en pantalla
            function --  Función a ejecutar
            param --  Parámetro de la función
            pantalla --  Objeto pantalla

        Returns:

        """
        if position == 'left':
            position = SCREEN[0]//2 - 300
        elif position == 'right':
            position = SCREEN[0]//2 + 300

        game_answer = AnswerButton(
            x=position,
            y=SCREEN[1]//2 + 200,
            texto=answer,
            pantalla=pantalla,
            on_click=function,
            on_click_param=param)
        self.show([game_answer])
        return game_answer

    def increment_puntaje(self) -> None:
        """
            Incrementa el puntaje y actualiza el marcador
            """
        self.hide([self.marcador_puntaje])
        self.puntaje += 10 * self.level_timer + 1
        # añada el multiplicador de tiempo

        print(f'Puntaje: {self.puntaje}')
        # self.widgets_list.remove(self.marcador_puntaje)
        self.marcador_puntaje = TextTitle(
            x=100,
            y=20,
            texto='Puntaje: ' + str(self.puntaje),
            pantalla=self.pantalla,
            font_size=30
        )
        self.widgets_list.append(self.marcador_puntaje)

    def remove_element(self, element=None, type_elem='default'):
        """
        _summary_ Remueve elementos de la vista

        Arguments:
            element --  (default: {None}) Elemento a remover, si se tiene acceso
            type_elem --  (default: {'default'}) Elemento a remover. Si no se tiene acceso.
                En este caso se remueven todos los elementos 'banner'
        """
        if element is not None and type_elem == 'default':
            self.widgets_list = [
                widget for widget in self.widgets_list if widget != element
            ]
        elif type_elem == 'banner':
            self.widgets_list = [
                widget for widget in self.widgets_list if widget not in self.public_banner
            ]

    def game_over(self) -> None:
        """
            _summary_ Final del juego
        """
        print('GAME OVER...')
        self.hide([self.game_question, self.answer_a,
                  self.answer_b, self.next_button])
        self.set_wildcards_used('ALL')
        if self.bar_graph:
            self.bar_graph.active = False

        self.title = TextTitle(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 350,
            texto='Game Over',
            pantalla=self.pantalla,
            font_size=90
        )
        self.play_again_button = Button(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 250,
            texto='Jugar de nuevo',
            pantalla=self.pantalla,
            on_click=self.play_again,
            on_click_param='play_again'
        )
        self.go_back_button = Button(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 200,
            texto='Volver al menu Principal',
            pantalla=self.pantalla,
            on_click=self.go_back,
            on_click_param='form_enter_name'
        )
        self.show(
            [self.title, self.play_again_button, self.go_back_button]
        )

    def win(self) -> None:
        """
            _summary_ Final del juego
        """
        print('WINNER WINNER CHICKEN DINNER')
        self.hide([self.game_question, self.answer_a,
                  self.answer_b, self.next_button])
        self.set_wildcards_used('ALL')
        if self.bar_graph:
            self.bar_graph.active = False

        self.title = TextTitle(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 350,
            texto='HAS GANADO!',
            pantalla=self.pantalla,
            font_size=90
        )
        self.play_again_button = Button(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 250,
            texto='Jugar de nuevo',
            pantalla=self.pantalla,
            on_click=self.play_again,
            on_click_param='play_again'
        )
        self.go_back_button = Button(
            x=SCREEN[0]//2,
            y=SCREEN[1]//2 - 200,
            texto='Volver al menu Principal',
            pantalla=self.pantalla,
            on_click=self.go_back,
            on_click_param='form_enter_name'
        )
        self.show(
            [self.title, self.play_again_button, self.go_back_button]
        )

    def show(self, lista: list) -> None:
        """
            _summary_ Agrega elementos a la vista

        Arguments:
            lista -- Lista de elementos para agregar a la vista
        """
        for element in lista:
            self.widgets_list.append(element)

    def hide(self, lista: list) -> None:
        """
            _summary_ Remueve elementos de la vista

        Arguments:
            lista --  Lista de elementos a remover de la vista
        """
        for element in lista:
            if element in self.widgets_list:
                self.remove_element(element)

    def play_again(self, param) -> None:
        """
            _summary_ Volver a jugar

        Arguments:
            param --  Texto informativo para terminal. No se muestra en vista
        """
        self.level_timer = 15
        self.hide([self.play_again_button,
                   self.go_back_button, self.title])
        self.remove_element(None, 'banner')
        self.start_game(param)

    def go_back(self, param):
        """
            Volver al menu.

        Arguments:
            param --  Menu al cual se vuelve
        """
        self.hide([self.play_again_button,
                   self.go_back_button, self.title])
        self.remove_element(None, 'banner')
        self.generate_play_button('JUGAR')
        if self.puntaje > 0:
            self.set_puntaje_jugador(self.puntaje)
            self.click_back(param)
        else:
            self.click_back("form_main_menu")

    def generate_public_answers(self) -> None:
        """
            _summary_ Simular la generación de Repuestas del público
        """
        red, blue = 0, 0
        if self.public_answers:
            self.public_answers.clear()
        for _ in range(self.public):
            value = random.choice([0, 1])
            self.public_answers.append(value)
            if value == 0:
                red += 1
            else:
                blue += 1
        if red == blue:
            # Forzar mayoría en N pares
            self.public_answers[0] = 1 - self.public_answers[0]

    def get_public_answers_result(self) -> str:
        """
        _summary_ Obtiene el resultado de las respuestas del público

        Returns:
             Devuelve el resultado de la mayoría: Rojo o Azul
        """
        red = 0
        blue = 0
        for i in range(self.public):
            if (self.public_answers[i] == 0):
                red += 1
            else:
                blue += 1
        if (red > blue):
            return 'red'
        return 'blue'

    def show_public_answers(self,  pantalla, scope_range=None) -> None:  # ANCHOR
        """
            _summary_ Muestra las respuestas del público

        Arguments:
            pantalla --  Objeto pantalla
        """
        if self.public_banner:
            self.remove_element(None, 'banner')
            self.public_banner.clear()
        i = 0
        position = 115
        for answer in self.public_answers:
            banner = self.generate_color_banner(
                answer, position, pantalla)
            self.public_banner.append(banner)
            self.widgets_list.append(self.public_banner[i])
            position += 55
            if scope_range != None and i >= 6:
                break
            if (i == 6):
                position = 737
            i += 1

        self.bar_graph.set_active(True)

    def generate_color_banner(self, answer, position, pantalla):  # Crear clase?
        """
            _summary_ Crea el objeto banner

            Arguments:
                answer -- Respuesta: 0 o 1 . paraa Rojo o Azul
                position --  Posición del marcador, horizontal, eje x
                pantalla --  Objeto pantalla

            Returns:
                 Devuelve el banner con los campos para agregar al a la lista de vista
        """
        color = (0, 0, 0)
        if (answer == 1):
            color = (0, 0, 255, 150)
        else:
            color = (255, 0, 0, 150)

        banner = Banner(
            position, 310, '', pantalla, 0, color, (20, 20))

        return banner

    def click_music_off(self, parametro):  # Mover a otra clase - Settings ?
        pg.mixer.music.pause()

    def get_question_and_answers(self) -> tuple:
        """
            _summary_ Obtiene la pregunta y sus respuestas. Depende clase Questions

            Returns:
                 Tupla con pregunta y lista derespuestas
        """
        question = questions.get_question(self.index)
        answers = questions.get_answers(self.index)
        return (question, answers)

    def click_back(self, parametro):
        self.index = 0
        self.puntaje = 0
        self.set_active(parametro)

    def draw(self):
        super().draw()
        if self.bar_graph is not None:
            self.bar_graph.draw()
        for widget in self.widgets_list:
            widget.draw()

    def update(self):
        super().draw()
        self.hide([self.contador_texto])
        self.actualizar_timer()
        self.contador_texto = TextTitle(
            x=800,
            y=20,
            texto=f'Tiempo: {self.level_timer}',
            pantalla=self.pantalla,
            font_size=20
        )
        self.show([self.contador_texto])
        self.clock.tick(30)
        if self.bar_graph:
            self.bar_graph.update()
        for widget in self.widgets_list:
            widget.update()

    def get_wildcards_used(self, key: str) -> bool:
        """
        _summary_ Obtener lista de comodines usados

        Arguments:
            key --  Clave nombre del comodín

        Returns:
             Booleano
        """
        match key:
            case 'NEXT':
                if self.wildcards_used_list[0] == 1:
                    return True
            case 'HALF':
                if self.wildcards_used_list[1] == 1:
                    return True
            case 'CHANGE':
                if self.wildcards_used_list[2] == 1:
                    return True
            case _:
                return False

    def set_wildcards_used(self, key: str) -> None:
        """
        _summary_ Establecer comodin usado o todos

        Arguments:
            key --  Nombre de la clave a settear o todos(ALL).
        """
        match key:
            case 'NEXT':
                self.wildcards_used_list[0] = 1
                self.next.set_disabled(True)
            case 'HALF':
                self.wildcards_used_list[1] = 1
                self.half.set_disabled(True)
            case 'CHANGE':
                self.wildcards_used_list[2] = 1
                self.change.set_disabled(True)
            case 'ALL':
                self.wildcards_used_list[0] = 1
                self.wildcards_used_list[1] = 1
                self.wildcards_used_list[2] = 1
                self.next.set_disabled(True)
                self.half.set_disabled(True)
                self.change.set_disabled(True)
            case 'NONE':
                self.wildcards_used_list[0] = 0
                self.wildcards_used_list[1] = 0
                self.wildcards_used_list[2] = 0
                self.next.set_disabled(False)
                self.half.set_disabled(False)
                self.change.set_disabled(False)

            case _:
                print(f'Error:No match for key:{key}')

    def handle_wildcard(self, key: str) -> None:
        """
        _summary_ Manejador de comodines

        Arguments:
            key --  Nombre de la clave a ejecutar.
        """
        match key:
            case 'NEXT':
                if not self.get_wildcards_used('NEXT'):
                    answer = self.get_public_answers_result()
                    self.game_logic(answer)
                    self.set_wildcards_used('NEXT')
            case 'HALF':
                if not self.get_wildcards_used('HALF'):
                    self.show_public_answers(self.pantalla, scope_range='half')
                    self.show(
                        [self.game_question, self.answer_a, self.answer_b])
                    self.hide([self.next_button])
                    self.set_wildcards_used('HALF')
                    self.bar_graph.set_active(False)
            case 'CHANGE':
                if not self.get_wildcards_used('CHANGE'):
                    self.next_question("WILDCARD")
                    self.set_wildcards_used('CHANGE')
            case _:
                print(f'Error:No match for key:{key}')

    def set_wildcards(self) -> list[Wildcard]:
        """
            _summary_: Genera botones de Comodines
        """
        next_wildcard = Wildcard(
            x=SCREEN[0]//2 + 450,
            y=SCREEN[1]//2,
            texto='', key='NEXT_IMG',
            on_click=self.handle_wildcard,
            pantalla=self.pantalla,
            on_click_param='NEXT'
        )

        half_wildcard = Wildcard(
            x=SCREEN[0]//2 + 490,
            y=SCREEN[1]//2,
            texto='',
            key='HALF_IMG',
            on_click=self.handle_wildcard,
            pantalla=self.pantalla,
            on_click_param='HALF'
        )

        change_wildcard = Wildcard(
            x=SCREEN[0]//2 + 530,
            y=SCREEN[1]//2,
            texto='',
            key='CHANGE_IMG',
            on_click=self.handle_wildcard,
            pantalla=self.pantalla,
            on_click_param='CHANGE'
        )
        self.show([next_wildcard, half_wildcard, change_wildcard])

        return [next_wildcard, half_wildcard, change_wildcard]

    def set_puntaje_jugador(self, puntaje: int):
        """
        _summary_ Establece el puntaje del jugador

        Arguments:
            puntaje -- Recibe el puntaje del jugador como entero y lo establece en la instancia
        """
        self.jugador.set_puntaje(puntaje)
