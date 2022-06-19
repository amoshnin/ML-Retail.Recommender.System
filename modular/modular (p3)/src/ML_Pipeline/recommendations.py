from ML_Pipeline import distance
from ML_Pipeline import load_models
from sklearn.metrics.pairwise import cosine_similarity, manhattan_distances, euclidean_distances
import numpy as np
import pandas as pd

# Comparing similarity to get the top matches using the selected vectorizer

def get_recommendation(product_col,product_id, df,input, vectorizer ,similarity, n=10):

    row = df.loc[df[product_col] == product_id]
    index = list(row.index)[0]
    description = row['desc_lowered'].loc[index]
    mat=0
    
    #Create vector using the choosen Vectorizer
    if vectorizer=='count_vectorizer':
        vector = load_models.count_vectorizer.fit_transform(input)
    elif vectorizer=='tfidf_vec':
        vector= load_models.tfidf_vec.fit_transform(input)
    else:
        if vectorizer=='fasttext_model':
            model=load_models.fasttext_model.wv
        elif vectorizer=='glove_model': 
            model=load_models.glove_model
        elif vectorizer=='word2vecModel': 
            model=load_models.word2vecModel
        elif vectorizer=='co-ocurrence matrix':
            mat=1
            co_occur_vector_matrix,co_ocr_vocab=load_models.co_ocurrence_mat(input=input)
        else:
            print('Vectorizer is not valid')  

    if mat==1:
            # for co oucurrence matrix
            vector = np.empty((len(input), len(co_ocr_vocab)))
            for index, each_sentence in enumerate(input):  
                sentence_vector = np.zeros((len(co_ocr_vocab),))
                count  = 0
                for each_word in each_sentence.split(): 
                    try:
                        sentence_vector += co_occur_vector_matrix[co_ocr_vocab.index(each_word)]
                        count += 1
                
                    except:
                        continue
        
                vector[index] = sentence_vector/count
    else:
            # for glove, fasttext and word2vec
            vector = np.empty((len(input), 300))
            for index, each_sentence in enumerate(input):   
                sentence_vector = np.zeros((300,))  
                count  = 0
                for each_word in each_sentence.split():      
                    try:
                        sentence_vector += model[each_word] 
                        count += 1
                    except:
                        continue
        
                vector[index] = sentence_vector       

    # different similarity measures
    if similarity == "cosine":
        sim_matrix = cosine_similarity(vector)
        products = distance.find_cosine_similarity(df=df,cosine_sim_matrix= sim_matrix , index=index,product_col=product_col)
        
    elif similarity == "manhattan":
        sim_matrix = manhattan_distances(vector)
        products = distance.find_distance(df=df,sim_matrix= sim_matrix , index=index,product_col=product_col)

    else:
        sim_matrix = euclidean_distances(vector)
        products = distance.find_distance(df=df,sim_matrix= sim_matrix , index=index,product_col=product_col)
    
    # storing the recommendations in output folder
    recommend_product = pd.DataFrame(products)
      
    data_path = "../output/"
    recommend_product.to_excel(data_path+"recommendations.xlsx")
    print("Top 10 eecommendations are saved in output folder")
    return products
