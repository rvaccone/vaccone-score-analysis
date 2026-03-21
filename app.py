from litestar import Litestar, get, post
from litestar.config.cors import CORSConfig

from analytics import analyze_matches
from schemas import AnalyzeRequest, AnalyzeResponse


@get("/health")
async def health() -> dict[str, bool]:
    return {"status": True}


@post("/analyze")
async def analyze(data: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_matches(data.matches, data.lambda_)


cors_config = CORSConfig(
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app = Litestar(
    route_handlers=[health, analyze],
    cors_config=cors_config,
)
