## Informativo: Logging e argparse no Axioma\_Py

### 1. Logging

**Configuração básica** (em `logger.py`):

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
            logging.FileHandler(nome_arquivo, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
)
logger = logging.getLogger('AxiomaLogger')
```

**Possibilidades de uso:**

* `logger.info("Mensagem informativa")`
* `logger.debug("Detalhes para depuração")`
* `logger.warning("Alerta leve")`
* `logger.error("Erro recuperável")`
* `logger.critical("Falha grave")`

> **Dica:** substitua `print()` por `logger` para registrar nível, horário e facilitar análises em produção.

---

### 2. argparse

**Ex: setup inicial** (em `main.py`):

```python
import argparse

parser = argparse.ArgumentParser(
    description="Axioma_Py: coleta e analisa dados via API ou arquivo local"
)
parser.add_argument("--query", type=str, help="Termo de busca (API)", default=None)
parser.add_argument("--limit", type=int, help="Número máximo de resultados", default=None)
parser.add_argument("--input_file", type=str, help="Caminho do arquivo local (CSV/JSON)", default=None)
parser.add_argument("--use_spark", action="store_true", help="Usar PySpark em vez de pandas")
args = parser.parse_args()
```

**Possibilidades de flags adicionais:**

* `--api_url`: especifique uma URL de API diferente da padrão.
* `--output_file`: defina nome e pasta de saída sem interação.

> **Dica:** usar argumentos torna o sistema sem prompts, ideal para automações e CI/CD.

---

**Combine ambos:** no início do `main()` você lê `args`, configura `logger` e passa `args` para módulos de coleta e análise.
