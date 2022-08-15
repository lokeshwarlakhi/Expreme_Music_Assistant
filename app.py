import cv2
import time
import numpy as np
from PIL import Image
import streamlit as st
import spotify_client as xy
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

emotion_dict = ["Angry", "Disgust", "Fear",
                "Happy", "Neutral", "Sad", "Surprise"]
classifier = load_model('expreme_engine.h5')


classifier.load_weights("expreme_engine.h5")

# load face
try:
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception:
    st.write("Error loading cascade classifiers")
global cnt
cnt = 0


class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.cnt = 0

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            image=img_gray, scaleFactor=1.3, minNeighbors=5)
        cnt = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(img=img, pt1=(x, y), pt2=(
                x + w, y + h), color=(136, 6, 138), thickness=2)
            roi_gray = img_gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48),
                                  interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                prediction = classifier.predict(roi)[0]
                maxindex = int(np.argmax(prediction))
                finalout = emotion_dict[maxindex]
                output = str(finalout)
            label_position = (x, y)
            cv2.putText(img, output, label_position,
                        cv2.FONT_ITALIC, 1, (28, 204, 248), 2)

        # self.cnt += 1
        # if(self.cnt == 40):
        #     xy.playsong(output)
        #     self.cnt =0
        #     return img
        return img


def main():

    # st.title("EXPRE-ME")
    activiteis = ["EXPRE-ME", "About"]
    choice = st.sidebar.selectbox("Select Activity", activiteis)
    st.sidebar.markdown(
        """ Built by Lokeswarlakhi   
            Mail me on lokeshwarlakhi@gmail.com""")

    if choice == "EXPRE-ME":
        img = Image.open('./expre-me-logo.png')
        st.image(img, width=700)
        st.header("Click on start and watch the magic happen!!")
        # st.write("Click on start to start the magic")
        cpq = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)
        # del(cpq)
        # cnt+=1

    elif choice == "About":
        img = Image.open('./expre-me-logo.png')
        st.image(img, width=700)
        st.subheader("About EXPREME")
        html_temp_about1 = """
        <div style="background-color:#cb1854;padding:10px;font-family: Verdana;">
            <h4 style="color:white;text-align:center;"> 
            A music player that helps users play tracks automatically without requiring much effort in searching songs . An emotion-based music player improves the listening experience for all music listeners and automates song selection.
            </h4>
        </div>
        </br>
        """
        st.markdown(html_temp_about1, unsafe_allow_html=True)

        html_temp4 = """
                <div style="background-color:#cb1854;padding:10px">
                <h4 style="color:white;text-align:center;"> </h4>
                <h4 style="color:white;text-align:center;">Thanks for Visiting</h4>
                </div>
                <br></br>
                """

        st.markdown(html_temp4, unsafe_allow_html=True)

    else:
        pass


# if __name__ == "__main__":
#     main()
