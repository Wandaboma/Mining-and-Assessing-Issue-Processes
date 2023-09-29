resultPath = "/home/sbh/APSEC/result/2023-09-19T00:40Z/"
from scipy.stats import mannwhitneyu
import statistics
file = open(resultPath + 'comparison.txt')
lines = file.readlines()
originK = []
originEntropy = []
newK = []
newEntropy = []
repo = 'microsoft/vscode'
for line in lines:
    if line.split()[0] != repo:
        with open(resultPath +'stats.txt', 'a') as f:
            f.write(f'current repo: {repo}\n')
            f.write(str(statistics.mean(originK))+ ' '+str(statistics.mean(newK)) + '\n')
            f.write(str(statistics.mean(originEntropy))+ ' ' + str(statistics.mean(newEntropy)) + '\n')
            stat, p_value = mannwhitneyu(originK, newK, alternative='greater')
            f.write(f'Greater Mann-Whitney U test on K: U={stat}, p={p_value}\n')

            stat, p_value = mannwhitneyu(originK, newK, alternative='less')
            f.write(f'Less Mann-Whitney U test on K: U={stat}, p={p_value}\n')

            stat, p_value = mannwhitneyu(originEntropy, newEntropy, alternative='greater')
            f.write(f'Greater Mann-Whitney U test on entropy: U={stat}, p={p_value}\n')

            stat, p_value = mannwhitneyu(originEntropy, newEntropy, alternative='less')
            f.write(f'Less Mann-Whitney U test on entropy: U={stat}, p={p_value}\n')

            repo = line.split()[0]
            originK = []
            originEntropy = []
            newK = []
            newEntropy = []
            f.write('=================================================================\n')

    originK.append(float(line.split()[1]))
    originEntropy.append(float(line.split()[2]))
    newK.append(float(line.split()[3]))
    newEntropy.append(float(line.split()[4]))

with open(resultPath +'stats.txt', 'a') as f:
    f.write(f'current repo: {repo}\n')
    f.write(str(statistics.mean(originK))+ ' '+str(statistics.mean(newK)) + '\n')
    f.write(str(statistics.mean(originEntropy))+ ' ' + str(statistics.mean(newEntropy)) + '\n')
    stat, p_value = mannwhitneyu(originK, newK, alternative='greater')
    f.write(f'Greater Mann-Whitney U test on K: U={stat}, p={p_value}\n')

    stat, p_value = mannwhitneyu(originK, newK, alternative='less')
    f.write(f'Less Mann-Whitney U test on K: U={stat}, p={p_value}\n')

    stat, p_value = mannwhitneyu(originEntropy, newEntropy, alternative='greater')
    f.write(f'Greater Mann-Whitney U test on entropy: U={stat}, p={p_value}\n')

    stat, p_value = mannwhitneyu(originEntropy, newEntropy, alternative='less')
    f.write(f'Less Mann-Whitney U test on entropy: U={stat}, p={p_value}\n')

    f.write('=================================================================\n')
# print(statistics.mean(originK), ' ', statistics.mean(newK))
# print(statistics.mean(originEntropy), ' ', statistics.mean(newEntropy))
# stat, p_value = mannwhitneyu(originK, newK, alternative='greater')
# print(f'Greater Mann-Whitney U test on K: U={stat}, p={p_value}')

# stat, p_value = mannwhitneyu(originK, newK, alternative='less')
# print(f'Less Mann-Whitney U test on K: U={stat}, p={p_value}')

# stat, p_value = mannwhitneyu(originEntropy, newEntropy, alternative='greater')
# print(f'Greater Mann-Whitney U test on entropy: U={stat}, p={p_value}')

# stat, p_value = mannwhitneyu(originEntropy, newEntropy, alternative='less')
# print(f'Less Mann-Whitney U test on entropy: U={stat}, p={p_value}')
