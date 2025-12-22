# Everything Toolbox 使用手册

**Language / 语言:**

- [English](README.md) &nbsp; | &nbsp; [中文 Chinese](README_CN.md)

## ☺️ 简介

- 本工具箱包含多种工具，包括系统清理、媒体处理、控制台特效和计算实用程序，功能杂项齐全。

- 这些代码最初是为我个人使用而编写。我在 Ubuntu 22.04 和 24.04 上使用，但除 `.sh` 脚本外，大多数工具也应该适用于其他系统。如果你希望支持其他操作系统（如 Windows），欢迎通过 ISSUE 反馈。

## 🧠 工具

### 计算工具 (`calc/`)

#### `calc/curriculum_planning.py`

- **课程规划日历**：用于规划课程表的交互式工具。
- **时间冲突检测**：查找所有没有时间冲突的有效课程安排。
- **必修/选修课程**：支持必修和选修课程，具有灵活的教程选择。
- **日历可视化**：以 ASCII 格式显示每周日历（DAY 1-5），每天有 7 个时间段，显示课程安排。

#### `calc/grade_percentile.py`

- **成绩百分位计算器**：计算截断正态分布中分数的百分位排名。
- **可视化**：绘制分布图，使用 5 分区间并标记用户的分数位置。
- **可自定义参数**：支持自定义均值、标准差、分数和边界。

#### `calc/machine_learning.py`

- **熵计算器**：交互式计算概率值的二进制熵。
- **分区熵**：计算跨分区的加权熵（例如，用于决策树）。
- **交叉熵损失**：实现用于模型评估的交叉熵损失。

### 媒体工具 (`media/`)

#### `media/pdf_handling.py`

- **合并 PDF**：引导用户从 `input/` 目录中选择 PDF 文件，并将它们合并到 `output/` 目录中的单个文件。
- **交互式选择**：允许用户交互式选择多个 PDF 并按顺序合并它们。

### 控制台工具 (`console/`)

#### `console/console_effect.py`

- **打字效果**：创建逐词或逐字符的打字机风格输出，速度可调——非常适合 CLI 故事叙述或戏剧性日志记录。

#### `console/scr.sh`

- **脚本记录器**：使用 `script` 命令记录终端会话。
- **带时间戳的日志**：将带时间戳和可选注释的日志保存到 `~/logging/` 目录。
- **自动命名**：生成格式为 `MMdd_HHmm_comment.log` 的文件名。

### 系统工具 (`sys/`)

#### `sys/clean.sh`

- **系统清理**：适用于 **Ubuntu 22.04** 的交互式系统清理脚本。可以选择清理：
  - 用户缓存 (`~/.cache/*`)
  - 超过 7 天的系统日志
  - APT 缓存和不必要的包
  - Conda 缓存和不必要的包
- **空间报告**：显示每次清理操作节省了多少空间。

#### `sys/ssh_host.sh`

- **SSH 主机设置**：在 Ubuntu 系统上配置 SSH 服务器。
- **防火墙配置**：为 SSH 访问设置 UFW 防火墙规则。
- **安全模式**：可选的基于 IP 的访问限制，以增强安全性。
- **服务管理**：自动启用并启动 SSH 服务。

---

## 🚀 开始使用

1. 安装依赖项：

    ```shell
    pip install -r requirements.txt
    ```

2. 某些 bash 文件需要以 root 权限运行：

    ```shell
    sudo ./file_name.sh
    ```

## 📋 要求

- Python 3.x
- 查看 `requirements.txt` 了解 Python 依赖项：
  - PyPDF2
  - scipy
  - matplotlib

## 👤 作者

**Yimeng (Rosalind)**

- GitHub: [@TeenSpirit1107](https://github.com/TeenSpirit1107)
- 邮箱: yimengteng@link.cuhk.edu.cn

