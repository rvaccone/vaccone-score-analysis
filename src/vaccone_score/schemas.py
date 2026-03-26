from pydantic import BaseModel, Field


class Match(BaseModel):
    id: str  # Should be UUID v4
    teamA: list[str]
    teamB: list[str]
    scoreA: int = Field(ge=0)
    scoreB: int = Field(ge=0)
    createdAt: str


class AnalyzeRequest(BaseModel):
    matches: list[Match]
    lambda_: float = Field(default=1.0, gt=0)


class ParticipantRating(BaseModel):
    participant: str
    rating: float
    matchesPlayed: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    pointDifferential: int


class AnalyzeResponse(BaseModel):
    participantOrder: list[str]
    ratings: dict[str, float]
    ranking: list[ParticipantRating]
    lambda_: float
    matchCount: int
    rmse: float
    mae: float
