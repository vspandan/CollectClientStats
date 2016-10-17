import random, base64
from Crypto.Cipher import AES, ARC2

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

# unpad padded bits
def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

#decrypts AES key which is encrypted with RC2 using key exchanged with Diffie Hellman
def ceaserExtractPlain(key,msg):
    cipher = ARC2.new(str(key), ARC2.MODE_CFB, "12345678")
    return cipher.decrypt(msg)

# performs AES decryption
def decrypt(key,enc):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')