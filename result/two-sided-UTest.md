## two sided Mann-Whitney U Test for comparision between orginal algorithm and our proposed algorithm
1. Null hypotheses H0: The number of clusters (𝐾), and the average overall entropy of the mined processes (H𝑝𝑟𝑜𝑐𝑒𝑠𝑠 ),
as a result of applying the original k-means++ and the proposed clustering algorithm, do
not show significant differences
2. Alternative hypotheses H1: 𝐾 and H𝑝𝑟𝑜𝑐𝑒𝑠𝑠 obtained by the proposed clustering algorithm are significantly different from those obtained by the original k-means++ algorithm
|    |  Number of Clusters(K) p value   | Average Entropy of Mined Processes(Hprocess) p value  |
|---- |  ----  | ----  |
|0.3 |  7.0118e-14***  |  0.0078**  |
|0.4 | 1.6021e-41***   | 1.5237e-07*** |
|0.5 | 2.6726e-122***  | 5.8096e-19*** |
|0.6 | 7.8438e-148***  | 2.9364e-23*** | 
|0.7 | 9.3531e-157***  | 2.5379e-25*** |
*: p < 0.05  **: p < 0.01 ***: p < 0.001
