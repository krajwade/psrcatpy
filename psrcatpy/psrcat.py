#! /usr/env/python

# A class that runs psrcat and returns the source within a box

import numpy as np
import subprocess as sp
from astropy.coordinates import SkyCoord
from astropy import units as u
import logging
import sys

import psrcatpy.params as params
import psrcatpy.json_parser as json_parser

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

class PsrCat():
    """ A class to run the psrcat query and return known sources within the bounding box
        Parameters:
        params_list: A list of parameters to be saved for the known source. Needs to be in psrcat format (str). Should start and end with '
        ra: RA of the beam boresite (str)
        dec: DEC of the beam boresite (str)
        smaj: semi-major axis in degrees
        smin: semi-minor axis in degress
        position_angle = position_angle of the beam  (This will change with Alt-AZ)
    """

    def __init__(self, param_list, ra, dec, smaj, smin, position_angle):
        try:
            self.Cmd = None
            self.ra_str = ra
            self.dec_str = dec
            self.sma = smaj  
            self.smi = smin 
            self.pos_ang = position_angle * u.deg
            self.param_flag = "-c"
            self.condition_flag = "-l"
            self.params = []
            self.param_list = param_list
            self.offset=None
            self.boresite = SkyCoord(self.ra_str, self.dec_str, frame='fk5', unit=("hourangle,deg"))
        except ValueError as error:
            logging.error("Error in parsing arguments")
            logggin.error(error)


    def generate_box(self):
        """
        Generate a bounding box for the ellipse of the beam.
        Returns min and max RA and DEC of the bounding box
        
        """
        angle = np.arctan(self.smi/self.sma) * 180.0/np.pi * u.deg
        corners_ra= []
        corners_dec = []
        corners_ra.append(self.boresite.directional_offset_by(self.pos_ang + angle, (np.sqrt(pow(self.sma,2) + pow(self.smi,2) )) * u.deg).ra.deg)
        corners_ra.append(self.boresite.directional_offset_by((180.0*u.deg) - angle, (np.sqrt(pow(self.sma,2) + pow(self.smi,2) ))* u.deg).ra.deg)
        corners_ra.append(self.boresite.directional_offset_by((180.0*u.deg) + 2.0 * angle, (np.sqrt(pow(self.sma,2) + pow(self.smi,2)))*u.deg).ra.deg) 
        corners_ra.append(self.boresite.directional_offset_by(angle - (180.0 * u.deg), (np.sqrt(pow(self.sma,2) + pow(self.smi,2))) * u.deg).ra.deg)  

        corners_dec.append(self.boresite.directional_offset_by(self.pos_ang + angle, (np.sqrt(pow(self.sma,2) + pow(self.smi,2))) * u.deg).dec.deg)
        corners_dec.append(self.boresite.directional_offset_by((180.0*u.deg) - angle, (np.sqrt(pow(self.sma,2) + pow(self.smi,2))) * u.deg).dec.deg)
        corners_dec.append(self.boresite.directional_offset_by((180.0*u.deg) + 2.0 * angle, (np.sqrt(pow(self.sma,2) + pow(self.smi,2))) * u.deg).dec.deg) 
        corners_dec.append(self.boresite.directional_offset_by(angle - (180.0 * u.deg), (np.sqrt(pow(self.sma,2) + pow(self.smi,2))) * u.deg).dec.deg)  
        
        return max(corners_ra), min(corners_ra), max(corners_dec), min(corners_dec)   
        


    def run_query(self):
        """
        Runs PSRCAT query to look for pulsars within the bounding box
        of the beam ellipse.
        Returns a JSON dictionary of all pulsars with the relevant parameters

        """
        corner_ra_max, corner_ra_min, corner_dec_max, corner_dec_min = self.generate_box()
        binaryCommand = "psrcat"
        condition= "'raj < " + str(corner_ra_max) + " && raj > " + str(corner_ra_min) + " && decj < " + str(corner_dec_max) + " && decj > " + str(corner_dec_min) + "'"
        Cmd = " ".join((binaryCommand, self.param_flag,"'", self.param_list,"'", self.condition_flag,condition, " |grep -v '*'"))
        logging.info("Running command...")
        logging.info(Cmd)

        try:
            Buf = sp.check_output(Cmd, shell=True, universal_newlines=True)
            Cols = Buf.split("\n")
            if (len(Cols) > 6):
               ind = 4
               while(ind < len(Cols) - 2):
                 if (len(list(filter(bool, Cols[ind].split(" ")))) !=0):
                       psr_coord = SkyCoord(list(filter(bool, Cols[ind].split(" ")))[9], list(filter(bool,Cols[ind].split(" ")))[12], frame='fk5', unit=("hourangle,deg"))
                       self.offset = psr_coord.separation(self.boresite).deg
                       self.params.append(params.Params(list(filter(bool,Cols[ind].split(" ")))[1], list(filter(bool,Cols[ind].split(" ")))[3], list(filter(bool,Cols[ind].split(" ")))[6], list(filter(bool, Cols[ind].split(" ")))[9], list(filter(bool, Cols[ind].split(" ")))[12], list(filter(bool, Cols[ind].split(" ")))[15], self.offset))
                       ind += 1
                 else:
                       ind += 1
            parser = json_parser.JSONParser(self.params)
            return parser.generate_json()

        except sp.CalledProcessError as e:
            logging.error("Error in running psrcat")
            logging.error(e.output)
            sys.exit()



