# Standard CAN frame
# [1] [11] [1]   [6]    [0-64]  [16] [2] [7]
# SOF  ID  RTR  Control  Data   CRC  ACK EOF
# SOF: The Start of Frame is a 'dominant 0' to tell the other nodes that a CAN node intends to talk
# ID: The ID is the frame identifier - lower values have higher priority
# Control: The Control contains the Identifier Extension Bit (IDE) which is a 'dominant 0' for 11-bit. It also contains the 4 bit Data Length Code (DLC) that specifies the length of the data bytes to be transmitted (0 to 8 bytes)
# Data: The Data contains the data bytes aka payload, which includes CAN signals that can be extracted and decoded for information
# CRC: The Cyclic Redundancy Check is used to ensure data integrity
# ACK: The ACK slot indicates if the node has acknowledged and received the data correctly
# EOF: The EOF marks the end of the CAN frame
from pprint import pprint

import cantools
import can

db = cantools.database.load_file('CSS-Electronics-SAE-J1939-DEMO.dbc')
print(db.messages)

example_message = db.get_message_by_name('EEC1')
print('em signals: ', example_message.signals)
print('em id:', example_message.frame_id)


packetDict = {}
source_list = []

f = open("packets.txt", "r")
f.readline()

#create packet dictionary{key = indicator, value = data}
for x in f:
    newline = (x.split(";"))
    packetDict[newline[2]] = newline[-1]

#decode source of indicators (assume first 2 values of string indicate region)
for key in packetDict.keys():
    source = key[:2]
    source_list.append(source)

#function to find each unique source in source_list
def name_list(source_list):
    unique_sources = []
    for source in source_list:
        if source not in unique_sources:
            unique_sources.append(source)
    return unique_sources

def print_nodes(node_id, packet_dictionary):
    for key in packet_dictionary.keys():
        if node_id == str(key[:2]):
            print(key)
            print(packet_dictionary.get(key))


#terminal interface
interface = 1

sources = name_list(source_list)
print('Select what node you would like to access: ', sources)
responce = raw_input()
print('You Selected: ', responce)
print_nodes(responce, packetDict)


    





