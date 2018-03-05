#!/usr/local/bin/python

import asyncio
import itertools

try:
    import RPi.GPIO as GPIO
except:
    from f47pt.gpiomock import GPIO

GPIO.setmode(GPIO.BOARD)


async def acount(start=0, step=1):
    for item in itertools.count(start, step):
        await asyncio.sleep(0)
        return item


async def check_pin(pin, t_iteration=0.01):
    await asyncio.sleep(t_iteration)
    return GPIO.input(pin) == GPIO.LOW


async def ldr_async(pin,  t_setup=0.025, t_iteration=0.05):
    count = 0

    # Output on the pin for
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    await asyncio.sleep(t_setup)

    # Change the pin back to input
    GPIO.setup(pin, GPIO.IN)

    # Count until the pin goes high
    while await check_pin(pin, t_iteration):
        count += 1

    return count


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        while True:
            result = loop.run_until_complete(ldr_async(7))
            print(result)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
