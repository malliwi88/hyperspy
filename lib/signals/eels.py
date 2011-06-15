#import Signal
#
#
#class EELSSignal(Signal):
#    def extract_zero_loss(self, zl = None,right = 0.2,around = 0.05):
#        """
#        Zero loss extraction by the reflected-tail or fingerprinting methods.
#        
#        Creates a new spectrum instance self.zero_loss with the zero loss 
#        extracted by the reflected-tail method if no zero loss in the vacuum is 
#        provided. Otherwise it use the zero loss fingerprinting method.
#
#        Parameters
#        ----------
#        zl : str
#            name of the zero loss in vacuum file for the fingerprinting method
#        right : float
#            maximum channel in energy units to use to fit the zero loss in the 
#            vacuum. Only has effect for the fingerprinting method.
#        around : float
#            interval around the origin to remove from the fit for the of the 
#            zero loss in the vacuum. Only has effect for the fingerprinting 
#            method.
#        
#        Notes
#        -----
#        It is convenient to align the SI and correct the baseline before using
#        this method.
#        """
#
#        print "Extracting the zero loss"
#        if zl is None: # reflected-tail
#            # Zero loss maximum
#            i0 = self.data_cube[:,0,0].argmax(0)
#            # FWQM from the first spectrum in channels
#            # Search only 2eV around the max to avoid counting the plasmons
#            # in thick samples
#            i_range = int(round(2. / self.energyscale))
#            fwqm_bool = self.data_cube[i0-i_range:i0+i_range,0,0] > \
#            0.25 * self.data_cube[i0,0,0]
#            ch_fwqm = len(fwqm_bool[fwqm_bool])
#            self.zero_loss = copy.deepcopy(self)
#            data = self.zero_loss.data_cube
#            canvas = np.zeros(data.shape)
#            # Reflect the tail
#            width = int(round(1.5 * ch_fwqm))
#            canvas[i0 + width : 2 * i0 + 1,:,:] = \
#            data[i0 - width::-1,:,:]
#            # Remove the "background" = mean of first 4 channels and reflects the
#            # tail
#            bkg = np.mean(data[0:4])
#            canvas -= bkg
#            # Scale the extended tail with the ratio obtained from
#            # 2 overlapping channels
#            ch = i0 + width
#            ratio = np.mean(data[ch: ch + 2] / canvas[ch: ch + 2], 0)
#            for ix in range(data.shape[1]):
#                for iy in range(data.shape[2]):
#                    canvas[:,ix,iy] *= ratio[ix,iy]
#            # Copy the extension
#            data[i0 + width:] = canvas[i0 + width:]
#        else:
#            import components
#            fp = components.ZL_Fingerprinting(zl)
#            m = Model(self,False)
#            m.append(fp)
#            m.set_energy_region(None,right)
#            m.remove_data_range(-around,around)
#            m.multifit()
#            self.zero_loss = copy.deepcopy(self)
#            self.zero_loss.data_cube = m.model_cube
#            self.zl_substracted = copy.deepcopy(self)
#            self.zl_substracted.data_cube -= self.zero_loss.data_cube
#        self._replot()
#        
#    def _process_gain_correction(self):
#        gain = self.gain_correction
#        # Check if the spectrum has the same number of channels:
#        if self.data_cube.shape[0] != gain.data_cube.shape[0]:
#            print 
#            messages.warning_exit(
#            "The gain and spectrum don't have the same number of channels")
#        dc = gain.data_cube.copy()
#        dc = dc.sum(1).mean(1)
#        dc /= dc.mean()
#        gain.normalized_gain = dc
#
#    def _process_readout(self):
#        """Readout conditioning
#        
#        Checks if the readout file provided contains more than one spectrum.
#        If that is the case, it makes the average and produce a single spectrum
#        Spectrum object to feed the correct spectrum function"""
#        channels = self.readout.data_cube.shape[0]
#        if self.readout.data_cube.shape[1:]  > (1, 1):
#            self.readout.data_cube = np.average(
#            np.average(self.readout.data_cube,1),1).reshape(channels, 1, 1)
#            self.readout.get_dimensions_from_cube()
#            self.readout.set_new_calibration(0,1)
#            if self.readout.dark_current:
#                self.readout._process_dark_current()
#                self.readout.dark_current_correction()
#
#    def _process_dark_current(self):
#        """Dark current conditioning.
#        
#        Checks if the readout file provided contains more than one spectrum.
#        If that is the case, it makes the average and produce a single spectrum
#        Spectrum object to feed the correct spectrum function. If 
#        a readout correction is provided, it corrects the readout in the dark
#        current spim."""
#        if self.dark_current.data_cube.shape[1:]  > (1, 1):
#            self.dark_current.data_cube = np.average(
#            np.average(self.dark_current.data_cube,1),1).reshape((-1, 1, 1))
#            self.dark_current.get_dimensions_from_cube()
#            self.dark_current.set_new_calibration(0,1)
#            
#    # Elements _________________________________________________________________
#    def add_elements(self, elements, include_pre_edges = False):
#        """Declare the elements present in the SI.
#        
#        Instances of components.edge.Edge for the current energy range will be 
#        created automatically and add to self.subshell.
#        
#        Parameters
#        ----------
#        elements : tuple of strings
#            The strings must represent a chemical element.
#        include_pre_edges : bool
#            If True, the ionization edges with an onset below the lower energy 
#            limit of the SI will be incluided
#        """
#        for element in elements:
#            self.elements.add(element)
#        self.generate_subshells(include_pre_edges)
#        
#    def generate_subshells(self, include_pre_edges = False):
#        """Calculate the subshells for the current energy range for the elements
#         present in self.elements
#         
#        Parameters
#        ----------
#        include_pre_edges : bool
#            If True, the ionization edges with an onset below the lower energy 
#            limit of the SI will be incluided
#        """
#        if not include_pre_edges:
#            start_energy = self.energy_axis[0]
#        else:
#            start_energy = 0.
#        end_energy = self.energy_axis[-1]
#        for element in self.elements:
#            e_shells = list()
#            for shell in edges_dict[element]['subshells']:
#                if shell[-1] != 'a':
#                    if start_energy <= \
#                    edges_dict[element]['subshells'][shell]['onset_energy'] \
#                    <= end_energy :
#                        subshell = '%s_%s' % (element, shell)
#                        if subshell not in self.subshells:
#                            print "Adding %s subshell" % (subshell)
#                            self.subshells.add('%s_%s' % (element, shell))
#                            e_shells.append(subshell)
#            if len(e_shells) > 0: 
#                self.generate_edges(e_shells)
#    
#    def generate_edges(self, e_shells, copy2interactive_ns = True):
#        """Create the Edge instances and configure them appropiately
#        Parameters
#        ----------
#        e_shells : list of strings
#        copy2interactive_ns : bool
#            If True, variables with the format Element_Shell will be created in
#            IPython's interactive shell
#        """
#        e_shells.sort()
#        master_edge = Edge(e_shells.pop())
#        self.edges.append(master_edge)
#        interactive_ns[self.edges[-1].__repr__()] = self.edges[-1]
#        element = self.edges[-1].__repr__().split('_')[0]
#        interactive_ns[element] = []
#        interactive_ns[element].append(self.edges[-1])
#        while len(e_shells) > 0:
#            self.edges.append(Edge(e_shells.pop()))
#            self.edges[-1].intensity.twin = master_edge.intensity
#            self.edges[-1].delta.twin = master_edge.delta
#            self.edges[-1].freedelta = False
#            interactive_ns[self.edges[-1].__repr__()] = self.edges[-1]
#            interactive_ns[element].append(self.edges[-1])
#            
#    def remove_background(self, start_energy = None, mask = None):
#        """Removes the power law background of the EELS SI if the present 
#        elements were defined.
#        
#        It stores the background in self.background.
#        
#        Parameters
#        ----------
#        start_energy : float
#            The starting energy for the fitting routine
#        mask : boolean numpy array
#        """
#        from spectrum import Spectrum
#        if mask is None:
#            mask = np.ones(self.data_cube.shape[1:], dtype = 'bool')
#        m = Model(self)
#        m.fit_background(startenergy = start_energy, type = 'multi', 
#        mask = mask)
#        m.model_cube[:, mask == False] *= 0
#        self.background = Spectrum()
#        self.background.data_cube = m.model_cube
#        self.background.get_dimensions_from_cube()
#        utils.copy_energy_calibration(self, self.background)
##        self.background.get_calibration_from()
#        print "Background stored in self.background"
#        self.__new_cube(self.data_cube[:] - m.model_cube[:], 
#        'background removal')
#        self._replot()
#        
#    def calculate_I0(self, threshold = None):
#        """Estimates the integral of the ZLP from a LL SI
#        
#        The value is stored in self.I0 as an Image.
#        
#        Parameters
#        ----------
#        thresh : float or None
#            If float, it estimates the intensity of the ZLP as the sum 
#            of all the counts of the SI until the threshold. If None, it 
#            calculates the sum of the ZLP previously stored in 
#            self.zero_loss
#        """
#        if threshold is None:
#            if self.zero_loss is None:
#                messages.warning_exit(
#                "Please, provide a threshold value of define the " 
#                "self.zero_loss attribute by, for example, using the "
#                "extract_zero_loss method")
#            else:
#                self.I0 = Image(dc = self.zero_loss.sum(0))
#        else:
#            threshold = self.energy2index(threshold)
#            self.I0 = Image(dc = self.data_cube[:threshold,:,:].sum(0)) 
#        
#    def correct_gain(self):
#        """Apply the gain correction stored in self.gain_correction
#        """
#        if not self.treatments.gain:
#            self._process_gain_correction()
#            gain = self.gain_correction
#            print "Applying gain correction"
#            # Gain correction
#            data = np.zeros(self.data_cube.shape)
#            for ix in range(0, self.xdimension):
#                for iy in range(0, self.ydimension):
#                    np.divide(self.data_cube[:,ix,iy], 
#                    gain.normalized_gain, 
#                    data[:,ix,iy])
#            self.__new_cube(data, 'gain correction')
#            self.treatments.gain = 1
#            self._replot()
#        else:
#            print "Nothing done, the SI was already gain corrected"
#
#    def correct_baseline(self, kind = 'pixel', positive2zero = True, 
#    averaged = 10, fix_negative = True):
#        """Set the minimum value to zero
#        
#        It can calculate the correction globally or pixel by pixel.
#        
#        Parameters
#        ----------
#        kind : {'pixel', 'global'}
#            if 'pixel' it calculates the correction pixel by pixel.
#            If 'global' the correction is calculated globally.
#        positive2zero : bool
#            If False it will only set the baseline to zero if the 
#            minimum is negative
#        averaged : int
#            If > 0, it will only find the minimum in the first and last 
#            given channels
#        fix_negative : bool
#            When averaged, it will take the abs of the data_cube to assure
#            that no value is negative.
#        
#        """
#        data = copy.copy(self.data_cube)
#        print "Correcting the baseline of the low loss spectrum/a"
#        if kind == 'global':
#            if averaged == 0:
#                minimum = data.min()
#            else:
#                minimum = np.vstack(
#                (data[:averaged,:,:], data[-averaged:,:,:])).min()
#            if minimum < 0. or positive2zero is True:
#                data -= minimum
#        elif kind == 'pixel':
#            if averaged == 0:
#                minimum = data.min(0).reshape(
#            (1,data.shape[1], data.shape[2]))
#            else:
#                minimum = np.vstack((data[:averaged,:,:], data[-averaged:,:,:])
#                ).min(0).reshape((1,data.shape[1], data.shape[2]))
#            mask = np.ones(data.shape[1:], dtype = 'bool')
#            if positive2zero is False:
#                mask[minimum.squeeze() > 0] = False
#            data[:,mask] -= minimum[0,mask]
#        else:
#            messages.warning_exit(
#            "Wrong kind keyword. Possible values are pixel or global")
#        
#        if fix_negative:
#            data = np.abs(data)
#        self.__new_cube(data, 'baseline correction')
#        self._replot()
#
#    def readout_correction(self):
#        if not self.treatments.readout:
#            if hasattr(self, 'readout'):
#                data = copy.copy(self.data_cube)
#                print "Correcting the readout"
#                for ix in range(0,self.xdimension):
#                    for iy in range(0,self.ydimension):
#                        data[:, ix, iy] -= self.readout.data_cube[:,0,0]
#                self.__new_cube(data, 'readout correction')
#                self.treatments.readout = 1
#                self._replot()
#            else:
#                print "To correct the readout, please define the readout attribute"
#        else:
#            print "Nothing done, the SI was already readout corrected"
#
#    def dark_current_correction(self):
#        """Apply the dark_current_correction stored in self.dark_current"""
#        if self.treatments.dark_current:
#            print "Nothing done, the dark current was already corrected"
#        else:
#            ap = self.acquisition_parameters
#            if hasattr(self, 'dark_current'):
#                if (ap.exposure is not None) and \
#                (self.dark_current.acquisition_parameters.exposure):
#                    if (ap.readout_frequency is not None) and \
#                    (ap.blanking is not None):
#                        if not self.acquisition_parameters.blanking:
#                            exposure = ap.exposure + self.data_cube.shape[0] * \
#                            ap.ccd_height / (ap.binning * ap.readout_frequency)
#                            ap.effective_exposure = exposure
#                        else:
#                            exposure = ap.exposure
#                    else:
#                        print \
#    """Warning: no information about binning and readout frequency found. Please 
#    define the following attributes for a correct dark current correction:
#    exposure, binning, readout_frequency, ccd_height, blanking
#    The correction proceeds anyway
#    """
#                            
#                        exposure = self.acquisition_parameters.exposure
#                    data = copy.copy(self.data_cube)
#                    print "Correcting the dark current"
#                    self.dark_current.data_cube[:,0,0] *= \
#                    (exposure / self.dark_current.acquisition_parameters.exposure)
#                    data -= self.dark_current.data_cube
#                    self.__new_cube(data, 'dark current correction')
#                    self.treatments.dark_current = 1
#                    self._replot()
#                else:
#                    
#                    messages.warning_exit(
#                    "Please define the exposure attribute of the spectrum"
#                    "and its dark_current")
#            else:
#                messages.warning_exit(
#               "To correct the readout, please define the dark_current " \
#                "attribute")
#                
#    def find_low_loss_origin(self, sync_SI = None):
#        """Calculate the position of the zero loss origin as the average of the 
#        postion of the maximum of all the spectra"""
#        old_origin = self.energyorigin
#        imax = np.mean(np.argmax(self.data_cube,0))
#        self.energyorigin = generate_axis(0, self.energyscale, 
#            self.energydimension, imax)[0]
#        self.updateenergy_axis()
#        if sync_SI:
#            sync_SI.energyorigin += self.energyorigin - old_origin
#            sync_SI.updateenergy_axis()
#
#    def fourier_log_deconvolution(self):
#        """Performs fourier-log deconvolution of the full SI.
#        
#        The zero-loss can be specified by defining the parameter 
#        self.zero_loss that must be an instance of Spectrum. Otherwise the 
#        zero loss will be extracted by the reflected tail method
#        """
#        if self.zero_loss is None:
#            self.extract_zero_loss()
#        z = np.fft.fft(self.zero_loss.data_cube, axis=0)
#        j = np.fft.fft(self.data_cube, axis=0)
#        j1 = z*np.log(j/z)
#        self.__new_cube(np.fft.ifft(j1, axis = 0).real, 
#        'fourier-log deconvolution')
#        self._replot()
#        
#    def calculate_thickness(self, method = 'threshold', threshold = 3, 
#    factor = 1):
#        """Calculates the thickness from a LL SI.
#        
#        The resulting thickness map is stored in self.thickness as an image 
#        instance. To visualize it: self.thickness.plot()
#        
#        Parameters
#        ----------
#        method : {'threshold', 'zl'}
#            If 'threshold', it will extract the zero loss by just splittin the 
#            spectrum at the threshold value. If 'zl', it will use the 
#            self.zero_loss SI (if defined) to perform the calculation.
#        threshold : float
#            threshold value.
#        factor : float
#            factor by which to multiple the ZLP
#        """
#        print "Calculating the thickness"
#        # Create the thickness array
#        dc = self.data_cube
#        integral = dc.sum(0)
#        if method == 'zl':
#            if self.zero_loss is None:
#                self.extract_zero_loss()
#            zl = self.zero_loss.data_cube
#            zl_int = zl.sum(0)
#            
#        elif method == 'threshold':
#            ti =self.energy2index(threshold)
#            zl_int = dc[:ti,...].sum(0) * factor 
#        self.thickness = \
#        Image({'calibration' : {'data_cube' : np.log( integral / zl_int)}})
#                
#    def calculate_FWHM(self, factor = 0.5, channels = 7, der_roots = False):
#        """Use a third order spline interpolation to estimate the FWHM of 
#        the zero loss peak.
#        
#        Parameters:
#        -----------
#        factor : float < 1
#            By default is 0.5 to give FWHM. Choose any other float to give
#            find the position of a different fraction of the peak.
#        channels : int
#            radius of the interval around the origin were the algorithm will 
#            perform the estimation.
#        der_roots: bool
#            If True, compute the roots of the first derivative
#            (2 times slower).  
#        
#        Returns:
#        --------
#        dictionary. Keys:
#            'FWHM' : float
#                 width, at half maximum or other fraction as choosen by
#            `factor`. 
#            'FWHM_E' : tuple of floats
#                Coordinates in energy units of the FWHM points.
#            'der_roots' : tuple
#                Position in energy units of the roots of the first
#            derivative if der_roots is True (False by default)
#        """
#        ix = self.coordinates.ix
#        iy = self.coordinates.iy
#        i0 = np.argmax(self.data_cube[:,ix, iy])
#        data = self.data_cube[i0 - channels:i0 + channels + 1, ix, iy]
#        x = self.energy_axis[i0 - channels:i0 + channels + 1]
#        height = np.max(data)
#        spline_fwhm = UnivariateSpline(x, data - factor * height)
#        pair_fwhm = spline_fwhm.roots()[0:2]
#        print spline_fwhm.roots()
#        fwhm = pair_fwhm[1] - pair_fwhm[0]
#        if der_roots:
#            der_x = np.arange(x[0], x[-1] + 1, (x[1] - x[0]) * 0.2)
#            derivative = spline_fwhm(der_x, 1)
#            spline_der = UnivariateSpline(der_x, derivative)
#            return {'FWHM' : fwhm, 'pair' : pair_fwhm, 
#            'der_roots': spline_der.roots()}
#        else:
#            return {'FWHM' : fwhm, 'FWHM_E' : pair_fwhm}
#            
#    def power_law_extension(self, interval, new_size = 1024, 
#                            to_the = 'right'):
#        """Extend the SI with a power law.
#        
#        Fit the SI with a power law in the given interval and use the result 
#        to extend it to the left of to the right.
#        
#        Parameters
#        ----------
#        interval : tuple
#            Interval to perform the fit in energy units        
#        new_size : int
#            number of channel after the extension.
#        to_the : {'right', 'left'}
#            extend the SI to the left or to the right
#        """
#        left, right = interval
#        s = self.data_cube.shape
#        original_size = s[0]
#        if original_size >= new_size:
#            print "The new size (in channels) must be bigger than %s" % \
#            original_size
#        new_cube = np.zeros((new_size, s[1], s[2]))
#        iright = self.energy2index(right)
#        new_cube[:iright,:,:] = self.data_cube[:iright,:,:]
#        self.data_cube = new_cube
#        self.get_dimensions_from_cube()
#        m = Model(self, False, auto_add_edges = False)
#        pl = PowerLaw()
#        m.append(pl)
#        m.set_energy_region(left,right)
#        m.multifit(grad = True)
#        self.data_cube[iright:,:,:] = m.model_cube[iright:,:,:]
#        
#    def hanning_taper(self, side = 'left', channels = 20,offset = 0):
#        """Hanning taper
#        
#        Parameters
#        ----------
#        side : {'left', 'right'}
#        channels : int
#        offset : int
#        """        
#        dc = self.data_cube
#        if side == 'left':
#            dc[offset:channels+offset,:,:] *= \
#            (np.hanning(2*channels)[:channels]).reshape((-1,1,1))
#            dc[:offset,:,:] *= 0. 
#        if side == 'right':
#            dc[-channels-offset:-offset,:,:] *= \
#            (np.hanning(2*channels)[-channels:]).reshape((-1,1,1))
#            dc[-offset:,:,:] *= 0. 
#        
#    def remove_spikes(self, threshold = 2200, subst_width = 5, 
#                      coordinates = None):
#        """Remove the spikes in the SI.
#        
#        Detect the spikes above a given threshold and fix them by interpolating 
#        in the give interval. If coordinates is given, it will only remove the 
#        spikes for the specified spectra.
#        
#        Paramerters:
#        ------------
#        threshold : float
#            A suitable threshold can be determined with 
#            Spectrum.spikes_diagnosis
#        subst_width : tuple of int or int
#            radius of the interval around the spike to substitute with the 
#            interpolation. If a tuple, the dimension must be equal to the 
#            number of spikes in the threshold. If int the same value will be 
#            applied to all the spikes.
#        
#        See also
#        --------
#        Spectrum.spikes_diagnosis, Spectrum.plot_spikes
#        """
#        int_window = 20
#        dc = self.data_cube
#        der = np.diff(dc,1,0)
#        E_ax = self.energy_axis
#        n_ch = len(E_ax)
#        index = 0
#        if coordinates is None:
#            for i in range(dc.shape[1]):
#                for j in range(dc.shape[2]):
#                    if der[:,i,j].max() >= threshold:
#                        print "Spike detected in (%s, %s)" % (i, j)
#                        argmax = der[:,i,j].argmax()
#                        if hasattr(subst_width, '__iter__'):
#                            subst__width = subst_width[index]
#                        else:
#                            subst__width = subst_width
#                        lp1 = np.clip(argmax - int_window, 0, n_ch)
#                        lp2 = np.clip(argmax - subst__width, 0, n_ch)
#                        rp2 = np.clip(argmax + int_window, 0, n_ch)
#                        rp1 = np.clip(argmax + subst__width, 0, n_ch)
#                        x = np.hstack((E_ax[lp1:lp2], E_ax[rp1:rp2]))
#                        y = np.hstack((dc[lp1:lp2,i,j], dc[rp1:rp2,i,j])) 
#                        # The weights were commented because the can produce nans
#                        # Maybe it should be an option?
#                        intp =UnivariateSpline(x,y) #,w = 1/np.sqrt(y))
#                        x_int = E_ax[lp2:rp1+1]
#                        dc[lp2:rp1+1,i,j] = intp(x_int)
#                        index += 1
#        else:
#            for spike_spectrum in coordinates:
#                i, j = spike_spectrum
#                print "Spike detected in (%s, %s)" % (i, j)
#                argmax = der[:,i,j].argmax()
#                if hasattr(subst_width, '__iter__'):
#                    subst__width = subst_width[index]
#                else:
#                    subst__width = subst_width
#                lp1 = np.clip(argmax - int_window, 0, n_ch)
#                lp2 = np.clip(argmax - subst__width, 0, n_ch)
#                rp2 = np.clip(argmax + int_window, 0, n_ch)
#                rp1 = np.clip(argmax + subst__width, 0, n_ch)
#                x = np.hstack((E_ax[lp1:lp2], E_ax[rp1:rp2]))
#                y = np.hstack((dc[lp1:lp2,i,j], dc[rp1:rp2,i,j])) 
#                # The weights were commented because the can produce nans
#                # Maybe it should be an option?
#                intp =UnivariateSpline(x,y) # ,w = 1/np.sqrt(y))
#                x_int = E_ax[lp2:rp1+1]
#                dc[lp2:rp1+1,i,j] = intp(x_int)
#                index += 1
#                
#    def spikes_diagnosis(self):
#        """Plots a histogram to help in choosing the threshold for spikes
#        removal.
#        See also
#        --------
#        Spectrum.remove_spikes, Spectrum.plot_spikes
#        """
#        dc = self.data_cube
#        der = np.diff(dc,1,0)
#        plt.figure()
#        plt.hist(np.ravel(der.max(0)),100)
#        plt.xlabel('Threshold')
#        plt.ylabel('Counts')
#        plt.draw()
#        
#    def plot_spikes(self, threshold = 2200):
#        """Plot the spikes in the given threshold
#        
#        Parameters
#        ----------
#        threshold : float
#        
#        Returns
#        -------
#        list of spikes coordinates
#        
#        See also
#        --------
#        Spectrum.remove_spikes, Spectrum.spikes_diagnosis
#        """
#        dc = self.data_cube
#        der = np.diff(dc,1,0)
#        index = 0
#        spikes =[]
#        for i in range(dc.shape[1]):
#            for j in range(dc.shape[2]):
#                if der[:,i,j].max() >= threshold:
#                    print "Spike detected in (%s, %s)" % (i, j)
#                    spikes.append((i,j))
#                    argmax = der[:,i,j].argmax()
#                    toplot = dc[np.clip(argmax-100,0,dc.shape[0]-1): 
#                    np.clip(argmax+100,0,dc.shape[0]-1), i, j]
#                    plt.figure()
#                    plt.step(range(len(toplot)), toplot)
#                    plt.title(str(index))
#                    index += 1
#        return spikes
#                        
#    def build_SI_from_substracted_zl(self,ch, taper_nch = 20):
#        """Modify the SI to have fit with a smoothly decaying ZL
#        
#        Parameters
#        ----------
#        ch : int
#            channel index to start the ZL decay to 0
#        taper_nch : int
#            number of channels in which the ZL will decay to 0 from `ch`
#        """
#        sp = copy.deepcopy(self)
#        dc = self.zl_substracted.data_cube.copy()
#        dc[0:ch,:,:] *= 0
#        for i in range(dc.shape[1]):
#            for j in range(dc.shape[2]):
#                dc[ch:ch+taper_nch,i,j] *= np.hanning(2 * taper_nch)[:taper_nch]
#        sp.zl_substracted.data_cube = dc.copy()
#        dc += self.zero_loss.data_cube
#        sp.data_cube = dc.copy()
#        return sp
#        
#    def jump_ratio(self, left_interval, right_interval):
#        """Returns the jump ratio in the given intervals
#        
#        Parameters
#        ----------
#        left_interval : tuple of floats
#            left interval in energy units
#        right_interval : tuple of floats
#            right interval in energy units
#            
#        Returns
#        -------
#        float
#        """
#        ilt1 = self.energy2index(left_interval[0])
#        ilt2 = self.energy2index(left_interval[1])
#        irt1 = self.energy2index(right_interval[0])
#        irt2 = self.energy2index(right_interval[1])
#        jump_ratio = (self.data_cube[irt1:irt2,:,:].sum(0) \
#        / self.data_cube[ilt1:ilt2,:,:].sum(0))
#        return jump_ratio
#        
#    def correct_dual_camera_step(self, show_lev = False, mean_interval = 3, 
#                                 pca_interval = 20, pcs = 2, 
#                                 normalize_poissonian_noise = False):
#        """Correct the gain difference in a dual camera using PCA.
#        
#        Parameters
#        ----------
#        show_lev : boolen
#            Plot PCA lev
#        mean_interval : int
#        pca_interval : int
#        pcs : int
#            number of principal components
#        normalize_poissonian_noise : bool
#        """ 
#        # The step is between pixels 1023 and 1024
#        pw = pca_interval
#        mw = mean_interval
#        s = copy.deepcopy(self)
#        s.energy_crop(1023-pw, 1023 + pw)
#        s.principal_components_analysis(normalize_poissonian_noise)
#        if show_lev:
#            s.plot_lev()
#            pcs = int(raw_input('Number of principal components? '))
#        sc = s.pca_build_SI(pcs)
#        step = sc.data_cube[(pw-mw):(pw+1),:,:].mean(0) - \
#        sc.data_cube[(pw+1):(pw+1+mw),:,:].mean(0)
#        self.data_cube[1024:,:,:] += step.reshape((1, step.shape[0], 
#        step.shape[1]))
#        self._replot()
#        return step