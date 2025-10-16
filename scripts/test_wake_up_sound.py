#!/usr/bin/env python3
"""
测试语音唤醒提示音功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.beep_generator import get_beep_generator

async def test_beep_sounds():
    """测试各种提示音"""
    print("开始测试语音唤醒提示音功能...")
    
    generator = get_beep_generator()
    
    print("\n1. 测试基础beep音...")
    await generator.play_beep_tone(frequency=800, duration=0.5, volume=0.3)
    await asyncio.sleep(1)
    
    print("2. 测试双声beep...")
    await generator.play_double_beep()
    await asyncio.sleep(1)
    
    print("3. 检查可用的MP3文件...")
    mp3_files = generator.get_available_mp3_files()
    print(f"   找到MP3文件: {mp3_files}")
    
    if mp3_files:
        print("4. 测试MP3播放...")
        for mp3_file in mp3_files:
            print(f"   播放: {mp3_file}")
            await generator.play_wake_up_mp3(mp3_file)
            await asyncio.sleep(1)
    else:
        print("4. 未找到MP3文件，跳过测试")
    
    print("\n提示音测试完成！")

async def test_wake_word_plugin():
    """测试WakeWordPlugin的提示音配置"""
    print("\n测试WakeWordPlugin配置...")
    
    try:
        from src.plugins.wake_word import WakeWordPlugin
        from src.utils.config_manager import ConfigManager
        
        # 模拟配置
        config = ConfigManager.get_instance()
        
        plugin = WakeWordPlugin()
        print(f"播放提示音: {plugin.play_beep_on_wake}")
        print(f"使用MP3: {plugin.use_mp3_sound}")
        print(f"MP3文件名: {plugin.mp3_filename}")
        print(f"使用双声beep: {plugin.use_double_beep}")
        
        # 测试提示音生成器
        if plugin.beep_generator:
            print("提示音生成器已初始化")
            print("测试播放MP3...")
            await plugin.beep_generator.play_wake_up_mp3(plugin.mp3_filename)
        else:
            print("提示音生成器未初始化")
            
    except Exception as e:
        print(f"WakeWordPlugin测试失败: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("语音唤醒提示音测试程序")
    print("=" * 50)
    
    try:
        # 运行异步测试
        asyncio.run(test_beep_sounds())
        asyncio.run(test_wake_word_plugin())
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()