import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,   # nivel mínimo: ignora DEBUG, muestra INFO en adelante
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )