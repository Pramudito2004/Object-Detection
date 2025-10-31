import cv2
import numpy as np
import cvlib as cv
from cvlib.object_detection import draw_bbox
from gtts import gTTS
from playsound import playsound
import os

def speech(text):
    print(text)
    language = "id" 
    output = gTTS(text=text, lang=language, slow=False)

    if not os.path.exists("./sounds"):
        os.makedirs("./sounds")
        
    output.save("./sounds/output.mp3")
    playsound("./sounds/output.mp3")

video = cv2.VideoCapture(0)
detected_labels = set() 

while True:
    ret, frame = video.read()
    if not ret:
        break
        
    bbox, label, conf = cv.detect_common_objects(frame)
    output_image = draw_bbox(frame, bbox, label, conf)

    cv2.imshow("Deteksi Objek", output_image)

    for item in label:
        detected_labels.add(item)

    if cv2.waitKey(10) & 0xFF == 27:
        break

video.release()
cv2.destroyAllWindows()

final_sentence = ""
if detected_labels:
    labels_list = list(detected_labels)
    if len(labels_list) == 1:
        final_sentence = f"Saya menemukan sebuah {labels_list[0]}."
    else:
        first_part = ", ".join(labels_list[:-1])
        last_part = labels_list[-1]
        final_sentence = f"Saya menemukan {first_part}, dan sebuah {last_part}."

if final_sentence:
    print(final_sentence)
    speech(final_sentence)
else:
    print("Tidak ada objek yang terdeteksi.")

