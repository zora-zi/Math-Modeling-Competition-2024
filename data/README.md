# Data Directory / 数据目录

## Directory Structure / 目录结构

```
data/
├── sample/           # Sample data files / 示例数据文件
│   └── *.csv         # Traffic monitoring data / 交通监控数据
└── processed/        # Processed datasets / 处理后的数据集
    └── data_sets.pkl # ML-ready datasets / 机器学习数据集
```

## Data Format / 数据格式

### Input CSV Files / 输入CSV文件

Each CSV file contains traffic parameters extracted from surveillance video analysis:

每个CSV文件包含从监控视频分析中提取的交通参数：

| Column | Description (EN) | Description (CN) | Unit |
|--------|------------------|------------------|------|
| 0 | Time index | 时间索引 | minutes / 分钟 |
| 1 | Vehicle count | 车辆数量 | count / 辆 |
| 2 | Average speed | 平均速度 | km/h |
| 3 | Traffic density | 交通密度 | vehicles/km |
| 4 | Large vehicle ratio | 大型车辆比例 | % |
| 5 | Lane change rate | 变道率 | times/min |
| 6 | Speed variance | 速度方差 | (km/h)² |
| 7 | Traffic flow rate | 交通流量 | vehicles/h |
| 8 | Congestion index | 拥堵指数 | - |
| 9 | Congestion level | 拥堵等级 | 0/1 |
| 10 | Time category | 时间类别 | 0/1 |

### File Naming Convention / 文件命名规则

Format: `{camera_id}_{video_id}_{status}_res_minute.csv`

格式：`{摄像头编号}_{视频编号}_{状态}_res_minute.csv`

- `camera_id`: Camera number (1-4) / 摄像头编号（1-4）
- `video_id`: Video segment ID / 视频片段ID
- `status`: `uncover` (normal) or `cover_far` (emergency lane open) / `uncover`（正常）或 `cover_far`（应急车道开启）

## Data Source / 数据来源

The original data was extracted from highway surveillance videos using:
- YOLOv8 for vehicle detection / YOLOv8用于车辆检测
- DeepSORT for vehicle tracking / DeepSORT用于车辆跟踪

原始数据通过以下工具从高速公路监控视频中提取：
- YOLOv8 进行车辆检测
- DeepSORT 进行车辆跟踪

## Note / 注意

Due to data privacy and competition regulations, only sample data is provided.
Full dataset is not included in this repository.

由于数据隐私和竞赛规定，仅提供示例数据。
完整数据集未包含在此仓库中。
