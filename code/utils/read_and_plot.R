library(ggplot2)
plot.multi.dens <- function(s, minn, maxx)
{
  plot(density(s[[1]]), xlim = (c(minn, maxx)), log= 'x', main = "", col='blue')
  for(i in 1:length(s)) {
    lines(density(s[[i]]), col = 'blue')
  }
}

fils = list.files('~/code/ocp/scratch/dti_formats', pattern='.gzip', full.names = TRUE)
data <- list()
for (i in 1:length(fils)){
  load(fils[i])
  temp <- as.numeric(unlist(bar))
  data[[length(data)+1]] <- temp
}
maxx <- max(unlist(data))
minn <- min(unlist(data))
plot.multi.dens(data, minn, maxx)
#dx = data.frame(data)
#print(dx)

#ggplot(dx, aes(x=values)) + geom_density()
