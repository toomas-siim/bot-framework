from keras.datasets import mnist
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, LSTM
from keras.optimizers import Adam
import os
import imp
import np


# Class NeuralNetEngine
# Neural network functionality.

class NeuralNetEngine:
    def __init__(self, output):
        basePath = os.path.dirname(os.path.realpath(__file__))
        self.dataEngine = imp.load_source('data.engine', basePath + '/engine.neuralnet.data.py').NeuralNetDataEngine(output)
        self.output = output
        output.log("Neural net initialized.")

    def plotImage(self, image):
        plt.imshow(image)

    def encode(self, dataX, dataY):
        dataX = to_categorical(dataX)
        dataY = to_categorical(dataY)
        return (dataX, dataY)

    def buildModel(self, inputDimension, outputDimension):
        model = Sequential()
        model.add(Conv2D(inputDimension, kernel_size=3, activation='relu', input_shape=(inputDimension, 96, 2)))
        # model.add(Conv2D(inputDimension, kernel_size=3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(outputDimension, activation='softmax'))
        self.output.log("Creating a new model.")
        self.output.log("Input dimensions: " + str(inputDimension))
        self.output.log("Output dimensions: " + str(outputDimension))
        self.model = model

    def compileModel(self):
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def trainModel(self, dataX, dataY):
        self.model.fit(dataX, dataY, epochs=3, batch_size=1, workers=6)

    def predict(self, dataX):
        return self.model.predict(dataX)
