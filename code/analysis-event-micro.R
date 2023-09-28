library("lme4")  
library("dplyr")
library(lmerTest)
library(memisc)
library("car")
library("performance")
library("emmeans")
eventList <- c('NormalIssueComment','CoreLabeledEvent','CoreMilestonedEvent','CoreAssignedEvent', 'CoreCrossReferencedEvent',
               'CoreClosedEvent', 'CoreIssueComment', 'NormalSubscribedEvent', 'CoreLockedEvent', 'CoreSubscribedEvent', 'CoreReopenedEvent',
               'CoreRenamedTitleEvent', 'NormalClosedEvent', 'CoreReferencedEvent', 'NormalCrossReferencedEvent', 'NormalRenamedTitleEvent',
               'NormalReferencedEvent', 'BotIssueComment', 'CoreMarkedAsDuplicateEvent', 'CoreCommentDeletedEvent', 
               'BotSubscribedEvent', 'BotClosedEvent', 'CoreAddedToProjectEvent', 'CoreMovedColumnsInProjectEvent',
               'BotLockedEvent', 'BotLabeledEvent', 'CoreTransferredEvent', 'CorePinnedEvent', 'BotCrossReferencedEvent',
               'CoreRemovedFromProjectEvent', 'BotAssignedEvent', 'CoreConnectedEvent',
               'BotReferencedEvent', 'NormalCommentDeletedEvent', 'NormalAddedToProjectEvent',
               'NormalMovedColumnsInProjectEvent','NormalRemovedFromProjectEvent', 'BotAddedToProjectEvent')
library(r2mlm)
library(rsq)
data <- read.csv('D:/FSE/mean_detailed_with_before_transtime.csv')
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

for (i in 1: 48) {
  print(eventList[i])
  issuedata = data[data$event_name == eventList[i],]
  #print(issuedata)
  model = glmer(transition_time ~ event_number + participant_number + entropy + core_issue + 
                        normal_issue + core_assign + core_label + core_subscribe + before_trans_time + before_average_time + entropy : event_number
                      + entropy : participant_number + entropy : core_issue + entropy : normal_issue + entropy : core_assign + entropy : core_label
                      + entropy : core_subscribe + entropy : before_trans_time + entropy : before_average_time + (1 | project_name), data = issuedata)
  filename = paste("D:/FSE/result/", eventList[i], "-log1.txt", sep = "")
  sink(file = filename)
  print(vif(model))
  print(summary(model))
  print(model_performance(model))
  print(Anova(model, type = "III"))
  sink()
}
