import paramiko, ast
from Server.Properties import CLIENT_SCRIPT_SRC, CLIENT_SCRIPT_REMOTE_DEST, SSH_REMOTE_EXEC_CMD, AUTH_FAILED_ERR_MSG,\
    CLIENT_CONN_ERR_MSG
from Server.DHKeyGenerator import decrypt, DHKeyGenerator, ceaserExtractPlain

"""
establishes ssh connection to client
transfers client script and executes remotely
receives encrypted response and decrypts it
"""
def connectClient(ipaddr,SMTP_PORT,uname,pword):
    try:
        s = paramiko.SSHClient()
        d=DHKeyGenerator()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ipaddr,SMTP_PORT,username=uname,password=pword,timeout=4)
        sftp = s.open_sftp()
        sftp.put(CLIENT_SCRIPT_SRC, CLIENT_SCRIPT_REMOTE_DEST)
        pk=d.getPublicKey()
        stdin, stdout, stderr = s.exec_command(SSH_REMOTE_EXEC_CMD + " -publicKey "+ str(pk))
        stdin.close()
        stderr.close()
        output=ast.literal_eval(stdout.read())
        sk=d.sharedKeyGen(output["pubkey"])
        key=ceaserExtractPlain(sk,output["enckey"])
        return decrypt(key,output["resp"])
    except paramiko.AuthenticationException as e:
        print(ipaddr + ":" + AUTH_FAILED_ERR_MSG, e)
    except Exception as e:
        print(CLIENT_CONN_ERR_MSG, e)
    return None