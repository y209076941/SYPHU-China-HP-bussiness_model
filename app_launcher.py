# app_launcher_fixed.py
import os
import sys
import subprocess
import webbrowser
import threading
import time
from pathlib import Path


def check_dependencies():
    """检查必要的依赖"""
    required_packages = ['streamlit', 'plotly', 'pandas', 'yfinance']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    return missing_packages


def fix_paths():
    """修复路径问题"""
    if getattr(sys, 'frozen', False):
        # 如果是打包版本
        base_path = sys._MEIPASS
    else:
        # 如果是开发版本
        base_path = os.path.dirname(os.path.abspath(__file__))

    # 添加必要的路径
    if base_path not in sys.path:
        sys.path.insert(0, base_path)

    return base_path


def start_streamlit():
    """启动Streamlit应用"""
    base_path = fix_paths()

    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"缺少必要的依赖包: {missing}")
        print("请安装缺少的包: pip install " + " ".join(missing))
        input("按回车键退出...")
        return

    # 设置环境变量
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

    # 构建命令
    app_path = os.path.join(base_path, 'app.py')
    if not os.path.exists(app_path):
        # 如果app.py不在当前目录，尝试在父目录查找
        app_path = 'app.py'

    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        app_path,
        '--server.port', '8501',
        '--server.address', 'localhost',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false'
    ]

    try:
        print("正在启动 Liver Cancer Drug Intelligence Platform...")
        print(f"应用将在 http://localhost:8501 启动")
        print("如果浏览器没有自动打开，请手动访问上述地址")
        print("按 Ctrl+C 停止应用")

        # 启动Streamlit
        subprocess.run(cmd)

    except Exception as e:
        print(f"启动失败: {e}")
        print("请确保已安装所有必要的依赖包")
        input("按回车键退出...")


if __name__ == "__main__":
    start_streamlit()