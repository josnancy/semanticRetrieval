
from sklearn.decomposition import TruncatedSVD
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
import pandas as pd
from sklearn.utils.extmath import randomized_svd
import numpy as np
from sklearn.metrics import euclidean_distances
import matplotlib.pyplot as plt
from sklearn import manifold
from scipy import linalg,dot

def transformMyMatrix(matrix, dimensions):
    """ Calculate SVD of objects matrix: U . SIGMA . VT = MATRIX 
    Reduce the dimension of sigma by specified factor producing sigma'.    
    Then dot product the matrices:  U . SIGMA' . VT = MATRIX'
    """
    rows,cols = matrix.shape
    #Sigma comes out as a list rather than a matrix
    u,sigma,vt = linalg.svd(matrix)

    #Dimension reduction, build SIGMA'
    for index in range(rows - dimensions, rows):
        sigma[index] = 0

    #Reconstruct MATRIX'
    transformed_matrix = dot(dot(u, linalg.diagsvd(sigma, len(matrix), len(vt))) ,vt)
    return transformed_matrix

def plot_document_clusters(labels,dists):
    adist = np.array(dists)
    amax = np.amax(adist)
    adist /= amax

    mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
    results = mds.fit(adist)

    coords = results.embedding_

    plt.subplots_adjust(bottom = 0.1)
    plt.scatter(
        coords[:, 0], coords[:, 1], marker = 'o'
        )
    for label, x, y in zip(labels, coords[:, 0], coords[:, 1]):
        plt.annotate(
            label,
            xy = (x, y), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    plt.show()

example = ["Machine learning is super fun",
"Python is super, super cool",
"Statistics is cool, too",
"Data science is fun",
"Python is great for machine learning",
"I like football",
"Football is great to watch"]

documents = np.array(example)
np.save("documents", documents)
vectorizer = CountVectorizer(min_df = 1, stop_words = 'english')
dtm = vectorizer.fit_transform(example)

#term count matrix
index=pd.DataFrame(dtm.toarray(),index=example,columns=vectorizer.get_feature_names())
indexterms=vectorizer.get_feature_names()
np.save("IndexTerms", indexterms)

documentIndex = np.array(index)
np.save("DocumentIndex",documentIndex)

#%%Computing TF-IDF DTM matrix
transform=TfidfTransformer()
tfidf=transform.fit_transform(dtm)
tfidf=tfidf.toarray()

#%%SVD
lsa = TruncatedSVD(2, algorithm = 'arpack')
dtm_lsa = lsa.fit_transform(tfidf)
dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)#normalise by l2 norm
termvector=pd.DataFrame(lsa.components_,index = ["component_1","component_2"],columns = vectorizer.get_feature_names())
docvector=pd.DataFrame(dtm_lsa, index = example, columns = ["component_1","component_2"])

#%% Saving the transformed tfid matrix, term & document vectors

U, Sigma, Vt = randomized_svd(tfidf, n_components=4,
                                      n_iter=5, transpose=True,
                                      random_state=None)

U_vectors = np.array(U)
Vt_vectors = np.array(Vt)
sigmaValues = np.array(Sigma)

np.save("U_vectors", U_vectors)
np.save("Vt_vectors",Vt_vectors)
np.save("SigmaValues",sigmaValues)

newMatrix = transformMyMatrix(tfidf,2)
LSI_TFIDF_Matrix = np.array(newMatrix)
np.save("LSI_TFIDF_Matrix",LSI_TFIDF_Matrix)

# Plotting document clusters
from scipy.spatial.distance import squareform,pdist
similarities = euclidean_distances(newMatrix)
plot_document_clusters(documents,similarities)