#!/usr/bin/env python

"""
Create a G'DAY met forcing file from the Ozflux netcdf

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (21.04.2016)"
__email__ = "mdekauwe@gmail.com"

import sys
import os
import csv
import math
import numpy as np
from datetime import date
import calendar
import pandas as pd
from cStringIO import StringIO
import datetime as dt
import netCDF4 as nc


class CreateMetData(object):

    def __init__(self, fdir, site):

        self.fdir = fdir
        self.site = site
        self.fname = os.path.join(self.fdir, "%sOzFlux2.0_met.nc" % (site))
        self.spinup_ofname = "%s_met_spinup.csv" % (site)
        self.forcing_ofname = "%s_met_forcing.csv" % (site)
        self.ovar_names = ['#year', 'doy', 'hod', 'rain', 'par', 'tair',
                           'tsoil', 'vpd', 'co2', 'ndep', 'wind', 'press']
        self.ounits = ['#--', '--', '--', 'mm/30min', 'umol/m2/s','degC',
                       'degC', 'kPa', 'ppm', 't/ha/30min', 'm/s','kPa']
        self.lat = -999.9
        self.lon = -999.9

        # unit conversions
        self.SEC_TO_HFHR = 60.0 * 30.0 # sec/half hr
        self.PA_TO_KPA = 0.001
        self.J_TO_MJ = 1.0E-6
        self.K_to_C = 273.15
        self.G_M2_to_TONNES_HA = 0.01
        self.MM_S_TO_MM_30MIN = 1800.0
        self.SW_2_PAR = 2.3
        self.J_TO_UMOL = 4.57
        self.UMOL_TO_J = 1.0 / self.J_TO_UMOL

    def main(self):

        df = self.read_nc_file()
        print self.lat, self.lon

        # Create spinup file
        start_yr = df.index.year[0]
        end_yr = df.index.year[-1]

        num_yrs = 20
        yr_sequence = self.get_random_year_sequence(start_yr, end_yr, num_yrs,
                                                    preserve_leap=False)

        ndep = -999.9
        co2 = 285.0
        self.write_spinup_file(df, yr_sequence, vary_co2=False, co2_data=co2,
                               vary_ndep=False, ndep_data=ndep)


        all_years = np.unique(df.year)
        self.write_met_file(df, all_years, vary_co2=True, co2_data=None,
                            vary_ndep=False, ndep_data=None)

    def write_hdr(self, yr_sequence, ofname, spinup=True):
        start_sim = yr_sequence[0]
        end_sim = yr_sequence[-1]
        year = str(start_sim)

        if spinup:
            tag = "spinup"
        else:
            tag = "forcing"

        try:
            ofp = open(ofname, 'wb')
            wr = csv.writer(ofp, delimiter=',', quoting=csv.QUOTE_NONE,
                            escapechar=None, dialect='excel')
            wr.writerow(['# %s 30 min met %s' % (self.site, tag)])
            wr.writerow(['# Data from %s-%s' % (start_sim, end_sim)])
            wr.writerow(['# Created by Martin De Kauwe: %s' % date.today()])
            wr.writerow([var for i, var in enumerate(self.ounits)])
            wr.writerow([var for i, var in enumerate(self.ovar_names)])
        except IOError:
            raise IOError('Could not write met file: "%s"' % ofname)

        return (ofp, wr)


    def write_spinup_file(self, df, yr_sequence, vary_co2=False, co2_data=None,
                          vary_ndep=False, ndep_data=None):

        start_sim = yr_sequence[0]
        end_sim = yr_sequence[-1]
        (ofp, wr) = self.write_hdr(yr_sequence, self.spinup_ofname, spinup=True)
        self.write_data(df, yr_sequence, ofp, wr, self.spinup_ofname, vary_co2,
                        co2_data, vary_ndep, ndep_data)

    def write_met_file(self, df, yr_sequence, vary_co2=False,
                        co2_data=None, vary_ndep=False, ndep_data=None):

        start_sim = yr_sequence[0]
        end_sim = yr_sequence[-1]
        (ofp, wr) = self.write_hdr(yr_sequence, self.forcing_ofname,
                                   spinup=False)
        self.write_data(df, yr_sequence, ofp, wr, self.forcing_ofname,
                        vary_co2, co2_data, vary_ndep, ndep_data)

    def write_data(self, df, yr_sequence, ofp, wr, ofname, vary_co2=False,
                   co2=None, vary_ndep=False, ndep=None):

        # There is no Tsoil data, so we are going to use the day average of air
        # temperature and a 7-day running mean to remove some of the Tair=Tsoil
        tsoil = []
        dates = []
        for i, yr in enumerate(yr_sequence):
            days = np.unique(df[df.year == yr].doy)
            for j, doy in enumerate(days):
                days_data = df[(df.year == yr) & (df.doy == doy)]
                tsoil.append( np.mean(days_data["tair"]-self.K_to_C) )

        # need to flatten the list of lists...
        #dates = [item for sublist in dates for item in sublist]

        # for the spinup stuff the years not being in order will mess the dates
        # up, so make up some random date series. It doesn't really matter as
        # we aren't using the actual date for anything other than to interface
        # with the pandas lib
        st = dt.datetime.strptime("01/01/80 00:00:00", '%d/%m/%y %H:%M:%S')
        nintervals = len(tsoil)
        dates = pd.date_range(st, periods=nintervals, freq='D')

        D = pd.Series(tsoil, dates)
        window_size = 7
        d_mva = D.rolling(window=window_size).mean()

        # The first few values will be nans, so we will use the 24-hr tair
        # values as replacements here
        for i in xrange(window_size-1):
            d_mva[i] = tsoil[i]
        tsoil_data = d_mva.values

        cnt = 0
        for i, yr in enumerate(yr_sequence):
            days = np.unique(df[df.year == yr].doy)
            for j, doy in enumerate(days):
                days_data = df[(df.year == yr) & (df.doy == doy)]

                # otherwise we can't index 0-47 for HOD
                days_data = days_data.reset_index()
                for hod in xrange(len(days_data)):

                    # mm/sec -> mm/30 min
                    rain = days_data.rain[hod] * self.MM_S_TO_MM_30MIN
                    par = days_data.sw[hod] * self.SW_2_PAR
                    if par < 0.0:
                        par = 0.0
                    tair = days_data.tair[hod] - self.K_to_C
                    #tsoil = np.mean(days_data.tair) - self.K_to_C
                    tsoil = tsoil_data[cnt]
                    qair = days_data.qair[hod]

                    if vary_co2:
                        co2_val = days_data.co2[hod]
                    else:
                        co2_val = co2

                    ndep = -999.9

                    wind = days_data.wind[hod]

                    # Zero wind values seem to be messing up simulations
                    if wind <= 0.05:
                        wind = 0.05

                    press = days_data.press[hod] * self.PA_TO_KPA
                    vpd = self.qair_to_vpd(qair, tair, press)
                    if vpd < 0.05:
                        vpd = 0.05


                    wr.writerow([yr, doy, hod, rain, par, tair, tsoil, vpd, \
                                 co2_val, ndep, wind, press])
                cnt += 1

        ofp.close()

    def read_nc_file(self):
        """ Build a DF from the netcdf outputs """

        f = nc.Dataset(self.fname)

        # check timestep, some are 30 min, some are an hour
        #t = nc.num2date(f.variables['time'][:]-1800.0, f.variables['time'].units)
        #for i in t:
        #    print i
        #sys.exit()

        times = f.variables['time']
        date_time = nc.num2date(times[:], times.units)

        self.lat = f.variables['latitude'][0,0]
        self.lon = f.variables['longitude'][0,0]

        df = pd.DataFrame(f.variables['SWdown'][:,0,0], columns=['sw']) # W/m^2
        df['tair'] = f.variables['Tair'][:,0,0]                         # deg K
        df['rain'] = f.variables['Rainf'][:,0,0]                        # mm/s
        df['qair'] = f.variables['Qair'][:,0,0]                         # kg/kg
        df['wind'] = f.variables['Wind'][:,0,0]                         # m/s
        df['press'] = f.variables['PSurf'][:,0,0]                       # Pa
        df['co2'] = f.variables['CO2air'][:,0,0]                        # ppmv

        # PALS netcdf is missing the first hours timestamp and has one extra
        # from the next year, so we need to fix this. We will duplicate the
        # first hour interval and remove the last

        # Correct for missing date
        #extra_time_index = date_time[0] - dt.timedelta(minutes=30)
        #date_time = np.insert(date_time, 0, extra_time_index)

        # Get the first row so we can reinsert it again
        #df2 = pd.DataFrame(df.iloc[0].values.reshape(1,7), columns=df.columns)

        # reinsert the first row
        #df = df2.append(df, ignore_index = True)

        # adding correct datetime information
        df['dates'] = date_time
        df = df.set_index('dates')
        df['year'] = df.index.year
        df['doy'] = df.index.dayofyear

        # Drop the final row which is from the next eyar.
        #df = df.ix[:-1]

        return df

    def round_minutes(self, t): # t is a datetime object
        return (t - dt.timedelta(minutes = t.minute - round(t.minute, -1),
                    seconds = t.second, microseconds = t.microsecond))

    def get_random_year_sequence(self, start_yr, end_yr, out_yrs,
                                 preserve_leap=False):

        # Set the seed so we can repeat this if required
        np.random.seed(42)
        yrs = np.arange(start_yr, end_yr+1)

        if preserve_leap:

            # preserve leap yrs, so find them first
            leapyrs = np.zeros(0)
            for yr in yrs:
                if calendar.isleap(yr):
                    leapyrs = np.append(leapyrs, yr)


            # However we don't want the leapyrs in the sequence, so exclude them
            yrs = np.array([yrs[i] for i, yr in enumerate(yrs) \
                                    if yr not in leapyrs])

            shuff_years = self.randomise_array(out_yrs, yrs)
            shuff_years_leap = self.randomise_array(out_yrs, leapyrs)

            sequence = []
            i = 0
            for yr in np.arange(start_yr, end_yr+1):

                if i == 0:
                    prev_yr_leap = 1666 # anything not in the sequence
                    prev_yr = 1666 # anything not in the sequence

                if calendar.isleap(yr):
                    out_yr = shuff_years_leap[i]

                    # Make sure we don't get the same year twice
                    while prev_yr_leap == int(out_yr):
                        i += 1
                        out_yr = shuff_years_leap[i]

                    sequence.append(out_yr)
                    prev_yr_leap = shuff_years_leap[i]
                else:
                    out_yr = shuff_years[i]

                    # Make sure we don't get the same year twice
                    while prev_yr == int(out_yr):
                        i += 1
                        out_yr = shuff_years[i]

                    sequence.append(out_yr)
                    prev_yr = shuff_years[i]

                i += 1
        else:
            yrs = np.array([yrs[i] for i, yr in enumerate(yrs)])
            shuff_years = self.randomise_array(out_yrs, yrs)
            yr_list = np.random.uniform(start_yr, end_yr,
                                        out_yrs).astype(np.int)
            sequence = []
            i = 0
            for yr in yr_list:

                if i == 0:
                    prev_yr = 1666 # anything not in the sequence

                out_yr = shuff_years[i]

                # Make sure we don't get the same year twice
                while prev_yr == int(out_yr):
                    i += 1
                    out_yr = shuff_years[i]

                sequence.append(out_yr)
                prev_yr = shuff_years[i]

                i += 1

        return sequence

    def randomise_array(self, out_yrs, yrs):
        # make a sequence longer than the number of years we actually want
        num_seq = np.ones(out_yrs * len(yrs))
        num_years = len(yrs) * len(num_seq)
        shuff_years = (yrs * num_seq[:,None]).reshape(num_years)
        np.random.shuffle(shuff_years)

        return shuff_years

    def qair_to_vpd(self, qair, tair, press):

        # convert back to Pa
        press /= self.PA_TO_KPA

        # saturation vapor pressure
        es = 100.0 * 6.112 * np.exp((17.67 * tair) / (243.5 + tair))

        # vapor pressure
        ea = (qair * press) / (0.622 + (1.0 - 0.622) * qair)

        vpd = (es - ea) * self.PA_TO_KPA

        return vpd

if __name__ == "__main__":

    fdir = "/Users/%s/Documents/Postdoc/OzFlux" % (os.getlogin())
    #fdir = os.getcwd()
    site = "CumberlandPlains"

    C = CreateMetData(fdir, site)
    C.main()
