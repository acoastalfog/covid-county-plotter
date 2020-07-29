#!/usr/bin/env

import county_plotter as cp

rocklandJHU = cp.countyDataPlotter ("Rockland", "New York", "JHU", insertType = 'right')
rocklandJHU.plotCasesAndDeathsTwoPanes (7)

henricoJHU = cp.countyDataPlotter ("Henrico", "Virginia", "JHU")
henricoJHU.plotCasesAndDeathsTwoPanes (7)

washingtonJHU = cp.countyDataPlotter ("Washington", "Oregon", "JHU")
washingtonJHU.plotCasesAndDeathsTwoPanes (7)

lickingJHU = cp.countyDataPlotter ("Licking", "Ohio", "JHU")
lickingJHU.plotCasesAndDeathsTwoPanes (7)

dupageJHU = cp.countyDataPlotter ("DuPage", "Illinois", "JHU")
dupageJHU.plotCasesAndDeathsTwoPanes (7)

cookJHU = cp.countyDataPlotter ("Cook", "Illinois", "JHU")
cookJHU.plotCasesAndDeathsTwoPanes (7)

deschutesJHU = cp.countyDataPlotter ("Deschutes", "Oregon", "JHU")
deschutesJHU.plotCasesAndDeathsTwoPanes (7)
