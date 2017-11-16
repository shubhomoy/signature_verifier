Note:
This utility is designed for running in linux platform (preferably Ubuntu 16.04 or 14.04)

1. Extract Bitslate.zip
2. Open terminal and cd to the extracted directory

-> cd /path/to/extracted/directory

3. Then type the following command

-> ./init.sh

4. This will install the dependencies needed to run the utility

Installing the apk file
5. Go to settings in your Android device and inside Security settings, make sure you have enabled "Unknown Sources".
This is because the apk attached is a debug apk version and may not install if "Unknown Sources is disabled"
5. Install the signature_verifier.apk app (for android)


Using the utility
------------------------------------------------------------

This utility has 2 main parts
1. Training
2. Prediction

1. Training
------------------------------------------------------------
For training signatures of individual person do the following
1. Make a directory with the person's name. eg: 'jack'
2. Make jack sign a white blank sheet with 5-10 signatures
3. From the android app, capture these signatures. Make sure each signature comes inside the green
box in the app.
4. After all the signatures have been captured, transfer them in 'jack' directory
5. Open terminal and cd to the extracted directory where the utility is present

-> cd /path/to/utility

6. Run the command

-> python utility.py -i path/to/jack --train

This will train jacks signature model.
The -i denotes the input directory. In this case, it is 'jack'. The --train flag denotes we are ready to train
jack's signature model.


2. Prediction
------------------------------------------------------------
For predicting a query signature, do the following
1. Make a temporary directory. Example: 'query_signatures'
2. Open the android app and scan some signatures (forged or genuine for jack)
2. Open terminal and cd to the extracted directroy where utility is present.

-> cd /path/to/utility

3. Run the command

-> python utility.py -i /path/to/query_signatures -identifier /path/to/jack --predict

This will give a prediction result for all the signature images present in 'query_signatures' tested on 'jack'.
The -identifier tells which directory from which the query signatures will be comapared, in this case, jack's.


For further help, you may type the command

-> python utility.py --help

Or email us at
shubhomoy.tubu@gmail.com
aditya2595p@gmail.com

Or call us at
+91 8851680923