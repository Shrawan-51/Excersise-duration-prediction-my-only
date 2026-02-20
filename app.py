from flask import Flask, render_template, request
import pandas as pd
import pickle

# Load pre-trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    # Default values for each field (empty string at start)
    mode = gender = age = height = weight = calories = heart_rate = body_temp = ''
    
    if request.method == 'POST':
        # Grab all form values and keep them
        mode = request.form['mode']
        gender = request.form['gender']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        calories = request.form['calories']

        if mode == 'walking':
            heart_rate = 90
            body_temp = 38
        elif mode == 'running':
            heart_rate = 120
            body_temp = 39
        else:
            heart_rate = request.form.get('heart_rate', '')
            body_temp = request.form.get('body_temp', '')

        # Prepare input for model (make sure all numbers)
        gender_val = 1 if gender == 'male' else 0
        input_values = [gender_val, age, height, weight, heart_rate, body_temp, calories]
        input_df = pd.DataFrame([input_values], columns=['Gender','Age','Height','Weight','Heart_Rate','Body_Temp','Calories'])
        # Safe casting to float; you can add error handling as needed
        input_df = input_df.astype(float)
        duration = model.predict(input_df)[0]
        prediction = f"Recommended Duration: {duration:.2f} minutes"

    return render_template(
        'form.html',
        prediction=prediction,
        mode=mode, gender=gender, age=age, height=height, weight=weight,
        calories=calories, heart_rate=heart_rate, body_temp=body_temp
    )

if __name__ == '__main__':
    app.run(debug=True)
