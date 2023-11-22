import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify, make_response
from io import BytesIO
import base64
import pandas as pd
import os
from datetime import datetime, timedelta
import random
import regex as re
import numpy as np
from datetime import datetime

app = Flask(__name__) 

df_s=pd.DataFrame()
for i in range(12,22):
    temp_df = pd.read_csv(f"Exchange_Rate_Report_20{i}.csv")
    df_s=pd.concat([df_s,temp_df], ignore_index=True)
df_s.set_index("Date")
df_s.index = pd.to_datetime(df_s.index)
df_s['Date'] = pd.to_datetime(df_s['Date'], format='%d-%b-%y')

df_s['Day'] = df_s['Date'].dt.day
df_s['Month'] = df_s['Date'].dt.month
df_s['Year'] = df_s['Date'].dt.year

df_s.columns = [re.sub(r'\s+', ' ', col) for col in df_s.columns]
df_s.columns = df_s.columns.str.strip()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/get_plot', methods=['GET','POST'])
def get_plot():

    if request.method =='POST':
        currency1 = request.form['currency1']
        currency2 = request.form['currency2']
        duration = request.form['duration']
        start_year = request.form['startDate']
        end_year  = request.form['endDate']

        df = df_s[(df_s['Year'] >= int(start_year)) & (df_s['Year'] <= int(end_year))]
        highest_rate = df[currency2].max()
        lowest_rate = df[currency2].min()
        average_rate = df[currency2].mean()


        file_path = "static/my_plot.png"
        if os.path.exists(file_path) :
            os.remove(file_path)
            print("hello")

        if(duration =="Yearly"):
            df_agg = df.groupby(['Date', 'Year'])[currency2].mean().reset_index()
    
            pivot_df = df_agg.pivot(index='Date', columns='Year', values=currency2)
            # if (currency1 != "U.S. dollar (USD)"):
            #     pivot_df = df_agg.pivot(index='Date',)

            original_missing_mask = pivot_df.isna()

            window_size = 50

            # Use rolling mean to calculate the mean of the neighboring 10 data points for each column
            pivot_df = pivot_df.apply(lambda col: col.fillna(col.rolling(window=window_size, min_periods=1).mean()))

            plt.figure(figsize=(12, 8))

            for col in pivot_df.columns:
                year_label = col

                plt.plot(pivot_df.index[original_missing_mask[col]], pivot_df[col][original_missing_mask[col]], 'o', label=f'Year {year_label} (Original Missing)', linestyle='None', markersize=1, color='red')

                plt.plot(pivot_df.index, pivot_df[col], label=f'Year {year_label} (Interpolated)')

            plt.xlabel('Year')
            plt.ylabel(currency2)
            plt.title(f'Line Plot for {currency2} - Yearly')

            plt.legend()

            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

        elif(duration == "Weekly"):
            #code
            print()
        
        elif(duration =="Quaterly"):
            #code
            print()

        elif(duration =="Monthly"):
            #cpde
            print()
        



        

        

        
        
        
        
        

        
    
        

        random_query_parameter = random.randint(1, 1000000)

        content = render_template('index.html', plot_url=file_path, random_query_parameter=random_query_parameter, highest_rate= highest_rate, 
        lowest_rate = lowest_rate, average_rate = average_rate )

        # Create a response object
        response = make_response(content)
        
        return response


        
    else:
        print("in post")
        return render_template('index.html')

app.secret_key= "its a secret"

if __name__ == '__main__':
    app.run(debug=True)

