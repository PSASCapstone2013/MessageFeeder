MessageFeeder
=============

This program opens a binary file containing non-delimited messages, packs them into UDP data blocks and sends them to the localhost.

Run it using command:
  python feeder.py

  
Usage: feeder.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        log file containing messages to be retransmitted
  -d, --debug           display debug messages
  -n INTERVAL, --interval=INTERVAL
                        time interval in seconds between sent packets
  -m MSGS_PER_PACKET, --mpp=MSGS_PER_PACKET
                        messages per packet to be sent
  -p PORT, --port=PORT  destination port number
  -i IP, --ip=IP        destination IP address
