# -*- coding: utf-8 -*-
# Copyright 2007-2016 The HyperSpy developers
#
# This file is part of  HyperSpy.
#
#  HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  HyperSpy.  If not, see <http://www.gnu.org/licenses/>.


import os

import numpy as np
from .generate_dm_testing_files import dm3_data_types

import nose.tools as nt
from hyperspy.io import load

my_path = os.path.dirname(__file__)

# When running the loading test the data of the files that passes it are
# stored in the following dict.
# TODO: fixtures should be used instead...
data_dict = {'dm3_1D_data': {},
             'dm3_2D_data': {},
             'dm3_3D_data': {}, }


def test_read_TEM_metadata():
    fname = os.path.join(my_path, "tiff_files", "test_dm_image_um_unit.dm3")
    s = load(fname)
    md = s.metadata
    nt.assert_equal(md.Acquisition_instrument.TEM.acquisition_mode, "TEM")
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.beam_energy, 200.0)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.exposure_time, 0.5)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.magnification, 51.0)
    nt.assert_equal(md.Acquisition_instrument.TEM.microscope, "FEI Tecnai")
    nt.assert_equal(md.General.date, "2015-07-20")
    nt.assert_equal(md.General.original_filename, "test_dm_image_um_unit.dm3")
    nt.assert_equal(md.General.title, "test_dm_image_um_unit")
    nt.assert_equal(md.General.time, "18:48:25")
    nt.assert_equal(md.Signal.quantity, "Intensity")
    nt.assert_equal(md.Signal.signal_type, "")


def test_read_Diffraction_metadata():
    fname = os.path.join(
        my_path,
        "dm3_2D_data",
        "test_diffraction_pattern.dm3")
    s = load(fname)
    md = s.metadata
    nt.assert_equal(md.Acquisition_instrument.TEM.acquisition_mode, "TEM")
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.beam_energy, 200.0)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.exposure_time, 0.2)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.camera_length, 320.0)
    nt.assert_equal(md.Acquisition_instrument.TEM.microscope, "FEI Tecnai")
    nt.assert_equal(md.General.date, "2014-07-09")
    nt.assert_equal(
        md.General.original_filename,
        "test_diffraction_pattern.dm3")
    nt.assert_equal(md.General.title, "test_diffraction_pattern")
    nt.assert_equal(md.General.time, "18:56:37")
    nt.assert_equal(md.Signal.quantity, "Intensity")
    nt.assert_equal(md.Signal.signal_type, "")


def test_read_STEM_metadata():
    fname = os.path.join(my_path, "dm3_2D_data", "test_STEM_image.dm3")
    s = load(fname)
    md = s.metadata
    nt.assert_equal(md.Acquisition_instrument.TEM.acquisition_mode, "STEM")
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.beam_energy, 200.0)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.dwell_time, 3.5E-6)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.camera_length, 135.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.magnification,
        225000.0)
    nt.assert_equal(md.Acquisition_instrument.TEM.microscope, "FEI Titan")
    nt.assert_equal(md.General.date, "2016-08-08")
    nt.assert_equal(md.General.original_filename, "test_STEM_image.dm3")
    nt.assert_equal(md.General.title, "test_STEM_image")
    nt.assert_equal(md.General.time, "16:26:37")
    nt.assert_equal(md.Signal.quantity, "Intensity")
    nt.assert_equal(md.Signal.signal_type, "")


def test_read_EELS_metadata():
    fname = os.path.join(my_path, "dm3_1D_data", "test-EELS_spectrum.dm3")
    s = load(fname)
    md = s.metadata
    nt.assert_equal(md.Acquisition_instrument.TEM.acquisition_mode, "STEM")
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.beam_energy, 200.0)
    nt.assert_equal(md.Acquisition_instrument.TEM.microscope, "FEI Titan")
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.camera_length, 135.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.magnification,
        640000.0)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.tilt_stage, 24.95,
                           places=2)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.convergence_angle, 21.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EELS.collection_angle, 0.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EELS.exposure,
        0.00349999)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EELS.frame_number, 50)
    nt.assert_equal(
        md.Acquisition_instrument.TEM.Detector.EELS.spectrometer,
        'GIF Quantum ER')
    nt.assert_equal(
        md.Acquisition_instrument.TEM.Detector.EELS.aperture_size,
        5.0)
    nt.assert_equal(md.General.date, "2016-08-08")
    nt.assert_equal(md.General.original_filename, "test-EELS_spectrum.dm3")
    nt.assert_equal(md.General.title, "EELS Acquire")
    nt.assert_equal(md.General.time, "19:35:17")
    nt.assert_equal(md.Signal.quantity, "Electrons (Counts)")
    nt.assert_equal(md.Signal.signal_type, "EELS")
    nt.assert_almost_equal(
        md.Signal.Noise_properties.Variance_linear_model.gain_factor,
        0.1285347)
    nt.assert_almost_equal(
        md.Signal.Noise_properties.Variance_linear_model.gain_offset,
        0.0)


def test_read_EDS_metadata():
    fname = os.path.join(my_path, "dm3_1D_data", "test-EDS_spectrum.dm3")
    s = load(fname)
    md = s.metadata
    nt.assert_equal(md.Acquisition_instrument.TEM.acquisition_mode, "STEM")
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EDS.azimuth_angle, 45.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EDS.elevation_angle, 18.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EDS.energy_resolution_MnKa, 130.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EDS.live_time, 3.806)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.Detector.EDS.real_time, 4.233)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.tilt_stage, 24.95,
                           places=2)
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.beam_energy, 200.0)
    nt.assert_equal(md.Acquisition_instrument.TEM.microscope, "FEI Titan")
    nt.assert_almost_equal(md.Acquisition_instrument.TEM.camera_length, 135.0)
    nt.assert_almost_equal(
        md.Acquisition_instrument.TEM.magnification,
        320000.0)
    nt.assert_equal(md.General.date, "2016-08-08")
    nt.assert_equal(md.General.original_filename, "test-EDS_spectrum.dm3")
    nt.assert_equal(md.General.title, "EDS Spectrum")
    nt.assert_equal(md.General.time, "21:46:19")
    nt.assert_equal(md.Signal.quantity, "X-rays (Counts)")
    nt.assert_equal(md.Signal.signal_type, "EDS_TEM")
    nt.assert_almost_equal(
        md.Signal.Noise_properties.Variance_linear_model.gain_factor,
        1.0)
    nt.assert_almost_equal(
        md.Signal.Noise_properties.Variance_linear_model.gain_offset,
        0.0)


def test_loading():
    dims = range(1, 4)
    for dim in dims:
        subfolder = 'dm3_%iD_data' % dim
        for key in dm3_data_types.keys():
            fname = "test-%s.dm3" % key
            filename = os.path.join(my_path, subfolder, fname)
            yield check_load, filename, subfolder, key


def test_dtypes():
    subfolder = 'dm3_1D_data'
    for key, data in data_dict[subfolder].items():
        yield check_dtype, data.dtype, np.dtype(dm3_data_types[key]), key

# TODO: the RGB data generated is not correct


# noinspection PyArgumentList
def test_content():
    for subfolder in data_dict:
        for key, data in data_dict[subfolder].items():
            if subfolder == 'dm3_1D_data':
                dat = np.arange(1, 3)
            elif subfolder == 'dm3_2D_data':
                dat = np.arange(1, 5).reshape(2, 2)
            elif subfolder == 'dm3_3D_data':
                dat = np.arange(1, 9).reshape(2, 2, 2)
            dat = dat.astype(dm3_data_types[key])
            if key in (8, 23):  # RGBA
                dat["A"][:] = 0
            yield check_content, data, dat, subfolder, key


def check_load(filename, subfolder, key):
    print('loading %s\\test-%i' % (subfolder, key))
    s = load(filename)
    # Store the data for the next tests
    data_dict[subfolder][key] = s.data


def check_dtype(d1, d2, i):
    nt.assert_equal(d1, d2, msg='test_dtype-%i' % i)


def check_content(dat1, dat2, subfolder, key):
    np.testing.assert_array_equal(dat1, dat2,
                                  err_msg='content %s type % i: '
                                  '\n%s not equal to \n%s' % (subfolder, key,
                                                              str(dat1),
                                                              str(dat2)))
