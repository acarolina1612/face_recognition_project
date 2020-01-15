import cv2
import numpy as np
from sklearn.externals import joblib


class MySpoof:

    def detect_face(self, faceCascade):
        faces = faceCascade.detectMultiScale(self, scaleFactor=1.1, minNeighbors=5, minSize=(110, 110))
        return faces

    def calc_hist(self):
        histogram = [0] * 3
        for j in range(3):
            histr = cv2.calcHist([self], [j], None, [256], [0, 256])
            histr *= 255.0 / histr.max()
            histogram[j] = histr
        return np.array(histogram)

    def load_spoof(self, frame, sample_number, count, decrease, number_falses):

        name = r'D:/FaceRec-master/Entrada ICA/spoofing_detection-master/trained_models/replay_attack_trained_models/' \
               'replay-attack_ycrcb_luv_extraTreesClassifier.pkl'  # name of trained model to perform spoofing detection
        threshold = 0.75  # default threshold used for the classifier to decide between genuine and a spoof attack

        # # Load model
        clf = None
        try:
            clf = joblib.load(name)
        except IOError as e:
            print("Error loading model <" + name + ">: {0}".format(e.strerror))
            exit(0)

        # # Initialize face detector
        cascPath = r"D:/FaceRec-master/Entrada ICA/spoofing_detection-master/python_scripts/" \
                   "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        measures = np.zeros(sample_number, dtype=np.float)

        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = MySpoof.detect_face(img_gray, faceCascade)

        measures[count % sample_number] = 0

        for i, (x, y, w, h) in enumerate(faces):

            roi = frame[y:y + h, x:x + w]

            img_ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)
            img_luv = cv2.cvtColor(roi, cv2.COLOR_BGR2LUV)

            ycrcb_hist = MySpoof.calc_hist(img_ycrcb)
            luv_hist = MySpoof.calc_hist(img_luv)

            feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
            feature_vector = feature_vector.reshape(1, len(feature_vector))

            prediction = clf.predict_proba(feature_vector)
            prob = prediction[0][1]

            measures[count % sample_number] = prob

            cv2.rectangle(frame, (x, y), (x + 150, y + 150), (255, 0, 0), 2)
            # bounding box with fixed height and width

            point = (x, y - 5)

            if 0 not in measures:
                text = "True"
                if np.mean(measures) >= threshold:
                    text = "False"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img=frame, text=text, org=point, fontFace=font, fontScale=0.9, color=(0, 0, 255),
                                thickness=2, lineType=cv2.LINE_AA)
                    number_falses += 1
                    return text, number_falses
                else:

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img=frame, text=text, org=point, fontFace=font, fontScale=0.9,
                                color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                    cv2.putText(img=frame, text=str(decrease), org=(10, 400), fontFace=font, fontScale=10,
                                color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)

                    return text, number_falses
        count += 1
        text = "False"
        number_falses += 1
        return text, number_falses
