
import numpy as np
from numpy import dot
from numpy.linalg import norm
import scipy.spatial.distance
from numpy import linalg as LA
from scipy import linalg,dot

def execute_search(qvector,term_indexes):

    lsaMatrix = np.load('LSI_TFIDF_Matrix.npy')

    #transQueryVector = transformQuery(qvector)

    cosine_scores = cos_cdist(lsaMatrix,qvector)
    print("cosine_scores: ")
    print(cosine_scores)
    threshold = 5 #needs to be tuned with cross-validation

    #pick a max_similary_score. Dont retreieve the doc if its similary score is above that max_similary_score

    ids = np.array(cosine_scores).argsort()[:threshold]

    documents = np.load('documents.npy')
    docs=[]
    for i in range(0, len(ids)):
        docs.append(documents[ids[i]])

    return docs

def cos_cdist(matrix, vector):
    v = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, v, 'cosine').reshape(-1)

def compute_accuracy(documents):
    print(documents)

def transformQuery(qvector):

    U = np.load('U_vectors.npy')
    Vt = np.load('Vt_vectors.npy')
    S = np.load('SigmaValues.npy')

    Sdiag = linalg.diagsvd(S, len(S), len(S))
    Sinv = LA.inv(Sdiag)

    for index in range(len(U) - 2, len(U)):
        Sinv[index] = 0


    transQuery = dot(dot(Sinv,U.T),qvector)
    return transQuery

def findSimilarTerms(term_indexes):
    threshold = 3
    similar_terms = []
    Vt_vectors = np.load('Vt_vectors.npy')
    for index in term_indexes:
        term = Vt_vectors.T[index]
        similarity_score = cos_cdist(Vt_vectors.T, term)
        term_ids = np.array(similarity_score).argsort()[:threshold]

        for t in range (0,len(term_ids)):
            similar_terms.append(term_ids[t])

    dup_removed = list(set(similar_terms))
    return dup_removed