from settings import SettingsLoader


class Ranking:
    """
    _summary_ Clase para manejar el Ranking
    """

    def __init__(self):
        self.config = SettingsLoader()
        self.config_file = self.config.base_dir + \
            self.config.get_key('RANK_FILE')

    def sort_matrix(self, matrix: list[list]) -> None:
        """
        Ordenar lista antes de mostrart

        Arguments:
            matrix -- _description_
        """

        for i in range(len(matrix) - 1):
            for j in range(i + 1, len(matrix)):
                if int(matrix[i][1].strip()) < int(matrix[j][1].strip()):
                    matrix[i], matrix[j] = matrix[j], matrix[i]

    def ranking(self, file):
        """
        _summary_ Carga el ranking desde archivo

        Arguments:
            file -- _description_ Ruta del archivo

        Returns:
            _description_ Lista con los 10 mejores puntajes
        """
        ranking = []
        base_dir = self.config.base_dir
        file_path = base_dir + file

        with open(file_path, 'r', encoding='utf-8') as rkng:
            lineas = rkng.read()
            for linea in lineas.split('\n'):
                # Strip extra spaces and ignore empty lines
                if linea.strip():  # Skip empty lines
                    ranking.append(linea.split(','))

        # Sort the matrix based on the second column (score)
        self.sort_matrix(ranking)
        return ranking[:10]

    def store_ranking(self, entry: tuple) -> None:
        """
         Agregar nueva entrada al ranking

        Arguments:
            entry -- _Objeto usuario
        """
        with open(self.config_file, 'a', encoding='utf-8') as rkng:
            rkng.write(f'{entry}\n')
