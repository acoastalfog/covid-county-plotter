#!/usr/bin/env/python

import os
import numpy as np
import pandas as pd
import matplotlib
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class countyDataPlotter:
    def __init__ (self, county, state):
        usCounties = pd.read_csv("https://github.com/nytimes/covid-19-data/raw/master/us-counties.csv")

        self.county = county
        self.state = state
        self.countyData = usCounties[(usCounties.state == self.state) & \
                                     (usCounties.county == self.county)].reset_index()
        
        self.dates = self.countyData['date'].tolist()
        self.dates = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in self.dates]
        self.dateLims = [self.dates[0], self.dates[-1]]
        
        self.cumulativeCases = self.countyData['cases'].tolist()
        self.cumulativeDeaths = self.countyData['deaths'].tolist()

        self.dailyCases = [self.cumulativeCases[0]]
        self.dailyDeaths = [self.cumulativeDeaths[0]]
        for i in range(1, len(self.cumulativeCases)):
            self.dailyCases.append(self.cumulativeCases[i] - self.cumulativeCases[i - 1])
            self.dailyDeaths.append(self.cumulativeDeaths[i] - self.cumulativeDeaths[i - 1])

    def convolutionMovingAverage (self, data, window):
        weights = np.repeat(1.0, window) / window
        dataExtension = np.hstack([[0] * (window - 1), data])

        # This is a bit of a hack. Just screw around with the convolution window to fit depending on the window size.
        dataMovingAverage = \
            np.convolve(dataExtension, weights)[window + (window - 7): -(window - (window - 5))]

        return dataMovingAverage 

    def plotCasesAndDeathsTwoPanes (self, window):
        # Compute the moving average but just don't just truncate
        dailyCasesMovingAverage = self.convolutionMovingAverage(self.dailyCases, window)
        dailyDeathsMovingAverage = self.convolutionMovingAverage(self.dailyDeaths, window)

        # Start figure
        fig, ax = plt.subplots(2, 1, constrained_layout = True, figsize = (5, 6), dpi=300)
        
        # Will use these to smooth out the x data for any called county
        locator = mdates.AutoDateLocator(maxticks = 10)
        formatter = mdates.ConciseDateFormatter(locator)
        
        # Ax[0] is cases
        ax[0].set_title(self.county + ", " + self.state + " Cumulative Cases and Cases/Day", fontsize = 8)
        ax[0].set_ylabel("Cumulative Cases", fontsize = 10)
        
        ax[0].plot(self.dates, self.cumulativeCases, '-', c='blue', lw=1.5)
        ax[0].plot(self.dates, self.cumulativeCases, '.', c='blue', lw=1.5)
        
        # Ensure cumulative curve sits on top of secondary cutve
        ax[0].set_zorder(10)
        ax[0].patch.set_visible(False)
        
        axDaily0 = ax[0].twinx()
        axDaily0.bar(self.dates, self.dailyCases, color='orange', align='edge')
        axDaily0.plot(self.dates, dailyCasesMovingAverage, c='grey')
        
        # Apply formatting after second axis
        axDaily0.xaxis.set_major_locator(locator)
        axDaily0.xaxis.set_major_formatter(formatter)
        axDaily0.set_ylabel("Daily Cases", fontsize=10)
        
        # Only need to set the xlim on the second axis
        axDaily0.set_xlim(self.dateLims)
        
        # NYTimes data is sometimes a little ridiculous
        axDaily0.set_ylim(bottom=0)
        
        # Custom legend
        convolutionLabel = str(window) + " Day Convolution"
        legendElements = [matplotlib.lines.Line2D([0], [0], color='b', marker='.', lw=1.5, label='Cumulative Cases'),                       matplotlib.lines.Line2D([0], [0], color='grey', lw=1.5, label=convolutionLabel)]
        ax[0].legend(handles=legendElements, fontsize=8)
        
        # Ax[1] is deaths
        ax[1].set_title(self.county + ", " + self.state + " Cumulative Deaths and Deaths/Day", fontsize=8)
        ax[1].set_ylabel("Cumulative Deaths", fontsize=10)
        
        ax[1].plot(self.dates, self.cumulativeDeaths, '-', c='blue', lw=1.5)
        ax[1].plot(self.dates, self.cumulativeDeaths, '.', c='blue', lw=1.5)
        
        # Ensure cumulative curve sits on top of secondary cutve
        ax[1].set_zorder(10)
        ax[1].patch.set_visible(False)
        
        axDaily1 = ax[1].twinx()
        axDaily1.bar(self.dates, self.dailyDeaths, color='orange', align='edge')
        axDaily1.plot(self.dates, dailyDeathsMovingAverage, c='grey')
        
        # Apply formatting after second axis
        axDaily1.xaxis.set_major_locator(locator)
        axDaily1.xaxis.set_major_formatter(formatter)
        axDaily1.set_ylabel("Daily Deaths", fontsize=10)
        
        # Only need to set the xlim on the second axis
        axDaily1.set_xlim(self.dateLims)
        
        # NYTimes data is sometimes a little ridiculous
        axDaily1.set_ylim(bottom=0)
        
        # Custom legend
        convolutionLabel = str(window) + " Day Convolution"
        legendElements = [matplotlib.lines.Line2D([0], [0], color='b', marker='.', lw=1.5, label='Cumulative Deaths'),                       matplotlib.lines.Line2D([0], [0], color='grey', lw=1.5, label=convolutionLabel)]
        ax[1].legend(handles=legendElements, fontsize=8)
        
        # Save a figure
        if not os.path.exists('images'):
          os.makedirs('images')

        nameOfFigure = 'images/' + self.county + "-" + self.state + ".png"
        plt.savefig(nameOfFigure)

