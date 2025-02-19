import time
import Adafruit_DHT
import paho.mqtt.client as mqtt
import json
import random  # Para simular calidad del aire en lugar de un sensor real

# Configuración de WiFi no es necesaria en Python, la Pi ya debe estar conectada a la red

# Configuración del sensor DHT11
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO donde está conectado el sensor

# Configuración de MQTT para Adafruit IO
MQTT_SERVER = "io.adafruit.com"
MQTT_PORT = 1883
MQTT_USER = "Danye3"
MQTT_KEY = "aio_GDcT61OYv2wafLx0GArOSkBuQnGi"
MQTT_FEED_TEMP = f"{MQTT_USER}/feeds/temperatura"
MQTT_FEED_HUM = f"{MQTT_USER}/feeds/humedad"
MQTT_FEED_AIR = f"{MQTT_USER}/feeds/calidad_del_aire"

# Configuración de MQTT para ThingsBoard
TB_SERVER = "thingsboard.cloud"
TB_PORT = 1883
TB_TOKEN = "cPfJur6LJ2lxnFKfjuAd"
TB_TOPIC = "v1/devices/me/telemetry"

# Cliente MQTT para Adafruit IO
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_KEY)

# Cliente MQTT para ThingsBoard
tb_client = mqtt.Client()
tb_client.username_pw_set(TB_TOKEN)

# Conectar a los servidores MQTT
def connect_mqtt(client, server, port):
    try:
        client.connect(server, port, 60)
        client.loop_start()
        print(f"Conectado a {server}")
    except Exception as e:
        print(f"Error conectando a {server}: {e}")

connect_mqtt(client, MQTT_SERVER, MQTT_PORT)
connect_mqtt(tb_client, TB_SERVER, TB_PORT)

def send_data(temp, hum, air_quality):
    """Envía datos a Adafruit IO y ThingsBoard."""
    client.publish(MQTT_FEED_TEMP, str(temp))
    client.publish(MQTT_FEED_HUM, str(hum))
    client.publish(MQTT_FEED_AIR, str(air_quality))

    payload = json.dumps({"temperature": temp, "humidity": hum, "airQuality": air_quality})
    tb_client.publish(TB_TOPIC, payload)
    
    print(f"Datos enviados - Temp: {temp}°C, Hum: {hum}%, Air Quality: {air_quality}")

# Loop principal
try:
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        air_quality = random.randint(0, 500)  # Simulación de calidad del aire
        
        if humidity is not None and temperature is not None:
            send_data(temperature, humidity, air_quality)
        else:
            print("Error leyendo el sensor DHT11")

        time.sleep(5)  # Esperar 5 segundos antes de enviar nuevos datos

except KeyboardInterrupt:
    print("\nFinalizando programa...")
    client.loop_stop()
    tb_client.loop_stop()
    client.disconnect()
    tb_client.disconnect()
