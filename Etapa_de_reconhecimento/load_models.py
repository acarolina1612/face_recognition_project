import argparse
import sys
from Etapa_de_reconhecimento.tf_graph import FaceRecGraph
from Etapa_de_reconhecimento.align_custom import AlignCustom
from Etapa_de_reconhecimento.face_feature import FaceFeature
from Etapa_de_reconhecimento.mtcnn_detect import MTCNNDetect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, help="Add New Face data", default="input")
    args = parser.parse_args(sys.argv[1:])
    FRGraph = FaceRecGraph()
    aligner = AlignCustom()
    extract_feature = FaceFeature(FRGraph)
    face_detect = MTCNNDetect(FRGraph, scale_factor=2)
    return parser, args, FRGraph, aligner, extract_feature, face_detect


if __name__ == "__main__":
    main()
