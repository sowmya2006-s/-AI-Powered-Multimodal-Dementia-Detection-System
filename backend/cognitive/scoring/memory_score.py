def compute_memory_score(round_scores):
    accuracy = sum(round_scores) / len(round_scores)
    decay_rate = round_scores[0] - round_scores[-1]

    if accuracy >= 0.75:
        risk = "LOW"
    elif accuracy >= 0.45:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "accuracy": accuracy,
        "decay_rate": decay_rate,
        "risk_level": risk
    }
