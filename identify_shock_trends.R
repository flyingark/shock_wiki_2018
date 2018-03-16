library(dplyr)
library(magrittr)
library(ggplot2)

# import politician shock data
df <- read.csv(file = 'pol_trends_data.csv')
df %<>% mutate(
  date = as.Date(date)
)
df <- df[order(df$scholar_name, df$scholar_profession, df$date),]
df %<>% filter(articleid != 0)

# identify shock using 5 IQR rule
df %<>% mutate(
  trends = ifelse(
    test = trends == 0,
    yes = NA, no = trends
  )
)
df %<>% 
  group_by(articleid) %<>%
  mutate(
    normal_5iqr_trends = mean(trends, na.rm = T) + sd(trends, na.rm = T) * (0.675 + 5 * 1.35)
  ) %<>% data.frame
df %<>%
  mutate(
    shock_normal_5iqr_trends = ifelse(
      test = trends > normal_5iqr_trends,
      yes = 1, no = 0
    )
  )
# export shock identified by wiki_trends
df %>% write.table(file="pol_trends_data.csv", append=FALSE, sep=",")
