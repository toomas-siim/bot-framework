from pynput import mouse
import imp
engine = imp.load_source('engine', './engine/engine.py')

engine = engine.Engine()
engine.start()
