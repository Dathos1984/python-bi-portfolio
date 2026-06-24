import pyaudio

p = pyaudio.PyAudio()
print("🔍 Buscando el dispositivo correcto para capturar tu PC...\n")

dispositivo_encontrado = False

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    nombre = dev['name'].lower()
    
    # Filtramos por las palabras clave que Windows usa para el audio interno
    if "mezcla" in nombre or "mix" in nombre or "loopback" in nombre or "wave" in nombre:
        print(f"✅ ¡ENCONTRADO!")
        print(f"   👉 ÍNDICE A USAR: {i}")
        print(f"   📌 Nombre: {dev['name']}\n")
        dispositivo_encontrado = True

if not dispositivo_encontrado:
    print("❌ No encontré Mezcla Estéreo o Loopback automáticamente.")
    print("Muestra los primeros 5 dispositivos de tu lista para ayudarte a elegir:")
    for i in range(min(5, p.get_device_count())):
        dev = p.get_device_info_by_index(i)
        print(f"   Índice {i}: {dev['name']}")

p.terminate()