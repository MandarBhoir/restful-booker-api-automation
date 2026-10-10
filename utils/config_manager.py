import configparser
from pathlib import Path


class ConfigManager:
    """
    Load and provide access to framework configuration.
    """

    def __init__(self):
        config_path = (
            Path(__file__).parent.parent
            / "config"
            / "settings.ini"
        )

        if not config_path.is_file():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        if not self.config.has_option("API", "base_url"):
            raise ValueError(
                "Missing required configuration: [API] base_url"
            )

    def get_base_url(self):
        return self.config["API"]["base_url"].rstrip("/")
