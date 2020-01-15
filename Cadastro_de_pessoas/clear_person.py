import os
import json
from Etapa_de_reconhecimento.return_path import return_path


class Clear:  # clear the person and its coordinates from the txt
    def __init__(self, RemoveName):
        self.RemoveName = RemoveName

        filename = 'coordinates.txt'
        temp_filename = 'coordinates_new.txt'

        coordinates_path = os.path.abspath(os.pardir)  # get the parent folder path. In this case is
        # face_recognition_project
        temp_coordinates_path = coordinates_path + '\\face_recognition_project\\Etapa_de_reconhecimento\\' + \
                                temp_filename
        coordinates_path = coordinates_path + '\\face_recognition_project\\Etapa_de_reconhecimento\\' + filename


        f = open(coordinates_path, 'r')  # read
        g = open(temp_coordinates_path, 'w')  # write

        with g as dest_file:
            with f as source_file:
                for line in source_file:
                    element = json.loads(line.strip())
                    if RemoveName in element:
                        del element[RemoveName]
                    dest_file.write(json.dumps(element))
        f.close()
        g.close()

        os.remove(coordinates_path)
        os.rename(temp_coordinates_path, coordinates_path)
