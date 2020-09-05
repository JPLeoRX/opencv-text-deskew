import cv2
from services.dataset_service import DatasetService
from services.deskew_service import DeskewService

# We can test how the results of deskew procedure look

# Open the dataset
dataset = DatasetService().openDataset()

# Go through each item
for i in range(0, len(dataset)):
    # Get image and angle
    item = dataset[i]
    imageCv = item[0]
    correctAngle = item[1]

    # Deskew the image, and compare calculated skew angle to real one
    deskewedImage, guessedAngle = DeskewService().deskew(imageCv)
    difference = abs(correctAngle - guessedAngle)
    differencePercentage = round(abs(difference / correctAngle) * 100, 2)

    # Debug
    print('Item #' + str(i) + ', with angle=' + str(correctAngle) + ', calculated=' + str(guessedAngle) + ', difference=' + str(differencePercentage) + '%')
    cv2.imshow('Skewed', imageCv)
    cv2.imshow('Deskewed', deskewedImage)
    cv2.waitKey()