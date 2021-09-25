from datetime import timedelta
from glob import glob
from os.path import exists
from os import mkdir
from shutil import move
from colorama import Fore, init, Style
from face_recognition import load_image_file, face_locations, face_encodings
from cv2 import imread, CascadeClassifier, CASCADE_SCALE_IMAGE, resize
from time import time
from cvlib import detect_common_objects
from dlib import get_frontal_face_detector, cnn_face_detection_model_v1
from tabulate import tabulate

bright = Style.BRIGHT
green, blue, red, cyan, reset = Fore.GREEN + bright, Fore.BLUE + bright, Fore.RED + bright, Fore.CYAN, Fore.RESET
init(convert=True, autoreset=True)


def folder_list():
    if not folder:
        print(f"{red}[+] Enter the folder name correctly")
        folder_list()
    img = glob(f'{folder}/**/*.jpg', recursive=True) + (glob(f'{folder}/**/*.png', recursive=True)) + (glob(f'{folder}/**/*.jpeg', recursive=True))
    if not (img) or (len(img)==0):
        print(f"{red}[+] Folder is empty or incorrect folder name try again with new folder")
        folder_list()
    img_process = {'1': img_cv2, '2': img_rec, '3': img_cv_lib, '4': img_dlib, '5': img_dlib}
    print(f"{green}[+] Total files in folder are {len(img)}")
    for img_file in range(len(img)):
        print(f'{blue}[{img_file + 1}] {green}processing the image {cyan}{img[img_file]}')
        img_process[str(choice)](img[img_file])


def img_rec(image):
    global faces_num, no_faces_num
    try:
        img = load_image_file(image)
        face_loc = face_locations(img, number_of_times_to_upsample=2)
        faces = face_encodings(img, known_face_locations=face_loc, num_jitters=1)[0]
        faces_num += 1
        move(image, "faces")
    except:
        no_faces_num += 1
        move(image, "no_face")


def img_cv2(image):
    global faces_num, no_faces_num
    gray = imread(image)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=4, flags=CASCADE_SCALE_IMAGE)
    eyes = face_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=4, flags=CASCADE_SCALE_IMAGE)
    if (len(faces) and len(eyes)) != 0:
        faces_num += 1
        move(image, "faces")
    else:
        no_faces_num += 1
        move(image, "no_face")


def img_cv_lib(image):
    global faces_num, no_faces_num
    face = imread(image)
    bbox, label, conf = detect_common_objects(face)
    if 'person' in label:
        faces_num += 1
        move(image, "faces")
    else:
        no_faces_num += 1
        move(image, "no_face")


def img_dlib(image):
    global faces_num, no_faces_num, cnn_face_detector
    image_file = resize(imread(str(image)), (224, 224))
    if choice == "5":
        hog = get_frontal_face_detector()
        faces = hog(image_file, 1)
    if choice == "4":
        faces = cnn_face_detector(image_file, 1)
    if len(faces) != 0:
        faces_num += 1
        move(image, "faces")
    else:
        no_faces_num += 1
        move(image, "no_face")


def choice():
    global choice, face_cascade, eye_cascade, cnn_face_detector, module_name
    print(
        tabulate({f"{green}MENU{reset}".center(30, " "): [f"{blue}[1] CV2{reset}", f"{blue}[2] Face recognition{reset}",
                                                          f"{blue}[3] Cvlib{reset}",
                                                          f"{blue}[4] Dlib(cnn Face detector){reset}",
                                                          f"{blue}[5] Dlib(hog face detector){reset}"]},
                 headers=f"keys", tablefmt='pretty', colalign=("left",)).replace("-", "*").replace("+", "*"))
    choice = input("[+] Enter your choice :- ")
    if choice == '1':
        print(f"{cyan}[*] Using cv2 for processing images")
        face_cascade = CascadeClassifier("data/haarcascade_frontalface_default.xml")
        eye_cascade = CascadeClassifier("data/haarcascade_eye.xml")
        module_name = 'cv2'
    elif choice == '2':
        print(f"{cyan}[*] Using face recognition for processing images")
        module_name = 'Face recognition'
    elif choice == '3':
        print(f"{cyan}[*] Using cvlib for processing images")
        module_name = 'cvlib'
    elif choice == '4':
        print(f"{cyan}[*] using dlib(cnn Face detector) for processing images")
        cnn_face_detector = cnn_face_detection_model_v1('data/mmod_human_face_detector.dat')
        module_name = 'dlib(cnn Face detector)'
    elif choice == '5':
        print(f"{cyan}[*] using dlib(Hog Face detector) for processing images")
        module_name = 'dlib(Hog Face detector)'


def credit():
    credit_text = f"""
               {red}IMAGE SEPARATOR
{green}               
     ██▀███   ▄▄▄       ██░ ██  █    ██  ██▓    
    ▓██ ▒ ██▒▒████▄    ▓██░ ██▒ ██  ▓██▒▓██▒    
    ▓██ ░▄█ ▒▒██  ▀█▄  ▒██▀▀██░▓██  ▒██░▒██░    
    ▒██▀▀█▄  ░██▄▄▄▄██ ░▓█ ░██ ▓▓█  ░██░▒██░    
    ░██▓ ▒██▒ ▓█   ▓██▒░▓█▒░██▓▒▒█████▓ ░██████▒
    ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░▓  ░
      ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░▒░ ░░░▒░ ░ ░ ░ ░ ▒  ░
      ░░   ░   ░   ▒    ░  ░░ ░ ░░░ ░ ░   ░ ░   
       ░           ░  ░ ░  ░  ░   ░         ░  ░ {blue}code generated by Rahul.p\n
    """
    print(credit_text)


def main():
    global faces_num, no_faces_num
    faces_num, no_faces_num = 0, 0
    [mkdir(folder) for folder in ["no_face", "faces"] if not exists(folder)]
    choice()
    folder_list()
    time_output = time() - start_time
    sec = str(timedelta(seconds=(int(time_output)))).split(":")
    print(f"[*]{green} Time taken to process images is -{reset} {sec[0]} H : {sec[1]} M : {sec[2]} S")
    print(f"{green}[~] Successfully completed [~]")
    print(f'{blue}[*] Using {module_name} \n{green}[+] faces are :- {faces_num}\n{red}[-] no faces are :- {no_faces_num}')


try:
    credit()
    start_time = time()
    main()
except KeyboardInterrupt:
    print(f'{red}\n[~] Exiting ....')
except Exception as e:
    print(f"{red}\n[-] error message is {e}")
