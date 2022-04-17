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




# db.decode_message(int(message[2], 16), bytes.fromhex(message[3]))
packetDict = {}
f = open("packets.txt", "r")
f.readline()
for x in f:
    newline = (x.split(";"))
    print(newline)

    packetDict[newline[2]] = newline[-1]

i = 0
for key in packetDict.keys():
    print(i, ': ', key)
    i+=1
