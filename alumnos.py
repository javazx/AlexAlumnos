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
        CREATE TABLE IF NOT EXISTS Alumno (
            id_alumno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            NombreAlumno TEXT(250) NOT NULL,
            EdadAlumno INTEGER NOT NULL,
            Semestre TEXT,
            Genero TEXT(1) NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Funciones CRUD


def add_alumno(nombre, edad, semestre, genero):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Alumno (NombreAlumno, EdadAlumno, Semestre, Genero) VALUES (?, ?, ?, ?)',
                   (nombre, edad, semestre, genero))
    conn.commit()
    conn.close()


def delete_alumno(id_alumno):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Alumno WHERE id_alumno = ?', (id_alumno,))
    conn.commit()
    conn.close()


def update_alumno(id_alumno, nombre, edad, semestre, genero):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Alumno
        SET NombreAlumno = ?, EdadAlumno = ?, Semestre = ?, Genero = ?
        WHERE id_alumno = ?
    ''', (nombre, edad, semestre, genero, id_alumno))
    conn.commit()
    conn.close()


def get_alumnos():
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Alumno')
    rows = cursor.fetchall()
    conn.close()
    return rows


# Crear la tabla al iniciar la aplicación
create_table()

# Interfaz de usuario con Streamlit
st.title('Gestión de Alumnos 👨‍🎓')

# Agregar logo
st.sidebar.image(
    'http://cbt2drmariojosemolinahenriquez.mx/assets/img/logo.jpg', width=250)
# Opciones de navegación
menu = ['Agregar Alumno', 'Actualizar Alumno',
        'Eliminar Alumno', 'Visualizar Datos']
choice = st.sidebar.selectbox('Menú', menu)

if choice == 'Agregar Alumno':
    st.subheader('Agregar Alumno')
    nombre = st.text_input('Nombre')
    edad = st.number_input('Edad', min_value=0)
    semestre = st.text_input('Semestre')
    genero = st.text_input('Genero')

    if st.button('Agregar'):
        add_alumno(nombre, edad, semestre, genero)
        st.success('Alumno agregado exitosamente')

elif choice == 'Actualizar Alumno':
    st.subheader('Actualizar Alumno')
    id_alumno = st.number_input('ID Alumno', min_value=1)
    nombre = st.text_input('Nombre')
    edad = st.number_input('Edad', min_value=1)
    semestre = st.text_input('Semestre')
    genero = st.text_input('Genero')

    if st.button('Actualizar'):
        update_alumno(id_alumno, nombre, edad, semestre, genero)
        st.success('Alumno actualizado exitosamente')

elif choice == 'Eliminar Alumno':
    st.subheader('Eliminar Alumno')
    id_alumno = st.number_input('ID Alumno', min_value=1)

    if st.button('Eliminar'):
        delete_alumno(id_alumno)
        st.success('Alumno eliminado exitosamente')

elif choice == 'Visualizar Datos':
    st.subheader('Visualizar Datos')
    alumnos = get_alumnos()
    if alumnos:
        df = pd.DataFrame(alumnos, columns=[
                          'ID', 'Nombre', 'Edad', 'Semestre', 'Genero'])
        st.dataframe(df)
    else:
        st.write('No hay datos para mostrar.')
