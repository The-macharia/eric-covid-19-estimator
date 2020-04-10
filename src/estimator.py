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


def normalize_days(data):
    if data['periodType'] == 'days':
        days = data['timeToElapse']
        return days
    if data['periodType'] == 'weeks':
        days = data['timeToElapse'] * 7
        return days
    if data['periodType'] == 'months':
        days = data['timeToElapse'] * 30
        return days


def estimation(data):
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
    return estimate


def estimationByTime(data):
    estimate = estimation(data)
    days = normalize_days(data)

    currentlyInfectedImpactByTime = estimate['impact']['currentlyInfected'] * (
        2 * int(days/3))
    currentlyInfectedSevereByTime = estimate['severeImpact']['currentlyInfected'] * (
        2 * int(days/3))

    estimate['impact']['infectionsByRequestedTime'] = currentlyInfectedImpactByTime
    estimate['severeImpact']['infectionsByRequestedTime'] = currentlyInfectedSevereByTime
    return estimate


def estimator(data):
    estimate = estimationByTime(data)
    return estimate


# print(estimator(sample))

