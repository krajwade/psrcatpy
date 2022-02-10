#! /usr/env/python

# A wrapper class to run psrcat and generate the JSON dictionary with pulsar parameters
import numpy as np
import logging
import json
from jinja2 import Template

import psrcatpy.params as params

log = logging.getLogger('json_parser')

class JSONParser:

        def __init__(self, params):
            self._params = params
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
            for i in range(len(self._params)):
                names.append(self._params[i].name)
                periods.append(self._params[i].period)
                dms.append(self._params[i].dm)
                ras.append(self._params[i].ra)
                decs.append(self._params[i].dec)
                s1400s.append(self._params[i].s1400)
                offsets.append(self._params[i].offset)

            json_string = self.template.render(pulsars=zip(names,periods,dms,ras,decs,s1400s,offsets))
            return json_string



