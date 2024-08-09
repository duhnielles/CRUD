import streamlit as st
import mysql.connector
import pandas as pd

# mydb = mysql.connector.connect(
#     host="127.0.0.1",
#     user="admin",
#     password="admin123",
#     database="crud_new"
# )

# mycursor=mydb.cursor()
# print("Connection established")

# Function to establish a database connection using secrets
def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["database"]["host"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            database=st.secrets["database"]["database"]
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        st.stop()  # Halt execution
    return None


# Function to fetch data from the database
def fetch_data():
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM phonebook")
            data = cursor.fetchall()
        finally:
            connection.close()
        return data
    else:
        return []


def main():
    st.title("BIZMATECH PHONEBOOK")

   
    option = st.sidebar.selectbox("Select an Operation", ("Add Info", "Update Info", "Delete Info", "Phonebook"))

    
    if option == "Add Info":
        st.subheader("Create a Record")
        company = st.text_input("Enter Company Name")
        industry = st.text_input("Enter Industry")
        contactNo = st.text_input("Enter Contact Number")
        email = st.text_input("Enter Email")
        contactPerson = st.text_input("Enter Contact Person")
        
        if st.button("Create"):
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                sql = "INSERT INTO phonebook(company, industry, contactNo, email, contactPerson) VALUES(%s, %s, %s, %s, %s)"
                val = (company, industry, contactNo, email, contactPerson)
                cursor.execute(sql, val)
                connection.commit()
                connection.close()
                st.success("Record Created Successfully!!!")

    elif option == "Update Info":
        st.subheader("Update a Record")
        id = st.number_input("Enter ID", min_value=1)
        company = st.text_input("Enter Company Name")
        industry = st.text_input("Enter Industry")
        contactNo = st.text_input("Enter Contact Number")
        email = st.text_input("Enter Email")
        contactPerson = st.text_input("Enter Contact Person")

        if st.button("Update"):
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                sql = "UPDATE phonebook SET company=%s, industry=%s, contactNo=%s, email=%s, contactPerson=%s WHERE id=%s"
                val = (company, industry, contactNo, email, contactPerson, id)
                cursor.execute(sql, val)
                connection.commit()
                connection.close()
                st.success("Record Updated Successfully!!!")

    elif option == "Delete Info":
        st.subheader("Delete a Record")
        id = st.number_input("Enter ID", min_value=1)

        if st.button("Delete"):
            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                sql = "DELETE FROM phonebook WHERE id=%s"
                val = (id,)
                cursor.execute(sql, val)
                connection.commit()
                connection.close()
                st.success("Record Deleted Successfully!!!")
                
    elif option == "Phonebook":
        st.subheader("Read Records")
        data = fetch_data()
        if data:
            columns = ["ID", "Company", "Industry", "Contact No", "Email", "Contact Person"]
            df = pd.DataFrame(data, columns=columns)
            st.dataframe(df)
            

if __name__ == "__main__":
    main()
