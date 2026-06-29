import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from django.shortcuts import render
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA

file_path = r'media\traffic.csv'

def train_vehicles_model(request):
    try:
        df = pd.read_csv(file_path)
        if 'DateTime' not in df.columns:
            raise KeyError("The 'DateTime' column is missing from the dataset.")
        df['DateTime'] = pd.to_datetime(df['DateTime'], format="%d-%m-%Y %H:%M", errors='coerce')
        df = df.dropna(subset=['DateTime'])
        df = df.sort_values('DateTime')

        df = df[['DateTime', 'Vehicles']].dropna()
        df.set_index('DateTime', inplace=True)

        split_idx = int(len(df) * 0.8)
        train, test = df[:split_idx], df[split_idx:]

        model = ARIMA(train['Vehicles'], order=(5,1,0))
        model_fit = model.fit()

        predictions = model_fit.forecast(steps=len(test))
        predictions.index = test.index

        y_test = test['Vehicles']
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        plt.figure(figsize=(10, 6))
        sns.lineplot(x=y_test.index, y=y_test.values, label='Actual', color='blue')
        sns.lineplot(x=predictions.index, y=predictions, label='Predicted', color='orange')
        plt.title("Actual vs Predicted Vehicle Counts (ARIMA)")
        plt.xlabel("Time")
        plt.ylabel("Vehicle Count")
        plt.legend()
        plt.tight_layout()
        plt.show()

        residuals = y_test - predictions
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=predictions, y=residuals)
        plt.axhline(y=0, color='red', linestyle='--')
        plt.title("Residuals vs Predicted Values")
        plt.xlabel("Predicted")
        plt.ylabel("Residuals")
        plt.tight_layout()
        plt.show()

        context = {
            'mae': mae,
            'mse': mse,
            'r2': r2,
        }

        return render(request, 'users/task2.html', context)

    except Exception as e:
        return render(request, 'users/task2.html', {'error': str(e)})




def training(request):
    try:
        mae, mse, r2 = train_vehicles_model(request)
        context = {
            'mae': mae,
            'mse': mse,
            'r2': r2,
        }
        print(context)

        return render(request, 'users/task1.html', context)

    except Exception as e:
        print(f"Error in training function: {e}")
        return render(request, 'users/task1.html', {'error': str(e)})
