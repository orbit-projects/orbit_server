from starlette.requests import Request


class RequestContext:
    """
    A wrapper around the Starlette Request object providing
    convenient access to commonly used request data.

    This abstraction simplifies handler logic by exposing
    frequently accessed properties in a clean interface.
    """

    def __init__(self, request: Request):
        """
        Initialize the request context.

        Args:
            request (Request): The incoming Starlette request object.
        """
        self.request = request

    @property
    def headers(self):
        """
        Get request headers as a dictionary.

        Returns:
            dict: Request headers.
        """
        return dict(self.request.headers)

    @property
    def query_params(self):
        """
        Get query parameters as a dictionary.

        Returns:
            dict: Query parameters from the request URL.
        """
        return dict(self.request.query_params)

    @property
    def method(self):
        """
        Get the HTTP method of the request.

        Returns:
            str: HTTP method (e.g., GET, POST).
        """
        return self.request.method

    @property
    def path(self):
        """
        Get the request path.

        Returns:
            str: URL path of the request.
        """
        return self.request.url.path

    @property
    def client_ip(self):
        """
        Get the client's IP address.

        Returns:
            str | None: The client's IP address if available, otherwise None.
        """
        return self.request.client.host if self.request.client else None
