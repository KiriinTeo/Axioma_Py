from infra.database.base import Base
from infra.database.session import engine
from infra.database.models.user import UserModel
from infra.database.models.dataset import DatasetModel

Base.metadata.create_all(bind=engine)
