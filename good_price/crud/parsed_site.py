from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from good_price.crud.base import CRUDBase
from good_price.models import ParsedSite


class CRUDParsedSite(CRUDBase):
    async def get_id_by_url(
            self,
            url: str,
            session: AsyncSession,
    ) -> Optional[int]:
        '''Возвращает id по его url'''
        db_project_id = await session.execute(
            select(ParsedSite.id).where(
                ParsedSite.url == url
            )
        )
        return db_project_id.scalars().first()


parsed_site_crud = CRUDParsedSite(ParsedSite)
