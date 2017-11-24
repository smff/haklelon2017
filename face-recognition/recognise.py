import cv2
import glob
import random
import numpy as np

emotions = ["happy", "normal", "sad"]  # Define emotions
fishface = cv2.createFisherFaceRecognizer() # Initialize fisher face classifier

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default")
data = {}


def get_files(emotion):  # Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("dataset\\%s\\*" % emotion)
    random.shuffle(files)
    training = files[:int(len(files) * 1)]  # get first 80% of file list
    prediction = files[-int(len(files) * 0.2):]  # get last 20% of file list
    return training, prediction


def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for emotion in emotions:
        training, prediction = get_files(emotion)
        # Append data to training and prediction list, and generate labels 0-7
        for item in training:
            image = cv2.imread(item)  # open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
            training_data.append(gray)  # append image array to training data list
            training_labels.append(emotions.index(emotion))

        for item in prediction:  # repeat above process for prediction set
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction_data.append(gray)
            prediction_labels.append(emotions.index(emotion))

    return training_data, training_labels, prediction_data, prediction_labels


def run():
    # while True:
    cv2.waitKey(30)
    cv2.destroyAllWindows()

    face = get_face()

    if face is None:
        pass

    pred, conf = fishface.predict(face)
    print emotions[pred], pred, conf
    cv2.imshow('OpenCV', face)
    cv2.waitKey(500)


def run_recognizer():
    training_data, training_labels, prediction_data, prediction_labels = make_sets()

    print "training fisher face classifier"
    # print "size of training set is:", len(training_labels), "images"
    fishface.train(training_data, np.asarray(training_labels))

    run()

    # print "predicting classification set"
    cnt = 0
    correct = 0
    incorrect = 0
    for image in prediction_data:
        pred, conf = fishface.predict(image)
        if pred == prediction_labels[cnt]:
            correct += 1
            cnt += 1
        else:
            cv2.imwrite("difficult\\%s_%s_%s.jpg" % (emotions[prediction_labels[cnt]], emotions[pred], cnt),
                        image)  # <-- this one is new
            incorrect += 1
            cnt += 1
    return ((100 * correct) / (correct + incorrect))


def get_face():
    webcam = cv2.VideoCapture(0)
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    faceDet = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faceDet_two = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    faceDet_three = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    faceDet_four = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")
    # Detect face using 4 different classifiers
    face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                    flags=cv2.CASCADE_SCALE_IMAGE)
    face_two = faceDet_two.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
    face_three = faceDet_three.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
    face_four = faceDet_four.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

    # Go over detected faces, stop at first detected face, return empty if no face.
    if len(face) == 1:
        facefeatures = face
    elif len(face_two) == 1:
        facefeatures = face_two
    elif len(face_three) == 1:
        facefeatures = face_three
    elif len(face_four) == 1:
        facefeatures = face_four
    else:
        facefeatures = ""

    # Cut and save face
    out = None
    for (x, y, w, h) in facefeatures:  # get coordinates and size of rectangle containing face
        gray = gray[y:y + h, x:x + w]  # Cut the frame to size

        out = cv2.resize(gray, (350, 350))
    return out


# Now run it
metascore = []
for i in range(0, 50):
    correct = run_recognizer()
    # print "got", correct, "percent correct!"
    metascore.append(correct)

# print "\n\nend score:", np.mean(metascore), "percent correct!"
