import json
import os
import re
import requests
import pandas as pd
from typing import List


class PlexClient:
    """
    Connect to Plex Server.

    Attributes:
        protocol: str
        host: str - Plex IP or URL
        port: int - Plex port (default is 32400)
        client_identifier: str - (X-Plex-Client-Identifier) randomly generated
        token: str - X-Plex-Token
        base: str - full Plex server URL
        headers: Dict
    """

    def __init__(self):
        self.protocol = "http"
        self.host = os.getenv("PLEX_URL")
        self.port = 32400
        self.client_identifier = os.getenv("PLEX_CLIENT_ID")
        self.token = os.getenv("PLEX_TOKEN")
        self.base = f"{self.protocol}://{self.host}:{self.port}"
        self.headers = {
            "Accept": "application/json",
            "X-Plex-Token": self.token,
            "X-Plex-Client-Identifier": self.client_identifier,
            "X-Plex-Product": "plex-kg",
            "X-Plex-Version": "0.1",
        }

    @property
    def properties(self) -> List[str]:
        """
        Returns:
            List[str]: properties for use in graph creation
        """
        return [
            "slug",
            "type",
            "title",
            "contentRating",
            # "rating",
            # "audienceRating",
            # "viewCount",
            # "lastViewedAt",
            # "year",
            # "duration",
            "Genre",
            "Director",
            "Writer",
            "Role",
        ]

    def create_structured_datasets(
        self,
    ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """
        Filter properties using the 'properties' property defined in this
        class, then create additional datasets with unique values for
        genres and persons.

        Appropriate slugs will be added to the values in the latter 2
        datasets, and then transform the initial values from the main
        dataset to use the slugs - this is to make it easier to create
        properties in rdf because the slugs will act as IDs.

        Returns:
            tuple(genres, persons, all_data)
        """
        section_data = self._get_section_items(1)
        metadata = section_data["MediaContainer"]["Metadata"]

        structured_df = pd.DataFrame(
            [{c: item.get(c) for c in self.properties} for item in metadata]
        )

        genre_df = self._property_unique_values(structured_df, ["Genre"])

        # merge the columns to create a unique dataset with persons
        person_cols = ["Director", "Writer", "Role"]
        person_df = self._property_unique_values(structured_df, person_cols)

        structured_df["Genre"] = structured_df["Genre"].apply(
            lambda x: self._map_property_slugs(x, genre_df)
        )

        # Map the next 3 columns to use person slugs
        structured_df["Director"] = structured_df["Director"].apply(
            lambda x: self._map_property_slugs(x, person_df)
        )
        structured_df["Writer"] = structured_df["Writer"].apply(
            lambda x: self._map_property_slugs(x, person_df)
        )
        structured_df["Role"] = structured_df["Role"].apply(
            lambda x: self._map_property_slugs(x, person_df)
        )

        return genre_df, person_df, structured_df

    def _get(self, path: str) -> pd.DataFrame:
        """
        Get request template.

        Args:
            path: str

        Returns:
            pd.DataFrame: result from get request.
        """
        url = f"{self.base}{path}"
        result = requests.get(url, headers=self.headers, timeout=10)
        result.raise_for_status()

        data = json.loads(result.text)
        return pd.DataFrame(data)

    def _get_libraries(self):
        return self._get("/library/sections")

    def _get_section_items(self, section_key):
        return self._get(f"/library/sections/{section_key}/all")

    def _map_property_slugs(
        self, property_vals: pd.DataFrame, property_unique_df: pd.DataFrame
    ):
        """
        Map property values to their corresponding slugs.

        Args:
            properties: pd.DataFrame

        Returns:
            List[str]
        """
        # maps slug directly to name for easy lookup
        slug_map = dict(
            zip(property_unique_df["name"], property_unique_df["slug"])
        )

        if not property_vals:
            return []
        return [
            str(slug_map[g["tag"]])
            for g in property_vals
            if g.get("tag") in slug_map
        ]

    def _property_unique_values(
        self, df: pd.DataFrame, property_names: List[str]
    ) -> pd.DataFrame:
        """
        Create unique value pd.DataFrame from a list of columns.

        Args:
            df: pd.DataFrame
            property_names: List[str]

        Returns:
            pd.DataFrame
        """
        records = set()

        # for loop takes list of dictionaries with the same
        # 'tag' structure and creates a basic list
        for _, row in df.iterrows():
            for p_name in property_names:
                val = row[p_name]
                if isinstance(val, list):
                    for item in val:
                        tag = item["tag"]
                        records.add(tag)

        return pd.DataFrame(
            [
                # lock slug characters to alphabetical and numerical values
                (re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"), name)
                for name in sorted(records)
            ],
            columns=["slug", "name"],
        )
