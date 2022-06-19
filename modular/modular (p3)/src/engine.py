from ML_Pipeline import preprocessing
from ML_Pipeline import recommendations
from ML_Pipeline import utils
import sys
import configparser

# loading parameters from config file
config = configparser.RawConfigParser()
config.read('config.ini')
DATA_DIR      = config.get('DATA','data_dir')

# reading the data
print("----Loading the data----")
df= utils.read_data(DATA_DIR)

# Data Preprocessing
print("----Data Preprocessing started----")
unique_df,desc_list=preprocessing.process_data(df=df,col1='Description',col2='Product Name')

# choose similarity measure 
val = int(input("Select the similarity measure\nCosine - 0\nManhattan - 1\nEucliden - 2\nEnter your value: "))
if val==0:
    distance='cosine'
elif val==1:
    distance='manhattan'
elif val==2:
    distance='euclidean'
else:
    sys.exit("Invalid option choosen")

# choose the vectorizer
val1 = int(input("Select the algorithm for recommendation\ncount_vectorizer - 0\ntfidf_vec - 1\nfasttext_model - 2\nglove_model - 3\nword2vecModel - 4\nco-ocurrence matrix - 5\nEnter your value: "))


if val1==0:
    model='count_vectorizer'
elif val1==1:
    model='tfidf_vec'
elif val1==2:
    model='fasttext_model'
elif val1==3:
    model='glove_model'
elif val1==4:
    model='word2vecModel'
elif val1==5:
    model='co-ocurrence matrix'        
else:
    sys.exit("Invalid option choosen")

id = config.get('DATA','Product')
top_products=recommendations.get_recommendation(product_col='Product Name',product_id=id, df=unique_df,input=desc_list, vectorizer=model ,similarity=distance, n=10)
