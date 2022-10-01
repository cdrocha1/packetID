import csv

class PacketManager:
    def createPacketDict(packets_file):
        packet_dict = {}
        fieldNames = ['Timestamp', 'Type', 'ID', 'Data']
        with open(packets_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldNames)
            for row in reader:
                print(row)
        return reader

PacketManager.createPacketDict('packets.csv')
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;cf00203;cde0270004b827ff'}
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;18fe592f;ffffffffe37cdd7c'}
