import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import urllib.parse

# Load CSS for styling
with open('css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading medicine-dataframe from pickle
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)

# Loading similarity-vector-data from pickle
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
    return recommended_medicines

# Title
st.markdown('<h1 style="font-size: 38.5px;" class="stTitle">JanAushadhi Medicine Recommender</h1>', unsafe_allow_html=True)

# Searchbox
selected_medicine_name = st.selectbox(
    'Type your medicine name whose alternative is to be recommended',
    medicines['Drug_Name'].values
)

# Recommendation Program
if st.button('Recommend Medicine', key='recommend', help="Click to get recommendations"):
    recommendations = recommend(selected_medicine_name)
    for idx, medicine in enumerate(recommendations, 1):
        # Encode the medicine name for URL
        encoded_medicine = urllib.parse.quote_plus(medicine)
        st.markdown(f"""
            <div class="recommendation">
                <p>{idx}. {medicine}</p>
                <ul>
                    <li><a href="https://janaushadhistore.online/?s={encoded_medicine}" target="_blank">Buy on Janaushadhi Store</a></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Image load
image = Image.open('images/bg.webp')
st.image(image, caption='Recommended Medicines', use_column_width=True)
