import RPi.GPIO as GPIO
import time

class Ultrasonic():

    def __init__(self):
        self.value = None
        self.trig_pin = 26
        self.echo_pin = 11
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BOARD)

    def get_value(self):  return self.value

    def update(self):
        self.value = self.sensor_get_value()
        return self.value

    def reset(self):
        self.value = None

    def sensor_get_value(self):
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        self.send_activation_pulse()

        # Sensoren starter saa programmet sitt.
        # Det den gjor er aa sende ut 8 sykler av et ultrasonisk signal paa 40kHz.
        # Den venter saa paa at signalet skal bli reflektert tilbake til leseren.

        # Vi leser signalet den mottar paa echo_pin
        read_val = GPIO.input(self.echo_pin)
        # Det som er interessent her er hvor lang tid det tar fra signalet er sendt ut, til noe er returnert
        # Naar sensoren mottar et reflektert signal vil echo pinnen settes hoy like lang tid som
        # signalet brukte fra det ble sendt ut til det ble returnert

        # Vi finner tiden paa siste gang echo signalet er lavt
        signaloff_start = time.time()
        signaloff = signaloff_start
        # signalet timer ut dersom det tar mer en 0.5 s, da annsees det som tapt og vi prover igjen
        while read_val == 0 and signaloff - signaloff_start < 0.5:
            read_val = GPIO.input(self.echo_pin)
            signaloff = time.time()

        signalon = signaloff
        # Finner saa den tiden det siste signalet kommer inn paa echo_pin
        while read_val == 1:
            read_val = GPIO.input(self.echo_pin)
            signalon = time.time() # Kan flytte denne ut av loopen dersom det skaper delay og unoyaktighet

        # Den kalkulerte avstanden
        distance = self.compute_distance(signalon, signaloff)

        # Returnerer distanset til objektet forran sensoren i cm
        return distance

    def send_activation_pulse(self):
        GPIO.output(self.trig_pin, GPIO.LOW)
        # Sensoren kan krasje dersom man ikke har et delay her. Dersom den fortsatt krasjer, prov aa oke delayet
        time.sleep(0.3)

        # Ultralyd sensoren starter naar den mottar en puls, med lengde 10uS paa trig pinnen.
        # Vi gjor dette ved aa sette trig_pin hoy, venter i 10uS og setter den lav igjen.
        GPIO.output(self.trig_pin, True)
        # 0.00001 seconds = 10 micro seconds
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

    def compute_distance(self, signalon, signaloff):
        # Tiden det tok fra signalet ble sendt til det ble returnert
        timepassed = signalon - signaloff

        # Vi vet at signalet gaar med lydens hastighet som er ca 344 m/s
        # Avstanden til objektet forran sensoren kan vi da finne med formelen: strekning = hastighet * tid
        distance = 344 * timepassed * 100
        # Dette er tur retur distansen. For aa faa distansen en vei deler vi bare paa 2
        distance = distance/2
        return distance
