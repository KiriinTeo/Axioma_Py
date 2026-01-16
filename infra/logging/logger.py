import logging
import sys

# pra adicionar observabilidade no projeto, deixar a estrutura dele a mais completa possível.
# formatando ele para poder funcionar no docker/vm também.

def setup_logger():
    logger = logging.getLogger("axioma")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
