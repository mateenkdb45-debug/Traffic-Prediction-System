from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

# Function to train the model
def train_vehicles_model(file_path, model_type="random_forest"):
    df = pd.read_csv(file_path)
    df['DateTime'] = pd.to_datetime(df['DateTime'], format="%d-%m-%Y %H:%M", errors='coerce')
    df = df.dropna(subset=['DateTime'])
    df['Hour'] = df['DateTime'].dt.hour
    df['Day'] = df['DateTime'].dt.day
    df['Month'] = df['DateTime'].dt.month
    df['Weekday'] = df['DateTime'].dt.weekday
    df['IsWeekend'] = df['Weekday'].apply(lambda x: 1 if x >= 5 else 0)
    df = df.drop(['DateTime', 'ID'], axis=1)

    X = df.drop('Vehicles', axis=1)
    y = df['Vehicles']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == "random_forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError("Unsupported model type")

    categorical_features = ['Junction']
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough'
    )
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    pipeline.fit(X_train, y_train)

    return pipeline

def make_predictions(model_pipeline, new_data):
    try:
        predictions = model_pipeline.predict(new_data)
        return predictions
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def predict_vehicles(request):
    file_path = r"media\traffic.csv"
    model_pipeline = train_vehicles_model(file_path, model_type="random_forest")

    if request.method == 'POST':
        st_hour = int(request.POST.get('start_hour'))
        end_hour = int(request.POST.get('end_hour'))
        st_day = int(request.POST.get('start_day'))
        end_day = int(request.POST.get('end_day'))
        st_month = int(request.POST.get('start_month'))
        end_month = int(request.POST.get('end_month'))
        st_week_day = int(request.POST.get('start_week_day'))
        end_week_day = int(request.POST.get('end_week_day'))

        # Prepare the new data for prediction
        new_data = pd.DataFrame({
            'Junction': ['Junction_1', 'Junction_2'],
            'Hour': [st_hour, end_hour],
            'Day': [st_day, end_day],
            'Month': [st_month, end_month],
            'Weekday': [st_week_day, end_week_day],
            'IsWeekend': [0, 1]
        })
        print(new_data)

        predictions = make_predictions(model_pipeline, new_data)
        print(predictions)
        for prediction in predictions:
            print(prediction)
        if predictions is not None:
            if predictions[0] <= 10 and predictions[1] <= 10:
                mark = "Green"
            elif 10 < predictions[0] <= 20 and 10 < predictions[1] <= 20:
                mark = "Yellow"
            else:
                mark = "Red"
            print(mark)    
        return render(request, 'users/task3.html', {'predictions': predictions, 'mark': mark})
    return render(request, 'users/task3.html')
