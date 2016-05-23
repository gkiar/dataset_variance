# Multi-Panel Scree Plots
Greg Kiar  
April 23, 2016  


Previously I showed how to compute a scree plot from this data. Now, in the interest of comparing results, I have processed many datasets using the same scree plot code and displayed them side by side.

Though this analysis will be carried out across multiple scales, here we show the case for the Desikan atlas, only.

```r
name = c('KKI2009 Desikan',
         'MRN114 Desikan',
         'MRN1313 Desikan',
         'SWU4 Desikan',
         'BNU1 Desikan',
         'BNU3 Desikan',
         'NKI1 Desikan',
         'NKIENH Desikan')
nodes = 70
path <- c('/Users/gkiar/code/classes/upward-spiral/grelliam/data/KKI2009',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/MRN114',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/MRN1313',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/SWU4',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/BNU1',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/BNU3',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/NKI1',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/NKIENH')
```



```
## [1] "Total number of graphs found: 42"
## [1] "Number of graphs which failed to load:  42"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 42"
```

```
## [1] "Total number of graphs found: 114"
## [1] "Number of graphs which failed to load:  114"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 114"
```

```
## [1] "Total number of graphs found: 1305"
## [1] "Number of graphs which failed to load:  1305"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 1305"
```

```
## [1] "Total number of graphs found: 454"
## [1] "Number of graphs which failed to load:  454"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 454"
```

```
## [1] "Total number of graphs found: 81"
## [1] "Number of graphs which failed to load:  81"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 81"
```

```
## [1] "Total number of graphs found: 46"
## [1] "Number of graphs which failed to load:  46"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 46"
```

```
## [1] "Total number of graphs found: 38"
## [1] "Number of graphs which failed to load:  38"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 38"
```

```
## [1] "Total number of graphs found: 198"
## [1] "Number of graphs which failed to load:  198"
## [1] "Graphs with improper dimensions:  0"
## [1] "Graphs with less than 1e+05 edges: 0"
## [1] "Remaining graphs available for processing: 198"
```

![](multipanel_scree_plots_files/figure-html/unnamed-chunk-3-1.png)<!-- -->
