pip install seaborn

# Importing libraries
import streamlit as st
import pandas as pd
import time
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

# Model denfnition
llm = HuggingFaceEndpoint(repo_id="openai/gpt-oss-20b", task="text-generation")
model = ChatHuggingFace(llm = llm)

# Intialization of key values in session states
if "text" not in st.session_state:
    st.session_state.text = ""
if "checked" not in st.session_state:
    st.session_state.checked = False
if "show_box" not in st.session_state:
    st.session_state.show_box = False
if "student_answer" not in st.session_state:
    st.session_state.student_answer = ""
if "edited_df_marks" not in st.session_state:
    st.session_state.edited_df_marks = None
if "second_box" not in st.session_state:
    st.session_state.second_box = False
if "final" not in st.session_state:
    st.session_state.final = False
if "am" not in st.session_state:
    st.session_state.am = 0.0



# Defining function of typing animation
def type_text(text, speed=0.05):
    placeholder = st.empty() #Reserves a spot in the Streamlit app to update text dynamically #Inserts a container into your app that can be used to hold a single element
    typed = "" # stores text
    for char in text:
        typed += char
        placeholder.markdown(typed) #Display string formatted as Markdown.
        time.sleep(speed) #Pauses to create the typing effect

# Loading all required datasets
data = pd.read_csv("data.csv")
correct_class = pd.read_csv("class_mark.csv")
marks = pd.read_csv("marks.csv")
marks_answer = pd.read_csv("marks_answer.csv")
final = pd.read_csv("final.csv")
final_answer = pd.read_csv("final_answer.csv")

st.header("Finding mean of grouped data using assumed mean method")
st.subheader("Finding Mid point of Class Interval")
st.markdown("In this lesson, we are going to find mean of a grouped data (data with class intervals) using assumed mean method. Look at the table below, which contains number of students scored marks in each marks range in mathematics test.")


##--------------------- Student Class Interval----------------------##

if st.session_state.checked == False or st.session_state.checked == True:
    st.table(data)
    st.markdown("Recall what is class mark from class 9? And write class mark for each class interval in table below."
    "  Note : Double click each cell to type the value of class interval.")
    edited_df_intervals = st.data_editor(
    data,
    disabled=["Class Interval","Number of students"],
    use_container_width=True, 
    #If this is True (default), Streamlit sets the width of the data editor to match the width of the parent container. If this is False, Streamlit sets the data editor's width according to width.
    column_config={
        "Your Answer": st.column_config.NumberColumn("Your Answer")
    },
)


# Checking button of class marks
if st.session_state.checked == False:
 if st.button("Check Answer", key ="class_marks_check"):

    if edited_df_intervals.equals(correct_class): #Test whether two objects contain the same elements.
            st.success("Correct Class Marks. Recall from class 9, Class Mark is midpoint of class interval, which is, average of upper limit and lower limit of class interval.")
            st.code("""
                    Recall from class 9, Class Mark is midpoint of class interval, which is, 

                    average of upper limit and lower limit of class interval.
                    
                    class mark = (upper limit + lower limit)/2

                    """)
            st.session_state.checked = True
    else:
            st.error("Some answers are incorrect or missing.")
            st.write("Your answer:")
            st.dataframe(edited_df_intervals)
            st.write("Correct answer:")
            st.dataframe(correct_class)
            st.session_state.checked = True
            st.code("""Recall from class 9, Class Mark is midpoint of class interval, which is, 

                    average of upper limit and lower limit of class interval.
                    
                    class mark = (upper limit + lower limit)/2
                    
                    """)



if st.session_state.show_box == False and st.session_state.checked == True :
       st.subheader("What is assumed mean?")
       type_text(" We know how to found average of grouped data using direct method; but how we can found average of this grouped data using method of assumed mean. But before that, let's have look at what is assumed mean? For example take marks of 5 students in mathematics : ")
    
       st.table(marks)

       type_text (" If we just guess mean of these five marks is 40, then we need to know how much given marks are away from the gussed mean?")
       st.markdown("Write the Actual Marks - Assumed Mean.  Note : Double click each cell to write values")
       st.session_state.edited_df_marks = st.data_editor(marks,
       disabled=["student_name", "marks"],
       use_container_width=True, #If this is True (default), Streamlit sets the width of the data editor to match the width of the parent container. If this is False, Streamlit sets the data editor's width according to width.
       column_config={
        "Your Answer": st.column_config.NumberColumn("Your Answer")
       })
       st.session_state.show_box = True
if st.session_state.show_box == True or st.session_state.second_box == True:
  if st.button("Check Your Answer",key="marks_answer_check"):
        if st.session_state.edited_df_marks.equals(marks_answer): #Test whether two objects contain the same elements.
            st.success("Correct differences")
            st.markdown("""Here, we can see marks of Rahul is 10 more than assumed mean and marks of Shyam is 10 less than assumed mean. So, these both distances from assumed mean can cancel each other. So, We now need to this 5 more marks of Ratul from assumed mean equally among all five students.
                        
            Now, actual mean = 40 + 5/5 = 40 + 1 = 41 Marks""")
            st.session_state.second_box = True
        else:
            st.error("Look at your answers again")
            st.write("Your answer:")
            st.dataframe(st.session_state.edited_df_marks)
            st.write("Correct answer:")
            st.dataframe(marks_answer)
            st.markdown("""Here, we can see marks of Rahul is 10 more than assumed mean and marks of Shyam is 10 less than assumed mean. So, these both distances from assumed mean can cancel each other. So, We now need to this 5 more marks of Ratul from assumed mean equally among all five students.
                        
            Now, actual mean = 40 + 5/5 = 40 + 1 = 41 Marks""")
            st.session_state.second_box = True
            
            

if st.session_state.second_box == True:
    st.subheader("How to use assumed mean to find mean of grouped data?")
    st.write("Now you know what does assumed mean do? Scroll up and by looking at class marks, can you give idea how to find mean of grouped data using assumed mean?")
    st.text_input("Enter your thoughts:", key="student_answer")
    if st.button("Submit your thoughts",key="student_thoughts"):
      st.spinner("Reading your thoughts")
      prompt = """ Context :  A student of class 10 is going to knows how to found mean of grouped data using direct method and now is going to learn how to find average using assumed mean, so, student is going to give some ideas on how to find mean of grouped data, but student do not know about any method. You have to listen student ideas and give your feedback. You do not have to give any method name or anything. Note : Do not show your thinking, you are directly interacting with student, so act like a teacher.Now look at the student's answer and give feedback. """ + "Student answer: " + st.session_state.student_answer
      result =  model.invoke(prompt)
      st.write(result.content)
      st.session_state.final = True

if st.session_state.final == True:
    st.subheader("Try with different assumed means!")
    st.table(final)
    st.markdown("Now, you will have to choose an assumed mean for this grouped data, based on that another table and a graph will show up, look at those carefully and try to understand it.")
    assumed_mean = st.number_input("Enter your assumed mean", format="%.2f",key ="am", min_value=0.0, step=None)
    if st.session_state.am == assumed_mean:
      final["Deviation = Class Mark - Assumed Mean"] = final["Class Mark"].apply(lambda x  : x - assumed_mean)
      final["Deviation*Frequency"] = final["Deviation = Class Mark - Assumed Mean"] * final["Number of students"]
      z = final["Class Mark"] + final["Deviation = Class Mark - Assumed Mean"]
      fig, ax = plt.subplots()
      sns.scatterplot(x = final["Class Mark"],y=z,label="Deviation")
      sns.scatterplot(x = final["Class Mark"],y=final["Class Mark"],label="Class Mark")
      ax.legend()
      st.pyplot(fig)
      st.table(final)
      total_dev = np.sum(final["Deviation*Frequency"])
      mean_dev = total_dev/np.sum(final["Number of students"])
      final_mean = assumed_mean+mean_dev

      st.code(f"""

          ### Mean by Assumed Mean Method

          Sum of toal deviations is : 
                  
          Sum of Deviation * Frequency of each class interval, 

          = {total_dev}. 
                  
          Mean of deviations is  :
                  
          Sum of toal deviations/Total number of students
          
          = {total_dev}/30, 
                  
          = {mean_dev}
          
         Now, actual mean = assumed mean + deviated mean

         = {assumed_mean}+({mean_dev})

        = {final_mean}
""")
      




      
            


