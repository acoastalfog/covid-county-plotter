#!/usr/bin/env

import county_plotter as cp

rocklandJHU = cp.countyDataPlotter ("Rockland", "New York", "JHU")
rocklandJHU.plotCasesAndDeathsTwoPanes (7)

rocklandNYT = cp.countyDataPlotter ("Rockland", "New York", "NYT")
rocklandNYT.plotCasesAndDeathsTwoPanes (7)
