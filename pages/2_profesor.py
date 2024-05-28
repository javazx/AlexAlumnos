import streamlit as st
import sqlite3
import pandas as pd

# Función para conectar con la base de datos SQLite


def init_connection():
    return sqlite3.connect('Alexander.db')

# Función para crear la tabla si no existe


def create_table():
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profesor (
            id_profesor INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            NombreProfesor TEXT(250) NOT NULL,
            Materia TEXT(250) NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Funciones CRUD


def add_profesor(nombre, materia):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Profesor (NombreProfesor, Materia) VALUES (?, ?)',
                   (nombre, materia))
    conn.commit()
    conn.close()


def delete_profesor(id_profesor):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM Profesor WHERE id_profesor = ?', (id_profesor,))
    conn.commit()
    conn.close()


def update_profesor(id_profesor, nombre, materia):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Profesor
        SET NombreProfesor = ?, Materia = ?
        WHERE id_profesor = ?
    ''', (nombre, materia, id_profesor))
    conn.commit()
    conn.close()


def get_profesor():
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Profesor')
    rows = cursor.fetchall()
    conn.close()
    return rows


# Crear la tabla al iniciar la aplicación
create_table()

# Interfaz de usuario con Streamlit
st.title('Gestión de Profesores 👨‍🎓')

# Agregar logo
st.sidebar.image(
    'https://pbs.twimg.com/profile_images/1588650015936987144/txXevZFe_400x400.jpg', width=250)
# Opciones de navegación
menu = ['Agregar Profesor', 'Actualizar Profesor',
        'Eliminar Profesor', 'Visualizar Datos Profesor']
choice = st.sidebar.selectbox('Menú', menu)

if choice == 'Agregar Profesor':
    st.subheader('Agregar Profesor')
    nombre = st.text_input('Nombre')
    materia = st.text_input('Materia')

    if st.button('Agregar'):
        add_profesor(nombre, materia)
        st.success('Profesor agregado exitosamente')

elif choice == 'Actualizar Profesor':
    st.subheader('Actualizar Profesor')
    id_profesor = st.number_input('ID Profesor', min_value=1)
    nombre = st.text_input('Nombre')
    materia = st.text_input('Materia')

    if st.button('Actualizar'):
        update_profesor(id_profesor, nombre, materia)
        st.success('Profesor actualizado exitosamente')

elif choice == 'Eliminar Profesor':
    st.subheader('Eliminar Profesor')
    id_profesor = st.number_input('ID Profesor', min_value=1)

    if st.button('Eliminar'):
        delete_profesor(id_profesor)
        st.success('Profesor eliminado exitosamente')

elif choice == 'Visualizar Datos Profesor':
    st.subheader('Visualizar Datos Profesor')
    profesor = get_profesor()
    if profesor:
        df = pd.DataFrame(profesor, columns=[
                          'ID', 'Nombre', 'Materia'])
        st.dataframe(df)
    else:
        st.write('No hay datos para mostrar.')
