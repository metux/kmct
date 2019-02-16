from config import Config
from generator import Generator

def getTarget(confdir, name):
    return Generator(Config(confdir, "target/"+name))
