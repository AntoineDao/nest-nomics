import os
from typing import Tuple

import folium
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from sklearn.cluster import KMeans


class PostCodes:

    def __init__(self, path: str = '../data/scotland_postcodes.csv'):
        base_path = os.path.dirname(__file__)
        full_path = os.path.join(base_path, path)
        self.df = pd.read_csv(full_path)

    def filter_by_constituencies(self, constituencies: list) -> pd.DataFrame:
        self.df = self.df[self.df['Constituency'].isin(constituencies)]

    def _distance(self, center: Tuple[float, float],
                  point: Tuple[float, float]) -> float:
        return geodesic(point, center).miles

    def filter_by_distance(self, lat: float, lng: float,
                           radius: float) -> pd.DataFrame:
        self.df = self.df[self.df.apply(lambda x: self._distance(
            (x['Latitude'], x['Longitude']), (lat, lng)) <= radius, axis=1)]

    # Find the postcode closest to the cluster center
    # @staticmethod
    def find_closest_postcode(self, cluster_center):
        distances = np.linalg.norm(
            self.df[['Latitude', 'Longitude']].values - cluster_center, axis=1)
        return self.df.iloc[np.argmin(distances)]['Postcode']

    def get_clustered_samples(self, n_samples: int) -> pd.DataFrame:
        # Extract latitude and longitude from the postcodes
        coords = self.df[['Latitude', 'Longitude']].values

        # Perform KMeans clustering to group the postcodes into 15 clusters
        kmeans = KMeans(n_clusters=n_samples, random_state=0).fit(coords)

        # Find the postcode in the middle of each cluster
        cluster_centers = kmeans.cluster_centers_

        # Get the representative postcode for each cluster
        representative_postcodes = []
        for i, cluster_center in enumerate(cluster_centers):
            representative_postcode = self.find_closest_postcode(
                cluster_center)
            representative_postcodes.append(representative_postcode)

        return representative_postcodes
