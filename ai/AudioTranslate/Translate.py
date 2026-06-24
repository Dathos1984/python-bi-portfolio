import pyaudiowpatch as pyaudio
import speech_recognition as sr
from deep_translator import GoogleTranslator
import numpy as np  # Para medir el volumen del audio de forma simple
import sys

def iniciar_traductor():
    p = pyaudio.PyAudio()
    
    try:
        wasapi_info = p.get_default_wasapi_loopback()
        print(f"✅ ¡Conectado al audio del sistema con éxito!")
        print(f"🔊 Capturando lo que suena en: {wasapi_info['name']}")
    except OSError:
        print("❌ Error: No se pudo encontrar el loopback de tus altavoces.")
        p.terminate()
        return

    recognizer = sr.Recognizer()
    
    sample_rate = int(wasapi_info["defaultSampleRate"])
    channels = wasapi_info["maxInputChannels"]
    device_index = wasapi_info["index"]

    print("\n🎧 ¡Listo! Traduciendo dinámicamente según las pausas de la PC...")
    print("(Presiona Ctrl + C para salir limpiamente)")
    print("-" * 60)

    # VARIABLES PARA EL MODO CONTINUO
    bloque_corto = int(sample_rate * 0.5)  # Lee pedacitos de medio segundo (0.5s)
    buffer_audio = b""                     # Aquí acumulamos el audio continuo
    hablando = False
    contador_silencio = 0
    
    # Umbral de volumen para detectar si hay voz sonando (puedes subirlo si hay estática)
    UMBRAL_VOLUMEN = 500  

    with p.open(format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                input_device_index=device_index) as stream:
        
        while True:
            try:
                # 1. Leer un fragmento muy pequeño de audio (en tiempo real)
                datos_parciales = stream.read(bloque_corto, exception_on_overflow=False)
                buffer_audio += datos_parciales
                
                # Calcular el volumen actual del fragmento
                audio_np = np.frombuffer(datos_parciales, dtype=np.int16)
                volumen = np.sqrt(np.mean(audio_np**2)) if len(audio_np) > 0 else 0

                # 2. Lógica de detección de voz/pausa
                if volumen > UMBRAL_VOLUMEN:
                    hablando = True
                    contador_silencio = 0  # Resetea el contador si siguen hablando
                else:
                    if hablando:
                        contador_silencio += 1

                # Si detectamos aproximadamente 1.5 segundos de silencio acumulado después de que hablaron...
                # O si el audio acumulado ya es muy largo (máximo 12 segundos para no saturar)
                if (hablando and contador_silencio >= 2) or (len(buffer_audio) > sample_rate * 2 * 12):
                    
                    # Convertimos todo el bloque acumulado para enviarlo a traducir
                    audio_data = sr.AudioData(buffer_audio, sample_rate, 2)
                    
                    try:
                        # Transcribir y traducir la frase completa
                        texto_ingles = recognizer.recognize_google(audio_data, language="en-US")
                        traduccion = GoogleTranslator(source='en', target='es').translate(texto_ingles)
                        
                        print(f"\n🇺🇸 [PC] : {texto_ingles}")
                        print(f"🇪🇸 [ESP]: {traduccion}")
                        print("-" * 60)
                    except sr.UnknownValueError:
                        # Ignora si lo acumulado era ruido o música de fondo
                        pass
                    
                    # Limpiamos las variables para la siguiente frase
                    buffer_audio = b""
                    hablando = False
                    contador_silencio = 0

            except KeyboardInterrupt:
                print("\n\n🛑 Programa detenido limpiamente por el usuario.")
                break
            except Exception as e:
                pass

    p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    iniciar_traductor()