from typing import Literal

from litestar import Router, get


@get("/health")
async def health() -> dict[Literal["status"], Literal[True]]:
    return {"status": True}


health_router = Router(
    path="",
    route_handlers=[health],
)
