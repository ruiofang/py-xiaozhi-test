#!/usr/bin/env python3
"""
检查音频设备和提示音生成器状态
"""

import sys
from pathlib import Path
import sounddevice as sd
import numpy as np

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.beep_generator import get_beep_generator
from src.utils.logging_config import setup_logging, get_logger

logger = get_logger(__name__)


def check_audio_devices():
    """检查音频设备状态"""
    print("=== 音频设备检查 ===")
    
    try:
        # 查询所有设备
        devices = sd.query_devices()
        print(f"共找到 {len(devices)} 个音频设备:")
        
        for i, device in enumerate(devices):
            if device['max_output_channels'] > 0:
                print(f"  输出设备 {i}: {device['name']} (采样率: {device['default_samplerate']:.0f}Hz)")
        
        # 查询默认设备
        default_devices = sd.default.device
        print(f"\n默认设备: 输入={default_devices[0]}, 输出={default_devices[1]}")
        
        if default_devices[1] is not None:
            default_output = devices[default_devices[1]]
            print(f"默认输出设备: {default_output['name']}")
        
    except Exception as e:
        print(f"检查音频设备时出错: {e}")


def test_direct_audio():
    """直接测试音频播放"""
    print("\n=== 直接音频测试 ===")
    
    try:
        # 生成简单的测试音调
        duration = 0.5
        sample_rate = 44100
        frequency = 800.0
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * frequency * t) * 0.5
        wave = (wave * 32767).astype(np.int16)
        
        print(f"播放测试音调: {frequency}Hz, {duration}s")
        print(f"音频数据: 长度={len(wave)}, 最大值={np.max(np.abs(wave))}")
        
        sd.play(wave, sample_rate)
        sd.wait()
        print("直接音频测试完成")
        
    except Exception as e:
        print(f"直接音频测试失败: {e}")


def test_beep_generator():
    """测试提示音生成器"""
    print("\n=== 提示音生成器测试 ===")
    
    try:
        setup_logging()
        beep_generator = get_beep_generator()
        
        # 检查生成器状态
        print(f"设备ID: {beep_generator._speaker_device_id}")
        print(f"采样率: {beep_generator._device_output_sample_rate}")
        
        if beep_generator._speaker_device_id is None:
            print("错误: 没有找到输出设备")
            return
            
        # 测试音频生成
        test_audio = beep_generator._generate_beep(800.0, 0.3, 0.5, beep_generator._device_output_sample_rate)
        print(f"生成的音频数据: 长度={len(test_audio)}, 最大值={np.max(np.abs(test_audio))}")
        
        if np.max(np.abs(test_audio)) == 0:
            print("错误: 生成的音频数据为空")
        else:
            print("音频数据生成正常")
            
    except Exception as e:
        print(f"提示音生成器测试失败: {e}")


if __name__ == "__main__":
    check_audio_devices()
    test_direct_audio()
    test_beep_generator()