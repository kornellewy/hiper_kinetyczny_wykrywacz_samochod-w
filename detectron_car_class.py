from typing import Tuple

import numpy as np
import cv2

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg


class DetectronCarClass:
    CAR_CLASS_IDX = 2
    def __init__(self) -> None:
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE = 'cpu'
        self.cfg.merge_from_file(model_zoo.get_config_file(
            "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        )
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
            "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        )
        self.predictor = DefaultPredictor(self.cfg)

    def detect(self, image: np.ndarray) -> Tuple[np.ndarray, int]:
        prediction = self.predictor(image)
        bboxes = self.filter_detector_prediction(prediction=prediction)
        image = self.draw_bboxes(image=image, bboxes=bboxes)
        car_number = len(bboxes)
        return image, car_number

    def filter_detector_prediction(self, prediction: dict) -> list:
        bboxes = []
        prediction = prediction["instances"].to("cpu").get_fields()
        for instance_idx, class_idx in enumerate(prediction["pred_classes"].tolist()):
            if class_idx != self.CAR_CLASS_IDX:
                continue
            bbox = prediction["pred_boxes"][instance_idx].tensor.tolist()[0]
            bbox = [int(cord) for cord in bbox]
            bboxes.append(bbox)   
        return bboxes
        
    def draw_bboxes(self, image: np.ndarray, bboxes: list) -> np.ndarray:
        for bbox in bboxes:
            image = cv2.rectangle(image,(bbox[0], bbox[1]),(bbox[2], bbox[3]),(0,255,0), 3)
        return image

if __name__ == "__main__":
    detetor = DetectronCarClass()
    image = cv2.imread("test_img.jpg")
    image, car_number=detetor.detect(image=image)
    print(f"car number {car_number}")
    cv2.imshow("image", image)
    cv2.waitKey(0) 