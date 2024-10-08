from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article
from core_apps.profiles.models import Profile


@registry.register_document
class ArticleDocument(Document):
    title = fields.TextField(attr="title")
    description = fields.TextField(attr="description")
    body = fields.TextField(attr="body")
    author_first_name = fields.TextField()
    author_last_name = fields.TextField()
    tags = fields.KeywordField()

    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Article
        fields = ["created_at"]

    def prepare_author_first_name(self, instance):
        return instance.author.first_name

    def prepare_author_last_name(self, instance):
        return instance.author.last_name

    def prepare_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]


@registry.register_document
class ProfileDocument(Document):
    user = fields.ObjectField(
        properties={
            "email": fields.TextField(),
            "first_name": fields.TextField(),
            "last_name": fields.TextField(),
            "date_joined": fields.DateField(),
        }
    )
    phone_number = fields.TextField()
    about_me = fields.TextField()
    gender = fields.TextField()
    country = fields.TextField(attr="get_country_code")
    city = fields.TextField()
    profile_photo = fields.TextField(attr="profile_photo.url")
    twitter_handle = fields.TextField()
    followers_count = fields.IntegerField()

    class Index:
        name = "profiles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Profile
        fields = [
            "id",
        ]

    def prepare_followers_count(self, instance):
        return instance.followers.count()

    def get_country_code(self, obj):
        # This method extracts the country code for serialization
        return obj.country.code if obj.country else None
