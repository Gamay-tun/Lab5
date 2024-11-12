import time
from threading import Thread
from hal.hal_lcd import lcd  

lcd_display = lcd()

def update_display():
    colon_visible = True  
    while True:
        local_time = time.localtime()
        time_string = time.strftime("%H:%M:%S", local_time)
        date_string = time.strftime("%d:%m:%Y", local_time)

        if colon_visible:
            display_time = time_string
        else:
            display_time = time_string.replace(":", " ")  

        lcd_display.lcd_display_string(display_time, line=1)
        lcd_display.lcd_display_string(date_string, line=2)
        
        colon_visible = not colon_visible //toggle the visibility
       time.sleep(1)

def main():
    clock_thread = Thread(target=update_display)
    clock_thread.start()
    clock_thread.join()

if __name__ == "__main__":
    main()
