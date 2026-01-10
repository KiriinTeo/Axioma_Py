# Axioma_Py – Project State

## Objetivo
Sistema ERP analítico em Python, evoluindo para SaaS.

## Stack
- FastAPI
- SQLAlchemy
- Pandas / Matplotlib
- JWT Auth
- Pytest
- OCI (planejado)

## Arquitetura
- core: lógica pura (DatasetContext, análises, ingestão, pipeline, gráficos etc)
- application: use cases, services e app_manager
- infra: banco, ORM, models, repositories etc
- api: FastAPI + rotas (com schemas e dependencies)
- auth: autenticação JWT
- tests: pytest

## Decisões importantes
- DatasetContext NÃO é ORM
- ORM só persiste metadados
- Use cases não dependem de FastAPI
- Repositórios vão encapsular SQLAlchemy
- Manter escalável de facil atualização

## Estado atual
- Auth funcional
- Dataset ORM criado
- Use cases funcionando
- Rotas funcionando
- Testes passando

## Próximo passo
- Aplicar testes para cada rota, 
