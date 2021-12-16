from fastapi import Query


class CommonPaginationParams:
    def __init__(
        self, number=Query(default=1, alias="page[number]"), size=Query(default=50, alias="page[size]")
    ):
        self.page_number = number
        self.page_size = size
