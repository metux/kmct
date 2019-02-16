
from sys import stderr

def info(text):
    stderr.write("[INFO]  %s\n" % text)

def err(text):
    stderr.write("[ERROR] %s\n" % text)
