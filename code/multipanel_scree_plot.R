source('/Users/gkiar/code/classes/upward-spiral/grelliam/code/getElbows.R')
source('/Users/gkiar/code/classes/upward-spiral/grelliam/code/load_graphs.R')
source('/Users/gkiar/code/classes/upward-spiral/grelliam/code/scree_with_elbows_utility.R')

library(igraph)
library(foreach)
library(ggplot2)

name = c('KKI2009',
         'MRN114',
         'MRN1313',
         'SWU4',
         'BNU1',
         'BNU3',
         'NKI1',
         'NKIENH')
nodes = 200
path <- c('/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/KKI2009',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/MRN114',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/MRN1313',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/SWU4',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/BNU1',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/BNU3',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/NKI1',
          '/Users/gkiar/code/classes/upward-spiral/grelliam/data/cpac200/NKIENH')
plotf = '/Users/gkiar/code/classes/upward-spiral/grelliam/figs/multipanel_scree_plots/test.png'

png(plotf, width=960, height=384, units="px")
par(mfrow=c(2,4))
botleft = 5
for (i in 1:length(name)){
  if (i == botleft) {
    scree_with_elbows(name[i], nodes, path[i], idx = 1)
  } else {
    scree_with_elbows(name[i], nodes, path[i])
  }
}

dev.off()
