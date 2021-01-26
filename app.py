from pandas.core.arrays.sparse import dtype
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

# @st.cache(persist= True)
def compute_svd(df):
    u,s,v = np.linalg.svd(df, full_matrices=False, compute_uv=True)
    return (u,s,v)

# @st.cache(persist = True)
def load_dataset(filename):
    data = pd.read_csv(f"Datasets/{filename}")
    return data

@st.cache(persist = True)
def load_labels(label_file):
    return np.genfromtxt(f"labels/{label_file}", delimiter=',')

st.title("Student Alcohol Consumption")
st.sidebar.title("Student Alcohol Consumption")

st.markdown("Visualization of the datasets from the kaggle about Student Alcohol Consumtpion")
st.sidebar.markdown("Visualization of the datasets from the kaggle about Student Alcohol Consumtpion")


datasets = st.sidebar.selectbox(
    "Dataset:", ('Math', "Portuguese")
)

if datasets == "Math":
    dataset = load_dataset("student-mat.csv")
    # encoded_dataset = load_dataset("mat_dataset_encoded.csv")
    reducted = np.genfromtxt('Datasets/mat_reduct.txt', delimiter =',')
    reducted_3d = np.genfromtxt("Datasets/mat_reduct_3d.txt", delimiter = ',', dtype=float)
    group_file = "mat"
elif datasets == "Portuguese":
    dataset = load_dataset("student-por.csv")
    encoded_dataset = load_dataset("por_dataset_encoded.csv")
    group_file = "por"
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
drink["weekly_drink"] = round((drink["Dalc"] + drink["Walc"])/2)
fig = px.box(drink, x = "famrel", y = "weekly_drink")
st.plotly_chart(fig)


st.markdown('## Go out vs Weekly Drinking')
drink = dataset[["goout", "Dalc", "Walc"]]
drink["weekly_drink"] = round((drink["Dalc"] + drink["Walc"])/2)
fig = px.scatter(drink, x = "goout", y='weekly_drink')
st.plotly_chart(fig)

st.markdown('## Higher education')
education = dataset['higher'].value_counts()
education = pd.DataFrame({"Higher Education": education.index, "Count": education.values})
fig = px.bar(education, x = 'Higher Education', y = "Count")
st.plotly_chart(fig)

st.markdown('## Plotting the Data')
# print(encoded_dataset)
data_reducted = np.array(reducted, dtype=float)
# data_reducted3d = np.array(reducted_3d, dtype=float)
# print(data_reducted3d)
# print(encoded_dataset)
# u,s,v = compute_svd(encoded_dataset)
# u,s,v = np.linalg.svd(encoded_dataset, full_matrices=False, compute_uv=True)
k = st.sidebar.slider("K", min_value=2, max_value=5, key = '1')
aux = f'{group_file}_{k}.txt'
labels = load_labels(aux)
if st.sidebar.checkbox("3D", True, key ='0'):
    # data_reducted = u[:, :3]@np.diag(s)[:3,:3]
    # data_reducted
    fig = px.scatter_3d(x = reducted_3d[:, 0], y = reducted_3d[:, 1],z = reducted_3d[:,2], color = labels)
    st.write(fig)

else:
# data_reducted = (u[:,:2]@np.diag(s)[:2, :2])
    print(data_reducted)
    fig = px.scatter(x = data_reducted[:, 0], y = data_reducted[:, 1], color = labels)
    st.plotly_chart(fig)


