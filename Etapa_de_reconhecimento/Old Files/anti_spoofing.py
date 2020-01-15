import numpy as np
import cv2
from sklearn.externals import joblib
# from time import gmtime, strftime

class my_spoof:

    def detect_face(img, faceCascade):
        faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(110, 110)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        return faces



    def calc_hist(img):
        histogram = [0] * 3
        for j in range(3):
            histr = cv2.calcHist([img], [j], None, [256], [0, 256])
            histr *= 255.0 / histr.max()
            histogram[j] = histr
        return np.array(histogram)



    def load_spoof(self):

        name = r'D:/FaceRec-master/Entrada ICA/spoofing_detection-master/trained_models/replay_attack_trained_models/' \
               'replay-attack_ycrcb_luv_extraTreesClassifier.pkl'  # name of trained model to perform spoofing detection
        device = 0  # camera identifier/video to acquire the image
        # 'D:/FaceRec-master/Entrada ICA/spoofing_detection-master/examples/spoofing_test.mp4'
        threshold = 0.85  # default threshold used for the classifier to decide between genuine and a spoof attack

        # # Load model
        clf = None
        try:
            clf = joblib.load(name)
        except IOError as e:
            print("Error loading model <"+name+">: {0}".format(e.strerror))
            exit(0)

        # # Open the camera
        cap = cv2.VideoCapture(device)

        if not cap.isOpened():
            print("Error opening camera")
            exit(0)

        width = 640
        height = 480
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        # # Initialize face detector
        cascPath = r"D:/FaceRec-master/Entrada ICA/spoofing_detection-master/python_scripts/" \
                   "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        sample_number = 1
        count = 0
        wait = 0
        decrease = 4
        measures = np.zeros(sample_number, dtype=np.float)

        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            if ret is False:
                print("Error grabbing frame from camera")
                break

            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = my_spoof.detect_face(img_gray, faceCascade)

            measures[count%sample_number]=0

            point = (0,0)
            for i, (x, y, w, h) in enumerate(faces):
                w = 215 #fixed width and height to determine specific distance to recognize
                h = 215

                roi = frame[y:y+h, x:x+w]

                img_ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)
                img_luv = cv2.cvtColor(roi, cv2.COLOR_BGR2LUV)

                ycrcb_hist = my_spoof.calc_hist(img_ycrcb)
                luv_hist = my_spoof.calc_hist(img_luv)

                feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
                feature_vector = feature_vector.reshape(1, len(feature_vector))

                prediction = clf.predict_proba(feature_vector)
                prob = prediction[0][1]

                measures[count % sample_number] = prob

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #bounding box with fixed height and width

                point = (x, y-5)

                #print(measures, np.mean(measures))
                if 0 not in measures:
                    text = "True"
                    if np.mean(measures) >= threshold:
                        text = "False"
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(img=frame, text=text, org=point, fontFace=font, fontScale=0.9, color=(0, 0, 255),
                                    thickness=2, lineType=cv2.LINE_AA)
                        wait = 0
                        decrease = 4
                    else:
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(img=frame, text=text, org=point, fontFace=font, fontScale=0.9,
                                    color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                        cv2.putText(img=frame, text=str(decrease), org=(10, 400), fontFace=font, fontScale=10,
                                    color=(0,0,255), thickness=2, lineType=cv2.LINE_AA)

                        wait += 1

                        if wait == 10 or wait == 20 or wait == 30 or wait == 40:
                            decrease -= 1

                            if decrease == 0:
                                cap.release()
                                wait = 0
                                decrease = 4
                                break


            count+=1
            cv2.imshow('AS', frame)
            cv2.resizeWindow('AS', 640, 480)

            key = cv2.waitKey(1)
            if key & 0xFF == ord("q"):
                break


