#!/usr/bin/env python
"""
nmaps_xml_parsing.py
"""
import xml.dom.minidom
import sys
import getopt
 
# language, output_encoding = locale.getdefaultlocale()
verbose = False
 
def main(argv):
    doc = ""
    try:
        opts, args = getopt.getopt(argv, "hv", ["help", "verbose"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            global verbose
            verbose = True
 
    if len(args) < 1: # Print usage if no arguments are given
        usage()
 
    input_files = args # The remainder of arguments are treated like input files
    for i in input_files:
        try:
            doc = xml.dom.minidom.parse(i)
        except:
            print("[!] Invalid XML, giving up...")
        parse_nmap(doc)
 
def parse_nmap(doc):
    usernames = []
 
    for host in doc.getElementsByTagName("host"):
        ip = name = output = ""
 
        # Get host IPv4 address (and potentially IPv6 and mac as well)
        addresses = host.getElementsByTagName("address")
        for address in addresses:
            ip = address.getAttribute("addr")
 
        # Get host name
        hostnames = host.getElementsByTagName("hostname")
        for hostname in hostnames:
            name = hostname.getAttribute("name")
 
        scripts = host.getElementsByTagName("script")
        for script in scripts:
            output = script.getAttribute("output") #.encode(output_encoding)
            usernames = output.split(',')
 
        if(verbose):
            print("[*] Users harvested from " + ip + " (" + name + "):")
 
        for username in usernames:
            print(username.strip())
 
def usage():
    print("""Usage: ./nmap_parsing.py [OPTIONS] results.xml
 
The input file should be generated using nmap with a similar syntax:
nmap --script=smb-enum-users -oX results.xml 127.0.0.17
 
    -h/--help:       Displays this message
    -v/--verbose:    Verbose mode""")
 
if __name__ == "__main__":
    main(sys.argv[1:])
