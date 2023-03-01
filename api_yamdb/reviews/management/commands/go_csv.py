import csv
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

TABLES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title',
    User: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    """Export data from csv."""

    def handle(self, *args, **options):

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'users.csv'), 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            User.objects.all().delete()
            for row in csv_reader:
                print(row)
                users = User.objects.create(
                    id=int(row[0]),
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    first_name=row[5],
                    last_name=row[6]
                )
                users.save()

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'category.csv'), 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            Category.objects.all().delete()
            for row in csv_reader:
                print(row)
                category = Category.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
                category.save()

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'titles.csv'), 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                print(row)
                category = Category.objects.get(id=row[3])
                titles = Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=category,
                )
                titles.save()

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'genre.csv'), 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            Genre.objects.all().delete()
            for row in csv_reader:
                print(row)
                genre = Genre.objects.create(
                    name=row[1],
                    slug=row[2],
                )
                genre.save()

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'genre_title.csv'), 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            GenreTitle.objects.all().delete()
            for row in csv_reader:
                print(row)
                genre_title = GenreTitle.objects.create(
                    id=row[0],
                    title_id=int(row[1]),
                    genre_id=int(row[2])
                )
                genre_title.save()

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'review.csv'), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            Review.objects.all().delete()
            for row in csv_reader:
                print(row)
                author = User.objects.get(id=row[3])
                review = Review.objects.create(
                    id=row[0],
                    title_id=int(row[1]),
                    text=row[2],
                    author=author,
                    score=row[4],
                    pub_date=row[5]
                )
                review.save()

        with open(os.path.join(settings.BASE_DIR, 'static', 'data',
                               'comments.csv'), 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            Comment.objects.all().delete()
            for row in csv_reader:
                print(row)
                author = User.objects.get(id=row[3])
                comment = Comment.objects.create(
                    id=row[0],
                    review_id=int(row[1]),
                    text=row[2],
                    author=author,
                    pub_date=row[4],
                )
                comment.save()
        self.stdout.write(self.style.SUCCESS('******* ALL DATA LOAD *******'))
