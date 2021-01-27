import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


@st.cache(persist = True)
def load_dataset(filename):
    data = pd.read_csv(f"Datasets/{filename}")
    return data

@st.cache(persist = True)
def load_labels(label_file):
    return np.genfromtxt(f"labels/{label_file}", delimiter=',')

st.title("Student Alcohol Consumption")
st.sidebar.title("Student Alcohol Consumption")

st.markdown("Visualizacion de los datasets de kaggle sobre Consumo de Alcohol en estudiantes")
st.sidebar.markdown("Visualizacion de los datasets de kaggle sobre Consumo de Alcohol en estudiantes")


datasets = st.sidebar.selectbox(
    "Dataset:", ('Matematicas', "Portugues")
)

if datasets == "Matematicas":
    dataset = load_dataset("student-mat.csv")
    reducted = np.genfromtxt('Datasets/mat_reduct.txt', delimiter =',')
    reducted_3d = np.genfromtxt("Datasets/mat_reduct_3d.txt", delimiter = ',', dtype=float)
    group_file = "mat"
elif datasets == "Portugues":
    dataset = load_dataset("student-por.csv")
    reducted = np.genfromtxt('Datasets/por_reduct_2d.txt', delimiter = ',')
    reducted_3d = np.genfromtxt('Datasets/por_reduct_3d.txt', delimiter = ',')   
    group_file = "por"
st.markdown('## Calificaciones por grupo')
st.sidebar.markdown("calificaiones")
if st.sidebar.checkbox("Calificaciones por sexo", True, key = "0"):
    sex = st.sidebar.selectbox("Sexo", ("M", "H"))
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


st.markdown('## Faltas contra Calificaciones')

absences = dataset[["absences", "G3"]]
fig = px.box(absences, x = "absences",y = "G3")
st.plotly_chart(fig)

st.markdown('## Faltas contra Relaciones familiares')

absences = dataset[["absences", "famrel"]]
fig = px.box(absences, x = "absences", y = "famrel")
st.plotly_chart(fig)


st.markdown ('## Salud contra Faltas')
absences = dataset[["absences", "health"]]
fig = px.box(absences, x = "absences", y = "health")
st.plotly_chart(fig)


st.markdown ('## Consumo a la semana vs Relaciones familiares')
drink = dataset[["famrel", "Dalc", "Walc"]]
drink["weekly_drink"] = round((drink["Dalc"] + drink["Walc"])/2)
fig = px.box(drink, x = "famrel", y = "weekly_drink")
st.plotly_chart(fig)


st.markdown('## Salir vs Consumo semanal')
drink = dataset[["goout", "Dalc", "Walc"]]
drink["weekly_drink"] = round((drink["Dalc"] + drink["Walc"])/2)
fig = px.scatter(drink, x = "goout", y='weekly_drink')
st.plotly_chart(fig)

st.markdown('## Educacion superior')
education = dataset['higher'].value_counts()
education = pd.DataFrame({"Higher Education": education.index, "Count": education.values})
fig = px.bar(education, x = 'Higher Education', y = "Count")
st.plotly_chart(fig)

st.markdown('## Graficando los datos')

data_reducted = np.array(reducted, dtype=float)

k = st.sidebar.slider("Numero de grupos (K)", min_value=2, max_value=5, key = '1')
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


