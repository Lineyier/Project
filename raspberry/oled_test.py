import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import serial

# python /home/evgenvt/Documents/projectPG/rpi-bluetooth-arduino-master/pythonClient/oled_test.py

# разрешение дисплея
WIDTH = 128
HEIGHT = 64

# ширина рамки
BORDER = 0

# инициализация шины I2C и дисплея с адресом 0x3D
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# заливаем экран черным цветом
oled.fill(0)
oled.show()

# будем работать с буфером экрана из библиотеки PIL
# первый параметр - цветность дисплея, для монохромного - 1
image = Image.new("1", (oled.width, oled.height))

# draw будет нашим карандашем, которым мы будем рисовать на экране
draw = ImageDraw.Draw(image)

# рисуем прямоугольник белого цвета во весь экран
#draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# рисуем прямоугольник поменьше черным цветом, так мы создаем контурную рамку
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# загружаем стандартный шрифт
font = ImageFont.load_default()

       
ser = serial.Serial(
    port='/dev/rfcomm0',
    baudrate= 115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()
dt = ["", "", ""]
time.sleep(2)
while 1 :
    tic = time.time()
    while time.time() - tic < 15 and ser.inWaiting() == 0: 
        time.sleep(1)
        
    for i in range(3):
        if ser.inWaiting() > 0:
            recv1 = ser.readline().rstrip().decode()
            dt[i] = recv1
    # пишем текст в центре экрана
    text = dt[0] + "\n" + dt[1] + "\n" + dt[2]
    #text = "1234567890"
    #(font_width, font_height) = font.getsize(text)
    font_width = 120
    font_height = 50
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    
    oled.fill(0)
    oled.show()
    #oled.clean()
    time.sleep(2)
    #print(text)
    # выводим буфер изображения на дисплей
    oled.image(image)
    oled.show()
    time.sleep(4)




