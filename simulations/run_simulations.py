#!/usr/bin/env python

"""
Ozflux simulations: CumberlandPlains

(i) Spin-up using 20 years of recycled met data: CO2 = 285; n-cycle off,
    LAI precribed from MODIS.
(ii) Run simulation using met forcing years, with CO2 varying.

For these simulations we are going to paramaterise GDAY as best we can using
CABLE's evergreen broadleaf forest paramaters.
"""

import numpy as np
import os
import shutil
import sys
import subprocess

__author__  = "Martin De Kauwe"
__version__ = "1.0 (31.03.2015)"
__email__   = "mdekauwe@gmail.com"

USER = os.getlogin()
sys.path.append('/Users/%s/Documents/Research/Projects/Temperature_acclimation/Git/GDAY/scripts' % (USER))
import adjust_gday_param_file as ad

sys.path.append("../scripts")
from read_flt_file import ReadFltFile

def main(experiment_id, latitude, longitude, albedo, topsoil_type,
         rootsoil_type, finesoil, SPIN_UP=False, RUN_SIM=False):

    GDAY_SPIN = "./gday -s -p "
    GDAY = "./gday -p "

    # dir names
    base_param_name = "base_start"

    base_dir = os.path.dirname(os.getcwd())
    base_param_dir = "/Users/%s/Documents/Git/GDAY/example/params" % (USER)
    param_dir = os.path.join(base_dir, "params")
    met_dir = os.path.join(base_dir, "met_data")
    run_dir = os.path.join(base_dir, "outputs")

    if SPIN_UP == True:

        # copy base files to make two new experiment files
        shutil.copy(os.path.join(base_param_dir, base_param_name + ".cfg"),
                    os.path.join(param_dir, "%s_model_spinup.cfg" % \
                                                (experiment_id)))

        # Run model to equilibrium assuming forest, growing C pools from effectively
        # zero
        itag = "%s_model_spinup" % (experiment_id)
        otag = "%s_model_spunup" % (experiment_id)
        mtag = "%s_met_spinup.csv" % (experiment_id)
        out_fn = itag + "_equilib.out"
        out_param_fname = os.path.join(param_dir, otag + ".cfg")
        cfg_fname = os.path.join(param_dir, itag + ".cfg")
        met_fname = os.path.join(met_dir, mtag)
        out_fname = os.path.join(run_dir, out_fn)
        replace_dict = {
                        # files
                        "out_param_fname": "%s" % (out_param_fname),
                        "cfg_fname": "%s" % (cfg_fname),
                        "met_fname": "%s" % (met_fname),
                        "out_fname": "%s" % (out_fname),

                        # default C:N 25.
                        "canht": "20.0",           # made this up
                        "activesoil": "0.001",
                       # "activesoil": "1.5",
                        "activesoiln": "0.00004",
                        "age": "0.0",
                        "branch": "0.001",
                        "branchn": "0.00004",
                        "cstore": "0.0",
                        "nstore": "0.0",
                        "inorgn": "0.00004",
                        "metabsoil": "0.0",
                        "metabsoiln": "0.0",
                        "metabsurf": "0.0",
                        "metabsurfn": "0.0",
                        "passivesoil": "0.001",
                        "passivesoiln": "0.0004",
                        "prev_sma": "1.0",
                        "root": "0.001",
                        "croot": "0.0",   # don't simulate coarse roots
                        "crootn": "0.0",  # don't simulate coarse roots
                        "rootn": "0.00004",
                        "sapwood": "0.001",
                        "shoot": "0.001",
                        "shootn": "0.00004",
                        "slowsoil": "0.001",
                        "slowsoiln": "0.00004",
                        "stem": "0.001",
                        "stemn": "0.00004",
                        "stemnimm": "0.00004",
                        "stemnmob": "0.0",
                        "structsoil": "0.001",
                        "structsoiln": "0.00004",
                        "structsurf": "0.001",
                        "structsurfn": "0.00004",

                        # parameters
                        #"fix_lai": "1.5",
                        "alpha_j": "0.30588",
                        "intercep_frac": "0.15",
                        "max_intercep_lai": "3.0",
                        "latitude": "%f" % (latitude),
                        "longitude": "%f" % (longitude),
                        "albedo": "%f" % (albedo),
                        "finesoil": "%f" % (finesoil),   # silt + clay fraction. Surface soil texture (upper 45 cm) for Clarenden sand: 80 +/- 8% sand, 9 +/- 5% silt, 11 +/- 3% clay
                        "slamax": "4.37",    # 43.7 +/- 1.5 cm2 g 1 dry mass
                        "sla": "4.37",       # 43.7 +/-  1.5 cm2 g 1 dry mass
                        "slazero": "4.37",   # 43.7+/-  1.5 cm2 g 1 dry mass
                        "lai_cover": "0.5",
                        "c_alloc_fmax": "0.35",      # max leaf alloc, using allometric model
                        "c_alloc_fmin": "0.35",
                        "c_alloc_rmax": "0.1",       # Fix root allocation
                        "c_alloc_rmin": "0.1",
                        "c_alloc_bmax": "0.1",       # 34% goes to wood, of which 24% goes to branches - email from DE, Keith et al. (1997) Plant and Soil 196: 81-99.
                        "c_alloc_bmin": "0.1",       # 34% goes to wood, of which 24% goes to branches - email from DE, Keith et al. (1997) Plant and Soil 196: 81-99.
                        "c_alloc_cmax": "0.0",       # turn off coarse roots!
                        "fretrans": "0.5",
                        "rretrans": "0.0",
                        "bretrans": "0.0",
                        "wretrans": "0.0",
                        "cretrans": "0.0",
                        "ncwnewz": "0.003",          #New stem ring N:C at zero leaf N:C (mobile)
                        "ncwnew": "0.003",           #New stem ring N:C at critical leaf N:C (mob)
                        "ncwimmz": "0.003",          #Immobile stem N C at zero leaf N C
                        "ncwimm": "0.003",           #Immobile stem N C at critical leaf N C
                        "ncbnewz": "0.003",          #new branch N C at zero leaf N C
                        "ncbnew": "0.003",           #new branch N C at critical leaf N C
                        "nccnewz": "0.003",          #new coarse root N C at zero leaf N C
                        "nccnew": "0.003",           #new coarse root N C at critical leaf N C
                        "ncrfac": "0.8",
                        "ncmaxfyoung": "0.04",
                        "ncmaxfold": "0.04",
                        "ncmaxr": "0.03",
                        "retransmob": "0.0",
                        "fdecay": "0.6",         # 18 mth turnover * 1/30
                        "fdecaydry": "0.6",      # 18 mth turnover * 1/30
                        "rdecay": "0.6",
                        "rdecaydry": "0.6",
                        "crdecay": "0.00",       # turn off coarse roots!
                        "bdecay": "0.02",        # no idea, assuming 50 years
                        "wdecay": "0.02",        # no idea, assuming 50 years
                        "watdecaydry": "0.0",
                        "watdecaywet": "0.1",
                        "ligshoot": "0.25",
                        "ligroot": "0.25",
                        "rateuptake": "3.0",
                        "rateloss": "0.1",
                        "topsoil_depth": "50.0",
                        "rooting_depth": "2000.0",
                        "topsoil_type": topsoil_type,
                        "rootsoil_type": rootsoil_type,
                        "ctheta_topsoil": "-999.9",     # Derive based on soil type
                        "ntheta_topsoil": "-999.9",     # Derive based on soil type
                        "ctheta_root": "-999.9",        # Derive based on soil type
                        "ntheta_root": "-999.9",        # Derive based on soil type
                        #"dz0v_dh": "0.1",
                        #"z0h_z0m": "1.0",
                        #"displace_ratio": "0.67",

                        "dz0v_dh": "0.05",         # Using Value from JULES for TREE PFTs as I don't know what is best. However I have used value from Jarvis, quoted in Jones 1992, pg. 67. Produces a value within the bounds of 3.5-1.1 mol m-2 s-1 Drake, 2010, GCB for canht=17
                        "displace_ratio": "0.75",  # From Jones, pg 67, following Jarvis et al. 1976
                        "z0h_z0m": "1.0",

                        "g1": "3.8667",      # Fit by Me to Teresa's data 7th Nov 2013
                        "jmax": "110.0",   # 2.0 * vcmax
                        "vcmax": "55.0",   # CABLE EBF
                        "jmaxna": "-999.9",
                        "jmaxnb": "-999.9",
                        "vcmaxna": "-999.9",
                        "vcmaxnb": "-999.9",
                        "measurement_temp": "25.0",
                        "heighto": "4.826",
                        "htpower": "0.35",
                        "height0": "5.0",
                        "height1": "30.0",
                        "leafsap0": "4000.0",
                        "leafsap1": "2700.0",
                        "branch0": "5.61",
                        "branch1": "0.346",
                        "croot0": "0.34",
                        "croot1": "0.84",
                        "targ_sens": "0.5",
                        "density": "480.0",
                        "nf_min": "0.005",
                        "nf_crit": "0.015",
                        "sapturnover": "0.1",

                        "prescribed_leaf_NC": "0.03",

                        # control
                        "adjust_rtslow": "false",  # priming, off
                        "alloc_model": "fixed",
                        "assim_model": "mate",
                        "calc_sw_params": "true",   #false=use fwp values, true=derive them
                        "deciduous_model": "false",
                        "disturbance": "false",
                        "exudation": "false",
                        "fixed_stem_nc": "true",
                        "fixed_lai": "false",
                        "fixleafnc": "false",
                        "grazing": "false",
                        "gs_model": "medlyn",
                        "output_ascii": "true",
                        "input_ascii": "true",
                        "model_optroot": "false",
                        "modeljm": "3",
                        "ncycle": "false",
                        "nuptake_model": "1",
                        "passiveconst": "false",
                        "print_options": "end",
                        "ps_pathway": "c3",
                        "respiration_model": "fixed",
                        "sub_daily": "true",
                        "strfloat": "0",
                        "sw_stress_model": "1",  # Sands and Landsberg
                        "water_stress": "true",
        }
        ad.adjust_param_file(cfg_fname, replace_dict)
        os.system(GDAY_SPIN + cfg_fname)


    if RUN_SIM == True:

        # dir names
        param_dir = os.path.join(base_dir, "params")
        met_dir = os.path.join(base_dir, "met_data")
        run_dir = os.path.join(base_dir, "outputs")

        shutil.copy(os.path.join(param_dir, "%s_model_spunup.cfg" % (experiment_id)),
                    os.path.join(param_dir, "%s_model_spunup_adj.cfg" % (experiment_id)))

        itag = "%s_model_spunup_adj" % (experiment_id)
        otag = "%s_simulation" % (experiment_id)

        mtag = "%s_met_forcing.csv" % (experiment_id)
        out_fn = "%s_simulation.csv" % (experiment_id)
        out_sd_fn = "%s_simulation_30min.csv" % (experiment_id)
        out_subdaily_fname = os.path.join(run_dir, out_sd_fn)
        out_param_fname = os.path.join(param_dir, otag + ".cfg")
        cfg_fname = os.path.join(param_dir, itag + ".cfg")
        met_fname = os.path.join(met_dir, mtag)
        out_fname = os.path.join(run_dir, out_fn)

        replace_dict = {

                         # files
                         "out_param_fname": "%s" % (out_param_fname),
                         "cfg_fname": "%s" % (cfg_fname),
                         "met_fname": "%s" % (met_fname),
                         "out_fname": "%s" % (out_fname),
                         "out_subdaily_fname": "%s" % (out_subdaily_fname),

                         # control
                         "print_options": "subdaily",
                         "sub_daily": "true",

                        }
        ad.adjust_param_file(cfg_fname, replace_dict)
        os.system(GDAY + cfg_fname)

        #""" Lets not waste time nicely formatting files, can do this later
        # add this directory to python search path so we can find the scripts!
        sys.path.append(os.path.join(base_dir, "scripts"))
        import translate_GDAY_output_to_NCEAS_format as tr
        tr.translate_output(out_fname, met_fname)
        #"""


def get_texture_name(sand, silt, clay):
    """ USDA soil texture calculator
    http://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/?cid=nrcs142p2_054167
    """
    if silt + 1.5 * clay < .15:
        soil_type = "sand"
    elif (silt + 1.5 * clay >= .15) and (silt + 2 * clay < .3):
        soil_type = 'loamy_sand';
    elif ((clay >= 0.07 and clay <= 0.2) and sand > 0.52 and
          (silt + 2 * clay >= 0.3)):
        soil_type = 'sandy_loam';
    elif (clay < 0.07 and silt < 0.5) and (silt + 2 * clay >= 0.3):
        soil_type = 'sandy_loam';
    elif ((clay >= 0.07 and clay <= 0.27) and (silt >= 0.28 and silt < 0.5) and
          sand <= 0.52):
        soil_type = 'loam';
    elif ((silt > 0.5 and (clay > 0.12 and clay < 0.27)) or
          (silt >= 0.5 and silt < 0.8) and clay < 0.12):
        soil_type = 'silty_loam';
    elif silt >= 0.8 and clay < 0.12:
        soil_type = 'silt';
    elif (clay >= 0.2 and clay < 0.35) and (silt < 0.28) and (sand > 0.45):
        soil_type = 'sandy_clay_loam';
    elif (clay >= 0.27 and clay < 0.4) and (sand > 0.2 and sand <= 0.45):
        soil_type = 'clay_loam';
    elif (clay >= 0.27 and clay < 0.4) and sand <= 0.2:
        soil_type = 'silty_clay_loam';
    elif clay >= 0.35 and sand > .45:
        soil_type = 'sandy_clay';
    elif clay >= 0.4 and silt >= 0.4:
        soil_type = 'silty_clay';
    elif clay >= 0.4 and sand <= 0.45 and silt < 0.4:
        soil_type = 'clay'
    else:
        print "SOIL TEXTURE UNDEFINED"
        sys.exit()

    return soil_type


if __name__ == "__main__":

    experiment_id = "CumberlandPlains"
    ncols = 841
    nrows = 681

    latitude = -30.1914
    longitude = 120.654

    cellsize = 0.05
    yurcorner = -9.975
    xllcorner = 111.975
    #latitude = yurcorner - (float(row - 1) * cellsize);
    #longitude = xllcorner + (float(col - 1) * cellsize);
    row = int( (yurcorner - latitude) / cellsize )
    col = int( (longitude - xllcorner) / cellsize )

    soils_base_path = "/Users/%s/Documents/PostDoc/GDAY" % (USER)


    F = ReadFltFile()
    fn = os.path.join(soils_base_path, "soil_surface_data/SurfaceAlbedo_AWAP_grid.flt")
    data = F.load_flt_file(fn)
    albedo = data[row-1, col-1]

    fn = os.path.join(soils_base_path, "Soils/CLY_top_soil_layer_AWAP_5km.bin")
    f = open(fn, "r")
    clay_topsoil = np.fromfile(f, np.float32).reshape(nrows, ncols)[row-1, col-1] / 100.
    f.close()

    fn = os.path.join(soils_base_path, "Soils/SND_top_soil_layer_AWAP_5km.bin")
    f = open(fn, "r")
    sand_topsoil = np.fromfile(f, np.float32).reshape(nrows, ncols)[row-1, col-1] / 100.
    f.close()

    silt_topsoil = max(0.0, 1.0 - sand_topsoil - clay_topsoil)

    fn = os.path.join(soils_base_path, "Soils/CLY_rootzone_soil_layer_AWAP_5km.bin")
    f = open(fn, "r")
    clay_rootzone = np.fromfile(f, np.float32).reshape(nrows, ncols)[row-1, col-1] / 100.
    f.close()

    fn = os.path.join(soils_base_path, "Soils/SND_rootzone_soil_layer_AWAP_5km.bin")
    f = open(fn, "r")
    sand_rootzone = np.fromfile(f, np.float32).reshape(nrows, ncols)[row-1, col-1] / 100.
    f.close()

    silt_rootzone = max(0.0, 1.0 - sand_rootzone - clay_rootzone)
    topsoil_type = get_texture_name(silt_topsoil, sand_topsoil, clay_topsoil)
    rootsoil_type = get_texture_name(silt_rootzone, sand_rootzone, clay_rootzone)
    finesoil = silt_topsoil + clay_topsoil

    main(experiment_id, latitude, longitude, albedo, topsoil_type,
         rootsoil_type, finesoil, SPIN_UP=True, RUN_SIM=True)
