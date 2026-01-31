from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user
from api.dependencies.deps import get_db
from infra.database.repositories.dataset_repo import DatasetRepository
from api.schemas.renameReq import RenameRequest

router = APIRouter(prefix="/dataset", tags=["Dataset"])


@router.post("/load")
def load_dataset(path: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(user["sub"])
    dataset_repo = DatasetRepository(db)

    ctx, dataset_id = manager.load_dataset_uc.execute(
        file_path=path,
        user_id=user_id,
        dataset_repo=dataset_repo
    )

    # memória pra operações com o dataset
    contexts[(user_id, dataset_id)] = ctx

    return {"dataset_id": dataset_id}


@router.get("/{dataset_id}/columns")
def list_columns(dataset_id: str, user: dict = Depends(get_current_user)):
    user_id = int(user["sub"])
    key = (user_id, dataset_id)

    if key not in contexts:
        raise HTTPException(
            status_code=404,
            detail="Dataset não encontrado na memória."
        )

    ctx = contexts[key]
    columns = manager.list_columns_uc.execute(ctx)

    return {"columns": columns}


@router.get("")
def list_datasets(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(user["sub"])
    dataset_repo = DatasetRepository(db)

    datasets = dataset_repo.list_by_user(user_id)

    return [
        {
            "id": d.id,
            "name": d.name
        }
        for d in datasets
    ]


@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_id = int(user["sub"])
    key = (user_id, dataset_id)

    dataset_repo = DatasetRepository(db)
    dataset = dataset_repo.get_by_id(dataset_id, user_id)

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset não encontrado."
        )

    dataset_repo.delete(dataset_id, user_id)

    # Remove da memória se estiver ativo ainda
    contexts.pop(key, None)

    return {"status": "deletado"}


@router.patch("/{dataset_id}/rename")
def rename_dataset(dataset_id: str, req: RenameRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(user["sub"])
    key = (user_id, dataset_id)

    dataset_repo = DatasetRepository(db)
    dataset = dataset_repo.get_by_id(dataset_id, user_id)

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset não encontrado."
        )

    # Atualiza o banco
    dataset_repo.rename(dataset_id, user_id, req.new_name)

    # Mantém contexto consistente
    if key in contexts:
        contexts[key].name = req.new_name

    return {"name": req.new_name}