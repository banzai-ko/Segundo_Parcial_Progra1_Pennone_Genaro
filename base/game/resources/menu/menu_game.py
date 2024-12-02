
import random
import pygame as pg
from tabulate import tabulate
from settings import SettingsLoader
from game.resources.timer import GameTimer
from game.resources.questions import Questions
from game.resources.menu import Menu
from game.resources.bar import AnimatedBar
from game.resources.widgets import (
    Button, AnswerButton, TextTitle, Banner, Logo, Wildcard
)

config = SettingsLoader()

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
        self.index, self.puntaje = 0, 0
        self.surface = pg.image.load(config.base_dir +
                                     config.get_key('GAME_BACKGROUND')).convert_alpha()
        self.surface = pg.transform.scale(self.surface, SCREEN)
        self.public_answers, self.widgets_list, self.public_banner = [], [], []
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.question, self.answers = self.get_question_and_answers()
        self.button_back = Button(x=120, y=SCREEN[1]//2+300, texto='VOLVER AL MENU',
                                  pantalla=pantalla, on_click=self.click_back, on_click_param='form_main_menu')
        self.pantalla = pantalla
        self.public = 14
        self.loop = True
        self.start = False
        self.segundos = 15
        self.simple_timer, self.play_button, self.play_again_button, self.go_back_button, self.title = None, None, None, None, None
        self.question, self.answer_a, self.answer_b = None, None, None
        self.marcador_puntaje, self.next, self.change, self.change = None, None, None, None
        self.wildcards_used_list = [0, 0, 0]
        self.bar_graph = None
        self.generate_play('JUGAR')

        self.contador_texto = TextTitle(
            x=800, y=20, texto='Tiempo: 10', pantalla=self.pantalla, font_size=20
        )
        self.logo = Logo(
            x=SCREEN[0]//2, y=SCREEN[1]//2 - 100,
            pantalla=pantalla, texto='', font_size=0, key='PYTHON_LOGO')

        self. button_blue = Button(
            x=349, y=576, texto='', pantalla=pantalla,
            on_click=self.game_logic, on_click_param='blue')

        self.button_red = Button(
            x=845, y=576, texto='', pantalla=pantalla,
            on_click=self.game_logic, on_click_param='red'
        )

        self.show([self.button_back, self.contador_texto, self.logo])

        self.music_update()
        # Testing the class in a Pygame application

    def set_marcador_puntaje(self, puntaje):
        self.hide([self.marcador_puntaje])
        self.marcador_puntaje = TextTitle(
            x=100, y=20, texto='Puntaje: ' + str(self.puntaje),
            pantalla=self.pantalla, font_size=30
        )
        self.show([self.marcador_puntaje])

    def get_wildcards_used(self, key):
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

    def set_wildcards_used(self, key):
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
            case _:
                print(f'Error:No match for key:{key}')

    def handle_wildcard(self, key):
        match key:
            case 'NEXT':
                if not self.get_wildcards_used('NEXT'):
                    answer = self.get_public_answers_result()
                    self.game_logic(answer)
                    self.set_wildcards_used('NEXT')
            case 'HALF':
                if not self.get_wildcards_used('HALF'):
                    self.show_public_answers(self.pantalla, scope_range='half')
                    self.set_wildcards_used('HALF')
            case 'CHANGE':
                if not self.get_wildcards_used('CHANGE'):
                    self.next_question()
                    self.set_wildcards_used('CHANGE')
            case _:
                print(f'Error:No match for key:{key}')

    def half_wildcard(self, show):
        print(f'Call half wildcard {show}')

    def reload_wildcard(self, show):
        print(f'Call Reload wildcard {show}')

    def set_wildcards(self):
        """
            _summary_: Genera botones de Comodines
        """
        self.next = Wildcard(
            x=SCREEN[0]//2 + 450,  y=SCREEN[1]//2,
            texto='', key='NEXT_IMG', on_click=self.handle_wildcard,
            pantalla=self.pantalla, on_click_param='NEXT')

        self.half = Wildcard(
            x=SCREEN[0]//2 + 490, y=SCREEN[1]//2,
            texto='', key='HALF_IMG', on_click=self.handle_wildcard,
            pantalla=self.pantalla, on_click_param='HALF')

        self.change = Wildcard(
            x=SCREEN[0]//2 + 530, y=SCREEN[1]//2,
            texto='', key='CHANGE_IMG', on_click=self.handle_wildcard,
            pantalla=self.pantalla, on_click_param='CHANGE'
        )
        self.show([self.next, self.half, self.change])

    def generate_play(self, texto: str):
        """
        _summary_ Genera botón de Play

        Arguments:
            texto -- _description_ Texto del botón
        """
        self.play_button = Button(
            x=SCREEN[0]//2, y=SCREEN[1]//2 - 200,
            texto=texto, pantalla=self.pantalla, on_click=self.start_game,
            on_click_param='play')
        self.widgets_list.append(self.play_button)

    def start_game(self, show):
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
        self.next_question()
        self.set_wildcards()
        self.remove_element(None, 'banner')

    def game_logic(self, answer):
        """
        _summary_ Lógica central del juego

        Arguments:
            answer -- _description_ Respuesta del USUARIO.
        """
        valid = self.check_response(
            answer, self.get_public_answers_result()
        )
        self.show_public_answers(self.pantalla)

        if (not valid):
            self.game_over()

        else:
            self.increment_puntaje()
            valid = False
            self.next_question()

    def check_response(self, answer: str, public_answer: str) -> bool:
        """
        _summary_: Verfica respuesta correcta

        Arguments:
            answer -- _description_ Respuesta del usuario
            public_answer -- _description_ Respuesta correcta

        Returns:
            _description_
        """
        print(f'Public Answer: {public_answer}')
        print(f'User Answer: {answer}')
        if (not answer == public_answer):
            print(f'PERDISTE, RESPUESTA CORRECTA: {public_answer}')
            return False

        print('GANASTE UN PUNTO SIGUIENTE PREGUNTA >>>')
        return True

    def next_question(self) -> None:
        """
        _summary_: Obtiene la siguiente pregunta y actualiza la vista
        """
        print('NEXT QUESTION >>>')
        self.hide([self.question, self.answer_a, self.answer_b])
        self.index += 1
        self.generate_public_answers()
        self.question, self.answers = self.get_question_and_answers()
        self.debugger(config.str_to_bool(config.get_key('DEBUGGER')))
        self.question = TextTitle(
            x=SCREEN[0]//2, y=SCREEN[1]//2 - 300,
            texto=self.question, pantalla=self.pantalla, font_size=25)

        self.answer_a = AnswerButton(
            x=SCREEN[0]//2 - 300, y=SCREEN[1]//2 - 200,
            texto=self.answers[0], pantalla=self.pantalla,
            on_click=self.game_logic, on_click_param='red')

        self.answer_b = AnswerButton(
            x=SCREEN[0]//2 + 300, y=SCREEN[1]//2 - 200,
            texto=self.answers[1], pantalla=self.pantalla,
            on_click=self.game_logic, on_click_param='blue')
        self.show([self.question, self.answer_a, self.answer_b])
        # Dataset
        self.hide([self.bar_graph])
        self.bg_image = pg.image.load(config.base_dir +
                                      config.get_key('BAR_GRAPH')).convert_alpha()
        # Create an instance of AnimatedBarGraph
        self.bar_graph = AnimatedBar(x=SCREEN[0]//2, y=SCREEN[1]//2, texto='',
                                     pantalla=self.pantalla, data=self.public_answers, image=self.bg_image)
        self.show([self.bar_graph])
        self.bar_graph.draw()
        self.bar_graph.update()

    def increment_puntaje(self) -> None:
        """
            Incrementa el puntaje y actualiza el marcador
            """
        self.hide([self.marcador_puntaje])
        self.puntaje += 1

        print(f'Puntaje: {self.puntaje}')
        # self.widgets_list.remove(self.marcador_puntaje)
        self.marcador_puntaje = TextTitle(
            x=100, y=20, texto='Puntaje: ' + str(self.puntaje), pantalla=self.pantalla, font_size=30
        )
        self.widgets_list.append(self.marcador_puntaje)

    def remove_element(self, element=None, type_elem='default'):
        """
        _summary_ Remueve elementos de la vista

        Keyword Arguments:
            element -- _description_ (default: {None}) Elemento a remover, si se tiene acceso
            type_elem -- _description_ (default: {'default'}) Elemento a remover. Si no se tiene acceso. En este caso se remueven todos los elementos 'banner'
        """
        if element is not None and type_elem == 'default':
            self.widgets_list = [
                widget for widget in self.widgets_list if widget != element
            ]
        elif type_elem == 'banner':
            self.widgets_list = [
                widget for widget in self.widgets_list if widget not in self.public_banner
            ]

    def game_over(self):
        """
            _summary_ Final del juego
        """
        self.hide([self.question, self.answer_a, self.answer_b])
        self.set_wildcards_used('ALL')
        print('GAME OVER')
        self.title = TextTitle(
            x=SCREEN[0]//2, y=SCREEN[1]//2 - 350,
            texto='Game Over', pantalla=self.pantalla, font_size=90
        )
        self.play_again_button = Button(
            x=SCREEN[0]//2, y=SCREEN[1]//2 - 250,
            texto='Jugar de nuevo', pantalla=self.pantalla,
            on_click=self.play_again, on_click_param='play_again'
        )
        self.go_back_button = Button(
            x=SCREEN[0]//2, y=SCREEN[1]//2 - 200,
            texto='Volver al menu Principal', pantalla=self.pantalla,
            on_click=self.go_back, on_click_param='form_main_menu'
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
            lista -- _description_ Lista de elementos a remover de la vista
        """
        for element in lista:
            if element in self.widgets_list:
                self.remove_element(element)

    def play_again(self, param) -> None:
        """
            _summary_ Volver a jugar

        Arguments:
            param -- _description_ Texto informativo para terminal. No se muestra en vista
        """
        self.hide([self.play_again_button,
                   self.go_back_button, self.title])
        self.remove_element(None, 'banner')
        self.start_game(param)

    def go_back(self, param):
        """
            Volver al menu.

        Arguments:
            param -- _description_ Menu al cual se vuelve
        """
        self.hide([self.play_again_button,
                   self.go_back_button, self.title])
        self.remove_element(None, 'banner')
        self.generate_play('JUGAR')
        self.click_back(param)

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
            _description_ Devuelve el resultado de la mayoría: Rojo o Azul
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
            pantalla -- _description_ Objeto pantalla
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

    def generate_color_banner(self, answer, position, pantalla):  # Crear clase?
        """
            _summary_ Crea el objeto banner

            Arguments:
                answer -- Respuesta: 0 o 1 . paraa Rojo o Azul
                position -- _description_ Posición del marcador, horizontal, eje x
                pantalla -- _description_ Objeto pantalla

            Returns:
                _description_ Devuelve el banner con los campos para agregar al a la lista de vista
        """
        color = (0, 0, 0)
        if (answer == 1):
            color = (0, 0, 255, 150)
        else:
            color = (255, 0, 0, 150)

        banner = Banner(
            position, 310, '', pantalla, 0, color, (20, 20))

        return banner

    def click_music_off(self, parametro):  # Mover a otro clase
        pg.mixer.music.pause()

    def get_question_and_answers(self) -> tuple:
        """
            _summary_ Obtiene la pregunta y sus respuestas. Depende clase Questions

            Returns:
                _description_ Tupla con pregunta y lista derespuestas
        """
        question = questions.get_question(self.index)
        answers = questions.get_answers(self.index)
        return (question, answers)

    def click_back(self, parametro):
        self.index = 0
        self.puntaje = 0
        self.set_active(parametro)

    def update_contador(self, segundos):
        pass

    def draw(self):
        super().draw()
        for widget in self.widgets_list:
            widget.draw()

    def update(self):
        super().draw()
        for widget in self.widgets_list:
            widget.update()

    def debugger(self, config):
        """
            Debugger method para probar dinámica del juego - Mover a clase separada

            Arguments:
            config -- Objeto settings
        """
        result = self.get_public_answers_result()

        table_data = [
            ["Public Answers", self.public_answers],
        ]

        headers = ["Public Answers"] + \
            [str(i + 1) for i in range(len(self.public_answers))]

        values_row = ["Value"] + self.public_answers

        table_data = [values_row]

        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        print(f'Resultado Publico: {result}')
        print(f'Pregunta {self.index} :{self.question}')
        print(f'Puntaje: {self.puntaje}')
        print('Respuestas: \n')
        print(f'Respuesta Rojo: {self.answers[0]}')
        print(f'Respuestas Azul: {self.answers[1]}')
