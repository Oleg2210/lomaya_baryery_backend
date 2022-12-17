import abc
from typing import Optional, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException

DatabaseModel = TypeVar("DatabaseModel")


class AbstractRepository(abc.ABC):
    """Абстрактный класс, для реализации паттерна Repository."""

    def __init__(self, session: AsyncSession, model: DatabaseModel) -> None:
        self._session = session
        self._model = model

    async def get_or_none(self, id: UUID) -> Optional[DatabaseModel]:
        """Получает из базы объект модели по ID. В случае отсутствия возвращает None."""
        db_obj = await self._session.execute(select(self._model).where(self._model.id == id))
        return db_obj.scalars().first()

    async def get(self, id: UUID) -> DatabaseModel:
        """Получает объект модели по ID. В случае отсутствия объекта бросает ошибку."""
        db_obj = await self.get_or_none(id)
        if db_obj is None:
            raise NotFoundException(object_name=self._model.__name__, object_id=id)
        return db_obj

    async def create(self, instance: DatabaseModel) -> DatabaseModel:
        """Создает новый объект модели и сохраняет в базе."""
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def update(self, id: UUID, instance: DatabaseModel) -> DatabaseModel:
        """Обновляет существующий объект модели в базе."""
        instance.id = id
        instance = await self._session.merge(instance)
        await self._session.commit()
        return instance  # noqa: R504
