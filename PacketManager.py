from asyncio.windows_events import NULL
import csv
from tkinter import Pack
import cantools
import numpy as np

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
                print(row)
                packets.append(row)
        print(packets)
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
        print("")
        print("")
        print(db.decode_message(2170562561 ,b'\xff\xff\xff\xc0\x0c\xff\xff\xff'))

        # try:
        #     db.decode_message(packetID, packetData)
        
        # except:
        #     print("no match found")
        
        # try:
        #     print(db.decode_message(packetID, packetData))
        # except:
        #     print('No Message found')

        


packetCSV = PacketManager.createPacketDict('packets1.csv')
packetCSV.pop(0)   #removes first line 

db = PacketManager.loadDBCFile('CSS-Electronics-SAE-J1939-DEMO.dbc')
# PacketManager.translatePackets(db.messages.frame_id, )

for x in packetCSV:
    #print(x)
    id = (x['ID'])
    data = (x['Data'])
    PacketManager.translatePackets(id, data, db)

# out : {'Timestamp;Type;ID;Data': '11T082557132;1;cf00203;cde0270004b827ff'}
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;18fe592f;ffffffffe37cdd7c'}
