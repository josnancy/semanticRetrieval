
import numpy as np
from numpy import dot
from numpy.linalg import norm
import scipy.spatial.distance

def execute_search(qvector):
    lsaMatrix = np.load('LSI_TFIDF_Matrix.npy')
    cosine_scores = cos_cdist(lsaMatrix,qvector)
    print("cosine_scores: ")
    print(cosine_scores)
    threshold = 3
    #x = numpy.argsort(a)
    ids = np.array(cosine_scores).argsort()[:threshold]
    print("ids: ")
    print(ids)
    return ids

def cos_cdist(matrix, vector):
    v = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, v, 'cosine').reshape(-1)

