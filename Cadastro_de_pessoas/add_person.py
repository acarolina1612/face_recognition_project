import os
import json
import imghdr
import ntpath
import re
import imutils
import numpy as np
import copy
import cv2
from win32api import GetSystemMetrics
from tkinter import messagebox


class AddUser:
    def create_manual_data(self, new_name, image, company, aligner, extract_feature,
                           face_detect):
        filename = 'coordinates.txt'

        coordinates_path = os.path.abspath(os.pardir)  # get the parent folder path. In this case is
        # face_recognition_project
        coordinates_path = coordinates_path + '\\face_recognition_project\\Etapa_de_reconhecimento\\' + filename

        f = open(coordinates_path, 'r')
        data_set = json.loads(f.read())
        person_imgs = {"Left": [], "Right": [], "Center": []}
        person_features = {"Left": [], "Right": [], "Center": [], "Class": []}
        f.close()

        try:
            imghdr.what(new_name)  # check if it's an image
            string = ntpath.basename(new_name)
            new_name = string[:string.index('.')]  # get the name before "."

            # loop over the rotation angles ensuring no part of the image is cut off
            images_add = []

            if re.match("^[a-zA-Z0-9 _]*$", new_name):  # check if the image name does not have special characters
                for angle in np.arange(-15, 15, 1):
                    rotated = imutils.rotate_bound(image, angle)
                    # cv2.imshow("Rotated", rotated)
                    images_add.append(rotated)
                    # cv2.destroyAllWindows()
                    # key = cv2.waitKey(0) & 0xFF
                    # if key == ord('q'):
                    #     cv2.destroyAllWindows()

                images_add_copy = copy.deepcopy(images_add)
                images_complete = images_add_copy
                images_flip = []

                for i in images_add_copy:
                    image_array = cv2.flip(i, 1)  # flip horizontally

                    images_flip.append(image_array)
                    # cv2.imshow('Pic', image_array)
                    # key = cv2.waitKey(0) & 0xFF
                    # if key == ord('q'):
                    #     cv2.destroyAllWindows()

                images_complete.extend(images_flip)  # add rotated and flipped images to images_complete

                for images_add_single in images_complete:
                    rects, landmarks = face_detect.detect_face(images_add_single, 80)  # min face size is set to 80x80
                    for (i, rect) in enumerate(rects):
                        aligned_frame, pos = aligner.align(160, images_add_single, landmarks[:, i])
                        if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                            person_imgs[pos].append(aligned_frame)

                for pos in person_imgs:
                    person_features[pos] = [
                        np.mean(extract_feature.get_features(person_imgs[pos]), axis=0).tolist()]
                data_set[new_name] = person_features
                data_set[new_name]["Class"] = [company]
                f = open(coordinates_path, 'w')
                f.write(json.dumps(data_set))
                f.close()
                cv2.destroyAllWindows()
                messagebox.showinfo("Adicionar Usuário", "Usuário adicionado!")

            else:  # if the image name has special characters
                messagebox.showwarning('Aviso', 'Não insira caracteres especiais no nome da foto!')

        except IOError:  # get the coordinates manually

            vs = cv2.VideoCapture(0)  # get input from webcam

            print(
                "Por favor, comece a mexer a cabeça devagar. Aperte 'q' para salvar e "
                "adicionar o novo usuário ao dataset.")

            while True:
                _, frame = vs.read()
                rects, landmarks = face_detect.detect_face(frame, 80)  # min face size is set to 80x80
                for (i, rect) in enumerate(rects):
                    aligned_frame, pos = aligner.align(160, frame, landmarks[:, i])
                    if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                        person_imgs[pos].append(aligned_frame)
                        cv2.imshow("Adicionar usuário", aligned_frame)

                        width = GetSystemMetrics(0)
                        height = GetSystemMetrics(1)
                        x = int((width / 2) - (80 / 2)) + 125
                        y = int((height / 2) - (80 / 2)) - 25

                        cv2.moveWindow("Adicionar usuário", x, y)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    vs.release()

                    break

            for pos in person_imgs:  # there r some exceptions here, but I'll just leave it as this to keep it simple
                person_features[pos] = [
                    np.mean(extract_feature.get_features(person_imgs[pos]), axis=0).tolist()]
            data_set[new_name] = person_features
            data_set[new_name]["Class"] = [company]
            f = open(coordinates_path, 'w')
            f.write(json.dumps(data_set))
            f.close()
            messagebox.showinfo("Adicionar Usuário", "Usuário adicionado!")
