from Server.FetchClients import getClientInfo
from Server.ConnectClients import connectClient
from threading import Thread
from Server.DBConnection import insertClientStats
from Server.MailNotifier import sendMail
import xml.etree.ElementTree as etree
from Server.Properties import ERR_PROCESSING_CLI_RESP

#processes the xml response received from client
def processResponse(response):
    root=etree.fromstring(response)
    data={}
    if root.tag == "client":
        data['username']=client['username']
        for child in root:
            if child.tag == "timestamp":
                data["timestamp"]=child.text
                continue
            if child.tag == "hostname":
                data["hostname"]=child.text
                continue
            if child.tag == "IP_Address":
                data["IPAddress"]=child.text
                continue
            if child.tag == "Statistics":
                for ch in child:
                    if ch.tag == "CPU_Count":
                        data["CPUCount"]=ch.text
                        continue
                    if ch.tag == "CPU":
                        for chld in ch:
                            if chld.tag == "idle":
                                    data["CPUUsage"]=str(100-float(chld.text))
                        continue
                    if ch.tag == "Memory":
                        for chld in ch:
                            if chld.tag == "PercentageUsed":
                                    data["MemoryUsage"]=chld.text
                        continue
                    if ch.tag == "UpTime":
                        data["Uptime"]=ch.text
                        continue
        return data

#Thread function, that connects to client and processes the response.
def runThread(client):
    try:
        response = connectClient(client["ip"], int(client["port"]), client["username"], client["password"])
        if response is None:
            return
        data=processResponse(response)
        insertClientStats(data)
        if float(data['MemoryUsage']) > float(client['limits']['memory'][:-1]) or float(data['CPUUsage']) > float(client['limits']['cpu'][:-1]):
            print("Sending alert notification")
            receivers = [client['mail']]
            message = "From: " + client['mail'] + "\nTo: " + client['username'] +" <" + client['mail'] + "> \nSubject: Memory/CPU usage limit exceeded \n\nMemory Usage: " + data['MemoryUsage'] + "%\nCPU Usage: " +  data['CPUUsage'] + "%\n"
            sendMail(receivers, message)
    except Exception as e:
        print(ERR_PROCESSING_CLI_RESP,e);


#start point of server script
if __name__ == '__main__':
    #fetch clients
    clients=getClientInfo()
    for client in clients:
        #create a thread for each client and run
        t=Thread(target=runThread,kwargs={"client": client})
        t.setName(client["ip"])
        t.start()
        t.join(10)