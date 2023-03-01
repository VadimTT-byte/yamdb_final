from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Categories of artworks"""

    name = models.CharField(
        max_length=256,
        verbose_name='Category name'
    )

    slug = models.SlugField(
        max_length=50,
        verbose_name='Shortname of group',
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    """Genres of artworks"""

    name = models.CharField(
        max_length=256,
        verbose_name='Genre name',
    )

    slug = models.SlugField(
        max_length=50,
        verbose_name='Shortname of genre',
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Title(models.Model):
    """Name of artwork"""

    name = models.CharField(
        max_length=256,
        verbose_name='name artwork',
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='year of creation',
    )

    description = models.TextField(
        verbose_name='artwork description',
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Category',
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Genre',
    )
    # внес изменения
    rating = models.IntegerField(
        verbose_name='Rating',
        null=True,
        default=None
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'От 1 до 10'),
            MaxValueValidator(10, 'От 1 до 10')
        ]
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
