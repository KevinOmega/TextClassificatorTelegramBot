import math
from collections import defaultdict
from DataProcess import datos_entrenamiento, procesar_texto_desde_cero

class NaiveBayesNativo:
    def __init__(self):
        self.clases = set()
        self.vocabulario = set()
        self.log_priors = {}    # P(Clase)
        self.log_likelihoods = {} # P(Palabra | Clase)

    def limpiar_texto(self, texto):
        """Pequeño preprocesamiento: minúsculas y split básico."""
        trans = str.maketrans('', '', '.,!?;:')
        return texto.lower().translate(trans).split()

    def fit(self, X_mensajes, y_categorias):
        """
        Entrena el modelo calculando conteos y probabilidades.
        """
        n_docs = len(X_mensajes)
        self.clases = set(y_categorias)

        # Estructuras para conteos
        conteo_palabras_por_clase = {c: defaultdict(int) for c in self.clases}
        total_palabras_en_clase = {c: 0 for c in self.clases}
        conteo_docs_por_clase = defaultdict(int)

        # 1. Llenar conteos
        print("Calculando frecuencias...")
        for mensaje, categoria in zip(X_mensajes, y_categorias):
            conteo_docs_por_clase[categoria] += 1
            palabras = self.limpiar_texto(mensaje)

            for palabra in palabras:
                self.vocabulario.add(palabra)
                conteo_palabras_por_clase[categoria][palabra] += 1
                total_palabras_en_clase[categoria] += 1

        # 2. Calcular Priors y Likelihoods (usando Logaritmos)
        # Usamos logaritmos porque log(a*b) = log(a) + log(b).
        # Esto evita errores numéricos con números muy pequeños.

        vocab_size = len(self.vocabulario)
        print(f"Tamaño del vocabulario: {vocab_size} palabras únicas.")

        for c in self.clases:
            # A. Prior: P(Clase) = docs_clase / total_docs
            self.log_priors[c] = math.log(conteo_docs_por_clase[c] / n_docs)

            # B. Likelihoods: P(Palabra | Clase)
            self.log_likelihoods[c] = {}
            denominator = total_palabras_en_clase[c] # Smoothing (+ |V|)

            for palabra in self.vocabulario:
                # Laplace Smoothing: (count + 1) / (total + vocab_size)
                count = conteo_palabras_por_clase[c].get(palabra, 0)
                prob = (count) / denominator
                self.log_likelihoods[c][palabra] = math.log(prob)

        print("Entrenamiento finalizado.")

    def predict(self, mensaje):
        """
        Predice la clase para un nuevo mensaje.
        """
        palabras = self.limpiar_texto(mensaje)
        scores = {c: self.log_priors[c] for c in self.clases}

        for c in self.clases:
            for palabra in palabras:
                # Si la palabra está en nuestro vocabulario, sumamos su log-probabilidad
                if palabra in self.vocabulario:
                    scores[c] += self.log_likelihoods[c][palabra]
                # Si la palabra es totalmente desconocida, la ignoramos
                # (o podríamos penalizarla, pero ignorar es estándar en implementaciones simples)

        # Devolver la clase con el score más alto (menos negativo)
        # max(diccionario, key=diccionario.get) devuelve la llave con el valor máximo
        mejor_clase = max(scores, key=scores.get)
        return mejor_clase, scores



def probar_modelo_nativo(mensaje, modelo):
    prediccion, scores = modelo.predict(mensaje)

    print("="*60)
    print(f"MENSAJE: '{mensaje}'")
    print("="*60)
    print(f"Predicción Final: --> {prediccion.upper()} <--\n")

    print("Detalle de Scores (Log-Probabilidades):")
    # Ordenamos los scores de mayor a menor
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    for clase, score in sorted_scores:
        # Un score más cercano a 0 (menos negativo) es mejor
        # Ejemplo: -5.2 es mejor que -12.8
          # barra = "█" * int((score + 50) / 2) if score > -50 else "" # Visualización simple
        print(f"   {clase:10}: {score:.4f}")
    print("\n")