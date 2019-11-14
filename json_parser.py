#! /usr/env/python

# A wrapper class to run psrcat and generate the JSON dictionary with pulsar parameters
import numpy as np
import logging
import params
import json
from jinja2 import Template


log = logging.getLogger('json_parser')

class JSONParser:

        def __init__(self, params):
            self.params = params
            self.template =  Template(''' 
            "Pulsars": {
                           {% for name, period, dm, ra, dec, s1400, offset in pulsars %}
                           {
                             "name": "{{name}}",
                             "period": "{{period}}"
                             "dm": "{{dm}}"
                             "ra": "{{ra}}"
                             "dec": "{{dec}}"
                             "s1400": "{{s1400}}"
                             "offset": "{{offset}}"
                           },
                           {% endfor %}
                       }
                      ''' )

        def generate_json(self):
          
            names = []
            periods = []
            dms = []
            ras = []
            decs = []
            s1400s = []
            offsets = []
            for i in range(len(self.params)):
                names.append(self.params[i].name)
                periods.append(self.params[i].period)
                dms.append(self.params[i].dm)
                ras.append(self.params[i].ra)
                decs.append(self.params[i].dec)
                s1400s.append(self.params[i].s1400)
                offsets.append(self.params[i].offset)

            json_string = self.template.render(pulsars=zip(names,periods,dms,ras,decs,s1400s,offsets))
            return json_string



