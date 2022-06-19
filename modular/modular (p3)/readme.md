# downlaod the following embeddings and place them in input folder

#### download w2v

 gdown https://drive.google.com/file/d/1LDdF6M6VzNhXfJyqb1OXLWno8TrExg6o/view?usp=sharing

#### download glove

## This will be downloaded in zip file unzip it and place it in input folder

 wget https://drive.google.com/file/d/1P9JFZ43Id9dXOo_xFpqLkx81jOsXrQC0/view?usp=sharing

#### download fastext

fastext https://drive.google.com/file/d/1hgb-kxJzFkcktsxBEpthmCxzlwe_IM6o/view?usp=sharing

## Install all the requirements

pip install -r requirements.txt

## Run the engine.py file to execute the code

## Select the appropriate options to get the recommendation for the product choosen in config file

# to run the streamlit API use the following command

streamlit run product_recommendation_streamlit.py

## Note

If Co-ocurrence matrix is choosen as the algorithm it will throw "numpy.core._exceptions.MemoryError" if there is no sufficient space(more than 3TiB) available
