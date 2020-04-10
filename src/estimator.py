import math
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
    estimate = {
        'data': data,
        'impact': impact,
        'severeImpact': severeImpact,
    }

    return estimate


def estimationByTime(data):
    estimate = estimation(data)
    days = normalize_days(data)

    currentlyInfectedImpactByTime = estimate['impact']['currentlyInfected'] * (
        2 ** int(days/3))

    currentlyInfectedSevereByTime = estimate['severeImpact']['currentlyInfected'] * (
        2 ** int(days/3))

    estimate['severeImpact']['infectionsByRequestedTime'] = currentlyInfectedSevereByTime
    estimate['impact']['infectionsByRequestedTime'] = currentlyInfectedImpactByTime
    return estimate


def severeEstimationCases(data):
    estimate = estimationByTime(data)
    hospitalBedsByRequestedTime = math.floor(
        0.35 * estimate['data']['totalHospitalBeds'])

    impact_severe_positive = math.floor(
        0.15 * estimate['impact']['infectionsByRequestedTime'])
    severe_positive = math.floor(
        0.15 * estimate['severeImpact']['infectionsByRequestedTime'])
    currentlyInfected = int(data['reportedCases'] * 10)
    estimate['impact']['severeCasesByRequestedTime'] = impact_severe_positive
    estimate['impact']['hospitalBedsByRequestedTime'] = hospitalBedsByRequestedTime - \
        estimate['impact']['severeCasesByRequestedTime']

    estimate['severeImpact']['severeCasesByRequestedTime'] = severe_positive
    estimate['severeImpact']['hospitalBedsByRequestedTime'] = hospitalBedsByRequestedTime - \
        estimate['severeImpact']['severeCasesByRequestedTime']

    return estimate


def infectionsToIcu(data):
    estimate = severeEstimationCases(data)

    impact_icu = math.floor(0.05 * estimate['impact']['infectionsByRequestedTime'])
    severe_impact_icu = math.floor(0.05 * estimate['severeImpact']['infectionsByRequestedTime'])

    estimate['impact']['casesForICUByRequestedTime'] = impact_icu
    estimate['severeImpact']['casesForICUByRequestedTime'] = severe_impact_icu
    return estimate

def requireVentilator(data):
    estimate = infectionsToIcu(data)

    # impact_ventilators =
    return estimate

def estimator(data):
    estimate = requireVentilator(data)
    return estimate


# print(estimator(sample))
