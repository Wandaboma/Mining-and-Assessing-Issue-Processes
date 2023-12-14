## Two sided Mann-Whitney U Test at project level
For comparision between orginal algorithm and our proposed algorithm
1. Null hypotheses H0: The number of clusters (𝐾), and the average overall entropy of the mined processes (H𝑝𝑟𝑜𝑐𝑒𝑠𝑠 ),
as a result of applying the original k-means++ and the proposed clustering algorithm, do
not show significant differences
2. Alternative hypotheses H1: 𝐾 and H𝑝𝑟𝑜𝑐𝑒𝑠𝑠 obtained by the proposed clustering algorithm are significantly different from those obtained by the original k-means++ algorithm

| Repository   |  Number of Clusters(K) p value   | Average Entropy of Mined Processes(Hprocess) p value  |
|-------- |  ------ | ------------------  |
|microsoft/vscode |  0.0005***   |  0.0149*  |
|flutter/flutter  | 0.0002***   | 0.0713 |
|golang/go |  4.3973e-08***  |  0.0089** |
|dotnet/runtime | 7.9303e-10***  |  0.0211* | 
|elastic/kibana | 2.8652e-11***  | 0.0163* |
| rust-lang/rust    |  1.5758e-14***    | 0.0039**    |
| kubernetes/kubernetes   |  1.0908e-17***      |   0.0009***   |
| cockroachdb/cockroach   | 2.5258e-18***     | 0.0010***    |
|  tensorflow/tensorflow  | 2.6707e-20***     | 0.0003***    |
| microsoft/TypeScript   |   3.8301e-25***    | 3.7815e-05***    |
| godotengine/godot   | 1.7002e-31***     | 4.9304e-07***    |
| ansible/ansible    | 7.4779e-33***     | 9.8893e-07***    |
| elastic/elasticsearch   | 6.4543e-34***      | 3.6303e-06***    |
| rancher/rancher   | 1.0211e-35***     |  2.0766e-06***   |
| dotnet/roslyn   | 1.7417e-38***     | 5.6969e-07***    |
|  home-assistant/core  | 4.7316e-39***     | 5.1303e-07***    |
|  dotnet/aspnetcore   | 1.4691e-40***   |  3.0044e-07***  |
|  pytorch/pytorch    |  1.6021e-41***   | 1.5237e-07***    |

*: p < 0.05  **: p < 0.01 ***: p < 0.001
