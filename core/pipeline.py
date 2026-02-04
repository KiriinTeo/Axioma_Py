from typing import Callable, List
from core.contexto import DatasetContext

class Pipeline:
    def __init__(self):
        self.steps: List[Callable[[DatasetContext], DatasetContext]] = []

    def add_step(self, step: Callable[[DatasetContext], DatasetContext]):
        self.steps.append(step)
        return self

    def run(self, ctx: DatasetContext) -> DatasetContext:
        for step in self.steps:
            ctx = step(ctx)
        return ctx
