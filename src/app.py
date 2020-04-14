from flask import Flask, render_template, redirect, url_for, request, session
from form import DataForm
from estimator import estimator

app = Flask(__name__)
app.secret_key = '9013654d84b8b311a460ca1d7bbb9ddfer'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = DataForm()
    if form.is_submitted():
        data = {
            'region': {
                'name': 'Africa',
                'avgAge': 19.7,
                'avgDailyIncomeInUSD': 5,
                'avgDailyIncomePopulation': 0.71,
            },
            'periodType': form.period_type.data,
            'timeToElapse': form.time_to_elapse.data,
            'reportedCases': form.reported_cases.data,
            'population': form.population.data,
            'totalHospitalBeds': form.hospital_beds.data
        }
        estimate = estimator(data)
        session['estimate'] = estimate
        return redirect(url_for('estimation'))
    return render_template('home.html', title='Home', form=form)


def create_impact_values(data):
    return {
        'currentlyInfected': data['impact']['currentlyInfected'],
        'infectionsByRequestedTime': data['impact']['infectionsByRequestedTime'],
        'severeCasesByRequestedTime': data['impact']['severeCasesByRequestedTime'],
        'casesForVentilatorsByRequestedTime': data['impact']['casesForVentilatorsByRequestedTime'],
        'hospitalBedsByRequestedTime': data['impact']['hospitalBedsByRequestedTime'],
        'casesForICUByRequestedTime': data['impact']['casesForICUByRequestedTime'],
        'dollarsInFlight': data['impact']['dollarsInFlight']}


def create_severe_impact_values(data):
    return {
        's_currentlyInfected': data['severeImpact']['currentlyInfected'],
        's_infectionsByRequestedTime': data['severeImpact']['infectionsByRequestedTime'],
        's_severeCasesByRequestedTime': data['severeImpact']['severeCasesByRequestedTime'],
        's_casesForVentilatorsByRequestedTime': data['severeImpact']['casesForVentilatorsByRequestedTime'],
        's_hospitalBedsByRequestedTime': data['severeImpact']['hospitalBedsByRequestedTime'],
        's_casesForICUByRequestedTime': data['severeImpact']['casesForICUByRequestedTime'],
        's_dollarsInFlight': data['severeImpact']['dollarsInFlight']}


@app.route('/estimation')
def estimation():
    if 'estimate' in session:
        estimate = session['estimate']

    impact_data = create_impact_values(estimate)
    severe_data = create_severe_impact_values(estimate)

    return render_template('estimation.html', title='Estimation', impact_data=impact_data, severe_data=severe_data)


if __name__ == "__main__":
    app.run(debug=True)
