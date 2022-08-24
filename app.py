from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
import cv2
from utils.utils import gen_frames 
from faceAnalyser.emotionrecognition import EmotionRecognition
from userSentiment.textsentiment import UserSentimentAnalysis

app = Flask(__name__)
camera = cv2.VideoCapture(0)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/about',methods = ['GET', 'POST'])
def about():
    return render_template('about_page.html')

@app.route('/depression-analysis',methods = ['GET', 'POST'])
def depressionanalysis():
    face_analysis = EmotionRecognition(camera)
    user_sentiment = UserSentimentAnalysis()

    if face_analysis and user_sentiment:
        my_prediction = face_analysis and user_sentiment
        return render_template('result.html', prediction=my_prediction)
        # return jsonify({'Result': "You have depression. Don't panic , You should consult a doctor"})
    
    if face_analysis or user_sentiment:
        return jsonify({'Result': "You have mild depression , You should consult a doctor"})
    
    result = face_analysis and user_sentiment
    return render_template('result.html', prediction=result)
    # return jsonify({'Result': "You don't have depression"})

@app.route('/video-feed', methods=['GET', 'POST'])
def video_feed():
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)