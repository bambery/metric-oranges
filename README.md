# US Adjacencies, COVID Deaths Time Series, and Domestic Flight Routes

This project uses COVID-19 death data as collected by Johns Hopkins University (henceforth referred to as "JHU"), which is available to the public on Github, and provides daily death counts by US region. The raw data set repository, JHU sources, and adjustments made to this data by JHU can be found in Appendix A2. The data as presented by JHU represents a daily cumulative total of deaths per region per day.

As the project ultimately depends on the JHU COVID-19 data set, the methodology used there sets the tone for the rest of the project. The JHU data is collected in the US by FIPS (described below), which roughly (but not exactly) divide the country into counties. This project specifically seeks to examine patterns of death along two primary transmission routes: adjacency via geography and adjacency via direct airline flight on a weekly death count schedule.

In order to build a dataset for testing of a [proposed improvement for algorithmic analysis of metric measure spaces](https://arxiv.org/abs/2011.00616v1), data of a certain shape was required. In order to test this new algorithm, the request was for several datasets:
- US COVID deaths by week
- A way to trace deaths in the US by geography
- A method to subdivide the US into a graph with meaningful "Nodes" regarding disease spread
- A way to determine geographical adjacency of each Node
- A list of major airports in the US and a list of domestic airline flights between public airports

The final result of these datasets may be found at this github:
[https://github.com/bambery/metric-oranges/tree/main/outputs](https://github.com/bambery/metric-oranges/tree/main/outputs)

A description of the content and the columns can be found at this link:
[https://github.com/bambery/metric-oranges/blob/main/outputs/contents.txt](https://github.com/bambery/metric-oranges/blob/main/outputs/contents.txt)

For a longer discussion on the work to generate this data, please see the following paper: [US Adjacencies, COVID Deaths Time Series, and Domestic Flight Routes](https://docs.google.com/document/d/1_DcsPpbk8-WekyRNpDN0htOQCxp5NIp5uk9T5acMc9E/edit?tab=t.0).
