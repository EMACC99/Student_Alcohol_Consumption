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



if st.sidebar.checkbox("Flter by sex", True):
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