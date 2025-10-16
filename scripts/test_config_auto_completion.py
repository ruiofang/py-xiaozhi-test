#!/usr/bin/env python3
"""
测试自动配置补全功能
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_config_auto_completion():
    """测试配置自动补全功能"""
    print("=" * 60)
    print("配置自动补全功能测试")
    print("=" * 60)
    
    # 保存原始配置文件
    original_config_path = project_root / "config" / "config.json"
    backup_config_path = None
    
    if original_config_path.exists():
        backup_config_path = original_config_path.with_suffix('.backup')
        shutil.copy2(original_config_path, backup_config_path)
        print(f"已备份原配置文件到: {backup_config_path}")
    
    try:
        # 创建一个不完整的配置文件
        incomplete_config = {
            "SYSTEM_OPTIONS": {
                "CLIENT_ID": "test-client-id",
                "DEVICE_ID": "test-device-id",
                "NETWORK": {
                    "WEBSOCKET_URL": "wss://test.example.com",
                    "WEBSOCKET_ACCESS_TOKEN": "test-token"
                }
            },
            "WAKE_WORD_OPTIONS": {
                "USE_WAKE_WORD": True,
                "MODEL_PATH": "models"
                # 缺少提示音相关配置
            }
        }
        
        print("创建不完整的配置文件...")
        print("缺少的配置项:")
        print("  - SYSTEM_OPTIONS.AUTO_START_CONVERSATION")
        print("  - WAKE_WORD_OPTIONS.PLAY_BEEP_ON_WAKE")
        print("  - WAKE_WORD_OPTIONS.USE_MP3_SOUND")
        print("  - WAKE_WORD_OPTIONS.MP3_FILENAME")
        print("  - WAKE_WORD_OPTIONS.BEEP_FREQUENCY")
        print("  - WAKE_WORD_OPTIONS.BEEP_DURATION")
        print("  - WAKE_WORD_OPTIONS.BEEP_VOLUME")
        print("  - WAKE_WORD_OPTIONS.USE_DOUBLE_BEEP")
        
        # 保存不完整配置
        with open(original_config_path, 'w', encoding='utf-8') as f:
            json.dump(incomplete_config, f, indent=2, ensure_ascii=False)
        
        print(f"\n已创建不完整配置文件: {original_config_path}")
        
        # 导入并初始化ConfigManager
        from src.utils.config_manager import ConfigManager
        
        # 重置单例实例
        ConfigManager._instance = None
        
        print("\n初始化ConfigManager...")
        config_manager = ConfigManager.get_instance()
        
        # 检查配置是否被自动补全
        print("\n检查配置补全结果:")
        
        # 检查自动启动对话配置
        auto_start = config_manager.get_config("SYSTEM_OPTIONS.AUTO_START_CONVERSATION")
        print(f"  AUTO_START_CONVERSATION: {auto_start}")
        
        # 检查提示音配置
        play_beep = config_manager.get_config("WAKE_WORD_OPTIONS.PLAY_BEEP_ON_WAKE")
        use_mp3 = config_manager.get_config("WAKE_WORD_OPTIONS.USE_MP3_SOUND")
        mp3_filename = config_manager.get_config("WAKE_WORD_OPTIONS.MP3_FILENAME")
        beep_freq = config_manager.get_config("WAKE_WORD_OPTIONS.BEEP_FREQUENCY")
        beep_duration = config_manager.get_config("WAKE_WORD_OPTIONS.BEEP_DURATION")
        beep_volume = config_manager.get_config("WAKE_WORD_OPTIONS.BEEP_VOLUME")
        use_double = config_manager.get_config("WAKE_WORD_OPTIONS.USE_DOUBLE_BEEP")
        
        print(f"  PLAY_BEEP_ON_WAKE: {play_beep}")
        print(f"  USE_MP3_SOUND: {use_mp3}")
        print(f"  MP3_FILENAME: {mp3_filename}")
        print(f"  BEEP_FREQUENCY: {beep_freq}")
        print(f"  BEEP_DURATION: {beep_duration}")
        print(f"  BEEP_VOLUME: {beep_volume}")
        print(f"  USE_DOUBLE_BEEP: {use_double}")
        
        # 验证结果
        expected_values = {
            "AUTO_START_CONVERSATION": True,
            "PLAY_BEEP_ON_WAKE": True,
            "USE_MP3_SOUND": True,
            "MP3_FILENAME": "wake_up.mp3",
            "BEEP_FREQUENCY": 800.0,
            "BEEP_DURATION": 0.3,
            "BEEP_VOLUME": 0.3,
            "USE_DOUBLE_BEEP": False
        }
        
        actual_values = {
            "AUTO_START_CONVERSATION": auto_start,
            "PLAY_BEEP_ON_WAKE": play_beep,
            "USE_MP3_SOUND": use_mp3,
            "MP3_FILENAME": mp3_filename,
            "BEEP_FREQUENCY": beep_freq,
            "BEEP_DURATION": beep_duration,
            "BEEP_VOLUME": beep_volume,
            "USE_DOUBLE_BEEP": use_double
        }
        
        success = True
        print(f"\n验证结果:")
        for key, expected in expected_values.items():
            actual = actual_values[key]
            if actual == expected:
                print(f"  ✅ {key}: {actual}")
            else:
                print(f"  ❌ {key}: 期望 {expected}, 实际 {actual}")
                success = False
        
        # 检查配置文件是否被更新
        print(f"\n检查配置文件更新:")
        with open(original_config_path, 'r', encoding='utf-8') as f:
            updated_config = json.load(f)
        
        # 检查是否包含新的配置项
        wake_word_config = updated_config.get("WAKE_WORD_OPTIONS", {})
        system_config = updated_config.get("SYSTEM_OPTIONS", {})
        
        has_beep_config = "PLAY_BEEP_ON_WAKE" in wake_word_config
        has_auto_start = "AUTO_START_CONVERSATION" in system_config
        
        if has_beep_config and has_auto_start:
            print(f"  ✅ 配置文件已自动更新")
        else:
            print(f"  ❌ 配置文件未正确更新")
            success = False
        
        if success:
            print(f"\n🎉 配置自动补全功能测试成功!")
        else:
            print(f"\n💥 配置自动补全功能测试失败!")
            
        return success
        
    except Exception as e:
        print(f"\n测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # 恢复原始配置文件
        if backup_config_path and backup_config_path.exists():
            shutil.copy2(backup_config_path, original_config_path)
            backup_config_path.unlink()
            print(f"\n已恢复原始配置文件")

def show_feature_info():
    """显示功能说明"""
    print("\n" + "=" * 60)
    print("功能说明")
    print("=" * 60)
    
    print("\n✨ 自动配置补全功能特性:")
    print("  1. 检测缺失的配置项")
    print("  2. 自动添加默认值")
    print("  3. 保存更新后的配置文件")
    print("  4. 保持用户自定义配置不变")
    
    print("\n🔧 自动补全的配置项:")
    print("  - SYSTEM_OPTIONS.AUTO_START_CONVERSATION: true")
    print("  - WAKE_WORD_OPTIONS.PLAY_BEEP_ON_WAKE: true")
    print("  - WAKE_WORD_OPTIONS.USE_MP3_SOUND: true")
    print("  - WAKE_WORD_OPTIONS.MP3_FILENAME: 'wake_up.mp3'")
    print("  - WAKE_WORD_OPTIONS.BEEP_FREQUENCY: 800.0")
    print("  - WAKE_WORD_OPTIONS.BEEP_DURATION: 0.3")
    print("  - WAKE_WORD_OPTIONS.BEEP_VOLUME: 0.3")
    print("  - WAKE_WORD_OPTIONS.USE_DOUBLE_BEEP: false")
    
    print("\n💡 使用场景:")
    print("  - 升级应用时自动添加新配置")
    print("  - 用户配置文件缺失部分配置")
    print("  - 首次运行时创建完整配置")

def main():
    """主函数"""
    try:
        success = test_config_auto_completion()
        show_feature_info()
        
        if success:
            print("\n✅ 所有测试通过!")
        else:
            print("\n❌ 测试失败!")
            
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试失败: {e}")

if __name__ == "__main__":
    main()