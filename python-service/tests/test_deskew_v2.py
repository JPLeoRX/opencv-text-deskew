from services.dataset_service import DatasetService
from tekleo_common_utils import UtilsImage, UtilsOpencv

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
    deskewedImage, guessedAngle = UtilsOpencv().deskew(imageCv)
    difference = abs(correctAngle - guessedAngle)
    differencePercentage = round(abs(difference / correctAngle) * 100, 2)

    # Debug
    print('Item #' + str(i) + ', with angle=' + str(correctAngle) + ', calculated=' + str(guessedAngle) + ', difference=' + str(differencePercentage) + '%')
    UtilsImage().debug_image_cv(imageCv, 'Skewed')
    UtilsImage().debug_image_cv(deskewedImage, 'Deskewed')

    #cv2.imshow('Skewed', imageCv)
    #cv2.imshow('Deskewed', deskewedImage)
    #cv2.waitKey()