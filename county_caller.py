#!/usr/bin/env

import county_plotter as cp

rockland = cp.countyDataPlotter ("Rockland", "New York", "JHU")
rockland.plotCasesAndDeathsTwoPanes (7)
