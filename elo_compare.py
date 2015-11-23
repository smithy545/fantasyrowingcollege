# All the elo ratings functions used for the project. Still needs some work.

def eloCompare(winner, loser, margin = 1, K = 32):
    # Expected rating of the winner and loser based on ELO formula (range 0-1)
    expectedWinner = 1 / (1 + 10.0**((loser - winner)/ 400.0))
    expectedLoser = 1 / (1 + 10.0**((winner - loser)/ 400.0))

    # Margin of Victory adjustment
    MOV_modifier = ((margin + 3.0)**0.8) / (7.5 + 0.006*(winner - loser))

    # K adjustment value (Base K * MOV adjustment)
    K *= MOV_modifier
    
    # In case of tie (pretty much impossible in rowing but maintained for completeness sake)
    if margin == 0:
        adjustedWinner = winner + K*(0.5 - expectedWinner)
        adjustedLoser = loser + K*(0.5 - expectedLoser)
        return (adjustedWinner, adjustedLoser)
    
    # New adjusted ratings based on previous ratings and victory
    adjustedWinner = winner + K*(1 - expectedWinner)
    adjustedLoser = loser + K*(0 - expectedLoser)

    return (adjustedWinner, adjustedLoser)

def eloCompareMany(times, ratings, K = 32):
    for i, time1 in enumerate(times):
        temp1 = 0
        temp2 = 0
        rating1 = ratings[i]
        for j in range(i + 1, len(times)):
            rating2 = ratings[j]
            time2 = times[j]
            if time1 == 0 or time2 == 0 or time1 == time2:
                # no participant in race
                continue
            elif time1 < time2:
                rating1, rating2 = eloCompare(rating1, rating2, time2 - time1, K)
            else:
                rating2, rating1 = eloCompare(rating2, rating1, time1 - time2, K)
            ratings[j] = rating2
        ratings[i] = rating1
    return ratings

def eloAdjust(times, ratings, raceType):
    KHEAD = 14
    KSPRINT = 24
    KSECOND = 5
    KOTHER = 10
    
    if raceType == "head":
        return eloCompareMany(times, ratings, KHEAD)
    elif raceType == "sprint":
        return eloCompareMany(times, ratings, KSPRINT)
    elif raceType == "second":
        return eloCompareMany(times, ratings, KSECOND)
    else:
        return eloCompareMany(times, ratings, KOTHER)
    
def roundList(a, degree = 2):
    temp = []
    for item in a:
        temp.append(round(item, degree))
    return temp
