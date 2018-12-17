#!/usr/bin/env python3
import subprocess
import optparse
import re
def get_arguments():
    parser = optparse.OptionParser(add_help_option=False)
    parser.add_option("-h", "--help", action="help")
    parser.add_option("-i", "--int", dest="interface", help="Connection interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="Set this mac address")
    #Returns options like -m or -i and arguments
    #like the interface name and mac address
    options, arguments = parser.parse_args()
    #Verification if it contains -m or -i
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info!")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac address, use --help for more info!")
    #Return the options like -m or -i
    return options
def change_mac(interface, new_mac):
    print("[+] Changing your current mac address " + interface + " for " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_result:
            return mac_result.group(0)
        else:
            print("[-] Could not read Mac Address")
            quit()
    except:
        print("Not able to get the current MAC address on this interface")
        quit()

#Set the return value of get_arguments function to the variable options
options = get_arguments()
#Launch the function to get the current mac address ifconfig options.interface (eth0)
old_current_mac = get_current_mac(options.interface)
print("Your current MAC address is " + str(old_current_mac))
#Launch the function with interface name and new mac address
change_mac(options.interface, options.new_mac)
#Verification if the mac address has been changed
new_current_mac = get_current_mac(options.interface)
if old_current_mac != new_current_mac:
    print("Your MAC address was successfully changed!")
else:
    print("Your MAC address wasn't successfully changed!")
