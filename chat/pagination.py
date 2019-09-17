from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class GetPageNumberPagination(PageNumberPagination):
    page_size = 3


class GetLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 10


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000