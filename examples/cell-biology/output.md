# SYNTHETIC：膜蛋白荧光漂白后恢复（FRAP）

本材料为合成教学示例。按给定公式实际计算：恢复比例（%）= 100 ×（观测平台强度 − 漂白后即刻强度）/（漂白前强度 − 漂白后即刻强度）。例如，R1 WT = 100 × (0.8 − 0.2)/(1.0 − 0.2) = 75.0%。

| 培养批次 | WT恢复比例（%） | Mut恢复比例（%） | 配对变化 Mut−WT（百分点） |
|---|---:|---:|---:|
| R1 | 75.0 | 50.0 | -25.0 |
| R2 | 62.5 | 37.5 | -25.0 |
| R3 | 87.5 | 62.5 | -25.0 |
| 均值 | 75.0 | 50.0 | -25.0 |
| 样本SD | 12.5 | 12.5 | 0.0 |

WT为75.0%（样本SD 12.5个百分点），Mut为50.0%（样本SD 12.5个百分点）；先按培养批次求Mut−WT，再汇总，配对变化均值为−25.0个百分点，样本SD为0.0个百分点。SD使用分母n−1=2。三个差值完全相同，因此差值SD为零；它只反映这组三次培养汇总值的离散度。

独立n=3次培养，每个构建各有3个培养层面的值，配对比较有3对。每行是同一培养来源下该构建3个细胞的已校正平均强度；这些细胞属于培养内观测，不能作为9个独立重复。这里先对所给平均强度应用公式，不把结果称作由原始轨迹计算的单细胞恢复比例均值。

## English Results（74词，按空白分词计）

SYNTHETIC: The membrane protein mutant showed lower recovery than WT across three paired independent cultures. Recovery was 75.0 ± 12.5% for WT and 50.0 ± 12.5% for Mut (mean ± sample SD). The paired Mut−WT change was −25.0 ± 0.0 percentage points (n = 3 culture pairs). Each construct value summarized three cells within a culture. These descriptive estimates apply to the supplied corrected intensity summaries and observation window; complete recovery trajectories were unavailable.

## 中文课题申请研究依据（约150字）

SYNTHETIC：三次独立培养的配对汇总显示，Mut恢复比例均较WT低25.0个百分点，为追踪突变体恢复差异提供初步依据。现有观测窗口内的汇总值尚不能区分恢复较慢与最终恢复水平较低。后续拟在同批配对培养中采集完整单细胞时间轨迹并延长观测，检验Mut与WT的差距是否随时间缩小，以区分这两种解释。


本页保留本轮实际答复的科研正文；完整代码、计算表和资源回执由维护者随交付保存。此合成例子展示目录外任务的处理，不代表所有生物方法均已实测。
