#on each project
library(r2mlm)
library(rsq)
library(car)
library("performance")

projectList <- c("microsoft/vscode" ,"flutter/flutter" , "golang/go" , "dart-lang/sdk", 
                 "dotnet/runtime", "elastic/kibana" ,"rust-lang/rust" , "kubernetes/kubernetes",
                 "cockroachdb/cockroach", "tensorflow/tensorflow","microsoft/TypeScript", 
                 "godotengine/godot", "ansible/ansible", 
                 "elastic/elasticsearch", "rancher/rancher", "dotnet/roslyn" , "qgis/QGIS")

result <- read.csv("D:/Research/issue process mining/data/mean.csv")
result = result[which(result$slice_time >= '2020-01-01'),]
result$delta_time <- result$resolution_time - result$before_average_time

data <- data.frame()
for (i in 1: 17) {
  issuedata = result[result$project_name == projectList[i],]
  issuedata$resolution_time <- log(issuedata$resolution_time+1)
  issuedata$event_number <- log(issuedata$event_number+1)
  issuedata$issue_length <- log(issuedata$issue_length+1)
  issuedata$participant_number <- log(issuedata$participant_number+1)
  issuedata$entropy <- log(issuedata$entropy + 1)
  issuedata$core_issue <- log(issuedata$core_issue + 1)
  issuedata$normal_issue <- log(issuedata$normal_issue + 1)
  issuedata$core_assign <- log(issuedata$core_assign + 1)
  issuedata$core_label <- log(issuedata$core_label + 1)
  issuedata$core_subscribe <- log(issuedata$core_subscribe + 1)
  issuedata$before_average_time <- log(issuedata$before_average_time+1)
  issuedata$slice_average_time <- log(issuedata$slice_average_time + 1)
  # issuedata$delta_time <- log(issuedata$delta_time + 825)

  # issuedata$resolution_time <- scale(issuedata$resolution_time)
  issuedata$event_number <- scale(issuedata$event_number)
  issuedata$issue_length <- scale(issuedata$issue_length)
  issuedata$participant_number <- scale(issuedata$participant_number)
  issuedata$entropy <- scale(issuedata$entropy)
  issuedata$core_issue <- scale(issuedata$core_issue)
  issuedata$normal_issue <- scale(issuedata$normal_issue)
  issuedata$core_assign <- scale(issuedata$core_assign)
  issuedata$core_label <- scale(issuedata$core_label)
  issuedata$core_subscribe <- scale(issuedata$core_subscribe)
  issuedata$before_average_time <- scale(issuedata$before_average_time)
  issuedata$slice_average_time <- scale(issuedata$slice_average_time)
  # issuedata$delta_time <- scale(issuedata$delta_time)
  data <- rbind(data, issuedata)
}
# macro.model = lm(resolution_time ~ event_number + participant_number + entropy + core_issue + normal_issue +
#                       core_assign + core_label + core_subscribe + before_average_time + entropy : event_number  + entropy : participant_number
#                     + entropy : core_issue + entropy : normal_issue + entropy : core_assign + entropy : core_label
#                     + entropy : core_subscribe + entropy : before_average_time, data = data)

macro.model = glmer(resolution_time ~ event_number + participant_number + entropy + core_issue + normal_issue +
                    core_assign + core_label + core_subscribe + before_average_time + entropy : event_number  + entropy : participant_number
                  + entropy : core_issue + entropy : normal_issue + entropy : core_assign + entropy : core_label
                  + entropy : core_subscribe + entropy : before_average_time + (1 | project_name), data = data)

summary(macro.model)
model_performance(macro.model)
print(Anova(macro.model, type = "III"))
