#!/usr/bin/env python
'''
THIS SCRIPT CHANGES YOUR MAC ADDRESS
##### --- example usage:
macchanger.py --i <interface_name> --m <new MAC>
or
macchanger.py --interface <interface_name> --mac <new MAC>
#######

#depends on ifconfig so it should be installed
#references
Zsecurity, python docs, stackoverflow etc
feel free to edit and reuse
'''
import subprocess
import argparse
import re
#optparse was depricated 
#linuxconfig.org
# run using python3

#this function gets commandline arguments using argparse
def get_arguments():
    parser = argparse.ArgumentParser(description="This tools helps change your MAC address")
    parser.add_argument("-i", "--interface", dest="interface", help="interface to change MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    options = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify the new mac, use --help for more info. ")
    return options

#this function changes your MAC address
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " +interface + " to " +new_mac)
    
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

#this function gets your current MAC address using regex and re
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    regex = re.compile(b'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', re.I)
    mac_result= regex.search(ifconfig_result)

    if mac_result:
        #return mac_result.group(0)
        new_mac_result = str(mac_result.group(0), 'utf-8')
        return new_mac_result
    else:
        print("[-] Could not read MAC Address.")

#creates an object options to get variables stored in argparse in get arguments function    
options = get_arguments()

current_mac = get_current_mac(options.interface)

#converts current MAC which was stored in byte string to string
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not change.")
