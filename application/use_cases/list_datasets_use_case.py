class ListDatasetsUseCase:
    def execute(self, user_id: int, dataset_repo):
        return dataset_repo.list_by_user(user_id)