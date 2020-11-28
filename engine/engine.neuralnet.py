from keras.datasets import mnist
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
import os
import imp


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

    def buildModel(self, inputDimensions, outputDimension):
        model = Sequential()
        model.add(Conv2D(inputDimensions[0] * 2, kernel_size=3, activation='relu', input_shape=(1, inputDimensions[0], inputDimensions[1], 3)))
        model.add(Conv2D(inputDimensions[0], kernel_size=3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(outputDimension, activation='softmax'))
        self.model = model

    def compileModel(self):
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def trainModel(self, dataX, dataY):
        self.model.fit(dataX, dataY, epochs=30)

    def predict(self, dataX):
        return self.model.predict(dataX)
