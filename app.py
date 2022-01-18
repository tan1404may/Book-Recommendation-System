import streamlit as st
import pandas as pd
import pickle
import sklearn
import numpy as np
import requests

# loading model and pivot table
model = pickle.load(open('model.pkl','rb'))
pivot = pickle.load(open('pivot.pkl','rb'))

st.title('Book Recommendation Engine')

option = st.selectbox(
    'Select Book',
    (pivot.index)
)


# this function will return predictions of books
def Recommendation(n):
    distance, suggestion = model.kneighbors(pivot.iloc[n, :].values.reshape(1, -1), n_neighbors=10)
    return pivot.index[suggestion[0]]


# this functin will return poster of books from google api
# for the books which were recommended by model
def get_poster(arr):
    url = "https://www.googleapis.com/books/v1/volumes?q="
    tmp = []
    flag = True
    for i in arr:
        new_url = url+i
        try:
            json_data = requests.get(url=new_url)
            data = json_data.json()
            tmp.append(data['items'][0]['volumeInfo']['imageLinks']['thumbnail'])
        except:
            flag = False
            break
    return flag, tmp


if st.button('Recommend'):
    # below code will find the position of book selected
    # in pivot table, cuz index of pivot tabel are title of books
    n = np.where(pivot.index == option)[0][0]
    recommendations = Recommendation(n)
    flag, images = get_poster(recommendations)

    # display data on page
    col1, col2, col3, col4, col5 = st.columns(5)
    arr = [col1, col2, col3, col4, col5]

    cnt = -1
    for i in range(len(recommendations)):
        cnt = (cnt + 1) % 5
        with arr[cnt]:
            st.write(recommendations[i])
            if(flag == True):
                st.image(images[i])
        st.write(" ")
