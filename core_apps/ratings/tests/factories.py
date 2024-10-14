import factory
from faker import Factory as FakerFactory

from core_apps.articles.tests.factories import ArticleFactory
from core_apps.ratings.models import Rating
from core_apps.users.tests.factories import UserFactory

faker = FakerFactory.create()


class RatingFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Rating

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)
    rating = factory.Iterator([choice[0] for choice in Rating.RATING_CHOICES])
    review = factory.LazyAttribute(lambda x: faker.text())
