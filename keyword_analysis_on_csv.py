# Import necessary libraries
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

# Load your data from a CSV file
# data = pd.read_excel('tempor.ods', engine='odf')
data = pd.read_csv('extracted_abstracts.csv')
data['text'] = data['abstract'].str.replace('Abstract: ', '')
# Vectorize the text and compute TF-IDF scores
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(data['text'])

# Perform PCA to reduce dimensionality
pca = PCA(n_components=25)
X = pca.fit_transform(X)

# Perform KMeans clustering on the reduced dimensions
kmeans = KMeans(n_clusters=75, random_state=42)
y_kmeans = kmeans.fit_predict(X)

# Create a new dataframe with original text and cluster labels
data['clusters'] = y_kmeans

data[['topic', 'title', 'text', 'clusters']].to_csv('test_clusters_by_keyword.csv', index=False)

#Plot the clusters using matplotlib
# plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=200, cmap='viridis')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.title('Clusters of Customer Complaints')
# plt.grid(True)
# plt.show()
