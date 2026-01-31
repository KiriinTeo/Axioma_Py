# Axioma_Py – Project State

## Objetivo
Sistema ERP analítico em Python

## Stack
- FastAPI
- SQLAlchemy / SQLite
- Pandas / Matplotlib
- JWT Auth
- Pytest
- Uvicorn
- Docker 
- Linux (Ubuntu 22.04 LTS)
- OCI (planejado)

## Arquitetura
- core: lógica pura (DatasetContext, análises, ingestão, pipeline, gráficos etc)
- application: use cases, services e app_manager
- infra: banco, ORM, models, repositories etc
- api: FastAPI + rotas (com schemas e dependencies)
- auth: autenticação JWT
- interface: UI (não adicionado ainda)
- data: dados usados para testes e salvamentos de resultados
- config: Configurações para variaveis de ambiente, conexão local ou cloud etc.
- domain: modulo legado (á ser retirada)
- cli: modulo legado (á ser retirada)
- wallet: para conexão mTLS com OCI (vazio no git)
- tests: pytest

## Decisões importantes
- DatasetContext NÃO é ORM
- Use cases não dependem de FastAPI
- Repositórios vão encapsular SQLAlchemy
- Manter escalável de facil atualização

## Estado atual
- Auth funcional
- Dataset ORM criado
- Use cases funcionando
- Rotas funcionando
- Testes passando
- Docker funcionando em VM local 
- Observabilidade mínima (logs, healthcheck, lifecycle)

## Próximo passo
- Integrando com Cloud OCI e preparando para billing
- Preparar para UI visando esse sistema
- Resolver erro DPY-6000 Similar ao ORA-12506 "Listener Refused" para container em VM Linux Ubuntu 22.04 LTS 
