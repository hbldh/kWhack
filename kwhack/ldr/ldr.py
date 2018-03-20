#!/usr/local/bin/python
import time

from RPi import GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


def rc_time(pin):
    # Output on the pin for
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.025)
    # Change the pin back to input
    GPIO.setup(pin, GPIO.IN)
    # Count until the pin goes high
    count = 0
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
    return count


def rc_time_with_sleep(pin, t_setup=0.025, t_iteration=0.05):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(t_setup)
    # Change the pin back to input
    GPIO.setup(pin, GPIO.IN)
    # Count until the pin goes high
    t = time.time()
    while GPIO.input(pin) == GPIO.LOW:
        time.sleep(t_iteration)
    return time.time() - t


def rc_time_edge(pin, t_setup=0.025, t_iteration=5.0):
    # Output on the pin for
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(t_setup)
    # Change the pin back to input
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    t = time.time()
    edge = GPIO.wait_for_edge(
        pin, GPIO.RISING, timeout=int(t_iteration * 1000)
    )
    return edge, time.time() - t


if __name__ == '__main__':
    # Catch when script is interrupted, cleanup correctly
    # define the pin that goes to the circuit
    pin_to_circuit = 7
    try:
        # Main loop
        while True:
            print(rc_time(pin_to_circuit))
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
