from rest_framework.pagination import PageNumberPagination


class ArticlePagination(PageNumberPagination):
    page_size = 30
    page_query_param = "page_size"
    max_page_size = 10
