#!/usr/bin/env python

import scapy.all as scapy
import argparse
'''
def scan(ip):
    scapy.arping(ip)

scan("192.168.88.1/24")
update scapy to recent version to accept ip range :
pip3 install --upgrade git+git://github.com/secdev/scapy
ref stackoverflow
    #list functions available on a class
    #scapy.ls(scapy.ARP())
    #print(arp_request.summary())
    #arp_request.show()

'''
def get_target():
    parser = argparse.ArgumentParser(description="Welcome to Arp network scanner type --h for help")
    parser.add_argument("-i","--ip", dest="target", help="specify the target IP in format *.*.*.*/subnet")
    option = parser.parse_args()
    if not option.target:
        parser.error("[!] Please enter the target, use --h for help")
    return option

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast/arp_request
    answered_req = scapy.srp(arp_broadcast, timeout=10, verbose=True)[0]
    client_list = []

    for n in  answered_req:
        client_dict ={"ip":n[1].psrc, "mac":n[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_requests(result_list):
    print("__________________________________________")
    print("IP\t\t MAC Address\n------------------------------------------")
    
    for n in result_list:
        print(n["ip"]+ "\t\t" + n["mac"])
        print("------------------------------------------")    

option = get_target()
scan_result = scan(option.target)
print_requests(scan_result)
    


