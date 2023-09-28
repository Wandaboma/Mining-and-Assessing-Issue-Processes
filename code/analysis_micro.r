library("car")
library("lme4")
library("performance")
library("emmeans")
library("data.table")  # 用于数据表操作
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

data <- read.csv("D:/FSE/mean_detailed_with_before_transtime_merged.csv")
data = data[data$before_trans_time > 0,]
data$transition_time <- log(data$transition_time + 1)
data$event_number <- log(data$event_number + 1)
data$issue_length <- log(data$issue_length + 1)
data$participant_number <- log(data$participant_number + 1)
data$entropy <- log(data$entropy + 1)
data$core_issue <- log(data$core_issue + 1)
data$normal_issue <- log(data$normal_issue + 1)
data$core_assign <- log(data$core_assign + 1)
data$core_label <- log(data$core_label + 1)
data$core_subscribe <- log(data$core_subscribe + 1)
data$before_average_time <- log(data$before_average_time + 1)
data$before_trans_time <- log(data$before_trans_time + 1)

data$transition_time <- scale(data$transition_time)
data$event_number <- scale(data$event_number)
data$issue_length <- scale(data$issue_length)
data$participant_number <- scale(data$participant_number)
data$entropy <- scale(data$entropy)
data$core_issue <- scale(data$core_issue)
data$normal_issue <- scale(data$normal_issue)
data$core_assign <- scale(data$core_assign)
data$core_label <- scale(data$core_label)
data$core_subscribe <- scale(data$core_subscribe)
data$before_average_time <- scale(data$before_average_time)
data$before_trans_time <- scale(data$before_trans_time)

get_points <- function(x, n = 3) {
  x_mean <- mean(x)  # 计算 x 的均值
  x_sd   <- sd(x) # 计算 x 的标准差
  
  x_bt   <- min(x)   # 计算 x 的最小值
  x_m2   <- x_mean - 2 * x_sd  # 计算 x 的均值减去两倍标准差的值
  x_m1   <- x_mean - x_sd # 计算 x 的均值减去标准差的值
  x_ct   <- x_mean # 获取 x 的均值
  x_p1   <- x_mean + x_sd # 计算 x 的均值加上标准差的值
  x_p2   <- x_mean + 2 * x_sd # 计算 x 的均值加上两倍标准差的值
  x_up   <- max(x) # 计算 x 的最大值
  
  # 将上面计算出的各个值保留一位小数
  x_bt_r <- round(x_bt, digits = 1)
  x_m2_r <- round(x_m2, digits = 1)
  x_m1_r <- round(x_m1, digits = 1)
  x_ct_r <- round(x_ct, digits = 1)
  x_p1_r <- round(x_p1, digits = 1)
  x_p2_r <- round(x_p2, digits = 1)
  x_up_r <- round(x_up, digits = 1)
  
  # 根据 n 的取值，返回不同数量的点
  # 这是原来的做法，返回最值和均值
  # if (n == 3) {
  #  points <- c(x_bt_r, x_ct_r, x_up_r)
  # }
  # 现在改成返回均值 和 加、减一个标准差
  
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
  # file: 输出的 CSV 文件名
  
  # 生成 emmip 数据
  emmip_data <- emmip(rq_model, formula, at = vary_project_age_fix_fork_entropy, plotit = FALSE)
  # file <- paste("./", file, sep = "/")
  # 将数据保存为 CSV 文件
  write.csv(as.data.table(emmip_data),
            file <- file,
            row.names = FALSE,
            fileEncoding = "UTF-8")
  
  cat("emmip data saved to", file, "\n")
}

trans.model = glmer(transition_time ~ event_number + participant_number + entropy + core_issue + 
               normal_issue + core_assign + core_label + core_subscribe + before_trans_time + before_average_time + entropy : event_number
               + entropy : participant_number + entropy : core_issue + entropy : normal_issue + entropy : core_assign + entropy : core_label
               + entropy : core_subscribe + entropy : before_trans_time + entropy : before_average_time + (1 | merge), data = data)

vif(trans.model)
summary(trans.model)
model_performance(trans.model)
print(Anova(trans.model, type = "III"))

entropy_c <- get_points(result$entropy)
data_point <- list(
  entropy=entropy_c,
  before_trans_time=seq(entropy_c[[1]], entropy_c[[length(entropy_c)]], by = 0.1))
generate_and_save_emmip(rq_model=trans.model,entropy ~ before_trans_time,file = "D:/FSE/micro_entropy_before_trans_time.csv",data_point)
