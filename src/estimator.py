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

    currentlyInfectedImpactByTime = int(estimate['impact']['currentlyInfected']
                                        * (2 ** int(days/3)))

    currentlyInfectedSevereByTime = int(estimate['severeImpact']
                                        ['currentlyInfected'] * (2 ** int(days/3)))

    estimate['severeImpact']['infectionsByRequestedTime'] = \
        currentlyInfectedSevereByTime
    estimate['impact']['infectionsByRequestedTime'] = \
        currentlyInfectedImpactByTime
    return estimate


def severeEstimationCases(data):
    estimate = estimationByTime(data)
    available_beds = int(
        0.35 * estimate['data']['totalHospitalBeds'])

    impact_severe_positive = int(0.15 *
                                 estimate['impact']['infectionsByRequestedTime'])
    severe_positive = int(0.15 *
                          estimate['severeImpact']['infectionsByRequestedTime'])

    estimate['impact']['severeCasesByRequestedTime'] = impact_severe_positive
    estimate['severeImpact']['severeCasesByRequestedTime'] = severe_positive

    estimate['impact']['hospitalBedsByRequestedTime'] = (
        available_beds - impact_severe_positive)
    estimate['severeImpact']['hospitalBedsByRequestedTime'] = (
        available_beds - severe_positive)
    return estimate


def infectionsToIcu(data):
    estimate = severeEstimationCases(data)

    impact_icu = int(
        0.05 * estimate['impact']['infectionsByRequestedTime'])
    severe_impact_icu = int(
        0.05 * estimate['severeImpact']['infectionsByRequestedTime'])

    estimate['impact']['casesForICUByRequestedTime'] = impact_icu
    estimate['severeImpact']['casesForICUByRequestedTime'] = severe_impact_icu
    return estimate


def requireVentilator(data):
    estimate = infectionsToIcu(data)

    impact_ventilators = int(
        0.02 * estimate['impact']['infectionsByRequestedTime'])
    severe_impact_ventilators = int(
        0.02 * estimate['severeImpact']['infectionsByRequestedTime'])

    estimate['impact']['casesForVentilatorsByRequestedTime'] = \
        impact_ventilators
    estimate['severeImpact']['casesForVentilatorsByRequestedTime'] = \
        severe_impact_ventilators

    return estimate


def dollarsInFlight(data):
    estimate = requireVentilator(data)
    days = normalize_days(data)

    loss = estimate['data']['region']['avgDailyIncomeInUSD'] * \
        estimate['data']['region']['avgDailyIncomePopulation']

    impact_dollars = int(
        (estimate['impact']['infectionsByRequestedTime'] * loss)/days)
    severe_impact_dollars = int(
        (estimate['severeImpact']['infectionsByRequestedTime'] * loss)/days)

    estimate['impact']['dollarsInFlight'] = impact_dollars
    estimate['severeImpact']['dollarsInFlight'] = severe_impact_dollars

    return estimate


def estimator(data):
    estimate = dollarsInFlight(data)
    return estimate


print(estimator(sample))
