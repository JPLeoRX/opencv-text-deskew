from services.dataset_service import DatasetService
from services.deskew_service import DeskewService

# We can load the dataset and compare how accurately we can determine the skew angle

# Open the dataset
dataset = DatasetService().openDataset()

# Track errors
errors = []

# Go through each item
for i in range(0, len(dataset)):
    # Get image and angle
    item = dataset[i]
    imageCv = item[0]
    correctAngle = item[1]

    # Calculate the angle, and compare it to real one
    guessedAngle = round(DeskewService().getSkewAngle(imageCv), 2)
    difference = abs(correctAngle - guessedAngle)
    differencePercentage = round(abs(difference / correctAngle) * 100, 2)

    # Debug, make sure that difference is less than 2% and track errors
    print('Item #' + str(i) + ', with angle=' + str(correctAngle) + ', calculated=' + str(guessedAngle) + ', difference=' + str(differencePercentage) + '%')
    assert differencePercentage < 2
    errors.append(differencePercentage)

print('Min Error: ' + str(min(errors)) + '%')
print('Max Error: ' + str(max(errors)) + '%')
print('Avg Error: ' + str(round(sum(errors) / len(errors), 2)) + '%')