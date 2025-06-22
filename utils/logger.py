import logging

def configurarLogger(nome_arquivo="logs/axioma.log"):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(nome_arquivo, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("AxiomaLogger")
