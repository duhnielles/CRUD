import mysql.connector
import streamlit as st
import pandas as pd

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin123",
    database="crud_new"
)

mycursor=mydb.cursor()
print("Connection established")

#main
def main():
    st.title("BIZMATECH PHONEBOOK")

    # Display Options for CRUD Operations
    option=st.sidebar.selectbox("Select an Operation",("Create","Read","Update","Delete"))
    # Perform Selected CRUD Operations
    if option=="Create":
        st.subheader("Create a Record")
        company=st.text_input("Enter Company Name")
        industry=st.text_input("Enter Industry")
        contactNo=st.text_input("Enter Contact Number")
        email=st.text_input("Enter Email")
        contactPerson=st.text_input("Enter Contact Person")
        
        if st.button("Create"):
            sql= "INSERT INTO phonebook(company, industry, contactNo, email, contactPerson) VALUES(%s, %s, %s, %s, %s)"
            val= (company, industry, contactNo, email, contactPerson)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Created Successfully!!!")

    elif option=="Read":
        st.subheader("Read Records")
        mycursor.execute("SELECT * FROM phonebook")
        result = mycursor.fetchall()

        # Define column names to display in the table
        columns = ["ID", "Company", "Industry", "Contact No", "Email", "Contact Person"]

        # Convert the result into a DataFrame
        df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame as a table
        st.dataframe(df)

    elif option=="Update":
        st.subheader("Update a Record")
        id=st.number_input("Enter ID", min_value=1)
        company=st.text_input("Enter Company Name")
        industry=st.text_input("Enter Industry")
        contactNo=st.text_input("Enter Contact Number")
        email=st.text_input("Enter Email")
        contactPerson=st.text_input("Enter Contact Person")
        if st.button("Update"):
            sql="UPDATE phonebook SET company=%s, industry=%s, contactNo=%s, email=%s, contactPerson=%s WHERE id=%s"
            val=(company, industry, contactNo, email, contactPerson, id)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Updated Successfully!!!")

    elif option=="Delete":
        st.subheader("Delete a Record")
        id=st.number_input("Enter ID", min_value=1)
        if st.button("Delete"):
            sql="DELETE FROM phonebook WHERE id=%s"
            val=(id,)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Deleted Successfully!!!")

if __name__ == "__main__":
    main()
