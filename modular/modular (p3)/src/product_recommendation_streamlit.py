import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, manhattan_distances, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
import re


st.set_page_config(layout="wide")

tfidf_vec = TfidfVectorizer(
    stop_words='english', analyzer='word', ngram_range=(1, 3))


def preprocess(df):

    # Combining Product and Description
    df['Description'] = df['Product Name'] + ' ' + df['Description']
    # Dropping Duplicates and keeping first record
    unique_df = df.drop_duplicates(subset=['Description'], keep='first')
    # Converting String to Lower Case
    unique_df['desc_lowered'] = unique_df['Description'].apply(
        lambda x: x.lower())
    # Remove Stop special Characters
    unique_df['desc_lowered'] = unique_df['desc_lowered'].apply(
        lambda x: re.sub(r'[^\w\s]', '', x))
    # Coverting Description to List
    desc_list = list(unique_df['desc_lowered'])
    unique_df= unique_df.reset_index(drop=True)

    return unique_df, desc_list

def find_similarity(cosine_sim_matrix, index, n=10):
    
    # calculate cosine similarity between each vectors
    result = list(enumerate(cosine_sim_matrix[index]))
    
    # Sorting the Score
    sorted_result = sorted(result,key=lambda x:x[1],reverse=True)[1:n+1]
    
    similar_products =  [{'value': unique_df.iloc[x[0]]['Product Name'], 'score' : round(x[1], 2)} for x in sorted_result]
     
    return similar_products

def find_euclidean_distances(sim_matrix, index, n=10): 

    # Getting Score and Index
    result = list(enumerate(sim_matrix[index]))

    # Sorting the Score and taking top 10 products
    sorted_result = sorted(result,key=lambda x:x[1],reverse=False)[1:10+1]

    # Mapping index with data
    similar_products =  [{'value': unique_df.iloc[x[0]]['Product Name'], 'score' : round(x[1], 2)} for x in sorted_result]
    
    return similar_products
    
def find_manhattan_distance(sim_matrix, index, n=10):   
     
    # Getting Score and Index
    result = list(enumerate(sim_matrix[index]))

    # Sorting the Score and taking top 10 products
    sorted_result = sorted(result,key=lambda x:x[1],reverse=False)[1:10+1]
    
    # Mapping index with data
    similar_products =  [{'value': unique_df.iloc[x[0]]['Product Name'], 'score' : round(x[1], 2)} for x in sorted_result]
    
    return similar_products


# Comparing similarity to get the top matches using TF-IDF

def get_recommendation_tfidf(desc_list, product_id, df, similarity, n=10):

    row = df.loc[df['Product Name'] == product_id]
    index = list(row.index)[0]
    description = row['desc_lowered'].loc[index]

    #Create vector using tfidf
    
    tfidf_matrix = tfidf_vec.fit_transform(desc_list)
    
    if similarity == "cosine":
        sim_matrix = cosine_similarity(tfidf_matrix)
        products = find_similarity(sim_matrix , index)
        
    elif similarity == "manhattan":
        sim_matrix = manhattan_distances(tfidf_matrix)
        products = find_manhattan_distance(sim_matrix , index)
        
    else:
        sim_matrix = euclidean_distances(tfidf_matrix)
        products = find_euclidean_distances(sim_matrix , index)

    return products



# st.set_page_config(layout="wide")
st.sidebar.title('Product Recommendation')
st.sidebar.title('###')

df = pd.read_excel("../input/data.xlsx")

unique_df, desc_list = preprocess(df)

# Creating the sidebars
option = st.sidebar.selectbox(
    "Select a product", options=([""] + df['Product Name'].unique().tolist()))
    
if len(option) > 0:
    similarity_option = st.sidebar.selectbox(
        "Select a Similarity", options=(['cosine', 'manhattan', 'euclidean']))

# Recommendations based on choosen options
if len(option) > 0 and len(similarity_option) > 0:
        
    st.sidebar.write("Description :")
    st.sidebar.write(df[df['Product Name'] == option].reset_index()['Description'][0])

    st.write('### Top 10 Products:')
    st.dataframe(pd.DataFrame(get_recommendation_tfidf(desc_list, 
        option, unique_df, similarity=similarity_option, n=10)))
