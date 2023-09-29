library("car")
library("lme4")
library("performance")
library("emmeans")
library("data.table")  
library("dplyr")
library("tidyverse")    # needed for data manipulation
library("knitr")
library("stringr")
library("lmerTest")     # to get p-value estimations
library("performance")
library("car")
library("pscl")
library("sjstats")
library("ggplot2")
library("MASS")
library("mlmRev")
library("agridat")
library("MCMCglmm")
library("plotMCMC")
library("see")
library("patchwork")

result <- read.csv("D:/FSE/mean_1.csv")
result$resolution_time <- log(result$resolution_time+1)
result$event_number <- log(result$event_number+1)
result$issue_length <- log(result$issue_length+1)
result$participant_number <- log(result$participant_number+1)
result$entropy <- log(result$entropy + 1)
result$core_issue <- log(result$core_issue + 1)
result$normal_issue <- log(result$normal_issue + 1)
result$core_assign <- log(result$core_assign + 1)
result$core_label <- log(result$core_label + 1)
result$core_subscribe <- log(result$core_subscribe + 1)
result$before_average_time <- log(result$before_average_time+1)

result$resolution_time <- scale(result$resolution_time)
result$event_number <- scale(result$event_number)
result$issue_length <- scale(result$issue_length)
result$participant_number <- scale(result$participant_number)
result$entropy <- scale(result$entropy)
result$core_issue <- scale(result$core_issue)
result$normal_issue <- scale(result$normal_issue)
result$core_assign <- scale(result$core_assign)
result$core_label <- scale(result$core_label)
result$core_subscribe <- scale(result$core_subscribe)
result$before_average_time <- scale(result$before_average_time)

get_points <- function(x, n = 3) {
  x_mean <- mean(x) 
  x_sd   <- sd(x) 
  
  x_bt   <- min(x)  
  x_m2   <- x_mean - 2 * x_sd  
  x_m1   <- x_mean - x_sd 
  x_ct   <- x_mean 
  x_p1   <- x_mean + x_sd 
  x_p2   <- x_mean + 2 * x_sd
  x_up   <- max(x)

  x_bt_r <- round(x_bt, digits = 1)
  x_m2_r <- round(x_m2, digits = 1)
  x_m1_r <- round(x_m1, digits = 1)
  x_ct_r <- round(x_ct, digits = 1)
  x_p1_r <- round(x_p1, digits = 1)
  x_p2_r <- round(x_p2, digits = 1)
  x_up_r <- round(x_up, digits = 1)

  # if (n == 3) {
  #  points <- c(x_bt_r, x_ct_r, x_up_r)
  # }
  
  if (n == 3) {
    points <- c(x_m1_r, x_ct_r, x_p1_r)
  } else if (n == 5) {
    points <- c(x_bt_r, x_m1_r, x_ct_r, x_p1_r, x_up_r)
  } else {
    points <- c(x_bt_r, x_m2_r, x_m1_r, x_ct_r, x_p1_r, x_p2_r, x_up_r)
  }
  return(points)
}

generate_and_save_emmip <- function(rq_model,formula, file,vary_project_age_fix_fork_entropy) {
  # formula: fork_entropy_scale ~ project_age_scale

  emmip_data <- emmip(rq_model, formula, at = vary_project_age_fix_fork_entropy, plotit = FALSE)
  write.csv(as.data.table(emmip_data),
            file <- file,
            row.names = FALSE,
            fileEncoding = "UTF-8")
  
  cat("emmip data saved to", file, "\n")
}

#macro.model = glmer(resolution_time ~ event_number + participant_number + entropy + core_issue + normal_issue + 
#            core_assign + core_label + core_subscribe + before_average_time + entropy : event_number  + entropy : participant_number
#          + entropy : core_issue + entropy : normal_issue + entropy : core_assign + entropy : core_label
#          + entropy : core_subscribe + entropy : before_average_time + (1 | project_name), data = result)

macro.model = glmer(resolution_time ~ event_number + participant_number + entropy + core_issue + normal_issue + 
                      core_assign + core_label + core_subscribe + entropy : event_number  + entropy : participant_number
                    + entropy : core_issue + entropy : normal_issue + entropy : core_assign + entropy : core_label
                    + entropy : core_subscribe + (1 | project_name), data = result)

vif(macro.model)
summary(macro.model)
model_performance(macro.model)
print(Anova(macro.model, type = "III"))

entropy_c <- get_points(result$entropy)
data_point <- list(
  entropy=entropy_c,
  before_average_time=seq(entropy_c[[1]], entropy_c[[length(entropy_c)]], by = 0.1))
generate_and_save_emmip(rq_model=macro.model,entropy ~ before_average_time,file = "D:/FSE/before_average_time.csv",data_point)
