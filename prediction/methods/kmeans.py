from sklearn.cluster import KMeans


def find_centers_kmeans(recent_pickups, num_taxis):
    """
    Given a matrix of recent pickups by x-y coordinates and a number of taxis, it finds a number of clusters
    to assign taxis to.
    :param recent_pickups: a Nx2 matrix of recent pickups
    :param num_taxis:
    :return: x-y coordinates of the centroids
    """
    km = KMeans(n_clusters=num_taxis, n_init=50)

    km.fit(recent_pickups)
    centers = km.cluster_centers_

    return centers
