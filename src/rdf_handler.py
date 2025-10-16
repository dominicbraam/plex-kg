import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

base_uri = "http://plex-kg/"
SCH = Namespace("https://schema.org/")


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
        self.g.bind("schema", SCH)

    def to_ttl(
        self,
        genres: pd.DataFrame,
        persons: pd.DataFrame,
        film_data: pd.DataFrame,
    ) -> str:
        """
        Main class runner.

        Args:
            genres: pd.DataFrame
            persons: pd.DataFrame
            film_data: pd.DataFrame

        Returns:
            str: .ttl file contents
        """
        for _, genre in genres.iterrows():
            self._add_genre_entry(genre)

        for _, person in persons.iterrows():
            self._add_person_entry(person)

        for _, movie in film_data.iterrows():
            self._add_movie_entry(movie)

        return self.g.serialize(format="turtle")

    def _genre_uri(self, slug) -> str:
        return URIRef(f"genre/{slug}")

    def _person_uri(self, slug) -> str:
        return URIRef(f"person/{slug}")

    def _add_genre_entry(self, genre_data: pd.Series) -> None:
        """
        Add genre to graph.

        Args:
            genre_data: pd.Series
        """
        print(type(genre_data))
        slug = genre_data["slug"]
        name = genre_data["name"]

        genre = self._genre_uri(slug)

        self.g.add((genre, RDF.type, SCH.genre))
        self.g.add((genre, SCH.name, Literal(name, lang="en")))

    def _add_person_entry(self, person_data: pd.Series) -> None:
        """
        Add person to graph.

        Args:
            person_data: pd.Series
        """
        slug = person_data["slug"]
        name = person_data["name"]

        person = self._person_uri(slug)

        self.g.add((person, RDF.type, SCH.Person))
        self.g.add((person, SCH.name, Literal(name, lang="en")))

    def _add_movie_entry(self, movie_data: pd.Series) -> None:
        """
        Add movie to graph.

        Args:
            movie_data: pd.Series
        """
        slug = movie_data["slug"]
        title = movie_data["title"]
        genre_slugs = movie_data["Genre"]
        director_slugs = movie_data["Director"]
        author_slugs = movie_data["Writer"]
        actor_slugs = movie_data["Role"]

        movie = URIRef(f"movie/{slug}")

        self.g.add((movie, RDF.type, SCH.Movie))
        self.g.add((movie, SCH.name, Literal(title, lang="en")))
        for slug in genre_slugs:
            self.g.add((movie, SCH.genre, self._genre_uri(slug)))
        for slug in director_slugs:
            self.g.add((movie, SCH.director, self._person_uri(slug)))
        for slug in author_slugs:
            self.g.add((movie, SCH.author, self._person_uri(slug)))
        for slug in actor_slugs:
            self.g.add((movie, SCH.actor, self._person_uri(slug)))
