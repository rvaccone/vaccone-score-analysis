from litestar import Litestar
from litestar.config.cors import CORSConfig

from vaccone_score.routers import route_handlers

cors_config = CORSConfig(
    allow_origins=[
        "http://localhost:3000",
        "https://vacconescore.com",
        "https://www.vacconescore.com",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app = Litestar(
    route_handlers=route_handlers,
    cors_config=cors_config,
)
