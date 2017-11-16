import numpy as np


class FeatureExtractor(object):
    def __init__(self, processed_image):
        self.processed_image = processed_image
        self.cropped_image = self.processed_image[0]
        self.binary_image = self.processed_image[1]
        self.rotated_image = self.processed_image[2]
        self.cropped_image = self.processed_image[3]
        self.corners = self.processed_image[4]
        self.file_name = self.processed_image[5]

    @staticmethod
    def __get_center_of_gravity(img, cond, x_add=0, y_add=0):
        x_sum = 0
        x_num = 0
        y_sum = 0
        y_num = 0
        for y, row in enumerate(img):
            row_indices = [i for i, e in enumerate(row) if e == cond]
            x_sum += sum(row_indices)
            x_num += len(row_indices)
            if len(row_indices) > 0:
                y_sum += y
                y_num += 1
        x = (x_sum * 1. / x_num) + x_add if x_num > 0 else 0
        y = (y_sum * 1. / y_num) + y_add if y_num > 0 else 0
        return tuple([x, y])

    def extract_height_to_width_ratio(self):
        width = self.cropped_image.shape[1]
        height = self.cropped_image.shape[0]
        return height * 1.0 / width

    def extract_occupancy_ratio(self):
        filled_pixel = len(np.where(self.cropped_image == 0)[0])
        total = self.cropped_image.shape[0] * self.cropped_image.shape[1]
        return filled_pixel*1.0 / total

    def extract_density_ratio(self):
        x_mid = self.cropped_image.shape[1]/2
        left_part = self.cropped_image[:, :x_mid]
        right_part = self.cropped_image[:, x_mid+1:]

        left_pixel_count = len(np.where(left_part == 0)[0])
        right_pixel_count = len(np.where(right_part == 0)[0])

        return left_pixel_count * 1.0 / right_pixel_count

    def extract_critical_points(self):
        return len(np.where(self.corners == 0)[0])

    def extract_center_of_gravity(self):
        return self.__get_center_of_gravity(self.cropped_image, 255)

    def extract_slope_of_cg(self):
        x_mid = self.cropped_image.shape[1] / 2
        left_part = self.cropped_image[:, :x_mid]
        right_part = self.cropped_image[:, x_mid + 1:]

        left_cg = self.__get_center_of_gravity(left_part, 0)
        right_cg = self.__get_center_of_gravity(right_part, 0, x_add=x_mid+1)

        slope = (right_cg[1] - left_cg[1])*1.0 / (right_cg[0] - left_cg[0])*1.0
        return slope
