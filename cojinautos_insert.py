import os
import mysql.connector
from mysql.connector import Error
import streamlit as st

def insert_data_cojinautos(df, table_name='clientes_servicios'):
    """Inserta los datos combinados de clientes y servicios en la tabla Clientes_Servicios."""
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            st.success("Connected to the database successfully.")
            cursor = connection.cursor()
            
            # Query de inserción
            insert_query = f"""
            INSERT INTO {table_name} (IDCustomer, CustomerName, Phone, Email, Address, RegistrationDate, IDService, TypeOfService, DateOfService, MaterialUsed, Cost, ResponsibleEmployee)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            df_data = df[['IDCustomer', 'CustomerName', 'Phone', 'Email', 'Address', 'RegistrationDate', 'IDService', 'TypeOfService', 'DateOfService', 'MaterialUsed', 'Cost', 'ResponsibleEmployee']].to_records(index=False).tolist()

            # Ejecutar la consulta en modo de inserción masiva
            cursor.executemany(insert_query, df_data)

            # Confirmar la transacción
            connection.commit()

            st.success(f"{cursor.rowcount} rows inserted successfully into Clientes_Servicios.")

    except Error as e:
        st.write(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


