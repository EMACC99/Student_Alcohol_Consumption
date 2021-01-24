import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


@st.cache(persist = True)
def load_dataset(filename):
    data = pd.read_csv(f"Datasets/{filename}")
    return data

st.title("Student Alcohol Consumption")
st.sidebar.title("Student Alcohol Consumption")

st.markdown("Visualization of the datasets from the kaggle about Student Alcohol Consumtpion")
st.sidebar.markdown("Visualization of the datasets from the kaggle about Student Alcohol Consumtpion")


datasets = st.sidebar.selectbox(
    "Dataset:", ('Math', "Portuguese")
)

if datasets == "Math":
    dataset = load_dataset("student-mat.csv")
elif datasets == "Portuguese":
    dataset = load_dataset("student-por.csv")

st.markdown('## Grades by group')
st.sidebar.markdown("Grades")
if st.sidebar.checkbox("Flter grades by sex", True, key = "0"):
    sex = st.sidebar.selectbox("Sex", ("F", "M"))
    grade_by_sex = dataset[dataset["sex"] == sex]
    final_grade = grade_by_sex["G3"].value_counts()
    final_grade = pd.DataFrame({"Grade" : final_grade.index, "Count": final_grade.values})
    fig = px.pie(final_grade, values = "Count", names = "Grade")
    st.plotly_chart(fig)

else:
    final_grade = dataset["G3"].value_counts()
    final_grade = pd.DataFrame({"Grade" : final_grade.index, "Count": final_grade.values})
    fig = px.pie(final_grade, values = "Count", names = "Grade")
    st.plotly_chart(fig)


st.markdown('## Absences vs Grades')

absences = dataset[["absences", "G3"]]
fig = px.box(absences, x = "absences",y = "G3")
st.plotly_chart(fig)

st.markdown('## Absences vs Family relations')

absences = dataset[["absences", "famrel"]]
fig = px.box(absences, x = "absences", y = "famrel")
st.plotly_chart(fig)


st.markdown ('## Health vs Absences')
absences = dataset[["absences", "health"]]
fig = px.box(absences, x = "absences", y = "health")
st.plotly_chart(fig)


st.markdown ('## Weekly drinking vs Family relations')
drink = dataset[["famrel", "Dalc", "Walc"]]
drink["weekly_drink"] = drink["Dalc"] + drink["Walc"]
fig = px.box(drink, x = "famrel", y = "weekly_drink")
st.plotly_chart(fig)


st.markdown('## Go out vs Weekly Drinking')
drink = dataset[["goout", "Dalc", "Walc"]]
drink["weekly_drink"] = drink["Dalc"] + drink["Walc"]
fig = px.scatter(drink, x = "goout", y='weekly_drink')
st.plotly_chart(fig)

st.markdown('## Higher education')
education = dataset['higher'].value_counts()
education = pd.DataFrame({"Higher Education": education.index, "Count": education.values})
fig = px.bar(education, x = 'Higher Education', y = "Count")
st.plotly_chart(fig)
