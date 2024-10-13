import factory
from factory import SubFactory
from faker import Factory as FakerFactory

from core_apps.profiles.models import Profile
from core_apps.users.tests.factories import UserFactory

faker = FakerFactory.create()


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    user = SubFactory(UserFactory)
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    about_me = factory.LazyAttribute(lambda x: faker.sentence())
    gender = factory.Iterator(
        [Profile.Gender.MALE, Profile.Gender.FEMALE, Profile.Gender.OTHER]
    )
    country = factory.LazyAttribute(lambda x: faker.country_code())
    city = factory.LazyAttribute(lambda x: faker.city())
    profile_photo = factory.django.ImageField(color="blue")
    twitter_handle = factory.LazyAttribute(lambda x: faker.user_name())
