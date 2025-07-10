def procesar_archivo_general(entrada_path, salida_path):
    with open(entrada_path, 'r', encoding='utf-8') as archivo_entrada:
        lineas_raw = archivo_entrada.readlines()

    lineas_procesadas = []
    autorefs_agregadas = set()  # Para evitar autoreferencias duplicadas
    lineas_set = set()          # Para evitar líneas duplicadas exactas

    for linea in lineas_raw:
        partes = linea.strip().split(',')

        if len(partes) == 5:
            # Formato sin procesar: tabla1,id1,tabla2,id2,aceptacion
            t1, i1, t2, i2, aceptacion = partes
            d1 = f'{t1}:{i1}'
            d2 = f'{t2}:{i2}'
        elif len(partes) == 3:
            # Formato ya procesado: dato1,dato2,aceptacion
            d1, d2, aceptacion = partes
        else:
            continue  # Ignorar líneas inválidas

        # Convertir aceptación 0 a -1
        if aceptacion.strip() == '0':
            aceptacion = '-1'

        linea_normal = f'{d1},{d2},{aceptacion}'

        if linea_normal not in lineas_set:
            lineas_procesadas.append(linea_normal)
            lineas_set.add(linea_normal)

        # Agregar línea simétrica si no existe
        simetrica = f'{d2},{d1},{aceptacion}'
        if simetrica not in lineas_set:
            lineas_procesadas.append(simetrica)
            lineas_set.add(simetrica)

        # Agregar autoreferencia para d1 si no existe
        autoref1 = f'{d1},{d1},1'
        if d1 not in autorefs_agregadas and autoref1 not in lineas_set:
            lineas_procesadas.append(autoref1)
            lineas_set.add(autoref1)
            autorefs_agregadas.add(d1)

        # Agregar autoreferencia para d2 si no existe
        autoref2 = f'{d2},{d2},1'
        if d2 not in autorefs_agregadas and autoref2 not in lineas_set:
            lineas_procesadas.append(autoref2)
            lineas_set.add(autoref2)
            autorefs_agregadas.add(d2)

    with open(salida_path, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.write('\n'.join(lineas_procesadas))

    print(f"Archivo procesado completamente: {salida_path}")


if __name__ == "__main__":
    # Cambia aquí tus archivos de entrada y salida
    archivo_entrada = 'pares_convertidos.csv'
    archivo_salida = 'pares_convertidos_procesado.csv'

    archivo_entrada2 = 'conjunto_bd_simetrico.csv'
    archivo_salida2 = 'conjunto_bd_simetrico_procesado.csv'

    procesar_archivo_general(archivo_entrada, archivo_salida)
    procesar_archivo_general(archivo_entrada2, archivo_salida2)
