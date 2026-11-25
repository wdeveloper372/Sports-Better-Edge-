"""Convert positive or negative American odds into raw implied probability.
This take in American odds and returns the corresponding implied probability(decimal)."""
def convert_american_odds_to_probability(odds: float) -> float:
    if odds == 0:
        raise ValueError("American odds cannot be 0.")

    if odds < 0:
        positive_magnitude = abs(odds)
        raw_probability = positive_magnitude / (positive_magnitude + 100.0)
    else:
        raw_probability = 100.0 / (odds + 100.0)

    return round(raw_probability, 4)


"""Remove vig from two-way sharp odds and return normalized true probabilities.
Does the calculation of the true probabilities after removing the vig and dividing it by the sum 
of the implied probabilities."""
def devig_to_probability(team_a_odds: float, team_b_odds: float) -> tuple[float, float]:
    implied_a = convert_american_odds_to_probability(team_a_odds)
    implied_b = convert_american_odds_to_probability(team_b_odds)
    total_implied = implied_a + implied_b

    true_prob_a = implied_a / total_implied
    true_prob_b = implied_b / total_implied
    return true_prob_a, true_prob_b


"""Convert a probability input like 55 (percent) or 0.55 (decimal) into 0.55.
Converts the input value to a decimal probability."""
def normalize_probability(value: float) -> float:
    return value / 100.0 if value > 1 else value


"""Calculate edge in percentage points and return a recommendation.
Does the calculation of the edge and provides a recommendation based on the result.
This grabs the true probability and market probability as inputs and outputs the edge and recommendation."""
def edge(true_prob: float, market_prob: float) -> tuple[float, str]:
    edge_percent = (true_prob - market_prob) * 100

    if edge_percent < 0:
        recommend = "Pass DONT BET ON THIS"
    elif edge_percent < 2.0:
        recommend = "Consider Betting the odds are not that great"
    else:
        recommend = "Go for it! The odds are in your favor!"

    return edge_percent, recommend


def main() -> None:
    # 1. Collect Pinnacle's two-way American odds and Polymarket's prices from the user
    pinnacle_side_a = float(input("Enter Pinnacle's odds for Side A (e.g. -118): "))
    pinnacle_side_b = float(input("Enter Pinnacle's odds for Side B (e.g. -112): "))
    polymarket_price_a = float(input("Enter Polymarket price for Side A (e.g. 55 or 0.55): "))
    polymarket_price_b = float(input("Enter Polymarket price for Side B (e.g. 46 or 0.46): "))

    # 2. Strip the vig from Pinnacle's odds to get the true no-vig probabilities (sum to 1.0)
    true_prob_a, true_prob_b = devig_to_probability(pinnacle_side_a, pinnacle_side_b)

    # 3. Convert Polymarket inputs (e.g., 55 or 0.55) into standard decimal probabilities (0.0 to 1.0)
    market_prob_a = normalize_probability(polymarket_price_a)
    market_prob_b = normalize_probability(polymarket_price_b)

    # 4. Compare true probabilities against Polymarket prices to get edge % and recommendation text
    edge_percent_a, recommend_a = edge(true_prob_a, market_prob_a)
    edge_percent_b, recommend_b = edge(true_prob_b, market_prob_b)

    # 5. Display formatted results (:.2% converts decimals like 0.5061 to 50.61%; :+.2f shows +/- sign)
    print(
        f"\nSide A -> True Prob: {true_prob_a:.2%} | Market Prob: {market_prob_a:.2%} | "
        f"Edge: {edge_percent_a:+.2f}% | {recommend_a}"
    )
    print(
        f"Side B -> True Prob: {true_prob_b:.2%} | Market Prob: {market_prob_b:.2%} | "
        f"Edge: {edge_percent_b:+.2f}% | {recommend_b}"
    )

if __name__ == "__main__":
    main()