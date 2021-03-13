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
        #model = Sequential()
        #model.add(Conv2D(inputDimensions[0] * 2, kernel_size=3, activation='relu', input_shape=(inputDimensions[0], inputDimensions[1], 3)))
        #model.add(Conv2D(inputDimensions[0], kernel_size=3, activation='relu'))
        #model.add(Flatten())
        #model.add(Dense(outputDimension, activation='softmax'))
        self.output.log("Creating a new model.")
        self.output.log("Input dimensions: " + str(inputDimension))
        self.output.log("Output dimensions: " + str(outputDimension))
        model = Sequential()
        model.add(Dense(int(inputDimension), input_shape=(1, inputDimension)))
        #model.add(LSTM(int(inputDimension), input_shape=(1, inputDimension), return_sequences=True))
        #model.add(LSTM(int(inputDimension) * 4, input_shape=(1, inputDimension), return_sequences=True))
        model.add(Dense(int(outputDimension), input_shape=(1, int(inputDimension)), activation='relu'))
        model.compile(loss='mean_squared_error', optimizer=Adam(decay=1e-6))
        self.model = model

    def compileModel(self):
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def trainModel(self, dataX, dataY):
        self.model.fit(dataX, dataY, epochs=30)

    def predict(self, dataX):
        return self.model.predict(dataX)
