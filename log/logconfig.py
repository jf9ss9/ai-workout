import logging

logger = logging.getLogger("asd")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("log/ai_workout.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
