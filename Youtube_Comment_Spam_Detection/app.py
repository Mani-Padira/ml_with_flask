from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    df = pd.read_csv("Youtube-Spam-Dataset-2.csv")
    df_data = df[["CONTENT", "CLASS"]]

    df_x = df_data['CONTENT']
    df_y = df_data.CLASS

    cv = CountVectorizer()
    X = cv.fit_transform(df_x)

    X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.33, random_state=42)

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    if request.method == 'POST':
        comment = request.form['comment']
        data = [comment]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)

    return render_template('result.html', prediction=my_prediction)

if __name__ == '__main__':
    app.run(debug=True)
