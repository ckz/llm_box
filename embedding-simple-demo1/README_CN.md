# 文本嵌入简单演示

本项目展示了使用Sentence Transformers库进行文本嵌入的基本用法,以及各种文本相似度分析和可视化技术。

## 什么是文本嵌入?

文本嵌入是捕捉语义含义的文本数值表示。它们将单词或文本片段转换为高维向量,其中语义相似的文本在向量空间中的位置更接近。这使得以下操作成为可能:
- 比较不同文本之间的相似度
- 查找相关内容
- 按主题组织文本
- 构建语义搜索系统

## 实现细节

该演示实现了以下主要功能:

1. **基本文本嵌入**
   - 使用Sentence Transformers的'all-MiniLM-L6-v2'模型
   - 将示例文本转换为向量表示
   - 演示多个文本的批处理

2. **自定义嵌入层**
   - 实现基于PyTorch的自定义嵌入层
   - 展示如何从头开始创建嵌入
   - 演示批量输入序列的处理

3. **向量相似度搜索**
   - 使用FAISS进行高效的相似度搜索
   - 实现k近邻搜索
   - 返回最相似的文本及其距离

4. **余弦相似度矩阵**
   - 计算所有文本嵌入之间的成对相似度
   - 使用scikit-learn的余弦相似度函数
   - 帮助可视化文本之间的关系

5. **嵌入可视化**
   - 使用t-SNE将高维嵌入降至2D
   - 创建文本关系的散点图
   - 针对小数据集优化perplexity参数
   - 添加文本标签便于解释

## 环境要求

项目需要以下Python包:
```
numpy>=1.24.0
sentence-transformers>=2.2.2
faiss-cpu>=1.7.4
scikit-learn>=1.3.0
torch>=2.0.0
matplotlib>=3.7.0
```

## 安装

1. 克隆仓库并进入项目目录

2. 使用requirements.txt文件安装所需依赖:
```bash
pip install -r requirements.txt
```

## 使用方法

运行演示:
```bash
python embedding_demo.py
```

脚本将:
- 为示例文本生成嵌入
- 演示自定义嵌入层功能
- 执行相似度搜索查询
- 计算相似度矩阵
- 创建嵌入的可视化

## 代码结构

- `basic_embeddings()`:生成示例文本的嵌入
- `SimpleEmbedding`:自定义PyTorch嵌入层类
- `demonstrate_custom_embedding()`:展示自定义嵌入用法
- `vector_similarity_search()`:实现基于FAISS的相似度搜索
- `compute_similarity_matrix()`:创建成对相似度矩阵
- `visualize_embeddings()`:使用优化的t-SNE参数创建嵌入的2D可视化

## 示例输出

该演示包含关于机器学习和天气的示例文本,展示了嵌入空间如何捕捉语义关系。可视化将显示相似概念聚集在一起,而不相关主题则相距较远。t-SNE可视化通过适当的perplexity设置针对小数据集进行了优化。

## 学习要点

1. 理解文本嵌入如何捕捉语义含义
2. 了解不同的相似度度量(L2距离、余弦相似度)
3. 探索使用FAISS进行高效的相似度搜索
4. 使用合适参数的t-SNE在2D空间中可视化高维数据
5. 使用PyTorch实现自定义嵌入层