from asyncio.windows_events import NULL
import csv
import cantools
import struct
import json

dbcMessages = []
dbcSignals = []

class PacketManager:
    def createPacketDict(packets_file):
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
        # print(db.decode_message(packetID, packetData))
        #print("")
        #print("")

        #example for 0x18fef1fe, when translated into Decimal 
        # print(db.decode_message(b'\x18\xfe\xf1\xfe' ,b'\xff\xff\xff\xc0\x0c\xff\xff\xff'))

       # print(db.decode_message(419361278 ,b'\xff\xff\xff\xc0\x0c\xff\xff\xff'))

        # try:
        #     db.decode_message(packetID, packetData)
        
        # except:
        #     print("no match found")


        ##print('packet id: '+packetID)
        ##print('packet data: '+ packetData)
        reformatedID = int(packetID, 16)
        # print('reformattedID: ' , reformatedID)
        
   

        reformatedData = b''.join([struct.pack('B', int(''.join(x),16)) for x in zip(packetData[0::2], packetData[1::2])])
        try:
            #example for 0x18fef1fe, when translated into Decimal 
            #  0x18fef1fe(hex) == 419361278(decimal)
            #  0xcf00203 == 217,055,747
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

            #print('No Message found')

        



db = PacketManager.loadDBCFile("C:\\Users\\chris\\OneDrive\\Documents\\SCHOOL\\CAN-Bus Visualizer\\packetID\\CSS-Electronics-SAE-J1939-DEMO.dbc")
# db = PacketManager.loadDBCFile('j1939.dbc')


#PacketManager.translatePackets(id, data, db)
packetCSV = PacketManager.createPacketDict('packets.csv')
packetCSV.pop(0)   #removes first line 
print("")
packetList = {}
i = 0
for x in packetCSV:
    id = (x['ID'])
    data = (x['Data'])
    packetInfo = PacketManager.translatePackets(id, data, db)
    if(packetInfo):
        #print(packetInfo)
        packetList[i] = (packetInfo)
        i+=1
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;cf00203;cde0270004b827ff'}
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;18fe592f;ffffffffe37cdd7c'}
print(json.dumps(packetList, indent =4 ))

