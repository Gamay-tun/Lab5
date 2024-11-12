import time
from hal.hal_lcd import lcd  # Importing the LCD class from hal_lcd
from hal.hal_keypad import init as keypad_init, get_key  
import RPi.GPIO as GPIO

CORRECT_PIN = "1234"
MAX_ATTEMPTS = 3
BUZZER_PIN = 18  

input_pin = ""
attempts = 0
lcd_display = lcd()

def display_message(line1, line2=""):
    lcd_display.lcd_clear()
    lcd_display.lcd_display_string(line1, line=1)
    lcd_display.lcd_display_string(line2, line=2)

def activate_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def handle_keypress(key):
    global input_pin, attempts
    
    if attempts >= MAX_ATTEMPTS:
        display_message("Safe Disabled", "")
        return

    if isinstance(key, int) or key == 0:
        input_pin += str(key)
        display_message("Safe Lock", "Enter PIN: " + "*" * len(input_pin))
    elif key == "#":
        if input_pin == CORRECT_PIN:
            display_message("Safe Unlocked", "")
            input_pin = ""  
            attempts = 0   
        else:
           
            attempts += 1
            if attempts >= MAX_ATTEMPTS:
                display_message("Safe Disabled", "")  # REQ-05
            else:
                display_message("Wrong PIN", "")  # REQ-04
                activate_buzzer()
            input_pin = ""  # Reset input after incorrect attempt

    elif key == "*":
        input_pin = ""
        display_message("Safe Lock", "Enter PIN: ")

def main():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW) 

    # REQ-01
    display_message("Safe Lock", "Enter PIN: ")
    keypad_init(handle_keypress)
    try:
        get_key()  # This will keep the program running to handle keypad input
    except KeyboardInterrupt:
        print("Exiting Program")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

if __name__ == "__main__":
    main()
