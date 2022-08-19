from datetime import datetime

def log(error):
    print("here")
    print(error)
    log = open("log.txt", "w")
    log.write("-" * 10 + "\n")
    log.write(str(datetime.now()) + "\n")
    log.write(str(error) + "\n")
    log.write("-" * 10 + "\n")
    log.close()