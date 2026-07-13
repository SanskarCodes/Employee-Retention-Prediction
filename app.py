import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="📊",
    layout="wide"
)

model = pickle.load(open("model/best_model.pkl","rb"))
encoder = pickle.load(open("model/encoder.pkl","rb"))
scaler = pickle.load(open("model/scaler.pkl","rb"))

st.title("📊 Employee Attrition Prediction Platform")

st.markdown("""
Predict whether an employee is likely to leave the company using a Machine Learning model.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Employee Details")
    Age = st.slider("Age",18,60,30)
    Gender = st.selectbox(
        "Gender",
        ["Male","Female"]
    )
    Education = st.selectbox(
        "Education",
        [1,2,3,4,5]
    )
    EducationField = st.selectbox(
        "Education Field",
        [
            "Life Sciences",
            "Medical",
            "Marketing",
            "Technical Degree",
            "Other"
        ]
    )
    MaritalStatus = st.selectbox(
        "Marital Status",
        [
            "Single",
            "Married",
            "Divorced"
        ]
    )
    Department = st.selectbox(
        "Department",
        [
            "Research & Development",
            "Sales",
            "Human Resources"
        ]
    )

with col2:
    st.subheader("Job Details")
    JobRole = st.selectbox(
        "Job Role",
        [
            "Sales Executive",
            "Research Scientist",
            "Laboratory Technician",
            "Manufacturing Director",
            "Healthcare Representative",
            "Manager",
            "Research Director",
            "Human Resources",
            "Sales Representative"
        ]
    )
    BusinessTravel = st.selectbox(
        "Business Travel",
        [
            "Travel_Rarely",
            "Travel_Frequently",
            "Non-Travel"
        ]
    )
    JobLevel = st.slider("Job Level", 1, 5, 2)
    JobInvolvement = st.slider("Job Involvement", 1, 4, 3)
    JobSatisfaction = st.slider("Job Satisfaction", 1, 4, 3)
    EnvironmentSatisfaction = st.slider(
        "Environment Satisfaction", 1, 4, 3
    )
    WorkLifeBalance = st.slider(
        "Work Life Balance", 1, 4, 3
    )
    OverTime = st.selectbox(
        "Over Time",
        ["No", "Yes"]
    )
    



st.divider()
st.subheader("Salary & Experience")
col3, col4, col5 = st.columns(3)

with col3:
    DailyRate = st.number_input("Daily Rate", min_value=100, value=800)
    HourlyRate = st.number_input("Hourly Rate", min_value=30, value=60)
    MonthlyIncome = st.number_input("Monthly Income", min_value=1000, value=7000)
    MonthlyRate = st.number_input("Monthly Rate", min_value=1000, value=15000)

with col4:

    DistanceFromHome = st.number_input("Distance From Home", min_value=1, value=5)
    NumCompaniesWorked = st.number_input("Companies Worked", min_value=0, value=2)
    TotalWorkingYears = st.number_input("Total Working Years", min_value=0, value=10)
    YearsAtCompany = st.number_input("Years At Company", min_value=0, value=5)

with col5:
    YearsInCurrentRole = st.number_input("Years In Current Role", min_value=0, value=3)
    YearsSinceLastPromotion = st.number_input("Years Since Last Promotion", min_value=0, value=1)
    YearsWithCurrManager = st.number_input("Years With Current Manager", min_value=0, value=3)
    TrainingTimesLastYear = st.number_input("Training Times Last Year", min_value=0, value=2)


PercentSalaryHike = st.slider("Percent Salary Hike", 10, 30, 15)
PerformanceRating = st.selectbox("Performance Rating", [3, 4])
RelationshipSatisfaction = st.slider("Relationship Satisfaction", 1, 4, 3)
StockOptionLevel = st.selectbox("Stock Option Level", [0, 1, 2, 3])


predict = st.button("🔮 Predict Attrition", use_container_width=True)

if predict:
    Gender = 1 if Gender == "Male" else 0
    OverTime = 1 if OverTime == "Yes" else 0
    sample = pd.DataFrame({

    "Age": [Age],
    "DailyRate": [DailyRate],
    "DistanceFromHome": [DistanceFromHome],
    "Education": [Education],
    "EnvironmentSatisfaction": [EnvironmentSatisfaction],
    "Gender": [Gender],
    "HourlyRate": [HourlyRate],
    "JobInvolvement": [JobInvolvement],
    "JobLevel": [JobLevel],
    "JobSatisfaction": [JobSatisfaction],
    "MonthlyIncome": [MonthlyIncome],
    "MonthlyRate": [MonthlyRate],
    "NumCompaniesWorked": [NumCompaniesWorked],
    "OverTime": [OverTime],
    "PercentSalaryHike": [PercentSalaryHike],
    "PerformanceRating": [PerformanceRating],
    "RelationshipSatisfaction": [RelationshipSatisfaction],
    "StockOptionLevel": [StockOptionLevel],
    "TotalWorkingYears": [TotalWorkingYears],
    "TrainingTimesLastYear": [TrainingTimesLastYear],
    "WorkLifeBalance": [WorkLifeBalance],
    "YearsAtCompany": [YearsAtCompany],
    "YearsInCurrentRole": [YearsInCurrentRole],
    "YearsSinceLastPromotion": [YearsSinceLastPromotion],
    "YearsWithCurrManager": [YearsWithCurrManager],
    "Department": [Department],
    "EducationField": [EducationField],
    "JobRole": [JobRole],
    "MaritalStatus": [MaritalStatus],
    "BusinessTravel": [BusinessTravel]
    })

    cat_cols = [
    "Department",
    "EducationField",
    "JobRole",
    "MaritalStatus",
    "BusinessTravel"
    ]

    encoded = encoder.transform(sample[cat_cols])
    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(),
        index=sample.index
    )
    sample = sample.drop(columns=cat_cols)
    sample = pd.concat([sample, encoded_df], axis=1)

    num_cols = list(scaler.feature_names_in_)
    sample[num_cols] = scaler.transform(sample[num_cols])

    sample = sample.reindex(
    columns=model.feature_names_in_,
    fill_value=0
    )

    prediction = model.predict(sample)
    probability = model.predict_proba(sample)

    if prediction[0] == 1:
        st.error("⚠️ Employee is likely to leave the company.")
    else:
        st.success("✅ Employee is likely to stay with the company.")
    st.subheader("Prediction Confidence")
    st.write(f"**Probability of Staying:** {probability[0][0] * 100:.2f}%")
    st.write(f"**Probability of Leaving:** {probability[0][1] * 100:.2f}%")

