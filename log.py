import logging


logging.basicConfig(level=logging.ERROR, filename="log.log",
                    filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")


def log(error):
    logging.exception(error)
