from loguru import logger
from pathlib import Path

def setup():
	log_path = Path.cwd() / "logs"
	log_path.mkdir(parents=True, exist_ok=True)
	logger.add(log_path / "error.log", level="ERROR", retention="10 days")
