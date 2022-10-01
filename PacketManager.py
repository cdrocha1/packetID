import csv

class PacketManager:
    def createPacketDict(packets_file):
        packet_dict = {}
        
        with open(packets_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
        return reader

PacketManager.createPacketDict('packets.csv')
# {'Timestamp;Type;ID;Data': '11T082557132;1;cf00203;cde0270004b827ff'}
