#!/usr/bin/env

import county_plotter as cp

rocklandJHU = cp.countyDataPlotter ("Rockland", "New York", "JHU")
rocklandJHU.plotCasesAndDeathsTwoPanes (7)

rocklandNYT = cp.countyDataPlotter ("Rockland", "New York", "NYT")
rocklandNYT.plotCasesAndDeathsTwoPanes (7)

henricoJHU = cp.countyDataPlotter ("Henrico", "Virginia", "JHU")
henricoJHU.plotCasesAndDeathsTwoPanes (7)

henricoNYT = cp.countyDataPlotter ("Henrico", "Virginia", "NYT")
henricoNYT.plotCasesAndDeathsTwoPanes (7)
