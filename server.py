from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import csv
import cantools
import struct
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
    return redirect(url_for('index'))

#run on localhost with directory as file var 
#ex: http://localhost:5000/insert?file=C:\\Users\\chris\\OneDrive\\Documents\\SCHOOL\\CAN-Bus Visualizer\\packetID\\packets.csv
@app.route("/insert")
def insert():
    file = request.args.get('file')
    db = loadDBCFile('CSS-Electronics-SAE-J1939-DEMO.dbc')
    #user enters filename
    packetCSV = createPacketDict(file)
    packetCSV.pop(0)
    packetList = {}
    i = 0
    for x in packetCSV:
        id = (x['ID'])
        data = (x['Data'])
        packetInfo = translatePackets(id, data, db)
        if(packetInfo):
            #print(packetInfo)
            packetList[i] = (packetInfo)
            i+=1
    
    return json.dumps(packetList, indent=4)


def createPacketDict(packets_file):
        packet_dict = {}
        packets = []
        fieldNames = ['Timestamp', 'Type', 'ID', 'Data']
        with open(packets_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldNames, delimiter=';')
            i = 0
            for row in reader:
                packets.append(row)
        # print(packets)
        return packets

def loadDBCFile(filename):
    print("DBC loading")
    db = cantools.database.load_file(filename)
    i = 0
    for x in db.messages:
        print("")
        print("Message ",i,": ", x)
        print("Signals ",i,": ", x.signals)
        i+=1
    return db

def translatePackets(packetID, packetData, db):
    print('packet id: '+packetID)
    print('packet data: '+ packetData)
    reformatedID = int(packetID, 16)
    reformatedData = b''.join([struct.pack('B', int(''.join(x),16)) for x in zip(packetData[0::2], packetData[1::2])])
    try:

        decoded_message = db.decode_message(reformatedID, reformatedData)
        print(decoded_message)
        print("")
        packetJson = {
            "packet_id": packetID,
            "packet_data": packetData,
            "decoded_message": decoded_message,
            "decoded_id": reformatedID,
        }
        return packetJson
    except:
        pass

if __name__ == "__main__":
    app.run(debug=True)
    #run app, located at localhost:5000


