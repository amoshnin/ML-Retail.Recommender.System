# function to calculate manhattan or Eucledian distance
def find_distance(df,sim_matrix, index, product_col,n=10):   
     
    # Getting Score and Index
    result = list(enumerate(sim_matrix[index]))

    # Sorting the Score and taking top 10 products
    sorted_result = sorted(result,key=lambda x:x[1],reverse=False)[1:10+1]
    
    # Mapping index with data
    similar_products =  [{'value': df.iloc[x[0]][product_col], 'score' : round(x[1], 2)} for x in sorted_result]
    
    return similar_products

# function to claculate cosine similarity
def find_cosine_similarity(df,cosine_sim_matrix, index, product_col,n=10):
    
    # calculate cosine similarity between each vectors
    result = list(enumerate(cosine_sim_matrix[index]))
    
    # Sorting the Score
    sorted_result = sorted(result,key=lambda x:x[1],reverse=True)[1:n+1]
    
    similar_products =  [{'value': df.iloc[x[0]][product_col], 'score' : round(x[1], 2)} for x in sorted_result]
     
    return similar_products


