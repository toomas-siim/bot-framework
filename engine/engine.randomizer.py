import time
import random

# Class RandomizerEngine
# Randomizes script behaviour
class RandomizerEngine:
    lastPause = None

    def __init__(self, output):
        self.output = output
        self.output.log("Randomizer engine initialized.")
        self.lastPause = time.time()

    def randomPause(self):
        # Minimum pause
        if time.time() - self.lastPause > 300:
            randomData = random.randint(0, 100)
            # 3% chance to make a pause
            if randomData > 97:
                # make a random pause. (up to 3 min)
                self.lastPause = time.time()
                pauseDuration = random.randint(90, 180)
                self.output.log("Starting a random pause for " + str(pauseDuration) + " seconds.")
                time.sleep(pauseDuration)
