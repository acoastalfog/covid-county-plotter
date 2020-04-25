#!/usr/bin/env

import county_plotter as cp

rockland = cp.countyDataPlotter ("Rockland", "New York", "JHU")
rockland.plotCasesAndDeathsTwoPanes (7)

nyc = cp.countyDataPlotter ("New York", "New York", "JHU")
nyc.plotCasesAndDeathsTwoPanes (7)

henrico = cp.countyDataPlotter ("Henrico", "Virginia", "JHU")
henrico.plotCasesAndDeathsTwoPanes (7)

washington = cp.countyDataPlotter ("Washington", "Oregon", "JHU")
washington.plotCasesAndDeathsTwoPanes (7)

westchester = cp.countyDataPlotter ("Westchester", "New York", "JHU")
westchester.plotCasesAndDeathsTwoPanes (7)
