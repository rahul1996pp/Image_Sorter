# Image_seperator
**IMAGE SEPERATOR USING FACE FACE_RECOGNITION MODULE AND CV2 AND CVLIB**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/rahul1996pp/Image_Sorter/blob/main/LICENSE)
- The images with faces are stored in face folder.
- The images withhout faces are stored in no_face folder.
- We can use CV2 or cvlib or face recogniton module to process image.
- CV2 is faster than face recogniton module.
- To increase accuracy results i made image classification in cv2 that if both face and eye is detetcted then it is valid image.
- Face recogniton is accurate than CV2.
- cvlib is faster and accurate as it uses GPU.
- Dlib(cnn) is very slow but most accurate .
-Dlib(hog) is fast and accurate.
- Run the script and let the script do the magic for you.

## # Overview of all modules

| Modules  | Speed  | Accuracy  |
| :------------: | :------------: | :------------: |
| CV2  | Very fast  | Medium  |
| Face recognition  |  Slow | High  |
| Cvlib  |  Fast | High  |
| Dlib(cnn Face detector)  | Very slow  | Very high  |
| Dlib(hog face detector) | Fast | Medium |

To install dependencies:
`pip install -r requirements.txt`

How to run script:
 `python image_sorter.py`

**Buy me a coffee : [click here](https://www.paypal.me/RahulPujari "Pay")**
