import calendar
from datetime import datetime
import streamlit as st;
from streamlit_option_menu import option_menu
import plotly.graph_objects as go;


incomes=["Salary", "Blog", "Otherincome"]
expenses=["Rent", "Utilities", "Groceries", "Car", "Other expenses", "Saving"]
Currency="Rupees"
page_title="Income expenses Tracker"
page_icon=":money_with_wings:"
layout="centered"


st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

years= [datetime.today().year, datetime.today().year +1]
months = list(calendar.month_name[1:])

#Hide-streamlit style

hide_st_style="""
         <style>
         #MainMenu {visibility:hidden;}
         footer {visibility: hidden;}
         header {visibility: hidden;}
         </style>

"""
st.markdown(hide_st_style, unsafe_allow_html=True)

#Navigation bar
selected= option_menu(
    menu_title=None,
    options=['Data entry', "Data visualisation"],
    icons=["pencil-fill","bar-chart-fill"], # https://icons.getbootstrap.com/
    orientation="horizontal",
)



if selected=="Data entry":
    st.header(f"Data entry in {Currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select month:", months, key="month")
        col2.selectbox("Select Year:", years, key="year")

        "--"

        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}", min_value=0, format='%i', step=10,key=income)
        with st.expander("Expenses"):
            for expenses in expenses:
                st.number_input(f"{expenses}", min_value=0, format="%i", step=10, key=expenses)
        with st.expander("Comment"):
            comment=st.text_area(" ",placeholder="Enter your comment here")

        "--"

        submitted=st.form_submit_button("Save data")
        if submitted:
            period= str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes= {income: st.session_state[income] for income  in incomes}
            expenses={expense: st.session_state[expense] for expense in expenses}
            #TODO: insert values in database:

            st.write(f"incomes: {incomes}")
            st.write(f"expenses: {expenses}")
            st.success("data saved!")


#--Plot periods--
if selected== "Data visualisation":
    st.header("Data visualisation")
    with st.form("saved_periods"):
        #TODO Get period from database
        period= st.selectbox("Select Period:", ["2023", "2024"])
        submitted=st.form_submit_button("Plot period")
        if submitted:
            #TODO get data from database

            comment="Uploaded successfully"
            incomes={'Salary':1500, 'Blog':50, 'Other expenses':10}
            expenses={'Rent':600, 'Utilities':200, 'Groceries':300, 'Car': 100 , 'Other expenses': 50 , 'Savings': 10} 

            #Create metrics
            total_income= sum(incomes.values())
            total_expenses= sum(expenses.values())
            remaining_budget= total_income- total_expenses
            col1, col2, col3= st.columns(3)
            col1.metric("Total_income", f"{total_income}{Currency}")
            col2.metric("Total_expense", f"{total_expenses}{Currency}")
            col3.metric("remaining_budget", f"{remaining_budget}{Currency}")
           
            st.text(f"Comment: {comment}")

# Create sankey chart

            label = list(incomes.keys()) +  ["Total Income"] + list (expenses.keys()) 
            source= list(range(len(incomes))) + [len (incomes)] *len(expenses) 

            target = [len(incomes)] * len(incomes) + [label.index (expense) for expense in expenses.keys()] 
            
            value = list(incomes.values()) + list (expenses.values())

# Data to dict, dict to sankey

            link = dict(source=source, target=target, value=value)

            node = dict(label=label, pad=20, thickness=30, color="#E694FF")

            data = go.Sankey (link=link, node=node)

# Plot it!

            fig = go.Figure(data)

            fig.update_layout (margin=dict(l=0, r=0, t=5, b=5))

            st.plotly_chart(fig, use_container_width=True)

