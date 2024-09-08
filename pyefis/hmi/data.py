#  Copyright (c) 2018 Phil Birkelbach
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

try:
    from PyQt6.QtGui import *
    from PyQt6.QtCore import *
except:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

import operator
import logging
log = logging.getLogger(__name__)

import pyavtools.fix as fix
from pyefis import hmi

__bindings = []


class DataBinding(object):
    __COMPARE_FUNCTIONS = {"=":operator.eq,
                           "<":operator.lt,
                           "<=":operator.le,
                           ">":operator.gt,
                           ">=":operator.ge}

    def __init__(self, config):
        print(f"DataBinding __init__ ({config})")
        self.key = config['key']
        self.compare = None
        self.args = ""
        self.value = None
        print(f"db.get_item {self.key}")
        self.item = fix.db.get_item(self.key, True, False)
        print(f"db.get_item returned {self.item}")
        self.lastResult = False

        a = config['action']
        if hmi.actions.findAction(a):
            print(f"Action: {a} was found...processing")
            self.action = a
        else:
            log.error("Action Not Found - {}".format(a))
            return None

        if 'args' in config:
            self.args = str(config['args'])
        if self.args == None: self.args = ""
        if self.args.lower() == "<value>":
            self.args = None

        if "condition" in config:
            self.parseCondition(config["condition"])

        # If we are unconditionally sending the value then we need to send
        # an initial one here in case the receiver needs it.
        if self.args == None and self.compare == None:
            hmi.actions.trigger(self.action, str(self.item.value))

        print(f"Attempting to connect to {self.item.dtype}")

        self.item.valueChanged[self.item.dtype].connect(self.changeFunctionFactory())

        print(f"Finished updating initialization for {self.key}")


    def changeFunctionFactory(self):
        if self.compare:
            cfunc = self.__COMPARE_FUNCTIONS[self.compare]

        def actionTrigger(value):
            if self.args == None:
                hmi.actions.trigger(self.action, str(value))
            else:
                hmi.actions.trigger(self.action, self.args)

        def compareFunction(value):
            if cfunc(value, self.value):
                if self.lastResult: return
                actionTrigger(value)
                self.lastResult = True
            else:
                self.lastResult = False

        if self.compare == None:
            return actionTrigger
        else:
            return compareFunction


    def parseCondition(self, condition):
        if type(condition) in [bool, int, float]:
            self.value = condition
            self.compare = "="
        else:
            s = condition.replace(" ","")
            op = ""
            val = ""
            for x,c in enumerate(s):
                if c in "=><":
                    op += c
                else:
                    val = s[x-1:]
            if op not in ["<", ">", "<=", ">=", "="]:
                log.error("Unknown Condition Operator {}".format(op))
                return None
            self.value = self.item.dtype(val)
            self.compare = op


    def __str__(self):
        if self.compare:
            s = "Data Binding: {}{}{} - {}({})".format(self.key, self.compare, self.value, self.action, self.args)
        else:
            s = "Data Binding: {} - {}({})".format(self.key, self.action, self.args)
        return(s)


def initialize(config):
    if config == None: return
    for x in config:
        try:
            print(f"initialize hmi: {x}") # BUGBUG DEBUG BTW
            d = DataBinding(x)
        except:
            log.error("Unable to load Data Binding {}".format(x))
            raise
