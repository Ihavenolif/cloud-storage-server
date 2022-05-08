from datetime import date
from sys import argv

class Log:
    date = ""
    time = ""
    messageType = ""
    IP = ""
    message = ""
    resCode = ""

def read_file(soubor):
    file = open(soubor,encoding="utf-8")
    return file.read()

if len(argv) < 3:
    print("Usage: python3 app.py <log_file> <result_file_name>.")
    exit()

rawString = read_file(argv[1])

listParsed = rawString.split("\n")

results = {}
for x in listParsed:
    log = Log()
    data = x.split(" ")
    log.date = data[0]
    log.time = data[1]
    log.messageType = data[2]
    if not data[3] == "":
        log.message = x[len(data[0]) + len(data[1]) + len(data[2]) + 2:]
        print("DATA:" + log.message)
        continue