import tkinter as tk
import tkinter.ttk as ttk
import time
import mydb20250506 as mydb
import RPi.GPIO as GPIO
import Adafruit_PCA9685

root = tk.Tk()
root.title('この画面は最小化してください')
root.geometry("250x0")

def func(data):
    print(data)
    if data is True:
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(60)
        GPIO.setmode(GPIO.BCM)
        gpio_sensor = 22
        GPIO.setup(gpio_sensor, GPIO.IN)
        time_start = time.time()
        try:
            num = 0
            while True:
                time_end = time.time()
                time_elapsed = time_end - time_start
                input_sensor = GPIO.input(gpio_sensor)
                print('Time : {:.1f}s, GPIO_input : {}'.format(time_elapsed, input_sensor))
                if input_sensor == 0:
                    pwm.set_pwm(15, 0, 5)
                    time.sleep(0.4)
                    pwm.set_pwm(15, 0, 0)
                    time.sleep(1)
                    num += 1
                    if num >= 5:
                        break
                else:
                    pwm.set_pwm(15, 0, 100)
                    time.sleep(0.2)
                    pwm.set_pwm(15, 0, 0)
                    time.sleep(0.1)
                    break
        except KeyboardInterrupt:
            print("\nCtrl+C")
            GPIO.cleanup(gpio_sensor)
    print(type(data))
    return data

def main_again():
    try:
        check = mydb.unit_do()
        print(check)
        try:
            whatdo = func(check)
        except Exception as e:
            print("servo_motor_disconnected!!", e)
    except Exception as e:
        print("wifi_connect_error", e)
    root.after(3000, main_again)

main_again()
root.mainloop()

