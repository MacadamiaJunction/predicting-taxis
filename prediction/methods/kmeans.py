from sklearn.cluster import KMeans


def find_centers_kmeans(recent_pickups, num_taxis):
    km = KMeans(n_clusters=num_taxis, n_init=50)

    km.fit(recent_pickups)
    centers = km.cluster_centers_

    return centers
