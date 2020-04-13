import math
sample = {
    'region': {
        'name': 'Africa',
        'avgAge': 19.7,
        'avgDailyIncomeInUSD': 5,
        'avgDailyIncomePopulation': 0.71,
    },
    'periodType': 'days',
    'timeToElapse': 58,
    'reportedCases': 100,
    'population': 66622705,
    'totalHospitalBeds': 100
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

    currentlyInfected = math.floor(data['reportedCases'] * 10)
    severeImpactCases = math.floor(data['reportedCases'] * 50)

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
        2 ** math.floor(days/3))

    currentlyInfectedSevereByTime = estimate['severeImpact']['currentlyInfected'] * (
        2 ** math.floor(days/3))

    estimate['severeImpact']['infectionsByRequestedTime'] = currentlyInfectedSevereByTime
    estimate['impact']['infectionsByRequestedTime'] = currentlyInfectedImpactByTime
    return estimate


def severeEstimationCases(data):
    estimate = estimationByTime(data)
    hospitalBedsByRequestedTime = 0.35 * estimate['data']['totalHospitalBeds']

    # impact_severe_positive = math.floor(
    #     0.15 * estimate['impact']['infectionsByRequestedTime'])
    # severe_positive = math.floor(
    #     0.15 * estimate['severeImpact']['infectionsByRequestedTime'])

    impact_severe_positive = 0.15 * \
        estimate['impact']['infectionsByRequestedTime']
    severe_positive = 0.15 * \
        estimate['severeImpact']['infectionsByRequestedTime']

    estimate['impact']['severeCasesByRequestedTime'] = math.floor(
        impact_severe_positive)
    estimate['severeImpact']['severeCasesByRequestedTime'] = math.floor(
        severe_positive)

    estimate['impact']['hospitalBedsByRequestedTime'] = math.floor(
        hospitalBedsByRequestedTime - impact_severe_positive)
    estimate['severeImpact']['hospitalBedsByRequestedTime'] = math.floor(
        hospitalBedsByRequestedTime - severe_positive)

    # estimate['impact']['hospitalBedsByRequestedTime'] = math.floor(hospitalBedsByRequestedTime - \
    #     estimate['impact']['severeCasesByRequestedTime'])

    # estimate['severeImpact']['hospitalBedsByRequestedTime'] = math.floor(hospitalBedsByRequestedTime - \
    #     estimate['severeImpact']['severeCasesByRequestedTime'])

    return estimate


def infectionsToIcu(data):
    estimate = severeEstimationCases(data)

    impact_icu = math.floor(
        0.05 * estimate['impact']['infectionsByRequestedTime'])
    severe_impact_icu = math.floor(
        0.05 * estimate['severeImpact']['infectionsByRequestedTime'])

    estimate['impact']['casesForICUByRequestedTime'] = impact_icu
    estimate['severeImpact']['casesForICUByRequestedTime'] = severe_impact_icu
    return estimate


def requireVentilator(data):
    estimate = infectionsToIcu(data)

    impact_ventilators = math.floor(
        0.02 * estimate['impact']['infectionsByRequestedTime'])
    severe_impact_ventilators = math.floor(
        0.02 * estimate['severeImpact']['infectionsByRequestedTime'])

    estimate['impact']['casesForVentilatorsByRequestedTime'] = impact_ventilators
    estimate['severeImpact']['casesForVentilatorsByRequestedTime'] = severe_impact_ventilators

    return estimate


def dollarsInFlight(data):
    estimate = requireVentilator(data)
    days = normalize_days(data)

    loss = estimate['data']['region']['avgDailyIncomeInUSD'] * \
        estimate['data']['region']['avgDailyIncomePopulation']
    impact_dollars = math.floor(
        (estimate['impact']['infectionsByRequestedTime'] * loss)/days)
    severe_impact_dollars = math.floor(
        (estimate['severeImpact']['infectionsByRequestedTime'] * loss)/days)

    estimate['impact']['dollarsInFlight'] = impact_dollars
    estimate['severeImpact']['dollarsInFlight'] = severe_impact_dollars

    return estimate


def estimator(data):
    estimate = dollarsInFlight(data)
    return estimate


# print(estimator(sample))
