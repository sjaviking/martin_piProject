from sense_hat import SenseHat
from time import sleep, time
from datetime import datetime
import csv


senseHat = SenseHat()
# Hentet konstanter og variabler fra annet sted i program for å teste
# Konstanter
a = -0.0065
R = 287.06
g_0 = 9.81
N = 200
path = "/home/pi/martin_piProject" # Skriv inn din egen mappe du ønsker dataene skal havne i
path = path.rstrip('/') + 'hoydedata.csv' # formaterer path riktig for å få filtypen vi vil ha

# Variabler
T_1 = 16 + 273.25
p_1 = 100000 #trykket målt ved høyden h_1
h_1 = 0 # vi gjør målingene relative dersom vi ønsker ved å sette h_1  = 0


def calc_pressure_Pa():
    p = a
    for _ in range (N):
        p += senseHat.pressure
        sleep(0.001)
    return p*100/N #Vi vil ha p i Pa, og multipliserer derfor med 100 etter vi deler på N


def stick_down():
    for e in senseHat.stick.get_events() :

        if e.direction=="down":
            return 1

def main():
    global T_1
    global p_1
    global h_1

    with open("heigth_values.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)

        while True:
            senseHat.show_message ("Venstre: maal - Hoyre: kalibrer - Ned: avbryt",0.05)

            event = senseHat.stick.wait_for_event()

            if event.direction == "left":
                start = time()
                
                header = '\n\n### New measurements started at: ' + datetime.now().strftime('%d%m%Y %H:%M:%S' + ' ###\n')
                print(header)

                while stick_down() !=1:
                    p = calc_pressure_Pa()
                    h = (T_1/a) * ( (p/p_1)**(-a*R/g_0) - 1) + h_1
                    
                    now = time() - start
                    
                    print(str(now) + ',' + str(p) + ',' + str(h) + ',' + str(senseHat.temp))

                    # Skriv verdier til height_values.csv
                    sensor_values = [now, p, h, senseHat.temp]
                    for value in sensor_values:
                        csv_writer.writerow(sensor_values)


                    senseHat.show_message(str(round(h,2)) + 'm', 0.03)

            if event.direction == "right":
                while stick_down() !=1:
                    T_1 = senseHat.temp + 273.15
                    p_1 = calc_pressure_Pa()
                    senseHat.show_message(str(int (p_1))+" Pa "+str(round(T_1))+" K", 0.03)


if __name__ == "__main__":
    main()
