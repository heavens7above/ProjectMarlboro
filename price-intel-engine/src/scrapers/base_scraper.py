from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from src.core.models import SearchQuery, Product
from src.core.user_agents import get_random_user_agent
from loguru import logger
from curl_cffi.requests import AsyncSession, RequestsError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class BaseScraper(ABC):
    def __init__(self, platform_name: str, headers: Optional[Dict[str, str]] = None):
        self.platform_name = platform_name
        self.headers = headers or {}
        # We will initialize session lazily or strictly
        self.session: AsyncSession = AsyncSession()

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    @abstractmethod
    async def search(self, query: SearchQuery) -> List[Product]:
        """
        Search for products based on the query.
        """
        pass

    @abstractmethod
    def parse(self, response: Dict) -> List[Product]:
        """
        Parse the raw API response into Product models.
        """
        pass

    def get_headers(self) -> Dict[str, str]:
        """
        Return headers for the request, rotating User-Agent.
        """
        headers = self.headers.copy()
        # Rotate UA if not explicitly set in config (or override it)
        if "User-Agent" not in headers:
             headers["User-Agent"] = get_random_user_agent()
        return headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RequestsError, Exception)),
        reraise=True
    )
    async def _make_request(self, method: str, url: str, **kwargs: Any) -> Any:
        """
        Wrapper for making async requests with retry logic and impersonation.
        """
        try:
            # impersonate="chrome" is key for bypassing TLS fingerprinting
            if "impersonate" not in kwargs:
                kwargs["impersonate"] = "chrome"
            
            # Merge dynamic headers
            request_headers = self.get_headers()
            # If caller passed headers, merge them (caller wins collisions if needed, or update logic)
            if "headers" in kwargs:
                request_headers.update(kwargs["headers"])
                del kwargs["headers"]

            logger.debug(f"Making async request to {url} with UA: {request_headers.get('User-Agent', 'N/A')}")
            
            response = await self.session.request(method, url, headers=request_headers, **kwargs) # type: ignore
            response.raise_for_status()
            return response
        except Exception as e:
            logger.warning(f"Request failed for {self.platform_name} (retrying): {e}")
            raise
