eventList = ['NormalLabeledEvent','NormalIssueComment','CoreLabeledEvent','CoreMilestonedEvent','CoreAssignedEvent', 'CoreCrossReferencedEvent',
               'CoreClosedEvent', 'CoreIssueComment', 'NormalSubscribedEvent', 'CoreLockedEvent', 'CoreSubscribedEvent', 'CoreReopenedEvent',
               'CoreRenamedTitleEvent', 'NormalClosedEvent', 'CoreReferencedEvent', 'NormalCrossReferencedEvent', 'NormalRenamedTitleEvent',
               'NormalReferencedEvent', 'BotIssueComment', 'CoreMarkedAsDuplicateEvent', 'CoreCommentDeletedEvent', 
               'BotSubscribedEvent', 'BotClosedEvent', 'CoreAddedToProjectEvent', 'CoreMovedColumnsInProjectEvent',
               'BotLockedEvent', 'BotLabeledEvent', 'CoreTransferredEvent', 'CorePinnedEvent', 'BotCrossReferencedEvent',
               'CoreRemovedFromProjectEvent', 'BotAssignedEvent', 'CoreConnectedEvent',
               'BotReferencedEvent', 'NormalCommentDeletedEvent', 'NormalAddedToProjectEvent',
               'NormalMovedColumnsInProjectEvent','NormalRemovedFromProjectEvent', 'BotAddedToProjectEvent']
positive = []
negative = []
for event in eventList: 
    f = open("D:/FSE/" + event + "-log1.txt")
    lines = f.readlines()
    result = 0
    print(lines[4])
    eCoef = float(lines[4].split()[1])
    ePVal = eval(lines[4].split()[5])
    R2 = float(lines[12].split()[1])
    print(eCoef, ePVal, R2)
    if ePVal < 0.05:
        CoString = str(eCoef) + '*'
    else:
        CoString = str(eCoef)
    if eCoef > 0:
        positive.append([event, CoString, R2])
    else:
        negative.append([event, CoString, R2])

for pos in positive:
    print(pos)

print("====================================================")
for neg in negative:
    print(neg)