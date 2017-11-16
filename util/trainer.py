import json

import numpy as np

from feature_extractor import FeatureExtractor


class Trainer(object):
    def __init__(self, processed_images):
        self.processed_images = processed_images
        self.trained_features = None

    def train(self):
        print 'Model training started'
        f1_arr = []
        f2_arr = []
        f3_arr = []
        f4_arr = []
        f5_arr = []
        f6_arr = []
        for processed_image in self.processed_images:
            feature_extractor = FeatureExtractor(processed_image)
            f1 = feature_extractor.extract_height_to_width_ratio()
            f2 = feature_extractor.extract_occupancy_ratio()
            f3 = feature_extractor.extract_density_ratio()
            f4 = feature_extractor.extract_critical_points()
            f5 = feature_extractor.extract_center_of_gravity()
            f6 = feature_extractor.extract_slope_of_cg()

            f1_arr.append(f1)
            f2_arr.append(f2)
            f3_arr.append(f3)
            f4_arr.append(f4)
            f5_arr.append(f5)
            f6_arr.append(f6)

        f1_mean = np.mean(f1_arr)
        f2_mean = np.mean(f2_arr)
        f3_mean = np.mean(f3_arr)
        f4_mean = np.mean(f4_arr)
        f5_unfold = zip(*f5_arr)
        f5_mean = np.mean(f5_unfold[0])
        f6_mean = np.mean(f5_unfold[1])
        f7_mean = np.mean(f6_arr)

        self.trained_features = tuple([f1_mean, f2_mean, f3_mean, f4_mean, f5_mean, f6_mean, f7_mean])
        return self.trained_features

    def get_threshold(self):
        eucl_dists = []
        for processed_image in self.processed_images:
            feature_extractor = FeatureExtractor(processed_image)
            f1 = feature_extractor.extract_height_to_width_ratio()
            f2 = feature_extractor.extract_occupancy_ratio()
            f3 = feature_extractor.extract_density_ratio()
            f4 = feature_extractor.extract_critical_points()
            f5 = feature_extractor.extract_center_of_gravity()
            f6 = feature_extractor.extract_slope_of_cg()

            dist = np.linalg.norm(np.array([f1, f2, f3, f4, f5[0], f5[1], f6]) - np.array(self.trained_features))
            eucl_dists.append(dist)
        return tuple([min(eucl_dists), max(eucl_dists)])

    def save(self, input_dir):
        threshold = self.get_threshold()
        model = {
            'f1': self.trained_features[0],
            'f2': self.trained_features[1],
            'f3': self.trained_features[2],
            'f4': self.trained_features[3],
            'f5': self.trained_features[4],
            'f6': self.trained_features[5],
            'f7': self.trained_features[6],
            'threshold': threshold
        }

        with open('{}/model'.format(input_dir), 'w') as output_file:
            json.dump(model, output_file)
