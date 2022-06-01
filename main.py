import serial

ser = serial.Serial("/dev/tty.usbserial-A50285BI", baudrate=230400)


def grab_data():
    try:
        unique_values = 0
        distance_list = [None] * 360
        while unique_values < 360:
            result = ser.read(42)
            if (result[-1] == result[-2]):
                rpm = result[3] * 256 + result[2]
                base_angle = (result[1] - 160) * 6
                for x in range(6):
                    angle = base_angle + x
                    distance = result[((6 * (x + 1)) + 1)] * 256 + result[((6 * (x + 1)))]
                    if distance_list[angle] == None:
                        unique_values += 1
                        if distance > 0:
                            print('angle: ' + str(angle) + ' distance: ' + str(distance))
                            distance_list[angle] = distance
                        else:
                            distance_list[angle] = 4200
    except IndexError:
        ser.write(b'e')
        print('Stopped! Out of sync.')


ser.write(b'b')
while True:
    grab_data()