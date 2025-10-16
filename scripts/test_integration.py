#!/usr/bin/env python3
"""
语音唤醒提示音集成测试
模拟完整的语音唤醒流程
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.plugins.wake_word import WakeWordPlugin
from src.utils.config_manager import ConfigManager

class MockApp:
    """模拟Application类"""
    def __init__(self):
        self.device_state = "IDLE"
        self.running = True
        
    def spawn(self, coro, name):
        """模拟spawn方法"""
        print(f"启动任务: {name}")
        # 创建任务并立即运行
        return asyncio.create_task(coro)
    
    def is_speaking(self):
        return self.device_state == "SPEAKING"
    
    async def abort_speaking(self, reason):
        print(f"中止语音输出: {reason}")
        self.device_state = "LISTENING"
    
    async def start_auto_conversation(self):
        print("开始自动对话")
        self.device_state = "LISTENING"

async def test_integration():
    """集成测试主函数"""
    print("=" * 60)
    print("语音唤醒提示音集成测试")
    print("=" * 60)
    
    # 创建模拟应用
    app = MockApp()
    
    # 创建插件实例
    plugin = WakeWordPlugin()
    
    # 设置插件
    await plugin.setup(app)
    
    print(f"\n配置信息:")
    print(f"  播放提示音: {plugin.play_beep_on_wake}")
    print(f"  使用MP3: {plugin.use_mp3_sound}")
    print(f"  MP3文件: {plugin.mp3_filename}")
    print(f"  使用双声beep: {plugin.use_double_beep}")
    print(f"  提示音生成器状态: {'已初始化' if plugin.beep_generator else '未初始化'}")
    
    if plugin.beep_generator:
        available_mp3 = plugin.beep_generator.get_available_mp3_files()
        print(f"  可用MP3文件: {available_mp3}")
    
    # 模拟语音唤醒事件
    print(f"\n开始模拟语音唤醒...")
    print("模拟检测到唤醒词: '你好小智'")
    
    # 调用唤醒检测回调
    await plugin._on_detected("你好小智", "你好小智")
    
    # 等待提示音播放完成
    await asyncio.sleep(2)
    
    print(f"\n设备状态: {app.device_state}")
    print("集成测试完成！")

def main():
    try:
        asyncio.run(test_integration())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()