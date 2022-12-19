<h1 align="center">
  DeepE
</h1>
<h4 align="center">DeepE: a deep neural network for knowledge graph embedding</h4>
<p align="center">
  <a href="https://arxiv.org/pdf/2211.04620"><img src="http://img.shields.io/badge/Paper-PDF-red.svg"></a>
</p>

<h2 align="center">
  <img align="center"  src="./overview.png" alt="...">
</h2>

## Abstract:
Recently, neural network based methods have shown their power in learning more expressive features on the task of knowledge graph em- bedding (KGE). However, the performance of deep methods often falls behind the shallow ones on simple graphs. One possible reason is that deep models are difficult to train, while shallow models might suffice for accurately representing the structure of the simple KGs.
In this paper, we propose a neural network based model, named DeepE, to address the problem, which stacks multiple building block- s to predict the tail entity based on the head en- tity and the relation. Each building block is an addition of a linear and a non-linear function. The stacked building blocks are equivalent to a group of learning functions with different non-linear depth. Hence, DeepE allows deep functions to learn deep features, and shallow functions to learn shallow features. Through extensive experiments, we find DeepE outper- forms other state-of-the-art baseline methods. A major advantage of DeepE is the robustness. DeepE achieves a Mean Rank (MR) score that is 6%, 30%, 65% lower than the best base- line methods on FB15k-237, WN18RR and YAGO3-10. Our design makes it possible to train much deeper networks on KGE, e.g. 40 layers on FB15k-237, and without scarifying precision on simple relations.

## paper:
The code for paper： DeepE: a deep neural network for knowledge graph embedding.
https://arxiv.org/pdf/2211.04620

## Requirements:
To reproduce the results, 
1) install pytorch=1.12.1
2) unzip data.zip to data fold.
3) run sh files in ./scripts, e.g. sh run_WN18RR.sh . 

## Citation:
@article{danhao2022deepe,
  title={DeepE: a deep neural network for knowledge graph embedding},
  author={Danhao, Zhu and Si, Shen and Shujian, Huang and Chang, Yin and Ziqi, Ding},
  journal={arXiv preprint arXiv:2211.04620},
  year={2022}
}

## Contact:
Feel free to contact me with any problems. 229369897@qq.com
