#!/usr/bin/env/python

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)

class countyDataPlotter:
    def __init__ (self, county, state, dataType, insertType = None):

        # County, state, and data type are static per instantiation
        self.county = county
        self.state = state
        self.dataType = dataType
        self.insertType = insertType

        # Data type readers just grab lists of dates, cases, and deaths. Preprocessing in __init__
        if self.dataType == "NYT":
            readFunction = self.readNYTData
        elif self.dataType == "JHU":
            readFunction = self.readJHUData
        else:
            print ("Unknown data type, options are 'NYT' or 'JHU'.")
            sys.exit ()

        # Should assert
        if self.insertType:
            if self.insertType == "right" or self.insertType == "left":
                pass
            else:
                print ("Unknown insert type, options are 'right' or 'left'.")
                sys.exit ()
            
        # Read data
        self.dates, self.cumulativeCases, self.cumulativeDeaths = readFunction ()

        # Compute date limits (future: adjustable) 
        self.dateLims = [self.dates[0], self.dates[-1]]
        
        # Compute daily cases from cumulatives
        self.dailyCases = [self.cumulativeCases[0]]
        self.dailyDeaths = [self.cumulativeDeaths[0]]
        for i in range(1, len(self.cumulativeCases)):
            self.dailyCases.append(self.cumulativeCases[i] - self.cumulativeCases[i - 1])
            self.dailyDeaths.append(self.cumulativeDeaths[i] - self.cumulativeDeaths[i - 1])

    def readNYTData (self):
        usCounties = pd.read_csv("https://github.com/nytimes/covid-19-data/raw/master/us-counties.csv")
        countyData = usCounties[(usCounties.state == self.state) & \
                                (usCounties.county == self.county)].reset_index()

        dates = countyData['date'].tolist()
        dates = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in dates]

        cumulativeCases = countyData['cases'].tolist()
        cumulativeDeaths = countyData['deaths'].tolist()

        return dates, cumulativeCases, cumulativeDeaths

    def readJHUData (self):
        usCases = pd.read_csv("https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
        usDeaths = pd.read_csv("https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv") 

        countyCases = usCases[(usCases.Province_State == self.state) & \
                              (usCases.Admin2 == self.county)].reset_index()
        countyDeaths = usDeaths[(usDeaths.Province_State == self.state) & \
                                (usDeaths.Admin2 == self.county)].reset_index()

        # Return cumulative case list, find first non-zero index
        # Deaths from JHU have one extra field, so offset the cumulative data in place
        nonZeroIndex = np.nonzero(countyCases.values.tolist()[0][12:])[0][0] + 12
        cumulativeCases = countyCases.values.tolist()[0][nonZeroIndex:]
        cumulativeDeaths = countyDeaths.values.tolist()[0][nonZeroIndex + 1:]

        dates = list(countyCases)[nonZeroIndex:]
        dates = [dt.datetime.strptime(date, '%m/%d/%y').date() for date in dates]

        return dates, cumulativeCases, cumulativeDeaths

    def convolutionMovingAverage (self, data, window):
        weights = np.repeat(1.0, window) / window
        dataExtension = np.hstack([[0] * (window - 1), data])

        # This is a bit of a hack. Just screw around with the convolution window to fit depending on the window size.

        dataMovingAverage = \
            np.convolve(dataExtension, weights)[window + (window - 8): -(window - (window - 6))]

        return dataMovingAverage 

    def setTwoPaneFormatPerPane (self, ax, axDaily):
        # Will use these to smooth out the x data for any called county
        locator = mdates.AutoDateLocator(maxticks = 10)
        formatter = mdates.ConciseDateFormatter(locator)

        # Ensure cumulative curve sits on top of secondary cutve
        ax.set_zorder(10)
        ax.patch.set_visible(False)

        ax.set_ylim(bottom=0)

        ax.tick_params(labelsize=8)

        # Apply formatting after second axis
        axDaily.xaxis.set_major_locator(locator)
        axDaily.xaxis.set_major_formatter(formatter)
        
        # Only need to set the xlim on the second axis
        axDaily.set_xlim(self.dateLims)
        
        # NYTimes data is sometimes a little ridiculous
        axDaily.set_ylim(bottom=0)

        axDaily.tick_params(labelsize=8)
        
    def plotCasesAndDeathsTwoPanes (self, window):
        # Compute the moving average but just don't just truncate
        dailyCasesMovingAverage = self.convolutionMovingAverage(self.dailyCases, window)
        dailyDeathsMovingAverage = self.convolutionMovingAverage(self.dailyDeaths, window)

        # Start figure
        fig, ax = plt.subplots(2, 1, constrained_layout = True, figsize = (5, 6), dpi=300)
        ax[0].plot(self.dates, self.cumulativeCases, '-', c='blue', lw=1.5)
        ax[0].plot(self.dates, self.cumulativeCases, '.', c='blue', lw=1.5)

        ax[0].set_title(self.county + ", " + self.state + " Cumulative Cases and Cases/Day", fontsize = 8)
        ax[0].set_ylabel("Cumulative Cases", fontsize = 8)
        
        axDaily0 = ax[0].twinx()
        axDaily0.bar(self.dates, self.dailyCases, color='orange', align='edge')
        axDaily0.plot(self.dates, dailyCasesMovingAverage, c='grey')

        axDaily0.set_ylabel("Daily Cases", fontsize=8)

        # Custom legend
        convolutionLabel = str(window) + " Day Convolution"
        legendElements = [matplotlib.lines.Line2D([0], [0], color='b', marker='.', lw=1.5, label='Cumulative Cases'), \
                          matplotlib.lines.Line2D([0], [0], color='grey', lw=1.5, label=convolutionLabel)]
        ax[0].legend(handles=legendElements, loc=2, fontsize=8)

        # Common pane format options
        self.setTwoPaneFormatPerPane(ax[0], axDaily0)

        if self.insertType:
            # Optional inset with log daily data
            axInset = plt.axes([0, 0, 1, 1])

            if self.insertType == 'right':
                ip = InsetPosition(ax[0], [0.40, 0.25, 0.4, 0.4])
            elif self.insertType == 'left':
                print ("'left' is not actually supported")
                sys.exit()
            axInset.set_axes_locator(ip)

            axInset.bar(self.dates[-30:], self.dailyCases[-30:], color='orange', align='edge')
            axInset.plot(self.dates[-30:], dailyCasesMovingAverage[-30:], c='grey')

            # Will use these to smooth out the x data for any called county
            locator = mdates.AutoDateLocator(maxticks = 6)
            formatter = mdates.ConciseDateFormatter(locator)

            # Apply formatting after second axis
            axInset.xaxis.set_major_locator(locator)
            axInset.xaxis.set_major_formatter(formatter)
            
            # Only need to set the xlim on the second axis
            newDateLims = [self.dates[-30], self.dates[-1]]
            axInset.set_xlim(newDateLims)
            
            # NYTimes data is sometimes a little ridiculous
            axInset.set_ylim(bottom=0)

            axInset.tick_params(labelsize=8)

        # Ax[1] is deaths
        ax[1].plot(self.dates, self.cumulativeDeaths, '-', c='blue', lw=1.5)
        ax[1].plot(self.dates, self.cumulativeDeaths, '.', c='blue', lw=1.5)

        ax[1].set_title(self.county + ", " + self.state + " Cumulative Deaths and Deaths/Day", fontsize=8)
        ax[1].set_ylabel("Cumulative Deaths", fontsize=8)
        
        axDaily1 = ax[1].twinx()
        axDaily1.bar(self.dates, self.dailyDeaths, color='orange', align='edge')
        axDaily1.plot(self.dates, dailyDeathsMovingAverage, c='grey')

        axDaily1.set_ylabel("Daily Deaths", fontsize=8)
        
        # Custom legend
        convolutionLabel = str(window) + " Day Convolution"
        legendElements = [matplotlib.lines.Line2D([0], [0], color='b', marker='.', lw=1.5, label='Cumulative Deaths'),                       matplotlib.lines.Line2D([0], [0], color='grey', lw=1.5, label=convolutionLabel)]
        ax[1].legend(handles=legendElements, fontsize=8)

        # Common pane format options
        self.setTwoPaneFormatPerPane(ax[1], axDaily1)

        
        # Save a figure
        if not os.path.exists('images'):
          os.makedirs('images')

        nameOfFigure = 'images/' + self.county + "-" + self.state + "-" + self.dataType + ".png"
        plt.savefig(nameOfFigure)

