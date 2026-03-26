from litestar import Router, post

from vaccone_score.analytics import analyze_matches
from vaccone_score.schemas import AnalyzeRequest, AnalyzeResponse


@post("/analyze")
async def analyze(data: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_matches(data.matches, data.lambda_)


analysis_router = Router(
    path="",
    route_handlers=[analyze],
)
