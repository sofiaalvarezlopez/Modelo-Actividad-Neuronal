from pathlib import Path
from vista.vistaPrincipal import ventana_principal


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    directorioActual = Path(__file__).parent
    ventana_principal(directorioActual)

