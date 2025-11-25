# ---------------------------------------------------------
# Proyecto      : Reconstrucción Numérica de Datos Hidroclimáticos
# Módulo        : main.py
# Descripción   : El programa implementa una solución para estimar los valores faltantes de precipitación 
#                 en estaciones climatológicas, utilizando información proveniente de estaciones vecinas. 
#                 El método aplicado es el Método del Porcentaje Normal, ampliamente utilizado en hidrología 
#                 cuando las estaciones comparadas tienen promedios anuales (normales) diferentes.
# Autor         : Laura Camila Rico Rincon
# Fecha         : 24-11-2025
# Versión       : 1.0.0
# ---------------------------------------------------------

#Librerías Importadas
#-------------------------------------------------------------

#1. pandas (import pandas as pd)
#   - Biblioteca especializada en el manejo y análisis de datos
#     en estructuras como DataFrame y Series.
#   - Usos principales en este módulo:
#        * Lectura de archivos Excel o CSV.
#        * Limpieza y transformación de datos.
   
#2. Data (from classes.data import Data)
#   - Clase personalizada definida dentro del proyecto.
#   - Representa una estructura de datos para almacenar información
#     organizada por año, estación o mes.

#3. defaultdict (from collections import defaultdict)
#   - Estructura de datos que permite crear diccionarios con valores
#     iniciales por defecto.
#   - Usos principales:
#        * Agrupar datos por categorías (estación, mes, año, etc.).
#        * Evitar errores al acceder a claves no existentes.

#4. math (import math)
#   - Biblioteca estándar para operaciones matemáticas avanzadas.
#   - Usos principales:
#        * Cálculo de valores estadísticos adicionales.
#        * Uso de funciones matemáticas como sqrt(), pow(), log(), etc.

#5. matplotlib.pyplot (import matplotlib.pyplot as plt)
#   - Biblioteca de visualización para generar gráficos y diagramas.

import pandas as pd
from classes.data import Data
from collections import defaultdict
import math
import matplotlib.pyplot as plt

print(pd.__version__)


def crear_data():
    """
    Lee un archivo Excel con información climatológica y crea una lista 
    de objetos `Data`. El archivo contiene cuatro columnas: año, estación 1, 
    estación 2 y mes. Las filas con valores de mes vacíos conservan el 
    último mes válido encontrado anteriormente.

    El comportamiento es equivalente al manejo típico de archivos 
    climatológicos donde el mes solo se escribe en la primera fila 
    correspondiente y se omite en las demás.

    Returns:
        list[Data]: 
            Una lista de objetos `Data`, cada uno representando los valores 
            de una fila del archivo Excel, con el mes propagado correctamente.

    Raises:
        FileNotFoundError: 
            Si el archivo "resources/data.xlsx" no existe.
        ValueError:
            Si el archivo no contiene al menos 4 columnas.
    """
    df = pd.read_excel("resources/data.xlsx", usecols="A:D", header=None)
    data = []
    month = None
    for _, row in df.iterrows():
        year, station_1, station_2, month_cell = row
        if pd.isna(month_cell):
            month_cell = None
        if month_cell is not None:
            month = month_cell
        data.append(Data(year=year, station_1=station_1, station_2=station_2, month=month))
    return data

def completar_porcentaje_normal(data, normales):
    """
    Completa valores faltantes de precipitación en las estaciones
    utilizando el método del porcentaje normal para dos estaciones.

    Si `station_1` está vacío y `station_2` tiene dato, se calcula:

        station_1 = (N1 / N2) * station_2

    Si `station_2` está vacío y `station_1` tiene dato, se calcula:

        station_2 = (N2 / N1) * station_1

    Donde N1 y N2 son las precipitaciones normales anuales de cada estación.

    Args:
        data (list[Data]):
            Lista de objetos `Data` con valores de estación 1 y estación 2.
            Puede contener valores None que se intentarán completar.
        normales (dict[str, float]):
            Diccionario con las precipitaciones normales, con claves:
            - "station_1"
            - "station_2"

    Returns:
        list[Data]:
            Lista de objetos `Data` con los valores completados cuando
            es posible mediante la relación del porcentaje normal.

    Notes:
        - Si ambas estaciones están vacías en una fila, no se modifica.
        - Si ambas tienen valor, también se conserva el dato original.
    """
    data_completo = []
    for row in data:
        s1 = row.station_1
        s2 = row.station_2
        if s1 is None and s2 is not None:
            row.station_1 = (normales["station_1"] / normales["station_2"]) * s2
        if s2 is None and row.station_1 is not None:
            row.station_2 = (normales["station_2"] / normales["station_1"]) * row.station_1
        data_completo.append(row)
    return data_completo

def imprimir_fila(nombre, dic, decimales=2):
    """
    Imprime una fila formateada en consola con valores mensuales alineados
    en columnas. El formato varía dependiendo de la cantidad de decimales
    solicitada.

    La función asume la existencia de la lista global `orden_meses`,
    la cual indica el orden en el que se deben imprimir los valores.

    Args:
        nombre (str):
            Etiqueta o nombre que se imprime al inicio de la fila.
        dic (dict[str, float]):
            Diccionario que contiene los valores por mes. Las claves deben 
            coincidir con los valores en `orden_meses`.
        decimales (int, optional):
            Cantidad de decimales a mostrar.  
            - Si vale 5 → imprime con formato `>15.5f`  
            - En otro caso → imprime con formato `>10.2f`  
            Por defecto es 2.

    Returns:
        None

    Example:
        >>> orden_meses = ["Enero", "Febrero", "Marzo"]
        >>> imprimir_fila("Promedio", {"Enero": 10, "Febrero": 15, "Marzo": 8})
        Promedio                10.00       15.00        8.00
    """
    fila = f"{nombre:<10} "
    for mes in orden_meses:
        if decimales == 5:
            fila += f"{dic[mes]:>15.5f} "
        else:
            fila += f"{dic[mes]:>10.2f} "
    print(fila)

orden_meses = [
    "ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
    "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"
]
"""
Lista que define el orden oficial de los meses del año.
Se utiliza como referencia para recorrer, imprimir o calcular valores mensuales
de manera consistente en todo el programa.
"""

normales = {"station_1": 1200, "station_2": 800}
"""
Diccionario que contiene las precipitaciones anuales normales
para cada estación meteorológica.

Keys:
    - "station_1": Normal anual de la estación 1 (en mm)
    - "station_2": Normal anual de la estación 2 (en mm)

Estas normales se utilizan para aplicar el método de
relación de promedios o porcentaje normal en la estimación de datos faltantes.
"""

estaciones = ["station_1", "station_2"]
"""
Lista con los nombres de las estaciones meteorológicas manejadas
en el sistema. Facilita iteraciones o validaciones.
"""

repetir = True
"""
Variable de control para el bucle principal del programa.
Mientras sea True, el programa continuará ejecutando el menú o proceso
interactivo hasta que el usuario decida finalizar.
"""
while repetir:
    """
    Bucle principal del análisis climático.

    Este ciclo controla todo el proceso interactivo para consultar,
    completar, procesar y visualizar series de precipitación mensual
    provenientes de un archivo Excel. Permite repetir el proceso para
    diferentes estaciones climatológicas.

    Pasos ejecutados dentro del ciclo:

    1. **Carga y completado de datos**
       - Se lee un archivo Excel mediante `crear_data()`.
       - Se completan los datos faltantes aplicando proporciones normales
         con `completar_porcentaje_normal()`.

    2. **Selección de estación**
       - El usuario elige `station_1` o `station_2`.
       - Se valida la entrada y se asigna un valor por defecto en caso de error.

    3. **Construcción de tabla año-mes**
       - Se genera un diccionario:
            tabla[año][mes] = valor_de_precipitación
       - Si un mes no tiene datos, se marca como vacío.

    4. **Cálculo de estadísticas mensuales**
       Para cada mes se calcula:
         - Promedio
         - Máximo
         - Mínimo
         - Desviación estándar
         - PMP (Precipitación Máxima Probable) = media + 1.5σ

       Si un mes no tiene datos, se asignan valores 0.

    5. **Impresión formateada de tabla**
       - Se imprime una tabla con todos los años y meses.
       - Luego se imprimen filas resumen usando `imprimir_fila()`:
         · Mínimos
         · Promedios
         · Máximos
         · Desviación estándar
         · PMP

    6. **Cálculo de la precipitación anual multianual**
       - Se suma el promedio de cada mes.

    7. **Generación de gráfica**
       - Grafica las curvas de:
            mínimo, promedio y máximo.
       - Configura título, ejes, cuadrícula y leyendas.

    8. **Repetición del proceso**
       - El usuario indica si desea analizar otra estación.

    El ciclo termina cuando el usuario responde algo diferente de "s".

    Dependencias:
        - crear_data()
        - completar_porcentaje_normal()
        - imprimir_fila()
        - matplotlib.pyplot
        - defaultdict
        - math

    Variables principales:
        repetir (bool): controla el ciclo.
        data (list[Data]): lista de registros leídos.
        data_completa (list[Data]): lista con valores completados.
        estacion (str): estación seleccionada.
        tabla (dict): datos organizados por año y mes.
        promedios, maximos, minimos, desviaciones, pmp (dict): estadísticas.
    """
    data = crear_data()
    data_completa = completar_porcentaje_normal(data, normales)

    print("\nSelecciona la estación que deseas analizar:")
    for i, est in enumerate(estaciones, 1):
        print(f"{i}. {est}")
    seleccion = input("Ingresa el número de la estación: ")
    try:
        estacion = estaciones[int(seleccion) - 1]
    except (IndexError, ValueError):
        print("Selección inválida. Se usará station_1 por defecto.")
        estacion = "station_1"
    print(f"\nSe analizará: {estacion}\n")

    tabla = defaultdict(lambda: {mes: "" for mes in orden_meses})
    for d in data_completa:
        tabla[d.year][d.month] = getattr(d, estacion)

    promedios, maximos, minimos, desviaciones, pmp = {}, {}, {}, {}, {}
    for mes in orden_meses:
        valores = [tabla[año][mes] for año in tabla if tabla[año][mes] != ""]
        if valores:
            n = len(valores)
            media = sum(valores) / n
            promedios[mes] = media
            maximos[mes] = max(valores)
            minimos[mes] = min(valores)
            varianza = sum((x - media) ** 2 for x in valores) / n
            desviaciones[mes] = math.sqrt(varianza)
            pmp[mes] = media + 1.5 * desviaciones[mes]
        else:
            promedios[mes] = maximos[mes] = minimos[mes] = desviaciones[mes] = pmp[mes] = 0

    titulo = f"TABLA DE PRECIPITACIÓN MENSUAL POR AÑO ({estacion.upper()})"
    print(titulo.center(150, "="))
    print()
    print(f"{'AÑO':<10} " + " ".join(f"{m[:3]:>10}" for m in orden_meses))

    for año in sorted(tabla.keys()):
        fila = f"{año:<10} "
        for mes in orden_meses:
            val = tabla[año][mes]
            val_str = f"{val:.2f}" if val != "" else "    -    "
            fila += f"{val_str:>10} "
        print(fila)

    print()
    imprimir_fila("MINIMO", minimos)
    imprimir_fila("PROMEDIO", promedios)
    imprimir_fila("MAXIMO", maximos)
    imprimir_fila("DESV_STD", desviaciones, decimales=5)
    imprimir_fila("PMP", pmp, decimales=5)

    suma_promedios_anual = sum(promedios[mes] for mes in orden_meses)
    print(f"\nSUMA DE PROMEDIOS ANUALES MULTIANUAL: {suma_promedios_anual:.2f} mm")

    val_min = [minimos[m] for m in orden_meses]
    val_prom = [promedios[m] for m in orden_meses]
    val_max = [maximos[m] for m in orden_meses]

    plt.figure(figsize=(12,6))
    plt.plot(orden_meses, val_min, marker='o', linestyle='--', color='blue', label='Mínimo')
    plt.plot(orden_meses, val_prom, marker='s', linestyle='-', color='green', label='Promedio')
    plt.plot(orden_meses, val_max, marker='^', linestyle='--', color='red', label='Máximo')
    plt.title(f"Precipitación Mensual ({estacion}) - Mínimo, Promedio y Máximo")
    plt.xlabel("Mes")
    plt.ylabel("Precipitación (mm)")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    respuesta = input("\n¿Desea repetir el proceso con otra estación? (s/n): ").lower()
    if respuesta != "s":
        repetir = False
        print("\nProceso terminado.")
