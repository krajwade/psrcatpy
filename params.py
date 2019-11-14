#!/usr/env/python

import numpy as np
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

class Params():

    def __init__(self,name, period, dm, ra, dec, s1400, offset):
        """
        Params: Class encompassing the known pulsar parameters

        parameters:
            name: J-name of the pulsar (str)
            period: Period in seconds (float)
            dm: DM of the pulsar (float)
            ra: RA string in hh:mm:ss.ss (str)
            dec: DEC string in dd:mm:ss.ss (str)
            s1400: 1.4 GHz flux density (float)
            offset: Offset from boresite of the beam in deg (float)

        """
        try:
            logging.info("Parsing pulsar parameters....")
            self.name = name
            self.period = float(period)   # period in seconds
            self.dm = float(dm)
            self.ra = ra # RA in degrees
            self.dec = dec# DEC in degrees
            self.s1400 = float(s1400) # flux in Jy
            self.offset = float(offset) # offset in degrees

        except ValueError as error:
            logging.error("Error on parsing arguments")
            logging.error(error.output)

    def name(self):
      return self.name

    def period(self):
        return self.period

    def dm(self):
      return self.dm

    def ra(self):
      return self.ra

    def dec(self):
      return self.dec

    def s1400(self):
      return self.s1400

    def offset(self):
      return self.offset
