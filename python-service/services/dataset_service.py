import random
import os
import shutil
from typing import List, Tuple
from services.graphics_service import GraphicsService

# This service provides all the basic operations needed to generate/load skewed image dataset
class DatasetService:
    def getDatasetPath(self) -> str:
        return '../sample-images/dataset'

    def getOriginalPdfPath(self) -> str:
        return '../sample-images/li.pdf'

    # Remove all files/directories inside a folder
    def clearFolder(self, pathToFolder):
        for root, dirs, files in os.walk(pathToFolder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    # Open original image that's used as the base for all skewed versions
    def loadOriginalImage(self):
        pageImagePath = GraphicsService().renderPdfDocumentPageToImageFromPath(self.getOriginalPdfPath(), 1, 300)
        imageCv = GraphicsService().openImageCv(pageImagePath)
        imageCv = GraphicsService().paintOverBorder(imageCv, 100, 250, (255, 255, 255))
        return imageCv

    # Create one skewed dataset image
    def generateDatasetItem(self, imageCv, minAngle: float, maxAngle: float):
        # Generate random angle
        angle = random.uniform(minAngle, maxAngle)
        angle = round(angle, 2)

        # We need a string representation for an angle to use in file names
        angleStr = str(abs(angle))
        if angle < 0:
            angleStr = '-' + angleStr
        else:
            angleStr = '+' + angleStr

        # Rotate the image
        rotated = GraphicsService().rotateImage(imageCv, angle)

        # Convert it back to PIL format, and save it on disk
        pilImage = GraphicsService().convertCvImagetToPilImage(rotated)
        filename = 'li_' + angleStr + '.png'
        filepath = self.getDatasetPath() + '/' + filename
        pilImage.save(filepath)

    # Generate completely new dataset
    def generateDataset(self, numberOfExamples: int = 20, minAngle: float = -10, maxAngle: float = 10):
        # Get original image
        imageCv = self.loadOriginalImage()

        # Clear up old dataset
        self.clearFolder(self.getDatasetPath())

        # Generate new items
        for i in range(0, numberOfExamples):
            self.generateDatasetItem(imageCv, minAngle, maxAngle)

    # Open one skewed dataset image
    def openDatasetItem(self, path: str) -> Tuple:
        imageCv = GraphicsService().openImageCv(path)
        angleStr = path.split('/')[-1].replace('.png', '').split('_')[-1]
        angleFloat = float(angleStr)
        return imageCv, angleFloat

    # Open the dataset
    def openDataset(self) -> List[Tuple]:
        path = self.getDatasetPath()
        result = []
        for root, dirs, files in os.walk(path):
            for f in files:
                filePath = path + '/' + str(f)
                item = self.openDatasetItem(filePath)
                result.append(item)
        return result
