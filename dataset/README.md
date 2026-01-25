# descripción del conjunto de datos

Este directorio se utiliza para almacenar los datos de entrenamiento y de prueba.


## estructura de directorios

‘’‘
dataset/
├── raw/                    # datos de vídeo originales

│   ├── squat/             # 深蹲动作
│   │   ├── correct/       # 正确动作
│   │   └── incorrect/     # 错误动作
│   └── pushup/            # 俯卧撑动作
│       ├── correct/       # 正确动作
│       └── incorrect/     # 错误动作
├── processed/             # 处理后的特征数据
├── train.csv              # 训练集
├── test.csv               # 测试集
└── README.md              # 本文件
```

## 数据采集指南

### 1. 使用数据采集工具

```bash
cd python
python data_collector.py
```

### 2. 采集要求

#### 深蹲 (Squat)
**正确动作**:
- 双脚与肩同宽
- 膝盖不超过脚尖
- 背部挺直
- 下蹲至大腿与地面平行

**常见错误**:
- 膝盖内扣 (knee_valgus)
- 下蹲不足 (insufficient_depth)
- 重心前倾 (forward_lean)

#### 俯卧撑 (Pushup)
**正确动作**:
- 身体保持一条直线
- 手臂打开略宽于肩
- 下降至肘部90度
- 保持核心收紧

**常见错误**:
- 塌腰 (sagging_back)
- 臀部过高 (high_hips)
- 手臂角度错误 (wrong_arm_angle)

### 3. 采集建议

**数量要求**:
- 每种动作至少30个正确样本
- 每种错误类型至少20个样本
- 总目标：400个样本

**质量要求**:
- 确保全身在摄像头视野内
- 光线充足，避免背光
- 背景简洁，减少干扰
- 多角度采集（正面、侧面）
- 多人采集（不同体型）

**标注规范**:
- 准确标记动作类型
- 明确标注正确/错误
- 详细记录错误类型
- 保存原始视频和特征数据

## 数据格式

### 原始数据
每个采集会话生成：
- `.mp4` - 原始视频文件
- `_features.json` - 提取的特征数据

### 处理后数据
CSV文件格式：
```csv
angle_knee_avg,angle_hip_avg,shoulder_width,trunk_length,...,label
120.5,85.3,0.15,0.25,...,squat_correct
95.2,110.5,0.16,0.24,...,squat_knee_valgus
...
```

## 特征说明

### 几何特征
- 关节角度（膝、髋、肘、肩）
- 身体比例（肩宽、髋宽、躯干长度）
- 肢体长度比例

### 运动特征
- 角速度、加速度
- 动作周期
- 运动平滑度

### 时序特征
- 角度变化范围
- 速度均值和标准差
- 加速度特征

## 数据预处理

运行特征提取脚本：

```bash
python python/feature_extractor.py \
    --input dataset/raw \
    --output dataset/processed \
    --normalize
```

## 数据增强

可选的数据增强方法：
1. 镜像翻转（左右对称）
2. 速度变化（0.8x - 1.2x）
3. 轻微旋转（±5度）

## 注意事项

- ⚠️ 原始视频文件较大，不要提交到Git
- ✅ 提交处理后的特征CSV文件
- ✅ 保持标注的一致性
- ✅ 定期备份数据

## 当前状态

- [ ] 深蹲正确动作: 0/30
- [ ] 深蹲膝盖内扣: 0/20
- [ ] 深蹲下蹲不足: 0/20
- [ ] 深蹲重心前倾: 0/20
- [ ] 俯卧撑正确动作: 0/30
- [ ] 俯卧撑塌腰: 0/20
- [ ] 俯卧撑臀部过高: 0/20
- [ ] 俯卧撑手臂角度错误: 0/20

**总进度**: 0/180 (0%)

---

更新日期: 2025-12-26

