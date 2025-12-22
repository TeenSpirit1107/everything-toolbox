# Rosalind's Misc Toolbox

**Language / 语言:**

- [English](README.md) &nbsp; | &nbsp; [中文 Chinese](README_CN.md)

## ☺️ Introduction

- This toolbox is originally designed for my personal use. It contains a miscellaneous collection of tools, including system cleaning, media handling, console effects, and calculating utilities. Not focused on a specific topic.

- I use it on Ubuntu 22.04 and 24.04 , but most tools (except `.sh`) probably work on other systems as well.

## 🧠 Utilities

### Calculator Tools (`calc/`)

#### `calc/curriculum_planning.py`

- **Curriculum Planning Calendar**: Interactive tool for planning course schedules.
- **Schedule Conflict Detection**: Finds all valid course schedules where no time slots conflict.
- **Required/Optional Courses**: Supports both required and optional courses with flexible tutorial selection.
- **Calendar Visualization**: Displays weekly calendars (DAY 1-5) with 7 time slots per day, showing course schedules in ASCII format.

#### `calc/grade_percentile.py`

- **Grade Percentile Calculator**: Computes percentile rank for scores in a truncated normal distribution.
- **Visualization**: Plots the distribution with 5-point bins and marks the user's score position.
- **Customizable Parameters**: Supports custom mean, standard deviation, score, and bounds.

#### `calc/machine_learning.py`

- **Entropy Calculator**: Interactively computes binary entropy for probability values.
- **Partition Entropy**: Computes weighted entropy across partitions (e.g., for decision trees).
- **Cross Entropy Loss**: Implements cross-entropy loss for model evaluation.

### Media Tools (`media/`)

#### `media/pdf_handling.py`

- **Merge PDFs**: Guides the user through selecting PDFs from the `input/` directory and merges them into a single file in the `output/` directory.
- **Interactive Selection**: Allows users to select multiple PDFs interactively and merge them in order.

### Console Tools (`console/`)

#### `console/console_effect.py`

- **Typing Simulation**: Creates either word-wise or character-wise typewriter-style output with adjustable speed—ideal for CLI storytelling or dramatic logging.

#### `console/scr.sh`

- **Script Logger**: Records terminal sessions using the `script` command.
- **Timestamped Logs**: Saves logs with timestamps and optional comments to `~/logging/` directory.
- **Automatic Naming**: Generates filenames in format `MMdd_HHmm_comment.log`.

### System Tools (`sys/`)

#### `sys/clean.sh`

- **System Cleanup**: Interactive system clean-up script for **Ubuntu 22.04**. Can choose to clean:
  - User cache (`~/.cache/*`)
  - System logs older than 7 days
  - APT cache and unnecessary packages
  - Conda cache and unnecessary packages
- **Space Reporting**: Shows how much space was saved by each cleanup operation.

#### `sys/ssh_host.sh`

- **SSH Host Setup**: Configures SSH server on Ubuntu systems.
- **Firewall Configuration**: Sets up UFW firewall rules for SSH access.
- **Secure Mode**: Optional IP-based access restriction for enhanced security.
- **Service Management**: Enables and starts SSH service automatically.

---

## 🚀 Getting Started

1. Install the dependencies:

    ```shell
    pip install -r requirements.txt
    ```

2. Some bash files need to be run as root:

    ```shell
    sudo ./file_name.sh
    ```

## 📋 Requirements

- Python 3.x
- See `requirements.txt` for Python dependencies:
  - PyPDF2
  - scipy
  - matplotlib

## 👤 Author

**Yimeng (Rosalind)**

- GitHub: [@TeenSpirit1107](https://github.com/TeenSpirit1107)
- Email: yimengteng@link.cuhk.edu.cn
