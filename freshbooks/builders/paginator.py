class PaginatorBuilder:
    """Builder for making paginated list queries.

    Has two attributes, `page` and `per_page`. When a `PaginatorBuilder` object is passed
    to a `.list()` call, the call will fetch only the `per_page` number of results and will
    fetch the results offset by `page`.

    ```python
    >>> from freshbooks import PaginatorBuilder

    >>> paginator = PaginatorBuilder(2, 4)
    >>> paginator
    PaginatorBuilder(page=2, per_page=4)

    >>> clients = freshBooksClient.clients.list(account_id, builders=[paginator])
    >>> clients.pages
    PageResult(page=2, pages=3, per_page=4, total=9)
    ```
    """

    MAX_PER_PAGE = 100
    MIN_PAGE = 1

    def __init__(self, page=None, per_page=None):
        """Builder for making paginated list queries.

        Args:
            page: (Optional) The page of results to return in the API call
            per_page: (Optional) The number of results to return in each API call

        Returns:
            The PaginatorBuilder instance
        """
        self._page = None
        self._per_page = None
        if page is not None:
            self._page = max(page, self.MIN_PAGE)
        if per_page is not None:
            self._per_page = min(per_page, self.MAX_PER_PAGE)

    def __str__(self):
        return f"PaginatorBuilder(page={self._page}, per_page={self._per_page})"

    def __repr__(self):  # pragma: no cover
        return f"PaginatorBuilder(page={self._page}, per_page={self._per_page})"

    def page(self, page=None):
        """Set the page you wish to fetch in a list call, or get the currently set the page.
        When setting, can be chained.

        ```python
        >>> paginator = PaginatorBuilder(1, 3)
        >>> paginator
        PaginatorBuilder(page=1, per_page=3)

        >>> paginator.page()
        1

        >>> paginator.page(2).per_page(4)
        >>> paginator
        PaginatorBuilder(page=2, per_page=4)
        ```

        Args:
            page: (Optional) The page of results to return in the API call

        Returns:
            The PaginatorBuilder instance if a `page` value is provided, otherwise
            returns the currently set `page` value.
        """
        if page:
            self._page = max(page, self.MIN_PAGE)
            return self
        return self._page

    def per_page(self, per_page=None):
        """Set the number of results you wish to fetch in a page of a list call,
        or get the currently set per_page. When setting, can be chained.

        The page size is capped at 100.

        ```python
        >>> paginator = PaginatorBuilder(1, 3)
        >>> paginator
        PaginatorBuilder(page=1, per_page=3)

        >>> paginator.per_page()
        3

        >>> paginator.per_page(4).page(2)
        >>> paginator
        PaginatorBuilder(page=2, per_page=4)
        ```

        Args:
            per_page: (Optional) The number of results to return in each API call

        Returns:
            The PaginatorBuilder instance if a `per_page` value is provided, otherwise
            returns the currently set `per_page` value.
        """
        if per_page:
            self._per_page = min(per_page, self.MAX_PER_PAGE)
            return self
        return self._per_page

    def build(self):
        """Builds the query string parameters from the PaginatorBuilder.

        Returns:
            The built query string
        """
        query_string = ""
        if self._page:
            query_string = f"&page={self._page}"
        if self._per_page:
            query_string = f"{query_string}&per_page={self._per_page}"
        return query_string
