import json
import os

import numpy as np

from feature_extractor import FeatureExtractor


class Predictor(object):
    def __init__(self, processed_images, iden):
        self.processed_images = processed_images
        self.iden = iden
        if not os.path.exists(self.iden):
            raise Exception('Identifier does not exists')
        else:
            with open('{}/model'.format(self.iden), 'r') as model_file:
                self.model = json.load(model_file)

    def predict(self):
        eucl_dists = []
        for processed_image in self.processed_images:
            feature_extractor = FeatureExtractor(processed_image)
            f1 = feature_extractor.extract_height_to_width_ratio()
            f2 = feature_extractor.extract_occupancy_ratio()
            f3 = feature_extractor.extract_density_ratio()
            f4 = feature_extractor.extract_critical_points()
            f5 = feature_extractor.extract_center_of_gravity()
            f6 = feature_extractor.extract_slope_of_cg()

            dist = np.linalg.norm(np.array([f1, f2, f3, f4, f5[0], f5[1], f6]) - np.array([self.model['f1'],
                                                                                           self.model['f2'],
                                                                                           self.model['f3'],
                                                                                           self.model['f4'],
                                                                                           self.model['f5'],
                                                                                           self.model['f6'],
                                                                                           self.model['f7']]))
            eucl_dists.append((dist, processed_image))
            print dist, processed_image.filename

        result = [(x[1].filename, True) if self.model['threshold'][0] <= x[0] <= self.model['threshold'][1] else (x[1].filename, False) for x in eucl_dists]
        return result
