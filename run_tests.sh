#!/bin/bash

echo "============================="
echo " Executando Testes Axioma_Py "
echo "============================="

pytest --maxfail=3 --disable-warnings --tb=short

PYTHONPATH=. pytest 

echo "============================="
echo " Testes Finalizados          "
echo "============================="
