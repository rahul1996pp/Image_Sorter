import os
import shutil
import time
import cv2
import face_recognition
import cvlib as cv
import dlib


def folder_list():
    folder = input("[+] Enter folder name or drag and drop :- ").replace('"', "")
    for (dirpath, dirnames, filenames) in os.walk(folder):
        print("[+] processing the folder :- ", dirpath)
        folder_files_list(dirpath)


def folder_files_list(dirpath):
    global n_num, f_num, num
    files = os.listdir(dirpath)
    print("[+] Total files in folder are ", len(files))
    for file in files:
        num += 1
        print("[{}] processing the image {}".format(num, file))
        img_process_selection(dirpath, file)


def img_process_selection(dirpath, file):
    if choice == '1':
        img_cv2(os.path.join(dirpath, file))
    elif choice == '2':
        img_rec(os.path.join(dirpath, file))
    elif choice == '3':
        img_cv_lib(os.path.join(dirpath, file))
    elif choice == '4':
        img_dlib_cnn(os.path.join(dirpath, file))
    elif choice == '5':
        img_dlib_hog(os.path.join(dirpath, file))


def img_move(file, folder):
    shutil.move(file, folder)


def img_folder():
    if not os.path.exists("no_face"):
        os.mkdir("no_face")
    if not os.path.exists("faces"):
        os.mkdir("faces")


def img_rec(image):
    global reg_f_num, reg_n_num
    try:
        img = face_recognition.load_image_file(image)
        face_loc = face_recognition.face_locations(img, number_of_times_to_upsample=2)
        faces = face_recognition.face_encodings(img, known_face_locations=face_loc, num_jitters=1)[0]
        reg_f_num += 1
        img_move(image, "faces")
    except:
        reg_n_num += 1
        img_move(image, "no_face")


def img_cv2(image):
    global cv_f_num, cv_n_num
    gray = cv2.imread(image)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=4, flags=cv2.CASCADE_SCALE_IMAGE)
    eyes = face_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=4, flags=cv2.CASCADE_SCALE_IMAGE)
    if (len(faces) and len(eyes)) != 0:
        cv_f_num += 1
        img_move(image, "faces")
    else:
        cv_n_num += 1
        img_move(image, "no_face")


def img_cv_lib(image):
    global cv_lib_f_num, cv_lib_n_num
    face = cv2.imread(image)
    bbox, label, conf = cv.detect_common_objects(face)
    if 'person' in label:
        cv_lib_f_num += 1
        img_move(image, "faces")
    else:
        cv_lib_n_num += 1
        img_move(image, "no_face")


def img_dlib_cnn(image):
    global dlib_cnn_f_num, dlib_cnn_n_num, cnn_face_detector
    image_file = cv2.imread(image)
    faces_cnn = cnn_face_detector(image_file, 1)
    if len(faces_cnn) != 0:
        dlib_cnn_f_num += 1
        img_move(image, "faces")
    else:
        dlib_cnn_n_num += 1
        img_move(image, "no_face")

def img_dlib_hog(image):
    global dlib_hog_f_num, dlib_hog_n_num
    image_file = cv2.imread(image)
    hog_face_detector = dlib.get_frontal_face_detector()
    faces_hog = hog_face_detector(image_file, 1)
    if len(faces_hog) != 0:
        dlib_hog_f_num += 1
        img_move(image, "faces")
    else:
        dlib_hog_n_num += 1
        img_move(image, "no_face")

def choice():
    global choice,face_cascade, eye_cascade, cnn_face_detector
    print("""
    ******************************************
    *                MENU                    *
    ******************************************
    *                                        *
    *    [1] CV2                             *
    *                                        *
    *    [2] Face recognition                *
    *                                        *
    *    [3] Cvlib                           *
    *                                        *
    *    [4] Dlib(cnn Face detector)         *
    *                                        *
    *    [5] Dlib(hog face detector)         *
    *                                        *
    ******************************************
    """)
    choice = input("[+] Enter your choice :- ")
    if choice == '1':
        print("[*] Using cv2 for processing images")
        face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("data/haarcascade_eye.xml")
    elif choice == '2':
        print("[*] Using face recognition for processing images")
    elif choice == '3':
        print("[*] Using cvlib for processing images")
    elif choice == '4':
        print("[*] using dlib(cnn Face detector) for processing images")
        cnn_face_detector = dlib.cnn_face_detection_model_v1('data/mmod_human_face_detector.dat')
    elif choice == '5':
        print("[*] using dlib(Hog Face detector) for processing images")


def credit():
    credit_text = """
    
               IMAGE SEPARATOR
               
     ██▀███   ▄▄▄       ██░ ██  █    ██  ██▓    
    ▓██ ▒ ██▒▒████▄    ▓██░ ██▒ ██  ▓██▒▓██▒    
    ▓██ ░▄█ ▒▒██  ▀█▄  ▒██▀▀██░▓██  ▒██░▒██░    
    ▒██▀▀█▄  ░██▄▄▄▄██ ░▓█ ░██ ▓▓█  ░██░▒██░    
    ░██▓ ▒██▒ ▓█   ▓██▒░▓█▒░██▓▒▒█████▓ ░██████▒
    ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░▓  ░
      ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░▒░ ░░░▒░ ░ ░ ░ ░ ▒  ░
      ░░   ░   ░   ▒    ░  ░░ ░ ░░░ ░ ░   ░ ░   
       ░           ░  ░ ░  ░  ░   ░         ░  ░ code generated by Rahul.p\n
    """
    print(credit_text)

def img_details():
    if reg_f_num != 0 or reg_n_num != 0:
        print('[*] Using face module \n[+] faces are :- {}\n[-] no faces are :- {}'.format(reg_f_num, reg_n_num))
    elif cv_f_num != 0 or cv_n_num != 0:
        print('[*] Using cv2 \n[+] faces are :- {}\n[-] no faces are :- {}'.format(cv_f_num, cv_n_num))
    elif cv_lib_f_num != 0 or cv_lib_n_num != 0:
        print('[*] Using cvlib \n[+] faces are :- {}\n[-] no faces are :- {}'.format(cv_lib_f_num, cv_lib_n_num))
    elif dlib_cnn_f_num != 0 or dlib_cnn_n_num != 0:
        print('[*] Using dlib(cnn) \n[+] faces are :- {}\n[-] no faces are :- {}'.format(dlib_cnn_f_num, dlib_cnn_n_num))
    elif dlib_hog_f_num != 0 or dlib_hog_n_num != 0:
        print('[*] Using dlib(hog) \n[+] faces are :- {}\n[-] no faces are :- {}'.format(dlib_hog_f_num, dlib_hog_n_num))


def main():
    img_folder()
    choice()
    folder_list()
    time_output = time.time() - start_time
    print("[*] Time taken to process images is -",
          time.strftime("%H:%M:%S", time.gmtime(int('{:.0f}'.format(float(str(time_output)))))))
    print("[~] Successfully completed [~]")
    img_details()


cv_n_num, cv_f_num, reg_n_num, reg_f_num, cv_lib_f_num, cv_lib_n_num, dlib_cnn_f_num, dlib_cnn_n_num,dlib_hog_f_num,dlib_hog_n_num, num = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
try:
    credit()
    start_time = time.time()
    main()
except KeyboardInterrupt:
    print("\n[~] Exiting ....")
except :
    print("\n[-] Download the files correctly")
