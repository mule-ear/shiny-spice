import serial, time, sqlite3 #for pySerial

ser = serial.Serial('/dev/ttyUSB2', 115200) #open serial port
print ('serial port = ' + ser.name) #print the port used

def convert2nums(aList):
    ln=[]
    del aList[0]
    for i in aList:
        ln.append(float(i.split('\\r')[0]))

    return ln

#while (True):
#    if (ser.in_waiting>0):
#        ser.read(ser.in_waiting)
#
#    else:
#        print ("Waiting ")

sqCon = sqlite3.Connection(database='voltages.db')
sqCon.isolation_level = None #Added for autocommit
cur = sqCon.cursor()

cur.execute("DROP TABLE IF EXISTS volts;")
cur.execute("CREATE TABLE volts (id INTEGER PRIMARY KEY AUTOINCREMENT, sensor int, time datetime, bus float, shunt float, current float);")

while (True):
    if (ser.inWaiting() > 0):
        l = ''
        ln = []
        x = str(ser.read(ser.inWaiting()))
        #print (x , len(x), type(x))
        if type(x) is str:
            l = x.split(':')
        else:
            print(x, type(x))
        if len(l) ==4:
            ln = convert2nums(l)

            for i in ln:
                print(i)
            cur.execute("INSERT INTO volts(sensor, time, bus, shunt, current) VALUES(1,datetime('now'),?,?,?);",ln )

    else:
        pass
        #print("Waiting")


