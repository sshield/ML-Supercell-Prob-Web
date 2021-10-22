import flask
import pickle
import pandas as pd
# Use pickle to load in the pre-trained model.
with open(f'model/SPI_GBT.sav', 'rb') as f:
    model = pickle.load(f)
app = flask.Flask(__name__, template_folder='templates')
@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        MUCAPE = flask.request.form['Most Unstable Parcel CAPE']
        MUCIN = flask.request.form['Most Unstable Parcel CIN']
        MULCL = flask.request.form['Most Unstable Parcel LCL']
        LLCAPE = flask.request.form['Most Unstable Parcel CAPE in the 3km above the LFC']
        sfc1shear = flask.request.form['0-1 Bulk Wind Difference']
        EBWD = flask.request.form['Effective Bulk Wind Difference']
        ESRH = flask.request.form['Effective Storm Relative Helicity']
        el_sr_wind = flask.request.form['Storm Relative Wind at the Equlibrium Level']
        eff_inflow_sr_wind = flask.request.form['Storm Relative Wind in the Effective Inflow Layer']
        input_variables = pd.DataFrame([[MUCAPE, MUCIN, MULCL, LLCAPE, sfc1shear, EBWD, ESRH, el_sr_wind, eff_inflow_sr_wind]],
                                       columns=['MUCAPE', 'MUCIN', 'MULCL', 'LLCAPE', 'sfc1shear', 'EBWD', 'ESRH', 'el_sr_wind', 'eff_inflow_sr_wind'],
                                       dtype=float)
        prediction = 100*round(model.predict_proba(input_variables)[:,-1][0],3)
        return flask.render_template('main.html',
                                     original_input={'Most Unstable Parcel CAPE':MUCAPE,
                                                     'Most Unstable Parcel CIN':MUCIN,
                                                     'Most Unstable Parcel LCL':MULCL,
                                                     'Most Unstable Parcel CAPE in the 3km above the LFC':LLCAPE,
                                                     '0-1 Bulk Wind Difference':sfc1shear,
                                                     'Effective Bulk Wind Difference':EBWD,
                                                     'Effective Storm Relative Helicity':ESRH,
                                                     'Storm Relative Wind at the Equlibrium Level':el_sr_wind,
                                                     'Storm Relative Wind in the Effective Inflow Layer':eff_inflow_sr_wind},
                                     result=prediction,)
                                     
if __name__ == '__main__':
    app.run()