import factory
from django.utils import timezone
from factory import Sequence, LazyFunction, LazyAttribute
from mimesis import Person, Business, Address

from devproject.core import models

_person = Person()
_business = Business()
_address = Address()


class Developer(factory.DjangoModelFactory):
    login = LazyFunction(_person.username)
    avatar_url = LazyFunction(_person.avatar)
    name = LazyFunction(_person.full_name)
    company = LazyFunction(_business.company)
    location = LazyFunction(_address.city)
    email = LazyFunction(lambda: _person.email(domains=["@tesorio.com"]))
    hireable = False
    bio = None
    github_id = Sequence(lambda n: n)
    github_node_id = Sequence(lambda n: f"GH_NODE_ID_{n}")
    created_at = LazyFunction(timezone.now)
    updated_at = LazyFunction(timezone.now)
    url = LazyAttribute(lambda o: f"https://api.github.com/users/{o.login}")
    raw = LazyAttribute(
        lambda o: {
            "login": o.login,
            "id": o.github_id,
            "node_id": o.github_node_id,
            "avatar_url": o.avatar_url,
            "gravatar_id": "",
            "url": o.url,
            "followers_url": f"{o.url}/followers",
            "following_url": "%s/following{/other_user}" % o.url,
            "gists_url": "%s/gists{/gist_id}" % o.url,
            "starred_url": "%s/starred{/owner}{/repo}" % o.url,
            "subscriptions_url": "%s/subscriptions" % o.url,
            "organizations_url": "%s/orgs" % o.url,
            "repos_url": "%s/repos" % o.url,
            "events_url": "%s/events{/privacy}" % o.url,
            "received_events_url": "%s/received_events" % o.url,
            "type": "User",
            "site_admin": False,
            "name": o.name,
            "company": o.company,
            "blog": "https://github.com/blog",
            "location": o.location,
            "email": o.email,
            "hireable": o.hireable,
            "bio": o.bio,
            "twitter_username": o.login,
            "public_repos": 0,
            "public_gists": 0,
            "followers": 0,
            "following": 0,
            "created_at": o.created_at.isoformat() if o.created_at else None,
            "updated_at": o.updated_at.isoformat() if o.updated_at else None,
        }
    )

    class Meta:
        model = models.Developer


class Repository(factory.DjangoModelFactory):
    name = LazyAttribute(lambda o: o.full_name.split("/")[1])
    full_name = Sequence(lambda n: f"repo/repo_{n}")
    private = False
    description = None
    github_id = Sequence(lambda n: 1000 + n)
    github_node_id = Sequence(lambda n: f"GH_REPO_NODE_ID_{n}")
    created_at = LazyFunction(timezone.now)
    updated_at = LazyFunction(timezone.now)
    url = LazyAttribute(lambda o: f"https://api.github.com/repos/{o.full_name}")
    raw = LazyAttribute(
        lambda o: {
            "name": o.name,
            "full_name": o.full_name,
            "id": o.github_id,
            "node_id": o.github_node_id,
            "url": o.url,
            "created_at": o.created_at.isoformat() if o.created_at else None,
            "updated_at": o.updated_at.isoformat() if o.updated_at else None,
        }
    )

    class Meta:
        model = models.Repository
