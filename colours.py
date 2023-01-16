class color:
    KEY = '\033[1;34;48m'
    SUCCESS = '\033[1;32;48m'
    ERROR = '\033[1;31;48m'
    RESET = '\u001b[0m'

def colorMessage(inputColor, message):
    return f"{inputColor} {message} {color.RESET}"
