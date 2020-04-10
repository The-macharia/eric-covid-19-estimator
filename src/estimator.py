# sample = {
#     'region': {
#         'name': 'Africa',
#         'avgAge': 19.7,
#         'avgDailyIncomeInUSD': 5,
#         'avgDailyIncomePopulation': 0.71,
#     },
#     'periodType': 'days',
#     'timeToElapse': 58,
#     'reportedCases': 674,
#     'population': 66622705,
#     'totalHospitalBeds': 1380614
# }


def estimator(data):
    impact = dict()
    severeImpact = dict()

    currentlyInfected = data['reportedCases'] * 10
    severeImpactCases = data['reportedCases'] * 50

    impact['currentlyInfected'] = currentlyInfected
    severeImpact['currentlyInfected'] = severeImpactCases
    estimate = {
        'data': data,
        'impact': impact,
        'severeImpact': severeImpact
    }

    currentlyInfectedImpactByTime = estimate['impact']['currentlyInfected'] * (
        2 * int(estimate['data']['timeToElapse']/3))

    currentlyInfectedSevereByTime = estimate['severeImpact']['currentlyInfected'] * (
        2 * int(estimate['data']['timeToElapse']/3))

    estimate['impact']['infectionsByRequestedTime'] = currentlyInfectedImpactByTime
    estimate['severeImpact']['infectionsByRequestedTime'] = currentlyInfectedSevereByTime

    return estimate

# print(estimator(sample))


# def estimationByTime(sample):
#     estimate = estimator(sample)

#     currentlyInfectedImpactByTime = estimate['impact']['currentlyInfected'] * (
#         2 * int(estimate['data']['timeToElapse']/3))
#     currentlyInfectedSevereByTime = estimate['severeImpact']['currentlyInfected'] * (
#         2 * int(estimate['data']['timeToElapse']/3))

#     estimate['impact']['infectionsByRequestedTime'] = currentlyInfectedImpactByTime
#     estimate['severeImpact']['infectionsByRequestedTime'] = currentlyInfectedSevereByTime
#     return estimate


# if __name__ == "__main__":
#     estimationByTime(data)