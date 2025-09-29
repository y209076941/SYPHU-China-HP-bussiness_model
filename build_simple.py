import os
import subprocess
import sys
import shutil
import datetime


def main():
    print("🧬 开始打包 Liver Cancer Drug Intelligence Platform")
    print("=" * 60)

    # 检查文件
    if not os.path.exists("app.py"):
        print("❌ 错误：未找到app.py")
        print("💡 请先将主文件重命名为app.py")
        return

    if not os.path.exists("app_launcher.py"):
        print("❌ 错误：未找到app_launcher.py")
        return

    # 创建专门的发布文件夹
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    release_folder = f"LiverCancerPlatform_Release_{timestamp}"

    if not os.path.exists(release_folder):
        os.makedirs(release_folder)

    print(f"📁 创建发布文件夹: {release_folder}")

    # 安装pyinstaller
    print("📦 安装PyInstaller...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 使用pyinstaller打包
    print("🛠️ 开始打包...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=LiverCancerDrugPlatform",
        "--add-data=app.py;.",
        "--hidden-import=streamlit",
        "--hidden-import=plotly",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=yfinance",
        "--hidden-import=requests",
        "app_launcher.py"
    ]
    subprocess.call(cmd)

    # 复制所有必要文件到发布文件夹
    print("📄 复制文件到发布文件夹...")

    # 复制可执行文件
    if os.path.exists("dist/LiverCancerDrugPlatform.exe"):
        shutil.copy2("dist/LiverCancerDrugPlatform.exe", release_folder)
        print("✅ 已复制可执行文件")
    else:
        print("❌ 未找到生成的可执行文件")
        return

    # 复制主应用文件
    shutil.copy2("app.py", release_folder)
    print("✅ 已复制app.py")

    # 复制启动器文件
    shutil.copy2("app_launcher.py", release_folder)
    print("✅ 已复制app_launcher.py")

    # 创建说明文件
    readme_content = """# 🧬 Liver Cancer Drug Intelligence Platform

## 肝癌药物智能分析平台

### 使用说明

1. **直接运行** (推荐):
   - 双击运行 `LiverCancerDrugPlatform.exe`
   - 等待应用启动 (约10-30秒)
   - 浏览器会自动打开并显示应用界面

2. **手动运行**:
   - 确保已安装Python和依赖包
   - 运行: `python app_launcher.py`

### 系统要求
- Windows 7/10/11
- 4GB 内存
- 100MB 可用空间
- 网络连接

### 注意事项
- 首次启动可能需要较长时间
- 确保端口8501未被占用
- 部分功能需要网络连接

### 技术支持
如遇问题，请检查:
1. 防火墙设置
2. 网络连接
3. 查看控制台错误信息
"""

    with open(os.path.join(release_folder, "README.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ 已创建说明文件")

    # 创建启动批处理文件
    bat_content = """@echo off
chcp 65001
echo ========================================
echo 🧬 Liver Cancer Drug Intelligence Platform
echo 📊 肝癌药物智能分析平台
echo ========================================
echo.
echo 正在启动应用...
echo.
LiverCancerDrugPlatform.exe
pause
"""

    with open(os.path.join(release_folder, "启动应用.bat"), "w", encoding="utf-8") as f:
        f.write(bat_content)
    print("✅ 已创建启动批处理文件")

    print("=" * 60)
    print("🎉 打包完成！")
    print(f"📁 所有文件已整理到: {release_folder} 文件夹")
    print("")
    print("🚀 启动方式:")
    print("   1. 双击 '启动应用.bat'")
    print("   2. 或直接双击 'LiverCancerDrugPlatform.exe'")
    print("")
    print("💡 您可以将整个文件夹复制到任何位置使用")


if __name__ == "__main__":
    main()