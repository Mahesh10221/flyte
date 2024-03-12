from flask import Flask, render_template
import streamlit as st
from flask_cors import CORS
import pickle
import pandas as pd

model = pickle.load(open('flight_rf.pkl', 'rb'))

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        dep_time = request.form['Dep_Time']
        Journey_day = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").day
        Journey_month = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").month
        Departure_hour = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").hour
        Departure_min = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").minute

        arrival_time = request.form['Arrival_Time']
        Arrival_hour = pd.to_datetime(arrival_time, format="%Y-%m-%dT%H:%M").hour
        Arrival_min = pd.to_datetime(arrival_time, format="%Y-%m-%dT%H:%M").minute

        Total_stops = int(request.form['stops'])

        dur_hour = abs(Arrival_hour - Departure_hour)
        dur_min = abs(Arrival_min - Departure_min)

        airline = request.form['airline']
        airline_map = {
            'Jet Airways': 'Jet_Airways',
            'IndiGo': 'IndiGo',
            'Air India': 'Air_India',
            'Multiple carriers': 'Multiple_carriers',
            'SpiceJet': 'SpiceJet',
            'Vistara': 'Vistara',
            'GoAir': 'GoAir',
            'Multiple carriers Premium economy': 'Multiple_carriers_Premium_economy',
            'Jet Airways Business': 'Jet_Airways_Business',
            'Vistara Premium economy': 'Vistara_Premium_economy',
            'Trujet': 'Trujet'
        }
        airline_column = airline_map.get(airline, 'Unknown')
        airline_columns = ['Jet_Airways', 'IndiGo', 'Air_India', 'Multiple_carriers', 'SpiceJet', 'Vistara', 'GoAir',
                           'Multiple_carriers_Premium_economy', 'Jet_Airways_Business', 'Vistara_Premium_economy',
                           'Trujet']
        airline_values = [0] * len(airline_columns)
        if airline_column in airline_columns:
            index = airline_columns.index(airline_column)
            airline_values[index] = 1

        source = request.form["Source"]
        source_map = {'Delhi': 's_Delhi', 'Kolkata': 's_Kolkata', 'Mumbai': 's_Mumbai', 'Chennai': 's_Chennai'}
        source_column = source_map.get(source, 'Unknown')
        source_columns = ['s_Delhi', 's_Kolkata', 's_Mumbai', 's_Chennai']
        source_values = [0] * len(source_columns)
        if source_column in source_columns:
            index = source_columns.index(source_column)
            source_values[index] = 1

        destination = request.form["Destination"]
        destination_map = {'Cochin': 'd_Cochin', 'Delhi': 'd_Delhi', 'Hyderabad': 'd_Hyderabad', 'Kolkata': 'd_Kolkata'}
        destination_column = destination_map.get(destination, 'Unknown')
        destination_columns = ['d_Cochin', 'd_Delhi', 'd_Hyderabad', 'd_Kolkata']
        destination_values = [0] * len(destination_columns)
        if destination_column in destination_columns:
            index = destination_columns.index(destination_column)
            destination_values[index] = 1

        input_data = [
            Total_stops, Journey_day, Journey_month, Departure_hour, Departure_min, Arrival_hour, Arrival_min,
            dur_hour, dur_min
        ] + airline_values + source_values + destination_values

        output = model.predict([input_data])[0]
        output = round(output, 2)
        return render_template('home.html', predictions='You will have to Pay approx Rs. {}'.format(output))

if __name__ == '__main__':
    app.run(debug=True)
