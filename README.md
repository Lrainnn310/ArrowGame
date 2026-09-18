# Arrow Game

这是一个使用 Python 和 Pygame 开发的“一箭又一箭”风格小游戏，作为软件工程课程第二次作业项目。

## 当前功能

- Start Screen 和 Start Game
- 6×6 网格棋盘与上、下、左、右四方向箭头
- 鼠标点击箭头
- 四方向路径阻挡检测
- 无阻挡箭头的非阻塞飞出动画
- 被阻挡箭头的红色碰撞反馈
- 每关 3 次错误机会
- PLAYING、PASSED、FAILED 状态
- 3 个可通关关卡
- Next Level、Restart 和 Restart Game
- Python `unittest` 自动测试

## 环境要求

- Python 3.13 或兼容版本
- Pygame 2.6.1

## 安装依赖

```powershell
python -m pip install -r requirements.txt
```

## 运行游戏

```powershell
python main.py
```

## 运行测试

```powershell
python -m unittest discover -s tests -v
```

## 项目文件

- `main.py`：Pygame 主循环、界面状态、输入和动画
- `board.py`：棋盘绘制、箭头绘制和三个关卡数据
- `models.py`：方向、箭头、飞行动画和游戏状态数据结构
- `path_detection.py`：箭头路径检测算法
- `game_logic.py`：点击、移除和错误次数逻辑
- `state_logic.py`：通关、失败、关卡切换和重启逻辑
- `tests/`：路径、点击、状态和关卡测试

## 开发记录

项目采用分阶段开发方式。每个阶段记录实现内容、测试结果和后续计划，便于编写课程 README、测试报告、PSP 表格和开发博客。
