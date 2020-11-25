from pynput import mouse
import imp
import os

basePath = os.path.dirname(os.path.realpath(__file__))
engine = imp.load_source('engine', basePath + '/engine/engine.py').Engine()

print("test")
engine.start()
