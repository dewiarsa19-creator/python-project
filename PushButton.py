import serial
import time
import RPi.GPIO as GPIO  # untuk push button di Raspberry Pi

# ======================
# Konfigurasi Serial
# ======================
ser = serial.Serial(
    port='COM5',
    baudrate=115200,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=2
)

# ======================
# Fungsi Kirim Perintah
# ======================
def send_command_wait_response(cmd, delay=0.3):
    try:
        data = bytes.fromhex(cmd)
    except ValueError:
        print(f"[ERROR] Format HEX salah: {cmd}")
        return b""

    print(f"\nMengirim: {cmd}")
    ser.write(data)
    time.sleep(delay)
    response = ser.read_all()

    if response:
        try:
            print("Response (ASCII):", response.decode(errors="ignore"))
        except:
            print("Response tidak bisa didecode ke ASCII")
        print("Response (HEX):", response.hex(" ").upper())
    else:
        print("Response: [kosong]")

    return response

# ======================
# Fungsi ON dan OFF
# ======================
def lcd_on():
    commands = [
        # 1. Connect
        "02E3030100001603",
        # 2. Konfigurasi X
        "02DD0201FF1D03",
        "02DD0202FF1C03",
        # 3. Konfigurasi Y
        "02DD0201FF1D03",
        "02DD0202FF1C03",
        "02DD0203FF1B03",
        "02DD0204011A03",
        # 4. Merge
        "02DD0201011C03",
        "02DD0202011B03",
        "02DD0203011A03",
        "02DD0204011903",
        # 5. ON semua layar
        "0240020101B903",
        "0240020201B803",
        "0240020301B703",
        "0240020401B603"
    ]
    print("\n[INFO] Menyalakan LCD...")
    for cmd in commands:
        send_command_wait_response(cmd)

def lcd_off():
    commands = [
        "02 41 01 00 03"
    ]
    print("\n[INFO] Mematikan LCD...")
    for cmd in commands:
        send_command_wait_response(cmd)

# ======================
# Konfigurasi Push Button
# ======================
BUTTON_PIN = 17  # ganti dengan pin GPIO yang dipakai
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ======================
# Main Loop (Toggle)
# ======================
lcd_state = False  # False = OFF, True = ON

print("Tekan tombol untuk toggle LCD (ON/OFF). CTRL+C untuk berhenti.")
try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # tombol ditekan
            if lcd_state:
                lcd_off()
                lcd_state = False
            else:
                lcd_on()
                lcd_state = True
            time.sleep(0.5)  # debounce delay
except KeyboardInterrupt:
    print("\nProgram dihentikan.")
finally:
    ser.close()
    GPIO.cleanup()