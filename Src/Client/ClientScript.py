import psutil, time, datetime, sys, random, socket, base64, hashlib
import xml.etree.ElementTree as etree
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import ARC2

bs=32

# Diffie Hellman Key Generator
class DHKeyGenerator(object):
    def __init__(self):
        self.prime = 17
        self.root = 3
        self.secretKey = self.secretnumber()
    
    # selects a random number as secret key
    def secretnumber (self):
        secret = int(random.randint(0,100))
        return secret
    
    # generates public key
    def getPublicKey (self):
        publicKey = (self.root ** self.secretKey) % self.prime
        return publicKey

    #with public key of other party generates shared key
    def sharedKeyGen(self,senderPubKey):
        return (senderPubKey ** self.secretKey) % self.prime

# performs AES encryption on the message
def encrypt(key,msg):
    raw = _pad(msg)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

# generates pad bits
def _pad(s):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

#encrypts AES key with RC2 using key exchanged by Diffie Hellman
def ceaserGenCipher(key,msg):
    cipher = ARC2.new(str(key), ARC2.MODE_CFB, "12345678")
    return cipher.encrypt(msg)

"""
collects system stats and generates xml
xml is encrypted using AES 
AES key is encrypted using RC2
"""
def collectSystemStats(d,key,sk,pk):
    e=etree.Element("client")
    e1=etree.SubElement(e,"timestamp")
    e1.text=str(datetime.datetime.now())
    e2=etree.SubElement(e,"hostname")
    e2.text=socket.gethostname()
    e3=etree.SubElement(e,"IP_Address")
    e3.text=str(socket.gethostbyname(socket.gethostname()))
    e4=etree.SubElement(e,"Statistics")
    
    all_cpu_usage=psutil.cpu_times_percent(interval=0.4, percpu=False)
    e6=etree.SubElement(e4,"CPU")
    c=etree.SubElement(e6,"UserUsage")
    c.text=str(all_cpu_usage.user)
    c=etree.SubElement(e6,"SystemUsage")
    c.text=str(all_cpu_usage.system)
    c=etree.SubElement(e6,"idle")
    c.text=str(all_cpu_usage.idle)
    
    e5=etree.SubElement(e4,"Indvidual_CPU")
    e6=etree.SubElement(e4,"CPU_Count")
    cpu_count=str(psutil.cpu_count())
    e6.text=cpu_count;
    
    all_cpu_usage=psutil.cpu_times_percent(interval=0.4, percpu=True)
    i=1
    for cpu_usage in all_cpu_usage:
        e6=etree.SubElement(e5,"CPU_Usage")
        c=etree.SubElement(e6,"CPU")
        c.text=str(i)
        i=i+1
        c=etree.SubElement(e6,"UserUsage")
        c.text=str(cpu_usage.user)
        c=etree.SubElement(e6,"SystemUsage")
        c.text=str(cpu_usage.system)
        c=etree.SubElement(e6,"idle")
        c.text=str(cpu_usage.idle)
    
    memory=psutil.virtual_memory()
    e5=etree.SubElement(e4,"Memory")
    m=etree.SubElement(e5,"Total")
    m.text=str(memory.total)
    m=etree.SubElement(e5,"PercentageUsed")
    m.text=str(memory.percent)
    m=etree.SubElement(e5,"Used")
    m.text=str(memory.used)
    m=etree.SubElement(e5,"Free")
    m.text=str(memory.free)
    
    memory=psutil.swap_memory()
    e5=etree.SubElement(e4,"Swap")
    s=etree.SubElement(e5,"Total")
    s.text=str(memory.total)
    s=etree.SubElement(e5,"PercentageUsed")
    s.text=str(memory.percent)
    s=etree.SubElement(e5,"Used")
    s.text=str(memory.used)
    s=etree.SubElement(e5,"Free")
    s.text=str(memory.free)
    
    uptime = time.time() - psutil.boot_time()
    e5=etree.SubElement(e4,"UpTime")
    e5.text = str(datetime.timedelta(uptime/1000000))
    xml=etree.tostring(e)
    
    output={}
    output["enckey"]=ceaserGenCipher(sk,key)
    output["pubkey"]=pk
    output["resp"]=encrypt(key, xml)
    print(output)


#Start point of client script execution
if __name__ == '__main__':
    args=sys.argv[1:]

    if len(args) == 2 and args[0] == "-publicKey":
        d=DHKeyGenerator()
        pk=d.getPublicKey()
        sk=d.sharedKeyGen(int(args[1]))
        random_key = "this is a random passphrase"
        key = hashlib.sha256(random_key.encode()).digest()
        collectSystemStats(d,key,sk,pk)