from sploitkit import *
from scapy.all import *
import time

class uds_read_data_by_id(Module):
    """ This module sends UDS Read Data By Identifier requests.

    Author:  superuserx
    Version: 0.1
    """
    config = Config({
        Option(
            'INTERFACE',
            "CAN interface",
            True,
        ): str("vcan0"),
        Option(
            'SID',
            "Sending ID (Default: 0x7DF)",
            True,
        ): 0x7DF,
        Option(
            'RID',
            "Receiving ID (Default: 0x7D8)",
            True,
        ): 0x7D8,
    })

    def __init__(self):
        load_contrib('isotp')
        load_contrib('automotive.uds')

    def run(self):
        dev = ISOTPNativeSocket(self.config.option('INTERFACE').value, tx_id=self.config.option('SID').value, rx_id=self.config.option('RID').value, basecls=UDS)

        for i in range (0xffff+1):
            packet = UDS()/UDS_RDBI(identifiers=i)
            print("[*] Reading identifier >> " + hex(i))
            recv = dev.sr1(packet, timeout=1, verbose=False)
            if recv and recv.service == 0x62:
                print(recv.load)
            time.sleep(0.1)
        pass
