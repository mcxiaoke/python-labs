from periphery import GPIO
import time


def led_set(on_or_off):
    pin = GPIO(26, "out")
    pin.write(on_or_off)
    pin.close()


def led_on():
    led_set(True)


def led_off():
    led_set(False)


if __name__ == "__main__":
    while True:
        print('LED On')
        led_on()
        time.sleep(1)
        print('LED Off')
        led_off()
        time.sleep(1)
