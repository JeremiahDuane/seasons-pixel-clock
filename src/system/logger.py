from datetime import datetime

def log(error):
    log = open("log.txt", "w")
    log.writelines(["-" * 10 + "\n", str(datetime.now()) + "\n", str(error) + "\n", "-" * 10 + "\n"])
    log.close()