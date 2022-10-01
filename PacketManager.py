import csv

class PacketManager:
    def createPacketDict(packets_file):
        packet_dict = {}
        packets = []
        fieldNames = ['Timestamp', 'Type', 'ID', 'Data']
        with open(packets_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldNames, delimiter=';')
            i = 0
            for row in reader:
                packets.append(row)

        return packets

packetCSV = PacketManager.createPacketDict('packets1.csv')

for x in packetCSV:
    print(x)
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;cf00203;cde0270004b827ff'}
# out : {'Timestamp;Type;ID;Data': '11T082557132;1;18fe592f;ffffffffe37cdd7c'}
