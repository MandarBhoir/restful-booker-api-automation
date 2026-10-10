import requests


class APIClient:
    """
    Reusable HTTP client for API automation.
    """

    def __init__(self, base_url, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method, endpoint, **kwargs):
        """
        Send an HTTP request to the configured API.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.request(
            method=method,
            url=url,
            timeout=self.timeout,
            **kwargs
        )

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)