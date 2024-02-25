# [algosolve](https://algosolve.pythonanywhere.com/)
## About project:
AlgoSolve - online service to learning algorithms and data structures. You can make conversation with outher users.

## Architecture
Project writed as Multi Page Application(MPA) and Single Page Application in the same time.

# Stack technologies:
## MPA:
[Django4](https://github.com/django/django): <br />
Service have backend part based on powerful django web framework and uses many django tags for create modyfied code  <br />
[django-bootstrap5](https://github.com/zostera/django-bootstrap5):  <br />
FrontEnd in MPA maked with bootstrap packages on django and have many modification(CSS, HTML, JS)  <br />
[django-simple-components](https://github.com/paqstd-dev/django-simple-components):  <br />
For making dynamic front end part in [Chapter "RoadMap"](https://algosolve.pythonanywhere.com/roadmap/) used techonology saving templates without addding his in template folder.  <br />
[Pillow](https://github.com/python-pillow/Pillow): <br />
Project have many images and works with pillow

## SPA:
[django-rest-framework](https://github.com/encode/django-rest-framework): <br />
Based on DRF project have: <br />

    Custom: Permissions, Throttles, Pagination, CRUD operations, Routers, Scopes
[djoser](https://github.com/sunscrapers/djoser) and [djangorestframework-simplejw](https://github.com/jazzband/djangorestframework-simplejwt): <br />
Making JWT authorization and CRUD opetaions with users, authorizations/authentications
[requests](https://github.com/psf/requests): <br />
Performed methods to work with HTTP queryes, status and more <br />
[drf-yasg](https://github.com/axnsan12/drf-yasg): <br />
Used for creation dynamic documentation on Swagger/OpenAPI shemas. [Swagger](https://algosolve.pythonanywhere.com/swagger/) [Redoc](https://algosolve.pythonanywhere.com/redoc/) <br />
Also Rest Framework API tested on [UnitTests](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/) and [PyTests](https://github.com/pytest-dev/pytest) / [pytest-django](https://github.com/pytest-dev/pytest-django)
## GraphQL
[graphene](https://github.com/graphql-python/graphene) and [graphene-django](https://github.com/graphql-python/graphene-django): <br />
Project have graphql api part and documentation on [graphiql](https://algosolve.pythonanywhere.com/graphql/) <br />

# Database Optimization:
Service use Django ORM(Object Relational Mapping) and optimized database queries.
# Debbuging:
[django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar): <br />
Ddt used for looking sql queries and optimization code in many places
