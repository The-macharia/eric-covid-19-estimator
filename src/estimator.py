sample = {
    'region': {
        'name': 'Africa',
        'avgAge': 19.7,
        'avgDailyIncomeInUSD': 5,
        'avgDailyIncomePopulation': 0.71,
    },
    'periodType': 'days',
    'timeToElapse': 58,
    'reportedCases': 674,
    'population': 66622705,
    'totalHospitalBeds': 1380614
}


def normalize_days(data):
    if data['periodType'] == 'days':
        days = data['timeToElapse']
    elif data['periodType'] == 'weeks':
        days = data['timeToElapse'] * 7
    elif data['periodType'] == 'months':
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
        'estimate': {
            'impact': impact,
            'severeImpact': severeImpact
        },
    }
    return estimate


def estimationByTime(data):
    estimate = estimation(data)
    days = normalize_days(data)

    currentlyInfectedImpactByTime = estimate['estimate']['impact']['currentlyInfected'] * (
        2 * int(days/3))

    currentlyInfectedSevereByTime = estimate['estimate']['severeImpact']['currentlyInfected'] * (
        2 * int(days/3))

    estimate['estimate']['severeImpact']['infectionsByRequestedTime'] = currentlyInfectedSevereByTime
    estimate['estimate']['impact']['infectionsByRequestedTime'] = currentlyInfectedImpactByTime
    return estimate


def estimator(data):
    estimate = estimationByTime(data)
    return estimate


print(estimator(sample))
