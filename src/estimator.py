# sample = {
#     'region': {
#         'name': 'Africa',
#         'avgAge': 19.7,
#         'avgDailyIncomeInUSD': 5,
#         'avgDailyIncomePopulation': 0.71,
#     },
#     'periodType': 'days',
#     'timeToElapse': 58,
#     'reportedCases': 100,
#     'population': 66622705,
#     'totalHospitalBeds': 100
# }


# def normalize_days(data):
#     if data['periodType'] == 'days':
#         days = data['timeToElapse']
#     elif data['periodType'] == 'weeks':
#         days = data['timeToElapse'] * 7
#     elif data['periodType'] == 'months':
#         days = data['timeToElapse'] * 30
#     return days


# def estimation(data):
#     impact = {}
#     severeImpact = {}

#     currentlyInfected = int(data['reportedCases'] * 10)
#     severeImpactCases = int(data['reportedCases'] * 50)

#     impact['currentlyInfected'] = currentlyInfected
#     severeImpact['currentlyInfected'] = severeImpactCases
#     estimate = {
#         'data': data,
#         'impact': impact,
#         'severeImpact': severeImpact,
#     }

#     return estimate


# def estimationByTime(data):
#     estimate = estimation(data)
#     days = normalize_days(data)

#     currentlyInfectedImpactByTime = int(estimate['impact']['currentlyInfected']
#                                         * (2 ** int(days/3)))

#     currentlyInfectedSevereByTime = int(estimate['severeImpact']
#                                         ['currentlyInfected'] * (2 ** int(days/3)))

#     estimate['severeImpact']['infectionsByRequestedTime'] = \
#         currentlyInfectedSevereByTime
#     estimate['impact']['infectionsByRequestedTime'] = \
#         currentlyInfectedImpactByTime
#     return estimate


# def severeEstimationCases(data):
#     estimate = estimationByTime(data)
#     available_beds = int(
#         0.35 * estimate['data']['totalHospitalBeds'])

#     impact_severe_positive = int(0.15 *
#                                  estimate['impact']['infectionsByRequestedTime'])
#     severe_positive = int(0.15 *
#                           estimate['severeImpact']['infectionsByRequestedTime'])

#     estimate['impact']['severeCasesByRequestedTime'] = impact_severe_positive
#     estimate['severeImpact']['severeCasesByRequestedTime'] = severe_positive

#     estimate['impact']['hospitalBedsByRequestedTime'] = (
#         available_beds - impact_severe_positive)
#     estimate['severeImpact']['hospitalBedsByRequestedTime'] = (
#         available_beds - severe_positive)
#     return estimate


# def infectionsToIcu(data):
#     estimate = severeEstimationCases(data)

#     impact_icu = int(
#         0.05 * estimate['impact']['infectionsByRequestedTime'])
#     severe_impact_icu = int(
#         0.05 * estimate['severeImpact']['infectionsByRequestedTime'])

#     estimate['impact']['casesForICUByRequestedTime'] = impact_icu
#     estimate['severeImpact']['casesForICUByRequestedTime'] = severe_impact_icu
#     return estimate


# def requireVentilator(data):
#     estimate = infectionsToIcu(data)

#     impact_ventilators = int(
#         0.02 * estimate['impact']['infectionsByRequestedTime'])
#     severe_impact_ventilators = int(
#         0.02 * estimate['severeImpact']['infectionsByRequestedTime'])

#     estimate['impact']['casesForVentilatorsByRequestedTime'] = \
#         impact_ventilators
#     estimate['severeImpact']['casesForVentilatorsByRequestedTime'] = \
#         severe_impact_ventilators

#     return estimate


# def dollarsInFlight(data):
#     estimate = requireVentilator(data)
#     days = normalize_days(data)

#     loss = estimate['data']['region']['avgDailyIncomeInUSD'] * \
#         estimate['data']['region']['avgDailyIncomePopulation']

#     impact_dollars = int(
#         (estimate['impact']['infectionsByRequestedTime'] * loss)/days)
#     severe_impact_dollars = int(
#         (estimate['severeImpact']['infectionsByRequestedTime'] * loss)/days)

#     estimate['impact']['dollarsInFlight'] = impact_dollars
#     estimate['severeImpact']['dollarsInFlight'] = severe_impact_dollars

#     return estimate


# def estimator(data):
#     estimate = dollarsInFlight(data)
#     return estimate


# print(estimator(sample))


def get_infected(reportedCases, factor):
    infected = reportedCases * factor
    return infected


def get_infections_by_requested_time(currentlyInfected, days):
    factor = int((days // 3))
    infections_after_time_period = currentlyInfected * (2**factor)
    return infections_after_time_period


def normalise_days(periodType, value):
    """
    This is a helper function to normalise periodtype
    to always reflect the number of days
    """
    periodType = periodType.lower()
    normalised_days = 0
    if periodType == 'weeks':
        normalised_days = value * 7
    elif periodType == 'months':
        normalised_days = value * 30
    else:
        normalised_days = value
    return normalised_days


def get_severe_cases_by_requested_time(value, factor=0.15):
    cases = factor * value
    return cases


def get_available_beds(servereCases, totalHospitalBeds, average_available=0.35):
    available_beds = int(
        (average_available * totalHospitalBeds) - servereCases)
    return available_beds


def get_cases_for_ICU(infectionsByRequestedTime, factor=0.05):
    cases_for_ICU = factor * infectionsByRequestedTime
    return int(cases_for_ICU)


def get_cases_requiring_ventilators(infectionsByRequestedTime, factor=0.02):
    cases_requiring_ventilators = factor * infectionsByRequestedTime
    return int(cases_requiring_ventilators)


def get_dollars_in_flight(infections_by_requested_time, avg_earners, avg_daily_income, days):
    expected_loss = (infections_by_requested_time *
                     avg_earners * avg_daily_income) // days
    return expected_loss


def estimator(data):
    currentlyInfectedImpact = get_infected(data['reportedCases'], 10)
    currentlyInfectedServereImpact = get_infected(data['reportedCases'], 50)
    infectionsByRequestedTimeImpact = get_infections_by_requested_time(
        currentlyInfectedImpact,
        normalise_days(data['periodType'], data['timeToElapse'])
    )

    infectionsByRequestedTimeSevereImpact = get_infections_by_requested_time(
        currentlyInfectedServereImpact,
        normalise_days(data['periodType'], data['timeToElapse'])
    )

    severeCasesByRequestedTimeImpact = get_severe_cases_by_requested_time(
        infectionsByRequestedTimeImpact
    )
    severeCasesByRequestedTimeSevereImpact = get_severe_cases_by_requested_time(
        infectionsByRequestedTimeSevereImpact
    )

    hospitalBedsByRequestedTimeImpact = get_available_beds(
        severeCasesByRequestedTimeImpact,
        data['totalHospitalBeds']
    )
    hospitalBedsByRequestedTimeSevereImpact = get_available_beds(
        severeCasesByRequestedTimeSevereImpact,
        data['totalHospitalBeds'])

    casesForICUByRequestedTimeImpact = get_cases_for_ICU(
        infectionsByRequestedTimeImpact)
    casesForICUByRequestedTimeSevereImpact = get_cases_for_ICU(
        infectionsByRequestedTimeSevereImpact)

    casesForVentilatorsByRequestedTimeImpact = get_cases_requiring_ventilators(
        infectionsByRequestedTimeImpact)
    casesForVentilatorsByRequestedTimeSevereImpact = get_cases_requiring_ventilators(
        infectionsByRequestedTimeSevereImpact)

    dollarsInFlightImpact = get_dollars_in_flight(
        infectionsByRequestedTimeImpact,
        data['region']['avgDailyIncomePopulation'],
        data['region']['avgDailyIncomeInUSD'],
        normalise_days(data['periodType'], data['timeToElapse'])
    )
    dollarsInFlightSevereImpact = get_dollars_in_flight(
        infectionsByRequestedTimeSevereImpact,
        data['region']['avgDailyIncomePopulation'],
        data['region']['avgDailyIncomeInUSD'],
        normalise_days(data['periodType'], data['timeToElapse'])
    )

    impact = {
        "currentlyInfected": currentlyInfectedImpact,
        "infectionsByRequestedTime": infectionsByRequestedTimeImpact,
        "severeCasesByRequestedTime": severeCasesByRequestedTimeImpact,
        "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeImpact,
        "casesForICUByRequestedTime": casesForICUByRequestedTimeImpact,
        "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeImpact,
        "dollarsInFlight": dollarsInFlightImpact

    }

    severeImpact = {
        "currentlyInfected": currentlyInfectedServereImpact,
        "infectionsByRequestedTime": infectionsByRequestedTimeSevereImpact,
        "severeCasesByRequestedTime": severeCasesByRequestedTimeSevereImpact,
        "hospitalBedsByRequestedTime": hospitalBedsByRequestedTimeSevereImpact,
        "casesForICUByRequestedTime": casesForICUByRequestedTimeSevereImpact,
        "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeSevereImpact,
        "dollarsInFlight": dollarsInFlightSevereImpact
    }

    output = {
        "data": data,
        "impact": impact,
        "severeImpact": severeImpact
    }
    return output
