from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
import led_control
from time import sleep

# Initialize the LCD
lcd = LCD.lcd()
lcd.lcd_clear()
current_mode = None

# Callback function invoked when any key on the keypad is pressed
def key_pressed(key):
    global current_mode
    print(f"Key pressed: {key}")  

    if key == 1:  # Check if the key is a character '1'
        current_mode = "Blink"
        lcd.lcd_clear()
        lcd.lcd_display_string("LED Control", 1)
        lcd.lcd_display_string("Blink LED", 2)
        led_control.set_blinking_mode()  # Assuming this function initiates blinking

    elif key == 0:  
        current_mode = "Off"
        lcd.lcd_clear()
        lcd.lcd_display_string("LED Control", 1)
        lcd.lcd_display_string("OFF LED", 2)
        led_control.stop_blinking()  # Assuming this function stops blinking

def main():
    lcd.lcd_display_string("LED Control", 1)
    lcd.lcd_display_string("0:Off 1:Blink", 2)
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    print("Keypad thread started")  

    led_control.led_control_init()

    print("LED control initialized")  

if __name__ == "__main__":  # Corrected the entry point check
    main()
