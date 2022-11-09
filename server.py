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
    
    db, nodeList = loadDBCFile("C:\\Users\\chris\\OneDrive\\Documents\\SCHOOL\\CAN-Bus Visualizer\\packetID\\CSS-Electronics-SAE-J1939-DEMO.dbc")
    # db = PacketManager.loadDBCFile('j1939.dbc')
    # db, nodeList = loadDBCFile('practiceDBC.dbc')
    #^^other DBC files, uncomment to use#

    print(json.dumps(nodeList, indent=4))
    packetCSV = createPacketDict('D:\\SCHOOL D\\packetID\\packets1.csv')
    packetCSV.pop(0)   #removes first line 
    print("")
    packetList = {}
    i = 0
    for x in packetCSV:
        id = (x['ID'])
        data = (x['Data'])
        timestamp = (x['Timestamp'])
        packetInfo = translatePackets(id, data, timestamp, db)
        if(packetInfo):
            packetList[i] = (packetInfo)
            i+=1
    return (json.dumps(packetList, indent =4 ))

def createPacketDict(packets_file):
        if(packets_file.endswith('.csv')):
            packet_dict = {}
            packets = []
            fieldNames = ['Timestamp', 'Type', 'ID', 'Data']
            with open(packets_file, newline='\n') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=fieldNames, delimiter=';')
                i = 0
                for row in reader:
                    print(row)
                    packets.append(row)
            return packets
        elif(packets_file.endswith('.log')):
            packet_dict = {}

def loadDBCFile(filename):
        print("DBC loading")
        db = cantools.database.load_file(filename)
        i = 0
        nodeList = {}
        for x in db.messages:
            print("")
            print("Message ",i,": ", x)
            print("Signals ",i,": ", x.signals)
            
            splitMessage = str(x).split(",")
            print("split messages: ", splitMessage)
        
            annotation = splitMessage[0].split("'")[1::2]
            annotation = str(annotation).strip("[']")
            nodeName = splitMessage[4].split("'")[1::2]
            nodeName = str(nodeName).strip("[']")
            nodeID = splitMessage[1][1:]
            node = {
                "Node_Name": nodeName,
                "Project_ID": '1.1.0',
                "Node_ID": nodeID,
                "Annotation": annotation,
                "Icon_Path": "",
                "xyPosition": ""
            }
            nodeList[i] = node
            i+=1
        return db, nodeList

def translatePackets(packetID, packetData, timestamp, db):
        print("packet ID: ", packetID)
        reformatedID = int(packetID, 16)
        reformatedData = b''.join([struct.pack('B', int(''.join(x),16)) for x in zip(packetData[0::2], packetData[1::2])])
        try:
            #example for 0x18fef1fe, when translated into Decimal 
            #  0x18fef1fe(hex) == 419361278(decimal)
            #  0xcf00203 == 217,055,747
            #print(reformatedData)
            decoded_message = db.decode_message(reformatedID, reformatedData)
            print(decoded_message)
            print("")
            canID = ''
            if("STATUS" in decoded_message):
                canID = '0x190'
            
            if("CMD" in decoded_message):
                canID = '0x65'
            
            if("SENSOR" in decoded_message):
                canID = '0xc8'
            
            if("IO" in decoded_message):
                canID = '0x1f4'
            
            if("HEARTBEAT" in decoded_message):
                canID = '0x64'
            if("Engine" in decoded_message):
                canID = '0Xcf004fe'
            if("Wheel" in decoded_message):
                canID = '0Xcf004fe'
            # endFrame = timestamp+=1

            packetJ = {
                "PacketID": packetID, 
                "NodeID": "1",
                "Frame_Start": timestamp,
                "CAN_ID" : canID,
                "Control_Field": "1",
                "Data_Field": decoded_message, 
                "CRC_Field": "",
                "ACK": "1",
                "Frame_End": timestamp,
            }

            packetJson = {
                "timestamp": timestamp,
                "packet_id": packetID,
                "packet_data": packetData,
                "decoded_message": decoded_message,
                "decoded_id": reformatedID,
            }
            return packetJ
        except:
            print("not found in dbc")
            pass




if __name__ == "__main__":
    app.run(debug=True)
    #run app, located at localhost:5000


