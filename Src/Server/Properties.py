SMTP_EMAIL_ADDR = "spandan.veggalam@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_SENDER_PASSWORD = "123"
SMTP_PORT = 587

SMTP_SUCC_MSG = "Successfully sent email"
SMTP_ERR_MSG = "Error: unable to send email"
AUTH_FAILED_ERR_MSG = "Client authentication failed."
CLIENT_CONN_ERR_MSG ="Issue in Client Connection"
DB_ERR_MSG = "Error in Handling Database"
ERR_PROCESSING_CLI_RESP = "Error in processing response from client"
CONFIG_FILE = "server/config.xml"
CLIENT_SCRIPT_SRC = "Client\ClientScript.py"
CLIENT_SCRIPT_REMOTE_DEST = 'ClientScript.py'
SSH_REMOTE_EXEC_CMD = "python "+CLIENT_SCRIPT_REMOTE_DEST

DB_USER = 'root'
DB_PASSWORD = '123'
DB_HOST = '127.0.0.1'
DB_NAME = 'crossoverproject'
INSERT_QUERY = "INSERT INTO `clientstats` (`username`, `timestamp`, `hostname`, `IPAddress`, `CPUCount`, `CPUUsage`,`MemoryUsage`,`Uptime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"