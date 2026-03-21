from dataclasses import dataclass

import numpy
from sklearn.linear_model import Ridge

from schemas import AnalyzeResponse, Match, ParticipantRating

FloatArray = numpy.typing.NDArray[numpy.float64]


class AnalyticsError(Exception):
    pass


@dataclass
class AnalyticsArtifacts:
    participants: list[str]
    X: FloatArray
    y: FloatArray


def collect_participants(matches: list[Match]) -> list[str]:
    return sorted(
        {
            participant
            for match in matches
            for participant in [*match.teamA, *match.teamB]
        }
    )


def validate_matches(matches: list[Match]) -> None:
    for match in matches:
        if len(match.teamA) == 0 or len(match.teamB) == 0:
            raise AnalyticsError(
                f"Match {match.id} must have at least one participant per team."
            )

        all_participants = [*match.teamA, *match.teamB]
        if len(set(all_participants)) != len(all_participants):
            raise AnalyticsError(f"Match {match.id} contains duplicate participants.")


def build_design_matrix(matches: list[Match]) -> AnalyticsArtifacts:
    participants = collect_participants(matches)
    participant_index = {
        participant: index for index, participant in enumerate(participants)
    }

    X: FloatArray = numpy.zeros((len(matches), len(participants)), dtype=float)
    y: FloatArray = numpy.zeros(len(matches), dtype=float)

    for row_index, match in enumerate(matches):
        y[row_index] = match.scoreA - match.scoreB

        team_a_weight = 1.0 / len(match.teamA)
        team_b_weight = 1.0 / len(match.teamB)

        for participant in match.teamA:
            X[row_index, participant_index[participant]] += team_a_weight

        for participant in match.teamB:
            X[row_index, participant_index[participant]] -= team_b_weight

    return AnalyticsArtifacts(
        participants=participants,
        X=X,
        y=y,
    )


def compute_match_stats(
    matches: list[Match],
    participants: list[str],
) -> dict[str, dict[str, int]]:
    stats = {
        participant: {
            "matchesPlayed": 0,
            "wins": 0,
            "losses": 0,
            "pointDifferential": 0,
        }
        for participant in participants
    }

    for match in matches:
        margin = match.scoreA - match.scoreB
        team_a_won = margin > 0
        team_b_won = margin < 0

        for participant in match.teamA:
            stats[participant]["matchesPlayed"] += 1
            stats[participant]["pointDifferential"] += int(margin)

            if team_a_won:
                stats[participant]["wins"] += 1
            elif team_b_won:
                stats[participant]["losses"] += 1

        for participant in match.teamB:
            stats[participant]["matchesPlayed"] += 1
            stats[participant]["pointDifferential"] -= int(margin)

            if team_b_won:
                stats[participant]["wins"] += 1
            elif team_a_won:
                stats[participant]["losses"] += 1

    return stats


def analyze_matches(
    matches: list[Match],
    lambda_: float = 1.0,
) -> AnalyzeResponse:
    if lambda_ <= 0:
        raise AnalyticsError("lambda_ must be greater than 0.")

    if len(matches) == 0:
        return AnalyzeResponse(
            participantOrder=[],
            ratings={},
            ranking=[],
            lambda_=lambda_,
            matchCount=0,
            rmse=0.0,
            mae=0.0,
        )

    validate_matches(matches)
    artifacts = build_design_matrix(matches)

    model = Ridge(alpha=lambda_, fit_intercept=False)
    model.fit(artifacts.X, artifacts.y)

    ratings_array = numpy.asarray(model.coef_, dtype=float)
    centered_ratings = ratings_array - ratings_array.mean()

    predictions = artifacts.X @ centered_ratings
    errors = predictions - artifacts.y

    rmse = float(numpy.sqrt(numpy.mean(errors**2)))
    mae = float(numpy.mean(numpy.abs(errors)))

    stats = compute_match_stats(matches, artifacts.participants)

    ratings = {
        participant: float(centered_ratings[index])
        for index, participant in enumerate(artifacts.participants)
    }

    ranking = [
        ParticipantRating(
            participant=participant,
            rating=ratings[participant],
            matchesPlayed=stats[participant]["matchesPlayed"],
            wins=stats[participant]["wins"],
            losses=stats[participant]["losses"],
            pointDifferential=stats[participant]["pointDifferential"],
        )
        for participant in artifacts.participants
    ]

    ranking.sort(key=lambda entry: (-entry.rating, entry.participant))

    return AnalyzeResponse(
        participantOrder=artifacts.participants,
        ratings=ratings,
        ranking=ranking,
        lambda_=lambda_,
        matchCount=len(matches),
        rmse=rmse,
        mae=mae,
    )
