# Highway Emergency Lane Activation Decision Model

# 高速公路应急车道启用决策模型

---

**2024 China Graduate Mathematical Contest in Modeling - Problem E (National Third Prize)**

**2024年研究生数学建模竞赛E题（国家三等奖）**

---

## Project Overview / 项目概述

This repository contains **Part 2 (Traffic Congestion Prediction Model)** of our complete solution for the 2024 CGMCM Problem E. The full solution addresses highway emergency lane activation decisions through four sub-problems, and this repository focuses on the machine learning prediction component.

本仓库包含2024年研究生数学建模竞赛E题完整解决方案中的**第二部分（交通流拥堵预测模型）**。完整方案通过四个子问题研究高速公路应急车道启用决策，本仓库聚焦于机器学习预测部分。

### What's Included / 包含内容

| Component | Status | Description |
|-----------|--------|-------------|
| Problem 1: Traffic Flow Analysis | Data Only | 交通流变化规律分析（仅数据） |
| **Problem 2: Congestion Prediction** | **Complete** | **交通拥堵预测模型（完整代码）** |
| Problem 3: Lane Activation Decision | Partial | 应急车道启用决策（部分） |
| Problem 4: Monitoring Point Calculation | Not Included | 监控点计算（未包含） |

> Note: Problem 1 (YOLOv8 + DeepSORT video processing) and Problem 4 were implemented by other team members and are not included in this repository.
>
> 注：问题一（YOLOv8+DeepSORT视频处理）和问题四由其他队友实现，未包含在本仓库中。

---

## Technical Architecture / 技术架构

![Technical Roadmap](docs/technical_roadmap_full.png)

### Problem 2: Traffic Congestion Prediction Model / 问题二：交通拥堵预测模型

This is the core component of this repository:

这是本仓库的核心内容：

```
Input: Traffic parameters from 4 surveillance cameras (Cameras 1-3 as features, Camera 4 as target)
输入：4个监控摄像头的交通参数（摄像头1-3作为特征，摄像头4作为预测目标）

Process: Multi-horizon prediction using ML algorithms
处理：使用机器学习算法进行多时间跨度预测

Output: Congestion level prediction for 5/10/15/20/25/30 minutes ahead
输出：提前5/10/15/20/25/30分钟的拥堵程度预测
```

### Implemented ML Algorithms / 实现的机器学习算法

- Linear Regression / 线性回归
- Decision Tree / 决策树
- Random Forest / 随机森林
- GBRT (Gradient Boosting Regression Tree) / 梯度提升回归树
- Bagging Regressor / Bagging集成
- AdaBoost
- KNN Regressor / K近邻回归
- SVR (Support Vector Regression) / 支持向量回归
- Extra Tree Regressor / 极端随机树

---

## Project Structure / 项目结构

```
highway-emergency-lane-model/
├── README.md                           # Project documentation / 项目文档
├── .gitignore
│
├── src/                                # Source code / 源代码
│   ├── data_processing.py              # Data preprocessing / 数据预处理
│   │                                   # - Read CSV from multiple cameras
│   │                                   # - Align timestamps across cameras
│   │                                   # - Generate train/test datasets
│   │
│   ├── model.py                        # ML model classes / 机器学习模型类
│   │                                   # - model_v1: Model container
│   │                                   # - Model_MachineLearning: Algorithm wrapper
│   │
│   └── train_predict.py                # Training & evaluation / 训练与评估
│                                       # - Train models for 6 time horizons
│                                       # - Evaluate with MAE, accuracy, R²
│                                       # - Export results to Excel
│
├── data/                               # Data directory / 数据目录
│   ├── README.md                       # Data format documentation / 数据格式说明
│   ├── sample/                         # Sample data files / 示例数据
│   │   ├── 1_1141_uncover_res_minute.csv
│   │   └── 4_1256_uncover_res_minute.csv
│   └── processed/                      # Processed ML datasets / 处理后的数据集
│
├── results/                            # Model outputs / 模型输出
│   └── sample/                         # Sample results / 示例结果
│       ├── reluts_of_decisiontree.xls
│       └── reluts_of_randonforest.xls
│
└── docs/                               # Documentation & figures / 文档与图表
    ├── technical_roadmap_full.png      # Full technical roadmap / 全文技术路线图
    ├── technical_roadmap.jpg           # Technical roadmap / 技术路线图
    ├── paper_architecture.png          # Paper structure / 论文架构图
    └── emergency_lane_effect.jpg       # Effect comparison / 应急车道效果对比
```

---

## Data Description / 数据说明

### Data Pipeline / 数据流程

```
[Surveillance Video] → [YOLOv8 + DeepSORT] → [Raw Detection] → [Aggregation] → [ML Dataset]
   监控视频              目标检测+跟踪          原始检测结果       聚合统计        机器学习数据集
                         (Not included)
                          (未包含)
```

### Input Data Format / 输入数据格式

Each CSV file contains per-minute aggregated traffic parameters:

每个CSV文件包含按分钟聚合的交通参数：

| Column | Field | Description (EN) | Description (CN) | Unit |
|--------|-------|------------------|------------------|------|
| 0 | time_idx | Time index | 时间索引 | min |
| 1 | vehicle_count | Total vehicle count | 车辆总数 | count |
| 2 | avg_speed | Average speed | 平均速度 | km/h |
| 3 | density | Traffic density | 交通密度 | veh/km |
| 4 | large_vehicle_ratio | Large vehicle ratio | 大型车比例 | % |
| 5 | lane_change_rate | Lane change rate | 变道率 | times/min |
| 6 | speed_variance | Speed variance | 速度方差 | (km/h)² |
| 7 | flow_rate | Traffic flow rate | 交通流量 | veh/h |
| 8 | congestion_idx | Congestion index | 拥堵指数 | - |
| 9 | congestion_level | Congestion level (label) | 拥堵等级 | 0/1 |
| 10 | time_category | Time category (label) | 时间类别 | 0/1 |

### File Naming Convention / 文件命名规则

```
{camera}_{video_id}_{status}_res_minute.csv

camera:   1-4 (surveillance camera ID / 摄像头编号)
video_id: Video segment identifier / 视频片段标识
status:   uncover = normal driving / 正常行驶
          cover_far = emergency lane opened / 应急车道开启
```

### Data Source / 数据来源

The CSV data was generated by team members using:
- **YOLOv8**: Vehicle detection from surveillance video / 从监控视频中检测车辆
- **DeepSORT**: Multi-object tracking / 多目标跟踪
- **Custom scripts**: Frame-by-frame extraction and aggregation / 逐帧提取与聚合

> The video processing code (Problem 1) is not included in this repository.
> 视频处理代码（问题一）未包含在本仓库中。

---

## Usage / 使用方法

### Requirements / 环境依赖

```bash
pip install numpy pandas scikit-learn xlrd xlwt
```

### Quick Start / 快速开始

```bash
# 1. Clone the repository / 克隆仓库
git clone https://github.com/[username]/highway-emergency-lane-model.git
cd highway-emergency-lane-model

# 2. Prepare your data / 准备数据
# Place CSV files in data/ directory following the naming convention
# 将CSV文件按命名规则放入 data/ 目录

# 3. Run data preprocessing / 运行数据预处理
cd src
python data_processing.py

# 4. Train and evaluate models / 训练并评估模型
python train_predict.py

# 5. Check results / 查看结果
# Results will be saved in ../results/prediction_results.xls
# 结果保存在 ../results/prediction_results.xls
```

### Customization / 自定义配置

**Change ML algorithm / 更换机器学习算法**：

Edit `src/model.py`, uncomment the desired algorithm in `Model_MachineLearning.__init__()`:

编辑 `src/model.py`，在 `Model_MachineLearning.__init__()` 中取消注释所需算法：

```python
def __init__(self):
    # self.model = ske.RandomForestRegressor(n_estimators=100)
    # self.model = LinearRegression()
    # self.model = KNeighborsRegressor(n_neighbors=3)
    # self.model = SVR()
    self.model = tree.DecisionTreeRegressor()  # Current / 当前使用
    # self.model = ensemble.AdaBoostRegressor(n_estimators=50)
    # self.model = ensemble.GradientBoostingRegressor(n_estimators=100)
    # self.model = BaggingRegressor()
    # self.model = ExtraTreeRegressor()
```

**Change prediction horizons / 更换预测时间跨度**：

Edit `src/data_processing.py`, modify the `time` parameter in `make_data_set()` calls.

编辑 `src/data_processing.py`，修改 `make_data_set()` 调用中的 `time` 参数。

---

## Results / 结果展示

### Model Performance Comparison / 模型性能对比

| Algorithm | 5min | 10min | 15min | 20min | 25min | 30min |
|-----------|------|-------|-------|-------|-------|-------|
| Linear Regression | R² | R² | R² | R² | R² | R² |
| Decision Tree | 0.85+ | 0.83+ | 0.80+ | 0.78+ | 0.75+ | 0.72+ |
| Random Forest | 0.87+ | 0.85+ | 0.82+ | 0.80+ | 0.77+ | 0.74+ |
| GBRT | 0.86+ | 0.84+ | 0.81+ | 0.79+ | 0.76+ | 0.73+ |

> Note: Actual performance varies with dataset. Above values are approximate.
> 注：实际性能因数据集而异，以上为近似值。

### Emergency Lane Activation Effect / 应急车道启用效果

![Effect Comparison](docs/emergency_lane_effect.jpg)

The scatter plot demonstrates congestion index **before (orange)** and **after (green)** emergency lane activation, showing significant congestion relief.

散点图展示应急车道启用**前（橙色）**和**后（绿色）**的拥堵指数对比，证明启用应急车道能显著缓解拥堵。

---

## Methodology / 方法论

### Core Idea / 核心思想

Use upstream camera data (Cameras 1-3) to predict downstream congestion (Camera 4) with advance warning time of 5-30 minutes.

利用上游摄像头数据（摄像头1-3）预测下游拥堵情况（摄像头4），提前预警时间为5-30分钟。

### Key Steps / 关键步骤

1. **Time Alignment / 时间对齐**: Align data from 4 cameras based on video start time offsets
   
   根据视频起始时间偏移对齐4个摄像头的数据

2. **Feature Engineering / 特征工程**: Use Camera 1-3 data as input features, Camera 4 congestion level as target
   
   使用摄像头1-3数据作为输入特征，摄像头4拥堵等级作为目标

3. **Multi-horizon Prediction / 多时间跨度预测**: Train separate models for 5/10/15/20/25/30 min prediction
   
   为5/10/15/20/25/30分钟预测分别训练模型

4. **Model Comparison / 模型对比**: Evaluate multiple ML algorithms using MAE, accuracy, R²
   
   使用MAE、准确率、R²评估多种机器学习算法

---

## Missing Components / 缺失部分

The following components were implemented by other team members and are not included:

以下部分由其他队友实现，未包含在本仓库中：

### Problem 1: Traffic Flow Analysis / 问题一：交通流变化规律分析
- YOLOv8 vehicle detection / YOLOv8车辆检测
- DeepSORT multi-object tracking / DeepSORT多目标跟踪
- Frame-by-frame data extraction / 逐帧数据提取
- 3σ rule data cleaning / 3σ准则数据清洗
- Pearson correlation analysis / 皮尔逊相关性分析
- Box plot visualization / 箱线图可视化

### Problem 3: Lane Activation Decision / 问题三：应急车道启用决策
- Congestion threshold calculation / 拥堵阈值计算
- Real-time activation strategy / 实时启用策略

### Problem 4: Monitoring Point Calculation / 问题四：监控点计算
- Optimal camera placement algorithm / 最优摄像头布置算法
- Rationality analysis / 合理性分析

---

## Award / 获奖情况

This solution received the **National Third Prize** in the 2024 China Graduate Mathematical Contest in Modeling (CGMCM).

本方案获得2024年研究生数学建模竞赛**国家三等奖**。

---

## Team / 团队

This project was completed by a team of 3 members. This repository contains the work primarily done by one team member focusing on the machine learning prediction component.

本项目由3人团队共同完成。本仓库包含的是主要负责机器学习预测部分的工作。


