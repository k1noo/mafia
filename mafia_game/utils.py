from random import choices
from string import ascii_uppercase, digits

import logging

GAME_TOKEN_LENGTH = 4


def generate_token(token_length: int = GAME_TOKEN_LENGTH):
    return ''.join(choices(ascii_uppercase + digits, k=token_length))


def generate_default_logger(name: str = 'Anonymous_logger', loglevel=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
