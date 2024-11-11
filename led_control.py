from threading import Thread
from time import sleep
from hal import hal_led as led

# Global variable to control the LED state
global delay
delay = 0  # Initialize delay to 0
running = False  # Flag to control the LED thread

def led_thread():
    global delay, running
    while True:
        if running and delay > 0:
            print("LED ON")  # Debug print
            led.set_output(24, 1)  # Turn on the LED
            sleep(delay)
            print("LED OFF")  # Debug print
            led.set_output(24, 0)  # Turn off the LED
            sleep(delay)
        else:
            led.set_output(24, 0)  # Ensure LED is off when not running
            sleep(0.1)  # Prevent high CPU usage when LED is off

def led_control_init():
    global running
    led.init()  # Initialize the LED GPIO
    running = True  # Set running flag to True
    t1 = Thread(target=led_thread, daemon=True)
    t1.start()
    print("LED control thread started")  # Debug print

def set_blinking_mode(blink_delay=1):
    """Set the LED to blinking mode with the specified delay."""
    global delay, running
    delay = blink_delay  # Set the delay for blinking
    running = True  # Ensure the thread runs
    print(f"LED set to blink mode with delay: {delay} seconds")  # Debug print

def stop_blinking():
    """Stop the LED from blinking."""
    global running
    running = False  # Stop the thread from blinking
    led.set_output(24, 0)  # Turn off the LED
    print("LED blinking stopped")  # Debug print
