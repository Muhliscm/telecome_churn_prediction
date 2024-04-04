from flask import Blueprint, render_template, request, flash
import pandas as pd
from .utils import load_data, predict

views = Blueprint('views', __name__)

data = load_data()

cat_columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
               'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
               'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
               'PaperlessBilling', 'PaymentMethod']

input_options = {}
for col in cat_columns:
    unique_list = data[col].unique()
    input_options.update({col: unique_list})

all_columns = [col for col in data.columns if col != "Churn"]

pd.DataFrame()


@views.route("/home", methods=["GET", "POST"])
@views.route("/", methods=["GET", "POST"])
def home():
    outputs = []
    if request.method == "POST":
        gender = request.form.get('gender')
        senior_citizen = request.form.get('SeniorCitizen')
        partner = request.form.get('Partner')
        dependents = request.form.get('Dependents')
        tenure = request.form.get('tenure')
        phone_service = request.form.get('PhoneService')
        multiple_lines = request.form.get('MultipleLines')
        internet_service = request.form.get('InternetService')
        online_security = request.form.get('OnlineSecurity')
        online_backup = request.form.get('OnlineBackup')
        device_protection = request.form.get('DeviceProtection')
        tech_support = request.form.get('TechSupport')
        streaming_tv = request.form.get('StreamingTV')
        streaming_movies = request.form.get('StreamingMovies')
        contract = request.form.get('Contract')
        paperless_billing = request.form.get('PaperlessBilling')
        payment_method = request.form.get('PaymentMethod')
        monthly_charges = request.form.get('MonthlyCharges')
        total_charges = request.form.get('TotalCharges')

        if not tenure or not monthly_charges or not total_charges:
            flash("Fill All Columns", category="error")
        else:
            flash("Your Query Submitted", category="success")

            data_dict = {
                'gender': [gender],
                'SeniorCitizen': [int(senior_citizen)],
                'Partner': [partner],
                'Dependents': [dependents],
                'tenure': [int(tenure)],
                'PhoneService': [phone_service],
                'MultipleLines': [multiple_lines],
                'InternetService': [internet_service],
                'OnlineSecurity': [online_security],
                'OnlineBackup': [online_backup],
                'DeviceProtection': [device_protection],
                'TechSupport': [tech_support],
                'StreamingTV': [streaming_tv],
                'StreamingMovies': [streaming_movies],
                'Contract': [contract],
                'PaperlessBilling': [paperless_billing],
                'PaymentMethod': [payment_method],
                'MonthlyCharges': [float(monthly_charges)],
                'TotalCharges': [float(total_charges)],
            }
            new_df = pd.DataFrame(data_dict)
            final_df = pd.concat([data, new_df], ignore_index=True)
            dummy_df = pd.get_dummies(final_df, drop_first=True)
            pred_data = dummy_df.tail(1)
            prediction, probability = predict(pred_data)

            if prediction == 1:
                o1 = "This customer is likely to be churned!!"
                probability = probability[-1]
                o2 = "Confidence: {}".format(probability*100)
            else:
                o1 = "This customer is likely to continue!!"
                probability = probability[0]
                o2 = "Confidence: {}".format(probability*100)

            outputs = [o1, o2]

    return render_template('home.html', all_columns=all_columns, input_options=input_options, outputs=outputs)
