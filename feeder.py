# Author: Bogdan Kovch
# Date:   August 14, 2013

# This program opens a binry log file containing messages dumped back-to-back. 
# These messages are packed into UDP packet data which is then sent into the
# network.

import dpkt # not a standard python library; download and install it manually
            # URL: http://code.google.com/p/dpkt/downloads/list
import time
import sys
import os
import socket
import struct
from optparse import OptionParser # for parsing command-line arguments
from dpkt.ethernet import Ethernet

LEN_MSG_ID = 4      # message id length in bytes
LEN_MSG_HEADER = 8  # message header length in bytes
packet_header = struct.Struct('!L')

# messages identifiers and their data length in bytes
msgs = {'GPS1':    52,
        'GPS\x01': 52,
        'ADIS':    24,
        'ROLL':    3,}

def main():
    """ program skeleton """
    global sock
    parse_args()
    display_options()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    read_and_feed()
    terminate()
    
def parse_args():
    """ parse command-line arguments into program options """
    global opts
    # Parse command-line arguments
    parser = OptionParser()
    parser.add_option(
        "-f", "--file", action="store", type="string", dest="filename",
        help="log file containing messages to be retransmitted",
        default="crescent-gps-av3.log")
    parser.add_option(
        "-d", "--debug", action="store_true", dest="debug",
        help="display debug messages",
        default=False)
    parser.add_option(
        "-n", "--interval", action="store", type="float", dest="interval",
        help="time interval in seconds between sent packets",
        default=0.1)
    parser.add_option(
        "-m", "--mpp", action="store", type="int", dest="msgs_per_packet",
        help="messages per packet to be sent",
        default=1)
    parser.add_option(
        "-p", "--port", action="store", type="int", dest="port",
        help="destination port number",
        default=35001)
    parser.add_option(
        "-i", "--ip", action="store", type="string", dest="ip",
        help="destination IP address",
        default=socket.gethostbyname(socket.gethostname()))
        # default: local IP address (ex.: 192.168.1.112)
    (opts, args) = parser.parse_args()

def display_options():
    """ display current program options """
    print "Options:"
    print "  filename:    ", opts.filename
    print "  debug:       ", opts.debug
    print "  IP address:  ", opts.ip
    print "  port:        ", opts.port
    print "  interval:    ", opts.interval, "seconds"
    print "  msgs/packet: ", opts.msgs_per_packet
    
def read_and_feed():
    """ read messages from the file, compile them into packet data and send """
    file = open(opts.filename, 'rb')
    eof = False
    while not eof:
        header = packet_header.pack(stats.pkts_sent)
        data = ''
        for i in range(0, opts.msgs_per_packet):
            msg_id, msg_data_len = read_msg_id(file)
            if msg_id == '':
                eof = True
                break
            file.seek(-LEN_MSG_ID, 1) # step back to position before message id
            msg_data = read_msg(file, msg_data_len)
            if msg_data == None:
                eof = True
                break
            stats.msgs_read += 1
            #print stats.msgs_read, msg_id, msg_data_len, len(msg_data)
            data += msg_data
        if data <> '':
            send(header + data)
            time.sleep(opts.interval)
        
def read_msg_id(file):
    """ read message identifier and get its data field length """
    msg_id = file.read(LEN_MSG_ID)
    if msg_id == '': # EOF
        return msg_id, -1
    try:
        msg_len = msgs[msg_id]
    except KeyError:
        print "Error: unsupported message id '" + msg_id + "'"
        exit()
    return msg_id, msg_len
        
def read_msg(file, data_len):
    """ read the entire message including id, header and data """
    msg_len = LEN_MSG_ID + LEN_MSG_HEADER + data_len
    return file.read(msg_len)
        
def terminate():
    """ display statistics and exit """
    print "tatal messages read:", stats.msgs_read
    print "tatal packets sent: ", stats.pkts_sent
    exit()
    
def stats():
    """ statistics data object """
    msgs_read = 0
    pkts_sent = 0
stats.msgs_read = 0
stats.pkts_sent = 0

def send(data):
    """ send compiled data through the socket """
    data_len = len(data)
    # print data_len
    stats.pkts_sent += 1
    sock.sendto(data, (opts.ip, opts.port))
            
if __name__ == "__main__":
    main()