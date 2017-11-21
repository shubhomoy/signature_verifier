import os
from collections import namedtuple

import cv2
import numpy as np
import logging
logging.basicConfig()
SignatureImage = namedtuple('SignatureImage', 'filename viewfinder_crop binary rotated corners cropped')

PIXEL_COUNT_ACCEPT_THRESHOLD = 0.06


class SignaturePreprocessor(object):

    def __init__(self, input_dir, output_dir=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.input_dir = input_dir
        self.output_dir = '{}/preprocessed'.format(input_dir) if output_dir is None else output_dir
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        if not os.path.exists("{}/binary".format(self.output_dir)):
            os.mkdir("{}/binary".format(self.output_dir))
        if not os.path.exists("{}/cropped".format(self.output_dir)):
            os.mkdir("{}/cropped".format(self.output_dir))

    def __crop(self, img_file):
        """
        Crop image according to view finder
        :param img_file:
        :return: cropped_image
        """
        img = cv2.imread("{}/{}".format(self.input_dir, img_file))
        img = cv2.resize(img, (1280, img.shape[0]*1280/img.shape[1]))
        x_center = img.shape[1] / 2
        y_center = img.shape[0] / 2
        x_lim = int((678.0 / 5312) * img.shape[1])
        y_lim = int((450.0 / 2988) * img.shape[0])
        cropped_image = img[y_center - y_lim:y_center + y_lim, x_center - x_lim:x_center + x_lim]
        cv2.imwrite('{}/{}'.format(self.output_dir, img_file), cropped_image)
        return cropped_image

    def __convert_to_binary(self, cropped_image, img_file):
        """
        Converts image to binary format
        :param cropped_image:
        :param img_file:
        :return: binary_image
        """
        grayscale = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)
        ret, thresh_img = cv2.threshold(grayscale, 100, 255, cv2.THRESH_BINARY)
        kernel = np.ones((2, 2), np.uint8)
        thresh_img = cv2.erode(thresh_img, kernel, iterations=2)
        cv2.imwrite('{}/binary/{}'.format(self.output_dir, img_file), thresh_img)
        return thresh_img

    def __fix_rotation(self, binary_image, img_file):
        """
        Rotate signature if required
        :param binary_image:
        :param img_file:
        :return:
        """
        # TODO: enhance this
        coords = np.column_stack(np.where(binary_image == 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = binary_image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(binary_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        rotated[rotated <= 0] = 0
        rotated[rotated > 0] = 255
        cv2.imwrite('{}/binary/{}'.format(self.output_dir, img_file), rotated)
        return rotated

    def __final_crop(self, rotated_image, img_file):
        """
        Crop around the signature to get width and height
        :param rotated_image:
        :param img_file:
        :return:
        """
        x_arr, y_arr = np.where(rotated_image <= 0)
        x_min, x_max, y_min, y_max = min(x_arr), max(x_arr), min(y_arr), max(y_arr)
        cropped_image = rotated_image[x_min:x_max, y_min:y_max]
        cv2.imwrite('{}/cropped/{}'.format(self.output_dir, img_file), cropped_image)
        return cropped_image

    @staticmethod
    def __detect_edge(binary_image):
        """
        Harris algorithm to detect corners of the signature
        :param binary_image:
        :return:
        """
        dst = cv2.cornerHarris(binary_image, 2, 3, 0.04)
        binary_image[:] = 0
        binary_image[dst > 0.01 * dst.max()] = 1
        return binary_image

    def process(self):
        print
        print 'Pre-processing'
        print '--------------------------------------'
        processed_images = []
        images_to_remove = []
        pixel_count_threshold = []
        for img_file in os.listdir(self.input_dir):
            if not img_file.lower().endswith(('.png', '.jpeg', '.jpg')):
                continue
            print 'Processing signature image - {}'.format(img_file)
            viewfinder_crop = self.__crop(img_file)
            binary_image = self.__convert_to_binary(viewfinder_crop, img_file)
            rotated_image = self.__fix_rotation(binary_image, img_file)
            cropped_image = self.__final_crop(rotated_image, img_file)
            pixel_count = len(np.where(cropped_image == 0)[0])*1.0/(cropped_image.shape[0]*cropped_image.shape[1])
            corners = self.__detect_edge(rotated_image)
            image = SignatureImage(img_file, viewfinder_crop, binary_image, rotated_image, corners, cropped_image)
            if pixel_count < PIXEL_COUNT_ACCEPT_THRESHOLD:
                images_to_remove.append(image)
                continue
            processed_images.append(image)
        print '--------------------------------------'

        idx_to_remove = np.where(pixel_count_threshold < PIXEL_COUNT_ACCEPT_THRESHOLD)[0]

        # remove the processed image which does not satisfy threshold
        print 'Images removed'
        for image in images_to_remove:
            print image.filename

        print
        return processed_images
