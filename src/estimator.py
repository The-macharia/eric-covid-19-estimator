sample = {
    'region': {
        'name': 'Africa',
        'avgAge': 19.7,
        'avgDailyIncomeInUSD': 5,
        'avgDailyIncomePopulation': 0.71,
    },
    'periodType': 'days',
    'timeToElapse': 61,
    'reportedCases': 674.56,
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
    impact = {}
    severeImpact = {}

    currentlyInfected = int(data['reportedCases'] * 10)
    severeImpactCases = int(data['reportedCases'] * 50)

    impact['currentlyInfected'] = currentlyInfected
    severeImpact['currentlyInfected'] = severeImpactCases
    # estimate = {
    #     'data': data,
    #     'impact': impact,
    #     'severeImpact': severeImpact,
    # }
    estimate = {
        'data': data,
        'impact': {
            'currentlyInfected': float(currentlyInfected),
        },
        'severeImpact': {
            'currentlyInfected': float(severeImpactCases)
        },
    }
    return estimate


def estimationByTime(data):
    estimate = estimation(data)
    days = normalize_days(data)

    currentlyInfectedImpactByTime = estimate['impact']['currentlyInfected'] * (
        2 * int(days/3))

    currentlyInfectedSevereByTime = estimate['severeImpact']['currentlyInfected'] * (
        2 * int(days/3))

    estimate['severeImpact']['infectionsByRequestedTime'] = currentlyInfectedSevereByTime
    estimate['impact']['infectionsByRequestedTime'] = currentlyInfectedImpactByTime
    return estimate


def severeEstimationCases(data):
    estimate = estimationByTime(data)
    hospitalBedsByRequestedTime = int(
        0.35 * estimate['data']['totalHospitalBeds'])

    impact_severe_positive = int(
        0.15 * estimate['impact']['infectionsByRequestedTime'])
    severe_positive = int(
        0.15 * estimate['severeImpact']['infectionsByRequestedTime'])

    estimate['impact']['severeCasesByRequestedTime'] = impact_severe_positive
    estimate['impact']['hospitalBedsByRequestedTime'] = hospitalBedsByRequestedTime - \
        estimate['impact']['severeCasesByRequestedTime']

    estimate['severeImpact']['severeCasesByRequestedTime'] = severe_positive
    estimate['severeImpact']['hospitalBedsByRequestedTime'] = hospitalBedsByRequestedTime - \
        estimate['severeImpact']['severeCasesByRequestedTime']

    return estimate


def estimator(data):
    estimate = severeEstimationCases(data)
    return estimate


print(estimator(sample))
