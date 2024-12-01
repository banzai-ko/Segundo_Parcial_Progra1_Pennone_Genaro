import os

settings_dir = os.path.dirname(os.path.abspath(__file__))


class SettingsLoader:
    """
    _summary_ Clase cargador de configuraciones y manejo de archivo Settings

    """
    _instance = None
    _settings_path = os.path.join(settings_dir, 'settings.ini')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.file_path = self._settings_path
        self.config = {}
        self.load_config()
        self._screen = {}
        self.base_dir = os.path.dirname(
            os.path.dirname(settings_dir)) + '/base'

    def load_config(self) -> None:
        """
        Lee Archivo de configuracion.

        :param file_path: Ruta al archivo .ini
        :return: Dict con la configuracion
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith(';'):
                    continue  # Ignorar líneas vacías y comentarios

                if '=' in line:
                    key, value = map(str.strip, line.split('=', 1))
                    self.config[key] = value

    def get_key(self, key: str) -> str:
        """
        _summary_ Busca en el objeto config una key

        Arguments:
            name: el nombre de la key
        Returns:
            _description_ Valor de la key
        """
        return self.config.get(key)

    def set_key(self, key: str, value: str, config: dict) -> None:
        """
        _summary_  Establece el valor de una clave y lo guarda en el archivo .ini.
        Arguments:
            name -- _description_ Nombre de la clave
            value -- _description_ Valor de la clave para setear
        """
        print(f'Setting {key} to {value}')
        config[key] = value
        print(key, config[key])
        self.save_config()

    def save_config(self) -> None:
        """
        _summary_ Guarda la configuracion en el archivo .ini
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for key, value in self.config.items():
                file.write(f'{key}={value}\n')

    @property
    def screen(self):
        """
        Returns the SCREEN resolution as a tuple (WIDTH, HEIGHT).
        This makes SCREEN read-only outside the class.
        """
        if self._screen is None or self._screen == {}:
            self._screen = (
                int(self.config.get('WIDTH')),
                int(self.config.get('HEIGHT'))
            )
        return self._screen

    @staticmethod
    def str_to_bool(s):
        """
        _summary_ Convierte una cadena a un booleano, settings config desde archivo ini
        """
        return True if s == "True" else False if s == "False" else None
