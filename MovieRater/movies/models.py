from django.db import models
from django.urls import reverse
from datetime import date


class Category(models.Model):
    """Category"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    """Actors and Producers"""
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Actor and Producer"
        verbose_name_plural = "Actors and Producers"


class Genre(models.Model):
    """Genre"""
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    """Film"""
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("Tagline", max_length=100, default='')
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Release date", default=2020)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(
        Actor, verbose_name="producer", related_name="film_director")
    actors = models.ManyToManyField(
        Actor, verbose_name="actors", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="genres")
    world_premiere = models.DateField("World premiere", default=date.today)
    budget = models.PositiveIntegerField("Budget", default=0,
                                         help_text="amount in dollars")
    fees_in_usa = models.PositiveIntegerField(
        "In the USA", default=0, help_text="amount in dollars"
    )
    fess_in_world = models.PositiveIntegerField(
        "In the World", default=0, help_text="amount in dollars"
    )
    category = models.ForeignKey(
        Category, verbose_name="Category", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"


class MovieShots(models.Model):
    """Movie shots"""
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="movie_shots/")
    movie = models.ForeignKey(
        Movie, verbose_name="Film", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Frame from the movie"
        verbose_name_plural = "Frame from the movies"


class RatingStar(models.Model):
    """Rating star"""
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating star"
        verbose_name_plural = "Rating stars"
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name="star")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name="film")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Reviews(models.Model):
    """Reviews"""
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Massage", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(
        Movie, verbose_name="film", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
