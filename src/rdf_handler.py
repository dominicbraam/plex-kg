import pandas as pd
from datetime import datetime, timezone
from decimal import Decimal
from pyshacl import validate
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, SDO, XSD

base_uri = "http://plex-kg/"
watcher_data = {"slug": "plex-watcher", "name": "Plex Watcher"}


class PlexRDFHandler:
    """
    Takes structured data and creates a graph in Turtle format.

    Attributes:
        g: RDF Graph
    """

    def __init__(
        self,
    ):
        self.g = Graph(base=base_uri)

        self.g.bind("rdf", RDF)
        self.g.bind("rdfs", RDFS)
        self.g.bind("schema", SDO)

    def to_ttl(
        self,
        genres: pd.DataFrame,
        persons: pd.DataFrame,
        film_data: pd.DataFrame,
        history_data: pd.DataFrame,
    ) -> str:
        """
        Main class runner.

        Args:
            genres: pd.DataFrame
            persons: pd.DataFrame
            film_data: pd.DataFrame
            history_data: pd.DataFrame

        Returns:
            str: .ttl file contents
        """
        for _, genre in genres.iterrows():
            self._add_genre_entry(genre)

        # For linking user watch history to a person node
        plex_watcher = pd.Series(watcher_data)
        self._add_person_entry(plex_watcher)

        for _, person in persons.iterrows():
            self._add_person_entry(person)

        for _, movie in film_data.iterrows():
            self._add_movie_entry(movie)

        for _, watch_action in history_data.iterrows():
            self._add_watch_action_entry(watch_action)

        conforms, report_graph = self._validate_graph()

        if not conforms:
            return conforms, report_graph.serialize(format="turtle")
        return conforms, self.g.serialize(format="turtle")

    def _genre_uri(self, slug) -> str:
        return URIRef(f"genre/{slug}")

    def _person_uri(self, slug) -> str:
        return URIRef(f"person/{slug}")

    def _movie_uri(self, slug) -> str:
        return URIRef(f"movie/{slug}")

    def _add_genre_entry(self, genre_data: pd.Series) -> None:
        """
        Add genre to graph.

        Args:
            genre_data: pd.Series
        """
        slug = genre_data["slug"]
        name = genre_data["name"]

        genre = self._genre_uri(slug)

        self.g.add((genre, RDF.type, SDO.genre))
        self.g.add((genre, SDO.name, Literal(name, lang="en")))

    def _add_person_entry(self, person_data: pd.Series) -> None:
        """
        Add person to graph.

        Args:
            person_data: pd.Series
        """
        slug = person_data["slug"]
        name = person_data["name"]

        person = self._person_uri(slug)

        self.g.add((person, RDF.type, SDO.Person))
        self.g.add((person, SDO.name, Literal(name)))

    def _add_movie_entry(self, movie_data: pd.Series) -> None:
        """
        Add movie to graph.

        Args:
            movie_data: pd.Series
        """
        media_type = movie_data["type"]
        if media_type != "movie":
            raise ValueError(
                f"Wrong media type. Expected 'movie', got '{media_type}'."
            )

        slug = movie_data["slug"]
        title = movie_data["title"]
        # contentRating = movie_data["contentRating"]
        rating = movie_data["rating"]
        date_published = movie_data["originallyAvailableAt"]
        duration = movie_data["duration"]
        genre_slugs = movie_data["Genre"]
        director_slugs = movie_data["Director"]
        author_slugs = movie_data["Writer"]
        actor_slugs = movie_data["Role"]

        movie = self._movie_uri(slug)

        self.g.add((movie, RDF.type, SDO.Movie))
        self.g.add((movie, SDO.name, Literal(title, lang="en")))
        self.g.add(
            (
                movie,
                SDO.datePublished,
                Literal(date_published, datatype=XSD.date),
            )
        )
        self.g.add(
            (movie, SDO.duration, Literal(duration, datatype=XSD.integer))
        )

        # Ratings
        # self.g.add(
        #     (
        #         movie,
        #         SDO.contentRating,
        #         Literal(contentRating, datatype=XSD.string),
        #     )
        # )

        # Don't try adding nodes with empty values
        if pd.notna(rating):
            rating_node = BNode()
            self.g.add((rating_node, RDF.type, SDO.Rating))
            self.g.add(
                (
                    rating_node,
                    SDO.ratingValue,
                    Literal(round(Decimal(rating), 1), datatype=XSD.decimal),
                )
            )
            self.g.add((movie, SDO.contentRating, rating_node))

        # Persons
        for slug in genre_slugs:
            self.g.add((movie, SDO.genre, self._genre_uri(slug)))
        for slug in director_slugs:
            self.g.add((movie, SDO.director, self._person_uri(slug)))
        for slug in author_slugs:
            self.g.add((movie, SDO.author, self._person_uri(slug)))
        for slug in actor_slugs:
            self.g.add((movie, SDO.actor, self._person_uri(slug)))

    def _add_watch_action_entry(self, watch_action_data: pd.Series) -> None:
        """
        Add watch action to graph.

        Args:
            watch_action_data: pd.Series
        """
        # data for single single watcher
        watcher_slug = watcher_data["slug"]

        history_slug = watch_action_data["historyKey"]
        movie_slug = watch_action_data["slug"]
        viewed_at = datetime.fromtimestamp(
            watch_action_data["viewedAt"], tz=timezone.utc
        ).isoformat()

        watch_action = URIRef(f"history{history_slug}")

        self.g.add((watch_action, RDF.type, SDO.WatchAction))
        self.g.add((watch_action, SDO.agent, self._person_uri(watcher_slug)))
        self.g.add((watch_action, SDO.object, self._movie_uri(movie_slug)))
        self.g.add(
            (
                watch_action,
                SDO.startTime,
                Literal(viewed_at, datatype=XSD.date),
            )
        )

    def _validate_graph(self) -> (bool, str):
        file_path = "/app/rdf/shape.ttl"
        shacl_graph = Graph().parse(file_path, format="turtle")

        conforms, report_graph, report_text = validate(
            data_graph=self.g,
            shacl_graph=shacl_graph,
            inference="rdfs",
            abort_on_first=False,
            meta_shacl=False,
            advanced=True,
            debug=False,
        )

        return conforms, report_graph
