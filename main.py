import streamlit as st
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

header=st.container()
dataset=st.container()
features=st.container()
model_training=st.container()

st.markdown(
    """
    <style>
    .main {
    background-color: '#FA6B6D'
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache
def get_data(filename):
    taxi_data=pd.read_csv(filename)

    return taxi_data


with header:
    st.title("Welcome to my project")
    st.text('Transactions of taxis in NYC')
    
with dataset:
    st.header("NYC taxi dataset")
    taxi_data=get_data("data/yellow_tripdata.csv")

    st.subheader('Pick-up location ID distribution on the NYC dataset')
    pulocation_dist=pd.DataFrame(taxi_data['PULocationID'].value_counts()).head(50)
    st.bar_chart(pulocation_dist)
    
#with features:
    #st.header("The features I created")

    #st.markdown('* **first feature:** I created this feature because of this..')
    #st.markdown('* **second feature:** I created this feature because of this..')

with model_training:
    st.header("Let's train the model")
    st.text("Here we can choose the hyperparameters of the model and see how the performance changes")

    sel_col,disp_col=st.columns(2)
    max_depth=sel_col.slider('What should the max_depth of the model be?',min_value=10,max_value=100,value=20,step=10)

    n_estimators=sel_col.selectbox('How many trees should there be?',options=[100,200,300,'No limit'],index=0)
    

    sel_col.text('Here is a list of input features in the data:')
    sel_col.write(taxi_data.columns)

    input_feature=sel_col.text_input('Which feature should be used as the input feature?','PULocationID')

    
    if n_estimators=='No limit': 
        regr=RandomForestRegressor(max_depth=max_depth)
    else:
        regr=RandomForestRegressor(max_depth=max_depth,n_estimators=n_estimators)

    regr=RandomForestRegressor(max_depth=max_depth,n_estimators=n_estimators)

    X=taxi_data[[input_feature]]
    y=taxi_data[['total_amount']]

    regr.fit(X,y)
    prediction=regr.predict(y)

    disp_col.subheader('Mean absolute error of the model:')
    disp_col.write(mean_absolute_error(y,prediction))

    disp_col.subheader('Mean sqauared error of the model:')
    disp_col.write(mean_squared_error(y,prediction))

    disp_col.subheader('R sqaured score of the model:')
    disp_col.write(r2_score(y,prediction))

   
