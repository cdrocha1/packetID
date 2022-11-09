from asyncio.windows_events import NULL
import csv
import cantools
import struct
import json

dbcMessages = []
dbcSignals = []

class PacketManager:
    def createPacketDict(packets_file):
        if(packets_file.endswith('.csv')):
            packet_dict = {}
            packets = []
            fieldNames = ['Timestamp', 'Type', 'ID', 'Data']
            with open(packets_file, newline='\n') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=fieldNames, delimiter=';')
                i = 0
                for row in reader:
                    #print(row)
                    packets.append(row)
            #print(packets)
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

        reformatedID = int(packetID, 16)
        reformatedData = b''.join([struct.pack('B', int(''.join(x),16)) for x in zip(packetData[0::2], packetData[1::2])])
        try:
            #example for 0x18fef1fe, when translated into Decimal 
            #  0x18fef1fe(hex) == 419361278(decimal)
            #  0xcf00203 == 217,055,747
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
            pass

            #print('No Message found')

        



db, nodeList = PacketManager.loadDBCFile("C:\\Users\\chris\\OneDrive\\Documents\\SCHOOL\\CAN-Bus Visualizer\\packetID\\CSS-Electronics-SAE-J1939-DEMO.dbc")
# db = PacketManager.loadDBCFile('j1939.dbc')
# db, nodeList = PacketManager.loadDBCFile('practiceDBC.dbc')

print(json.dumps(nodeList, indent=4))
#PacketManager.translatePackets(id, data, db)
packetCSV = PacketManager.createPacketDict('packets1.csv')
packetCSV.pop(0)   #removes first line 
print("")
packetList = {}
i = 0
for x in packetCSV:
    id = (x['ID'])
    data = (x['Data'])
    timestamp = (x['Timestamp'])
    packetInfo = PacketManager.translatePackets(id, data, timestamp, db)
    if(packetInfo):
        #print(packetInfo)
        packetList[i] = (packetInfo)
        i+=1
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;cf00203;cde0270004b827ff'}
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;18fe592f;ffffffffe37cdd7c'}
print(json.dumps(packetList, indent =4 ))

