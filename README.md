Spatiotemporal Dynamics & Defense Baseline of ALB in TNSP
基于贝叶斯时空变系数模型（BSTVC）的“三北”防护林光肩星天牛灾害驱动机制与系统防御底线研究

R
INLA
License: MIT

📖 项目简介 (Overview)
本项目是针对大尺度林业病虫害（光肩星天牛，ALB）时空演化机制的开源分析代码库。研究区域覆盖中国“三北”防护林体系（TNSP）的核心区（共 929 个县域）。

传统研究多局限于静态截面分析，本项目引入了前沿的贝叶斯时空变系数模型（Bayesian Spatiotemporal Varying Coefficients Model, BSTVC），精准剥离了时空混杂效应，量化了气候约束、寄主资源与人为社会因子在不同空间单元上的“时空非平稳性”（Non-stationarity）。

基于本代码的输出结果，我们提出了区域生态安全的**“系统防御底线”（Systematic Defense Baseline）**理论，为“三北”六期工程的三大标志性战役提供了从“大水漫灌”向“分区靶向”转变的精准防控策略。

✨ 核心亮点 (Key Features)
时空非平稳性建模：利用 R-INLA 算法高效处理大尺度长时序（2003-2018）的面板数据。
机制进化/转换探测：突破全局唯一系数的局限，输出 929 个县域各自独立的局部回归系数（Varying Coefficients）。
STVPI 贡献度量化：通过时空方差划分指数（STVPI），直观展示不同驱动因子的重要性排序。
GIS 完美衔接：内置拓扑修复（st_make_valid）与多边形强制转换（st_cast），一键导出符合 ArcGIS 规范的 Shapefile。
🛠️ 环境依赖 (Prerequisites)
运行本仓库代码，您需要安装 R 环境（建议 >= 4.1.0）及以下核心包：

# 基础数据处理与可视化
install.packages(c("tidyverse", "ggplot2", "ggthemes", "ggbeeswarm", "forestplot"))

# GIS 与空间数据处理
install.packages(c("sf", "lwgeom"))

# 核心贝叶斯模型依赖包 (INLA 需通过其官方库安装)
install.packages("INLA",repos=c(getOption("repos"),INLA="https://inla.r-inla-download.org/R/stable"), dep=TRUE)

# BSTVC (请根据原作者提供的渠道安装)
# install.packages("BSTVC") 
📁 数据准备 (Data Preparation)
代码运行需要两部分核心数据（请放置于您的本地路径或项目中）：

空间底图数据 (.shp)：包含 PAC（县域行政代码）多边形矢量文件。
面板数据集 (.csv)：需包含长格式（Long-format）的面板数据。
PAC: 空间单元 ID
Year: 时间标识（如 2003-2018）
PDI: 潜在破坏指数（连续变量）
X2...X13: 驱动因子（如降水、日照、路网密度等）
🚀 代码执行流程 (Pipeline Usage)
本仓库提供的 main.R 脚本包含了完整的分析流，主要分为四个模块：

1. 空间拓扑修复与坐标系统一
自动检测并修复复杂的县域边界自相交等拓扑错误，统一投影至 WGS84 (EPSG:4326)，防止空间权重矩阵计算报错。

map <- st_make_valid(map)
map <- st_transform(map, "EPSG:4326")
2. 数据标准化与模型拟合 (Model Fitting)
利用 Z-score 标准化消除量纲差异。运用 ifelse 构建二分类定殖变量 (occurrence)，并通过 6 线程并行运算拟合贝叶斯时空二项分布模型：

model_occ <- BSTVC(
  formula = occurrence ~ ST(X2+X3+X7+X10+X11+X12+X13),
  data = data, study_map = map, Time = "Year", Space = "PAC",
  response_type = "binary", threads = 6
)
3. 时空贡献度 (STVPI) 森林图绘制
提取模型后验评价指标（WAIC/DIC），并利用 ggplot2 绘制具有高度可读性的 STVPI 时空方差划分指数图，直观定位核心控制变量（如日照 X3）。

4. 局部空间变系数提取与 GIS 导出
提取 929 个县域特异性的回归系数（均值），融合几何信息，并通过类型强制转换安全导出为 Shapefile，供进一步在 ArcGIS/QGIS 中进行符号化渲染。

st_write(Space.Coef.Map_Clean, "Space_Coefficients_Fixed.shp", driver = "ESRI Shapefile")
📊 预期结果 (Expected Outputs)
运行成功后，您将在指定目录获得以下文件：

results of model evaluation_occ.csv: 贝叶斯模型拟合优度评价指标。
STVPI 森林图 (Plots): 展示各环境变量对灾害格局的相对解释率。
Space_Coefficients_Fixed.shp: 包含各县域局部回归系数的地理空间数据，可直接用于绘制机制空间异质性分布图。
📜 引用说明 (Citation)
如果您在研究中使用了本代码或受到“系统防御底线”理论的启发，请引用我们的论文：

[作者姓名], [导师姓名]. (202X). "三北"工程区光肩星天牛灾害的时空演化机制与系统防御底线研究. [期刊名称/学位授予单位].

[Author Names]. (202X). Spatiotemporal Driving Mechanisms and Systematic Defense Baseline of Anoplophora glabripennis in the “Three-North” Region using BSTVC. [Journal/University].

✉️ 联系方式 (Contact)
如有关于代码运行或数据获取的疑问，欢迎提交 Issue 或通过邮件联系：

Author: [您的名字]
Email: [您的邮箱@domain.com]
Institution: [您的学校/研究机构名称]
