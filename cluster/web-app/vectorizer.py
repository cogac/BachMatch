from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorize(text):

    tfidf_vectorizer = TfidfVectorizer()
    vectorized = tfidf_vectorizer.fit_transform(text)
    return vectorized


def reduce_dimensions(vectorized):

    pca = TruncatedSVD(n_components=25)
    reduced = pca.fit_transform(vectorized)
    return reduced


def cluster(reduced):

    kmeans = KMeans(n_clusters=75, random_state=42)
    clusters = kmeans.fit_predict(reduced)
    return clusters
