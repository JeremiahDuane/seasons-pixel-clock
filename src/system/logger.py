from curses import nonl
from datetime import datetime
from system.config import package
from system.colors import colors

debug = 0
def debugger():        
    global debug
    debug+=1
    print(debug)

def boot():
    appendToLog(colors.fg.blue, "BOOT: Startup sequence...", "")

def logger(message="", error=""):
    fg = "" if error == "" else colors.fg.red
    appendToLog(fg, message, error)

def appendToLog(fg, message, error):
    def log(newLine):
        global debug
        global package
        nonlocal fg
        nonlocal message
        nonlocal error

        return [
            f'{fg}',
            f'----------------------------------------------------------|{str(datetime.now())}|     {newLine}',
            f'    Log#: {debug}                                                                     {newLine}',
            f'    Message: {message}                                                                {newLine}' if message != "" else "",
            f'    Error: {error}                                                                    {newLine}' if error   != "" else "",
            f'----------------------------------------------------------|{package["version"]}|      {newLine}'
        ]

    with open("/home/jgage/code/seasons-pixel-clock/src/system/log.txt", "a") as file:
        file.writelines(log('\n'))
        file.close

    for line in log('\n'):
        print(line)
    
    print(colors.reset)