
import logging
from subprocess import check_output
print (check_output(['hostname', '-I']))


from flask import Flask, g, request, abort, flash, render_template, redirect
from flask_socketio import SocketIO, emit, send
from flaskext.mysql import MySQL
from flask_httpauth import HTTPBasicAuth
from passlib import pwd
from passlib.hash import argon2




from smbus import SMBus
from RPi import GPIO
import time
from threading import Thread


import random

# init hardware


bus = SMBus()  # Rev 2 Pi uses 1
bus.open(1)

DEVICE = 0x20  # Device address (A0-A2)
DEVICE1 = 0x21
IODIRA = 0x00  # Pin direction register
GPIOA = 0x12  # Register for inputs
GPPUA = 0x0C
IODIRB = 0x01  # Pin direction register
GPIOB = 0x13  # Register for inputs
GPPUB = 0x0D




bus.write_byte_data(DEVICE, 0x04, 0b11111111)
bus.write_byte_data(DEVICE, IODIRA, 0b11111111)
bus.write_byte_data(DEVICE, GPPUA, 0b11111111)
bus.write_byte_data(DEVICE, IODIRB, 0b11111111)
bus.write_byte_data(DEVICE, GPPUB, 0b11111111)

bus.write_byte_data(DEVICE1, IODIRA, 0b11111111)
bus.write_byte_data(DEVICE1, GPPUA, 0b11111111)

# init motor
DIR = 20
STEP = 21
CW = 1
CCW = 0
SPR = 200

pin_to_circuit = 22
step_count = SPR
delay = 0.003
start = 0
game_start = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CCW)

game = 0
round = 0


log = logging.getLogger(__name__)
app = Flask(__name__, template_folder='./templates')
socketio = SocketIO(app, async_mode="threading")
app.config['SECRET_KEY'] = 'secret!'
mysql = MySQL(app)
auth = HTTPBasicAuth()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'project1-web'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Project1Tibo'
app.config['MYSQL_DATABASE_DB'] = 'project1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# session config
app.secret_key = pwd.genword(entropy=128)

def tijd(channel):
    # deg = 0
    # step_count = SPR * 2
    # delay = 0.003 / 16
    global timeout, start

    timer = random.randrange(1,10)
    start = 1
    timeout = time.time() + timer

def rc_time(pin_to_circuit):
    count = 0
    GPIO.setmode(GPIO.BCM)
    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)


    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

def change(channel):
    print("knop ingedrukt")
    socketio.emit('my data',
                  "24",
                  namespace='/test')
    data = get_data("SELECT * FROM user")
    print(data)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button
# GPIO.add_event_detect(22, GPIO.BOTH, callback=change, bouncetime=500)


def get_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    records = []

    try:
        log.debug(sql)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        for row in result:
            records.append(list(row))

    except Exception as e:
        log.exception("Fout bij het ophalen van data: {0})".format(e))

    cursor.close()
    conn.close()

    return records


def set_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        log.debug(sql)
        cursor.execute(sql, params)
        conn.commit()
        log.debug("SQL uitgevoerd")

    except Exception as e:
        log.exception("Fout bij uitvoeren van sql: {0})".format(e))
        return False

    cursor.close()
    conn.close()

    return True





@app.route('/index',methods = ['POST', 'GET'])
def index():
    global game, round, game_start
    game_start = 1
    players = []
    game = get_data("SELECT MAX(spelID) FROM spel")
    game = game[0][0] + 1
    round = 0
    if request.method == 'POST':
        result = request.form
    set_data('INSERT INTO project1.spel (Winnaar) VALUES ("T");')

    for key,value in result.items():
        if value != "":

            speler = value.split(' ', 1)
            set_data('INSERT INTO project1.user (Naam, Voornaam) VALUES (%s, %s);', (speler[1], speler[0]))
            userID = get_data('SELECT U.UserID FROM user as U WHERE U.Voornaam = %s;', (speler[0]))
            print(userID)
            print(game)
            set_data('INSERT INTO project1.user_has_spel (User_UserID, Spel_SpelID) VALUES (%s, %s);', (userID[0][0], game))

            players.append(speler[0])

    players_count = len(players)
    return render_template('index.html', result = players)

@app.route('/')
def home():
    global game_start
    game_start = 0
    return render_template('home.html')

@app.route('/Nieuw_Spel')
def nieuw_spel():

    return render_template('Nieuw_Spel.html')

@app.route('/about')
def about():
    global game_start
    game_start = 0
    return render_template('about.html')


@app.route('/winner/<winnaar>')
def winner_db(winnaar):
    global game_start
    game_start = 0
    set_data('UPDATE spel SET spel.Winnaar = %s WHERE spel.Winnaar = "T";', (winnaar))
    return redirect('/winner')

@app.route('/winner')
def winner():
    return render_template("winner.html")

@app.route('/historiek')
def historiek():
    winnaars = []
    winnaars = get_data("SELECT spel.Winnaar, historiek.Datum FROM zet JOIN spel ON spel.spelID = zet.SpelID JOIN historiek ON historiek.SpelID = zet.SpelID ORDER BY historiek.Datum;")

    i = 1
    print(winnaars[i])
    while i-1 < len(winnaars):
        winnaars[i-1].insert(0, i)
        i = i + 1
    return render_template('historiek.html', winnaars = winnaars)

@socketio.on('connect')
def handle_message():
    print("connected")
    test()
    time.sleep(5)
    # socketio.emit('my data',
    #               "test1",
    #               namespace='/test')
    print("ok")

@socketio.on('move')
def handle_my_custom_event(json):
    print('received json: ' + str(json))



def test():
    socketio.emit("my data", 'test', namespace='/test')




def read_inputs():
    MySwitchA = bus.read_byte_data(DEVICE, GPIOA)
    MySwitchB = bus.read_byte_data(DEVICE, GPIOB)
    MySwitchA1 = bus.read_byte_data(DEVICE1, GPIOA)

    MySwitchA = (int(MySwitchA) ^ 0xff)
    MySwitchA = str(bin(MySwitchA))
    MySwitchA = MySwitchA[2:]
    while len(MySwitchA) < 8:
        MySwitchA = "0" + MySwitchA
    MySwitchA = MySwitchA[::-1]

    MySwitchB = (int(MySwitchB) ^ 0xff)
    MySwitchB = str(bin(MySwitchB))
    MySwitchB = MySwitchB[2:]
    while len(MySwitchB) < 8:
        MySwitchB = "0" + MySwitchB

    MySwitchB = MySwitchB[::-1]

    MySwitchA1 = (int(MySwitchA1) ^ 0xff)
    MySwitchA1 = str(bin(MySwitchA1))
    MySwitchA1 = MySwitchA1[2:]
    while len(MySwitchA1) < 8:
        MySwitchA1 = "0" + MySwitchA1

    MySwitchA1 = MySwitchA1[::-1]

    code = MySwitchA + MySwitchB + MySwitchA1
    return code

def get_move(deg):
    move = []
    if (deg < 90):
        move.append("Rechter voet ")
    elif (deg > 90 and deg < 180):
        move.append("Rechter hand ")
        deg = deg-90
    elif (deg > 180 and deg < 270):
        move.append("Linker voet ")
        deg = deg-180
    elif (deg < 360):
        move.append("Linker hand ")
        deg = deg-270

    if (deg < 15):
        move.append("Blauw")
    elif (deg > 15 and deg < 30):
        move.append("Geel")
    elif (deg > 30 and deg < 45):
        move.append("Lucht")
    elif (deg > 45 and deg < 60):
        move.append("Groen")
    elif (deg > 60 and deg < 75):
        move.append("Rood")
    elif (deg < 90):
        move.append("De draaier mag kiezen")

    return move

def printit():
    deg = 0
    codeMEM = 0
    time.sleep(2)
    global round
    while True:
      code = read_inputs()
      # print(rc_time(pin_to_circuit))
      if rc_time(pin_to_circuit) > 50000:
          tijd(22)
      if start == 1 and game_start == 1:
          GPIO.setup(STEP, GPIO.OUT)

          while time.time() < timeout:
              # while(deg < 360):
              for x in range(step_count):
                  GPIO.output(STEP, GPIO.HIGH)
                  time.sleep(delay)
                  GPIO.output(STEP, GPIO.LOW)
                  time.sleep(delay)
                  deg += 1.8
                  # print(deg)
                  if deg > 360:
                      deg = 0
                  if (time.time() > timeout):
                      code = read_inputs()
                      round += 1
                      move = get_move(deg)
                      set_data('INSERT INTO project1.zet (Ronde, SpelID, Kleur, Lichaamsdeel) VALUES (%s, %s, %s, %s);', (round, game, move[1], move[0]))
                      bol = get_data("SELECT MAX(ID) FROM bollen")
                      bol = bol[0][0]
                      teller = 0

                      for i in code:
                          teller = teller + 1
                          bol = bol + 1
                          if i == "1":
                              set_data('INSERT INTO project1.bollen (ID, BolID, Ronde, Status) VALUES (%s, %s, %s, "aan");',(bol, teller, round))
                          elif i == "0":
                              set_data('INSERT INTO project1.bollen (ID, BolID, Ronde, Status) VALUES (%s, %s, %s, "uit");',(bol, teller, round))
                      datum = time.strftime("%Y-%m-%d")
                      historyID = get_data("SELECT MAX(HistoriekID) FROM historiek")
                      historyID = historyID[0][0] + 1
                      set_data('INSERT INTO project1.historiek (Ronde, SpelID, HistoriekID, Datum) VALUES (%s, %s, %s, %s);',(round, game, historyID, datum))
                      socketio.emit('round',
                                    deg,
                                    namespace='/test')
                      time.sleep(2)
                      break

      # print(deg)
      while (deg != 0):

          for x in range(step_count):
              GPIO.output(STEP, GPIO.HIGH)
              time.sleep(delay)
              GPIO.output(STEP, GPIO.LOW)
              time.sleep(delay)
              deg += 1.8
              print(deg)
              if deg > 360:
                  deg = 0
                  break
      if codeMEM != code:

          socketio.emit('my data',
                        code,
                        namespace='/test')
          codeMEM = code
      time.sleep(0.2)

thread_print = Thread(target=printit)
thread_print.start()

if __name__ == '__main__':
    time.sleep(1)
    logging.basicConfig(level=logging.DEBUG)
    log.info("Flask app starting")
    # app.run(host='0.0.0.0', debug=True)
    socketio.run(app, host='0.0.0.0')

    # while True:
    #     MySwitch = bus.read_byte_data(DEVICE1, GPIOA)
    #
    #     if MySwitch == 0:
    #         print("knop op GPA7 ingedrukt")

