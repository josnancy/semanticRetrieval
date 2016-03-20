
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold

# Distance file available from RMDS project:
#    https://github.com/cheind/rmds/blob/master/examples/european_city_distances.csv
reader = csv.reader(open("european_city_distances.csv", "r"), delimiter=';')
data = list(reader)

dists = []
cities = []
for d in data:
    cities.append(d[0])
    s = (d[1:-1])
    temparr=[]
    for i in range(0,len(s)):
        temparr.append(float(s[i]))

    dists.append(temparr)

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
for label, x, y in zip(cities, coords[:, 0], coords[:, 1]):
    plt.annotate(
        label,
        xy = (x, y), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

plt.show()