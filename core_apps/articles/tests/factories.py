import factory
from autoslug.utils import slugify
from faker import Factory as FakerFactory

from core_apps.articles.models import Article, ArticleView, Clap
from core_apps.users.tests.factories import UserFactory

faker = FakerFactory.create()


class ArticleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Article

    author = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda x: faker.sentence())
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    body = factory.LazyAttribute(lambda x: faker.paragraph())
    description = factory.LazyAttribute(lambda x: faker.sentence())
    banner_image = factory.django.ImageField(color="green")

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        """
        Adds tags to the article.

        `extracted` can be either a list of tag strings or None.
        """
        if not created:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def clap(self, created, extracted, **kwargs):
        """
        Adds claps to the article.

        `extracted` is expected to be a list of users that clapped for the article.
        """
        if not created:
            return
        if extracted:
            for user in extracted:
                Clap.objects.create(user=user, article=self)


class ArticleViewFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ArticleView

    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)
    viewer_ip = factory.LazyAttribute(lambda x: faker.ipv4())


class ClapFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Clap

    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)
