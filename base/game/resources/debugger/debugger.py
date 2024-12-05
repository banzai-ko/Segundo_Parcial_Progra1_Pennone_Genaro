from tabulate import tabulate


class Debugger():
    """
        Debugger method para probar dinámica del juego
    """
    @staticmethod
    def show(public_question, public_answers, public_result, index, puntaje, data):
        """
        _summary_ Muestra info por terminal
        """
        headers = [str(i) for i in range(1, 15)]
        table_data = [[val for val in data]]
        print('Publico')
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f'Resultado Público: {public_result}')
        print(f'Pregunta {index}: {public_question}')
        print(f'Puntaje: {puntaje}')
        print('Respuestas: \n')
        print(f'Respuesta Rojo: {public_answers[0]}')
        print(f'Respuesta Azul: {public_answers[1]}')
