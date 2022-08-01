import env_lab
import sys
from ncclient import manager
import xmltodict
import xml.dom.minidom
from flask import Flask

app = Flask(__name__) 

def connect():
    return manager.connect(
            host=env_lab.IOS_XE_1["host"],
            port=env_lab.IOS_XE_1["netconf_port"],
            username=env_lab.IOS_XE_1["username"],
            password=env_lab.IOS_XE_1["password"],
            hostkey_verify=False
            )


@app.route('/get')
def get_interfaces():
    netconf_filter = """
    <filter>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface></interface>
        </interfaces>
    </filter>"""

    netconf_reply = connect().get_config(source = 'running', filter = netconf_filter)
    #print(netconf_reply)
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    
    interfaces = netconf_data["interfaces"]["interface"]
    #print("Here is the raw XML data returned from the device.\n")
    #print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
    data="<div><h2>The interface status of the device is: </h2><ul>"
    for interface in interfaces:
        data+=f'<li>Interface {interface["name"]} enabled status is {interface["enabled"]}</li>'
    data += "</ul></div>"
    return data

@app.route('/del/<int:num>')
def delInterface(num):
    new_loopback = {}
    new_loopback["name"] = "Loopback" + str(num)
    netconf_data = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>{new_loopback["name"]}</name>
            </interface>
        </interfaces>
    </config>"""
    netconf_reply = connect().edit_config(netconf_data, target = 'running')
    #print("Here is the raw XML data returned from the device.\n")
    #print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
    data=f"<h1>Interface Number {num} got deleted:</h1>"+get_interfaces()
    return data


@app.route('/add/<int:num>/<string:desc>/<string:ip>/<string:mask>')
def addInterface(num,desc="default",ip="10.10.10.10",mask="255.255.255.0"):
    IETF_INTERFACE_TYPES = {
    "loopback": "ianaift:softwareLoopback",
    "ethernet": "ianaift:ethernetCsmacd"
    }
    new_loopback = {}
    new_loopback["name"] = "Loopback" + str(num)
    new_loopback["desc"] = desc
    new_loopback["type"] = IETF_INTERFACE_TYPES["loopback"]
    new_loopback["status"] = "true"
    new_loopback["ip_address"] = ip
    new_loopback["mask"] = mask
    #print(new_loopback)
    netconf_data = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{new_loopback["name"]}</name>
                <description>{new_loopback["desc"]}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    {new_loopback["type"]}
                </type>
                <enabled>{new_loopback["status"]}</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{new_loopback["ip_address"]}</ip>
                        <netmask>{new_loopback["mask"]}</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>"""

    netconf_reply = connect().edit_config(netconf_data, target = 'running')
    data=f"<h1>Interface Number {num} was created:</h1>"+get_interfaces()
    return data
    
@app.route('/')
def show_options():
    options=[("Show Interfaces","/get"),("Add Interface","/add/num/description/ip/subnet_mask"),("Delete interface","/del/num")]
    data="<div><h1>Welcome, What would you like to do?</h1><ol>"
    for option in options:
        data+=f"<li>{option[0]}: go to ----> {option[1]}</li>"
    data += "</ol></div>"
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
     
