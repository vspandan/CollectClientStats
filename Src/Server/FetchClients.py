import xml.etree.ElementTree as etree
from Server.Properties import CONFIG_FILE

#assume config.xml has fixed structure and extracts client information
def getClientInfo():
    clients=[]
    root=etree.parse(CONFIG_FILE).getroot();
    if root.tag == "clients":
        for child in root:
            if child.tag == "client":
                limits={}
                for ch in child:
                    if ch.tag == "alert":
                        limits[ch.attrib['type']]=ch.attrib['limit']
                attributes=child.attrib
                attributes["limits"]=limits
                clients.append(attributes)
    return clients