from settings import SettingsLoader


class Ranking:
    """
    _summary_ Clase para manejar el Ranking
    """
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.config = SettingsLoader()
            self.config_file = self.config.base_dir + \
                self.config.get_key('RANK_FILE')
            self._initialized = True

    @classmethod
    def get_ranking(cls):
        """Get or create singleton instance"""
        if cls.__instance is None:
            cls()
        return cls.__instance

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
                if linea.strip():
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
            nombre, puntaje = entry
            rkng.write(f'{nombre}, {puntaje}\n')
