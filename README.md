# COVID County Plotter

I was frustrated that simple visual time series plots of county-level COVID data seemed to be hard to come by, so I wrote a simple, poorly-engineered, quick and dirty script to plot what I wanted to see. It only has one feature and only makes one chart.

It's pretty easy to use.

```python
import county_plotter as cp

westchester = cp.countyDataPlotter ("Westchester", "New York", "JHU")
westchester.plotCasesAndDeaths (7)
```

Takes county and state, and then you can select between the JHU or NYT live github data. JHU tends to be ahead. Parameter passed to the plotting function is the moving window size. And it just writes to a fixed format ```images``` folder.

It's all very hacky.

If you want to add a new plot or feature, please feel free to throw me a PR.

Here's an example of the only thing it does for my home county of Rockland.

![Rockland][media/rockland.png]
