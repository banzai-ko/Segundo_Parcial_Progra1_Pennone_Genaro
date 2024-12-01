import json


class Questions:
    """
    _summary_ Clase Questions - Carga las preguntas y respuestas de un archivo JSON

    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Questions, cls).__new__(cls)
        return cls._instance

    def __init__(self, file_path=None):
        if not hasattr(self, 'initialized'):
            self.file_path = file_path
            self.qna_list = []
            self.initialized = True

    def load_file(self):
        """
        _summary_ Cargador del archivo
        """
        if not self.file_path:
            print("Error: Ruta del archivo.")
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                if self.file_path.endswith(".json"):
                    self.qna_list = json.load(file)
                else:
                    print("Error: Formato de archivo no soportado.")
        except FileNotFoundError:
            print(f"Error: Archivo '{self.file_path}' no encotrado.")
        except json.JSONDecodeError:
            print(f"Error: No se puede decodificar '{self.file_path}'.")
        except Exception as e:
            print(f"Error: {e}")

    def get_question(self, index: list) -> str:
        """
        _summary_ Obtiene la pregunta de la lista, en la posición index

        Returns:
            _description_ Pregunta de la lista en la posicion index, como string
        """
        if 0 <= index < len(self.qna_list):
            return self.qna_list[index]["pregunta"]
        print("Error: Indice.")
        return None

    def get_answers(self, index: int) -> list:
        """
        _summary_ Obtiene las respuestas de la lista, para la pregunta en laposición index

        Returns:
            _description_ Respuestas de la lista en la posicion index
        """
        if 0 <= index < len(self.qna_list):
            return self.qna_list[index]["respuestas"]
        print("Error: Indice.")
        return None
