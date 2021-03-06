import pandas as pd 
import numpy as np 
import streamlit as st
import text
import base64
from ClusteringNLP import Clustering_NLP
from ClassificationNLP import Classification_NLP
from sklearn.metrics import accuracy_score
import charts
import tools
# from geopy.geocoders import Nominatim

def landing():
    file_ = open("./resources/comp_teach.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    
    # Heading
    st.markdown("## **Master's Project**")
    st.markdown('---')
    st.markdown("# **Automated Short Response Grading**")
    
    st.markdown(f'## Purpose')
    st.markdown(
        """ Grading has to be one of the most tedious, unfun aspects of being a teacher. Having talked to former collegues, most would be willing to even pay an external party to do grading for them. Personally as a teacher, I always felt I had a duty to my students to complete grading on time, but with all of the other preparation work, it can feel overwhelming.   
        
Recognizing that most problems of repatition are perfect for programs, I set out to see if I could create an application which would, to some extent, reduce the amount of grading a teacher had to do. Specifically, attempting to use unsupervised and supervised machine learning methods to address short answer response questions. """
    )
    
    button = st.button('Result of Teacher using Application')
    if button:
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )
        st.markdown(" *Example of a teacher using my application*")
        st.balloons()  

def clustering():
    st.markdown("## **Master's Project**")
    st.markdown('---')
    st.markdown("# **Unsupervised Learning | Clustering**")
    
    st.markdown("### Choose a Dataset")
    files = tools.get_files()
    option = st.selectbox(
        'Select a Teacher Answer',
        files['name']
    )
    
    index = files['name'].index(option)
    st.write('You selected:', index)

    doc= files['doc'][index] 
    data= files['data'][index]
    
    st.markdown("## Modeling Example")
    st.markdown('**Select the below based on what you want to see:**')
    doc_flag = st.checkbox('Display Question Info')
    data_flag = st.checkbox('Display Prediction Data')
    chart_flag = st.checkbox('Display Reduced-Dimensionality Chart')
    model_flag = st.checkbox('Display Model Info and Performance')    
    
    nlp = Clustering_NLP(data, doc)
    nlp.correct_cluster_labels()
    
    
    if doc_flag:
        st.markdown('## Question Info')
        st.write(doc)
    if data_flag:
        st.write(data.columns)
        st.markdown('## Prediction Data')
        st.write(data)
        st.write(pd.Series(data.columns, name = 'Features'))
    if chart_flag:
        col1, col2 = st.beta_columns(2)
        fig1, ax1 = charts.plot_pca_chart(data, doc['label'], nlp.model.cluster_centers_)
        fig2, ax2 = charts.plot_tsne_chart(data, doc['label'], nlp.model.cluster_centers_)
        with col1:
            st.pyplot(fig = fig1)
            
        with col2:
            st.pyplot(fig = fig2)

    if model_flag:
        st.markdown('## Model Data') 
        st.markdown(f'### **Accuracy of Model: {round(nlp.accuracy(),3)}**  ')
        st.pyplot(fig = charts.plot_confusion_matrix(nlp.doc['label'], nlp.doc.cluster))
        
        
        results = doc[['student_answer', 'label', 'cluster']]
        try_it = st.checkbox('Try it Yourself!')
        explore_flag = st.checkbox('Explore Data')
        if try_it:
            tryit(nlp)
                
            
        if explore_flag:
            st.markdown(f"""**Dataset Length: {len(results)}** """)
            start, end = st.slider(
                label = 'Data View Select',
                min_value = 0,
                max_value = len(nlp.doc)-1,
                value = (0,5)
            )
            st.markdown(f"""**Teacher Answer: {nlp.doc['teacher_answer'].values[0]}**""")
            for i in range(int(start),int(end)+1):
                st.markdown(f"""{i}. {'Label:':>10} {str(nlp.doc.loc[i,'label'])}  Pred: {str(nlp.doc.loc[i,'cluster'])}    {str(nlp.doc.loc[i,'student_answer'])}""")
                
        
        
def classification():
    st.markdown("## **Master's Project**")
    st.markdown('---')
    st.markdown("# **Supervised Learning | Classification**")
    
    st.markdown("### Choose a Dataset")
    files = tools.get_files()
    option = st.selectbox(
        'Select a Teacher Answer',
        files['name']
    )
    
    index = files['name'].index(option)
    st.write('You selected:', index)

    doc= files['doc'][index] 
    data= files['data'][index]

   
    st.markdown("## Modeling Example")
    st.markdown('**Select the below based on what you want to see:**')
    doc_flag = st.checkbox('Display Question Info')
    data_flag = st.checkbox('Display Prediction Data')
    model_flag = st.checkbox('Display Model Info and Performance')
    
    test_size = st.number_input(
            'Test Size',
            min_value = 0.01,
            max_value = 0.91,
            value = .75,
            step = 0.05
            )
    nlp = Classification_NLP(data, doc, test_size)
    st.markdown(f'Training Set Size: {len(nlp.X_train)}')
    st.markdown(f'Test Set Size: {len(nlp.X_test)}')
    if doc_flag:
        st.markdown('## Question Info')
        st.write(doc)
    if data_flag:
        st.markdown('## Prediction Data')
        st.write(data)
        st.write(pd.Series(data.columns, name = 'Features'))
    if model_flag:
        st.markdown('## Model Data')
        
        _, accuracy =  nlp.accuracy()
        st.markdown(f'### **Test Set Accuracy of Model: {round(accuracy, 3)}**  ')
        st.pyplot(fig = charts.plot_confusion_matrix(nlp.y_test, nlp.pred))
        
        
        results = doc[['student_answer', 'label', 'prediction']]
        try_it = st.checkbox('Try it Yourself!')
        explore_flag = st.checkbox('Explore Data')
        
        if try_it:
            tryit(nlp)
        if explore_flag:
            st.markdown(f"""**Dataset Length: {len(results)}** """)
            start, end = st.slider(
                label = 'Data View Select',
                min_value = 0,
                max_value = len(nlp.doc)-1,
                value = (0,5)
            )
            st.markdown(f"""**Teacher Answer: {nlp.doc['teacher_answer'].values[0]}**""")
            for i in range(int(start),int(end)+1):
                if nlp.doc.loc[i,'label'] != nlp.doc.loc[i,'prediction']:
                    st.markdown(f"""{i}. {'Label:':>10} {str(nlp.doc.loc[i,'label'])}  Pred: {str(nlp.doc.loc[i,'prediction'])}    {str(nlp.doc.loc[i,'student_answer'])}""")
                else:
                    st.markdown(f"""{i}. {'Label:':>10} {str(nlp.doc.loc[i,'label'])}  Pred: {str(nlp.doc.loc[i,'prediction'])}    {str(nlp.doc.loc[i,'student_answer'])}""")

def tryit(nlp):
    st.markdown(f"""**Teacher Answer: {nlp.doc['teacher_answer'].values[0]}**""")
    answer = st.text_input("Submit Your Own Answer")
    if answer != '':
        nlp.create_features(answer)
        st.write(nlp.sep)
        st.write(nlp.new_answers)
        st.write(nlp.new_answers.iloc[:,nlp.sep:])
        st.write(nlp.new_answers.columns)
        st.write(nlp.doc.columns)
        st.write(nlp.data.columns)
        st.write(nlp.new_answers.iloc[:,nlp.sep:].columns)
        # It is missing some vars for some reason?
        # THERE IS A WEIRD DATA ISSUE 
        """
        Weird issue where a random dataset gets injected into it
        maybe an object or caching issue?
        """
        nlp.grade_new_answer()
        prediction = nlp.new_answers.iloc[0,6]
        pred = ''
        if prediction == 1:
            pred = 'correct'
            st.balloons()
        else:
            pred = "incorrect"
        
        if pred != '':
            st.markdown(f' Your answer is predicted {pred}')
