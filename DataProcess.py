from trainData import datos_entrenamiento

stop_words_simon = {'hubo', 'que', 'o', 'el', 'suyo', 'hayáis', 'habido', 'es', 'habréis', 'hubiste',
                    'sin', 'poco', 'fuésemos', 'suyos', 'siente', 'tenga', 'tenida', 'tuvieseis', 'donde',
                    'cual', 'todos', 'fui', 'estemos', 'tendría', 'haya', 'nuestro', 'habíais', 'estuvo',
                    'tuviésemos', 'tendrás', 'fueron', 'te', 'fueras', 'tendrías', 'tengo', 'habidas',
                    'eran', 'estos', 'hubieseis', 'habida', 'entre', 'eres', 'sentida', 'estaba',
                    'hubiéramos', 'al', 'estar', 'éramos', 'él', 'tendrá', 'tendrán', 'habidos',
                    'estuvierais', 'seamos', 'fuéramos', 'habrán', 'estuvimos', 'esta', 'somos',
                    'hubieras', 'tuviera', 'será', 'estuviese', 'tuvo', 'para', 'habrías',
                    'las', 'hubieran', 'había', 'algunas', 'contra', 'otros', 'en', 'fueses',
                    'tú', 'como', 'míos', 'fue', 'habríais', 'tuyas', 'estábamos', 'tuvierais',
                    'estarían', 'hubiesen', 'mí', 'tanto', 'soy', 'estuve', 'era', 'fuesen',
                    'algo', 'fueseis', 'sintiendo', 'tuvieran', 'la', 'lo', 'estarán',
                    'sentido', 'hubiera', 'seremos', 'hubierais', 'ellos', 'estando',
                    'habríamos', 'mi', 'habrás', 'tuya', 'ese', 'hubiésemos', 'muy',
                    'tenemos', 'tendremos', 'están', 'tened', 'tendríamos', 'habré',
                    'vuestras', 'sobre', 'pero', 'estuvieras', 'estuvisteis', 'tuvimos', 'por',
                    'un', 'tenido', 'ante', 'teniendo', 'su', 'nosotros', 'estaréis', 'estuvieses', 'tuyos', 'estéis',
                    'tuviese', 'estaríamos', 'hubisteis', 'estén', 'hubimos', 'habían', 'estará', 'a', 'esté', 'habría', 'ya',
                    'estuvieran', 'quien', 'fuerais', 'sentidos', 'serán', 'estad', 'hubieron', 'nuestros', 'muchos', 'estuviésemos',
                    'quienes', 'estás', 'hayamos', 'estuviéramos', 'fuese', 'tenían', 'habrían', 'fuera', 'fuisteis', 'nos', 'nada', 'e', 'otro', 'y', 'tendré',
                    'estuviste', 'habéis', 'hubiese', 'hasta', 'algunos', 'hayas', 'cuando', 'del', 'esa', 'fuimos', 'seríamos', 'todo', 'tuviéramos', 'has',
                    'estabas', 'hay', 'tendréis', 'tuvisteis', 'le',
                    'tenidas', 'una', 'tenías', 'tuvieron', 'tuviste', 'tus', 'tenía', 'estuvieseis', 'tendríais', 'desde'
                    ,'han', 'les', 'esto', 'esas', 'serías', 'estoy', 'estaban', 'habiendo', 'mío', 'no', 'sentidas', 'tuve', 'tienen',
                    'sus', 'vuestra', 'hayan', 'tuviesen', 'habremos', 'estés', 'sois', 'tenidos', 'ellas', 'durante', 'fuiste', 'esos', 'yo', 'estaríais',
                    'suya', 'este', 'vuestros', 'sea', 'estaremos', 'estarás', 'vosotros', 'estados', 'de', 'antes', 'otra', 'sí', 'tenéis', 'estuviesen', 'seas', 'os', 'ella', 'estadas',
                    'mía', 'estuvieron', 'estuviera', 'estabais', 'tuvieses', 'estas', 'estarías', 'eso', 'vuestro', 'tuyo', 'seréis', 'uno', 'habíamos', 'estado', 'nosotras', 'he', 'está',
                    'teníamos', 'vosotras', 'sentid', 'también', 'otras', 'ni', 'tengáis', 'hube', 'qué', 'nuestras', 'tendrían', 'tuvieras', 'hubieses', 'los', 'estáis', 'con', 'tienes', 'ti',
                    'habías', 'hemos', 'son', 'mis', 'fueran', 'habrá', 'tiene', 'tengamos', 'sería', 'mucho', 'estaré', 'suyas', 'estamos', 'erais', 'tu', 'serían', 'porque', 'mías', 'más', 'seré',
                    'sean', 'estaría', 'tengas', 'eras', 'tengan', 'estada', 'unos', 'seríais', 'me', 'se', 'ha', 'teníais', 'seáis', 'nuestra', 'serás'}




puntuacion = {'/', '*', '+', '`', '\\', '^', '=', ')',
               ':', '#', '&', '|', '-', '<', '@', '[', '%', ';', '(', '~', '>', '$', ']',
                 '.', '_', '?', '{', '!', '"', "'", ',', '}'}


def obtener_raiz_casera(palabra):
    if palabra.endswith("ar"):
        return palabra[:-2]

    if palabra.endswith("er"):
        return palabra[:-2]

    if palabra.endswith("ir"):
        return palabra[:-2]

    if palabra.endswith("as"):
        return palabra[:-2]

    if palabra.endswith("es"):
        return palabra[:-2]

    if palabra.endswith("os"):
        return palabra[:-2]

    if palabra.endswith("s"):
        return palabra[:-1]



    return palabra

def procesar_texto_desde_cero(texto):
    texto = texto.lower()

    reemplazos = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        )
    
    for con_tilde, sin_tilde in reemplazos:
        texto = texto.replace(con_tilde, sin_tilde)


    for signo in puntuacion:
        texto = texto.replace(signo, "")


    palabras_enlista = texto.split()

    print(palabras_enlista)

    # Stemming
    palabras_procesadas = []

    for palabra in palabras_enlista:

        if palabra not in stop_words_simon:
            raiz = obtener_raiz_casera(palabra)
            palabras_procesadas.append(raiz)


    return " ".join(palabras_procesadas)

