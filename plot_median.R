plot_median <- function(df) {
  # plot mean and errorbar.
  # df contains only two columns, each representing x and y
  if (length(df) == 2) {
    df %<>% mutate(group = 1)
  }
  names(df) <- c("x", "y", "group")
  
  xvals <- c(unique(df$x))
  
  df_res <- data.frame(x = xvals,
                       median = double(length(xvals)),
                       se = double(length(xvals)))
  
  groupvals <- c(unique(df$group))
  for (val in xvals) {
    yvals <- df %>% filter(x == val & !is.nan(y)) %>% dplyr::select(y)
    yvals <- yvals$y
    df_res[df_res$x == val, "median"] <- median(yvals)
    df_res[df_res$x == val, "se"] <- sd(sapply(1:100, function(x) median(sample(yvals, size = length(yvals), replace = T)))) / sqrt(100)
  }
  
  df_res %<>% mutate(upper_bound = median + se,
                     lower_bound = median - se)
  plot <- ggplot(
    df_res,
    aes(x = x, y = median)) +
    geom_line(position = position_dodge(0.1)) +
    geom_errorbar(
      aes(
        ymin = lower_bound,
        ymax = upper_bound
      ),
      position = position_dodge(0.1), width = 0.3
    ) +
    geom_point(
      aes(x = x, y = median),
      size = 1.5, position = position_dodge(0.1)
    ) +
  theme(legend.position = "none")
  return(plot)
}
