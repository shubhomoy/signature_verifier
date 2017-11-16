#!/usr/bin/python
import argparse

from util.predictor import Predictor
from util.preprocessor import SignaturePreprocessor
from util.trainer import Trainer

parser = argparse.ArgumentParser()
parser.add_argument('-i', metavar='InputDir', type=str, required=True,
                    help='Input directory path where all the raw signature images of one person is stored. '
                         'This is used to train model when passed with --train flag, or can be used to store '
                         'query signature images to get prediction result when passed with --predict flag. '
                         'Note: These raw images should be taken from the app. ')

group = parser.add_mutually_exclusive_group()
group.add_argument('--train', required=False, action='store_true', help='Pass this flag to train the model')
group.add_argument('--predict', required=False, action='store_true',
                   help='Pass this flag along with the -identifier <input directory> in which training was done.')

parser.add_argument('-identifier', metavar='IdentifierDirectory', type=str, default=None,
                    help='Directory path in which training was done. (the \'InputDir\' when --train flag was passed)')

args = parser.parse_args()

if __name__ == '__main__':
    if not any([args.train, args.predict]):
        print 'Pass --train or --predict flag. Type with --help to get details'
        exit()
    preprocessor = SignaturePreprocessor(args.i)
    processed_images = preprocessor.process()

    if args.train:
        trainer = Trainer(processed_images)
        trained_features = trainer.train()
        trainer.save(args.i)
        print 'Model successfully trained!'

    if args.predict:
        if not args.identifier:
            print 'Pass an identifier for prediction. Type with --help to get details'
        predictor = Predictor(processed_images, args.identifier)
        scores = predictor.predict()
        print
        print 'Prediction results'
        print '--------------------------------------'
        for score in scores:
            print 'Signature {} is {}'.format(score[0], 'genuine' if score[1] else 'forged')
        print '--------------------------------------'
        print







