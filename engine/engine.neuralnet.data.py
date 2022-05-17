import os
from keras.utils import load_img
from keras.utils import img_to_array
from sklearn.preprocessing import MinMaxScaler
import np
import zipfile
import glob

# Class NeuralNetDataEngine
# Neural network data functionality.

class NeuralNetDataEngine:
    scalerInput = None
    scalerOutput = None

    def __init__(self, output):
        basePath = os.path.dirname(os.path.realpath(__file__))
        self.output = output
        self.output.log("Neural net data engine initialized.")

    def imagePathToData(self, path):
        img = load_img(path).convert('LA')
        return self.imageToData(img)

    def imageToData(self, screen):
        input_arr = img_to_array(screen)
        return input_arr

    def zipData(self, zipPath, path):
        zipf = zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED)
        data = glob.glob(path)
        actionData = {}
        for file in data:
            zipf.write(file, "./" + os.path.basename(file))
            os.remove(file)
        zipf.close()

    def extractZipData(self, zipPath, destDir):
        with zipfile.ZipFile(zipPath) as zf:
            zf.extractall(destDir)

    def reshapeData(self, data, dim, flatten = False):
        result = []
        for v in data:
            if flatten == True:
                result.append(np.reshape(np.array(v), dim).flatten())
            else:
                result.append(np.reshape(np.array(v), dim))
        return np.array(result)

    def normalizeData(self, inputData, outputData):
        # normalize the input dataset
        inputData = np.array(inputData, dtype=np.float32)
        self.scalerInput = MinMaxScaler(feature_range=(0, 1))
        datasetInput = self.scalerInput.fit_transform(inputData)

        # normalize the output dataset
        outputData = np.array(outputData, dtype=np.float32)
        self.scalerOutput = MinMaxScaler(feature_range=(0, 1))
        datasetOutput = self.scalerOutput.fit_transform(outputData)

        return (datasetInput, datasetOutput)

    # converts to ascii number
    def textToData(self, text):
        return int("".join([str(ord(c)) for c in s]))
