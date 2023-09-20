"""El módulo utils provee metodos generales usadas en demas modulos"""

import json
from datetime import datetime
from typing import Union


def get_timestamp() -> str:
    """Retorna el tiempo y hora actual

    Returns:
        srt: String Del Tiempo Actual
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def key_split(key: str, split_ch:str = "_") -> Union[str, str]:
    """Separa las llaves de los diccionarios tipo nombre_id (implementado para que en los logs y json se puedan identificar
       con usuario o nombre)

    Args:
        key (str): _description_
        split_ch (str, optional): Caracter que separa la llave/valor. Defaults to "_".

    Returns:
        Union[str str]: [Llave separada, Valor separado]
    """

    for i in range(len(key)-1, 0, -1):
        if key[i] == split_ch:
            break

    return key[0:i], key[i+1:len(key)]