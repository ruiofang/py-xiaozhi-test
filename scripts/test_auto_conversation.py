#!/usr/bin/env python3
"""
测试自动对话模式启动功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config_manager import ConfigManager

def test_auto_conversation_config():
    """测试自动对话配置"""
    print("=" * 50)
    print("自动对话模式配置测试")
    print("=" * 50)
    
    try:
        # 获取配置管理器
        config = ConfigManager.get_instance()
        
        # 读取自动启动对话配置
        auto_start = config.get_config("SYSTEM_OPTIONS.AUTO_START_CONVERSATION", True)
        
        print(f"当前配置:")
        print(f"  AUTO_START_CONVERSATION: {auto_start}")
        
        if auto_start:
            print("\n✅ 自动对话模式已启用")
            print("   - 应用启动后会自动进入对话模式")
            print("   - 用户可以直接开始语音对话")
            print("   - 无需手动激活或按快捷键")
        else:
            print("\n❌ 自动对话模式已禁用")
            print("   - 应用启动后需要手动激活对话")
            print("   - 可以通过快捷键或唤醒词启动")
        
        # 其他相关配置
        print(f"\n相关配置:")
        try:
            aec_enabled = config.get_config("AEC_OPTIONS.ENABLED", True)
            use_wake_word = config.get_config("WAKE_WORD_OPTIONS.USE_WAKE_WORD", True)
            
            print(f"  AEC音频增强: {aec_enabled}")
            print(f"  语音唤醒: {use_wake_word}")
            
            if aec_enabled:
                print("  - 将使用实时对话模式 (REALTIME)")
            else:
                print("  - 将使用自动停止模式 (AUTO_STOP)")
                
        except Exception as e:
            print(f"  读取相关配置失败: {e}")
            
        print(f"\n配置文件位置: {config.config_file}")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

def show_usage_instructions():
    """显示使用说明"""
    print("\n" + "=" * 50)
    print("使用说明")
    print("=" * 50)
    
    print("\n1. 启用自动对话模式:")
    print('   在 config/config.json 中设置:')
    print('   "AUTO_START_CONVERSATION": true')
    
    print("\n2. 禁用自动对话模式:")
    print('   在 config/config.json 中设置:')
    print('   "AUTO_START_CONVERSATION": false')
    
    print("\n3. 启动应用:")
    print("   python3 main.py")
    
    print("\n4. 手动控制 (当自动模式禁用时):")
    print("   - Ctrl+K: 切换自动对话")
    print("   - Ctrl+J: 按住说话")
    print("   - 语音唤醒: '你好小智'")
    
    print("\n注意事项:")
    print("   - 自动对话模式需要音频设备正常工作")
    print("   - 首次使用需要允许麦克风权限")
    print("   - 如果遇到问题，可以禁用自动模式手动激活")

def main():
    """主函数"""
    test_auto_conversation_config()
    show_usage_instructions()

if __name__ == "__main__":
    main()