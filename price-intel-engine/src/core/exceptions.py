class AppError(Exception):
    """Base exception for the application."""
    pass

class ScraperError(AppError):
    """Base exception for scraping errors."""
    pass

class NetworkError(ScraperError):
    """Raised when network requests fail after retries."""
    pass

class ParsingError(ScraperError):
    """Raised when response parsing fails."""
    pass

class ConfigError(AppError):
    """Raised when configuration is invalid or missing."""
    pass

class ExportError(AppError):
    """Raised when data export fails."""
    pass
