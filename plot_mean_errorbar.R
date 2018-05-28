plot_mean_errorbar <- function(df) {
  # plot mean and errorbar.
  # df contains only two columns, each representing x and y
  if (length(df) == 2) {
    df %<>% mutate(group = 1)
  }
  names(df) <- c("x", "y", "group")
  df %<>% group_by(x, group)
  df %<>% summarise(
    mean = mean(y, na.rm = T),
    sd = sd(y, na.rm = T),
    cnt = sum(!is.na(y))
    )
  df %<>% mutate(
    upper_bound = mean + sd / sqrt(cnt),
    lower_bound = mean - sd / sqrt(cnt)
    )
  df %<>% data.frame
  df %<>% ungroup
  plot <- ggplot(
    df,
    aes(
      x = x,
      y = mean,
      colour = group,
      group = group
      )
    ) +
    geom_line(position = position_dodge(0.1)) +
    geom_errorbar(
      aes(
        ymin = lower_bound,
        ymax = upper_bound
        ),
      position = position_dodge(0.1), width = 1
      ) +
    geom_point(
      aes(x = x, y = mean),
      size = 2, position = position_dodge(0.1)
    )
    theme(legend.position = "bottom")
  return(plot)
}
