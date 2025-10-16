"""
语音唤醒提示音生成器和播放器
支持合成beep音和mp3文件播放
"""

import asyncio
import os
import threading
from pathlib import Path
from typing import Optional

import numpy as np

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class BeepGenerator:
    """提示音生成器和播放器"""
    
    def __init__(self):
        self.audio_initialized = False
        self.playback_device = None
        self.sample_rate = 44100
        
        # 尝试初始化音频播放设备
        self._init_audio_device()
        
        # MP3文件路径
        self.assets_audio_dir = Path(__file__).parent.parent.parent / "assets" / "audio"
        
    def _init_audio_device(self):
        """初始化音频播放设备"""
        try:
            import sounddevice as sd
            
            # 获取默认输出设备
            device_info = sd.query_devices(kind='output')
            self.sample_rate = int(device_info['default_samplerate'])
            self.audio_initialized = True
            logger.debug(f"音频设备初始化成功，采样率: {self.sample_rate}")
            
        except ImportError:
            logger.warning("sounddevice库未安装，将尝试其他音频后端")
            self.audio_initialized = False
        except Exception as e:
            logger.warning(f"音频设备初始化失败: {e}")
            self.audio_initialized = False
    
    def _generate_beep_tone(self, frequency: float, duration: float, volume: float = 0.3) -> np.ndarray:
        """生成纯音频beep信号"""
        try:
            # 生成时间序列
            t = np.linspace(0, duration, int(self.sample_rate * duration), False)
            
            # 生成正弦波
            tone = np.sin(2 * np.pi * frequency * t) * volume
            
            # 添加渐变效果，避免爆音
            fade_samples = int(self.sample_rate * 0.01)  # 10ms渐变
            if len(tone) > 2 * fade_samples:
                # 淡入
                tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
                # 淡出
                tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            return tone.astype(np.float32)
        except Exception as e:
            logger.error(f"生成beep音频失败: {e}")
            return np.array([], dtype=np.float32)
    
    async def play_beep_tone(self, frequency: float = 800.0, duration: float = 0.3, volume: float = 0.3):
        """播放beep提示音"""
        if not self.audio_initialized:
            logger.warning("音频设备未初始化，无法播放beep音")
            return
            
        try:
            import sounddevice as sd
            
            # 生成音频数据
            audio_data = self._generate_beep_tone(frequency, duration, volume)
            if len(audio_data) == 0:
                return
            
            # 在线程中播放音频，避免阻塞
            def play_in_thread():
                try:
                    sd.play(audio_data, self.sample_rate)
                    sd.wait()  # 等待播放完成
                except Exception as e:
                    logger.error(f"播放beep音频失败: {e}")
            
            # 异步执行
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, play_in_thread)
            
        except Exception as e:
            logger.error(f"播放beep音失败: {e}")
    
    async def play_double_beep(self, frequency: float = 800.0, duration: float = 0.2, 
                             gap: float = 0.1, volume: float = 0.3):
        """播放双声beep提示音"""
        try:
            # 播放第一声
            await self.play_beep_tone(frequency, duration, volume)
            # 间隔
            await asyncio.sleep(gap)
            # 播放第二声
            await self.play_beep_tone(frequency * 1.2, duration, volume)  # 第二声略高频
        except Exception as e:
            logger.error(f"播放双声beep失败: {e}")
    
    async def play_wake_up_beep(self, frequency: float = 800.0, duration: float = 0.3, volume: float = 0.3):
        """播放语音唤醒beep音（兼容旧接口）"""
        await self.play_beep_tone(frequency, duration, volume)
    
    async def play_mp3_file(self, mp3_path: str):
        """播放MP3文件"""
        try:
            # 检查文件是否存在
            file_path = Path(mp3_path)
            if not file_path.exists():
                logger.warning(f"MP3文件不存在: {mp3_path}")
                return
            
            # 尝试使用不同的MP3播放后端
            await self._play_mp3_with_pygame(str(file_path))
            
        except Exception as e:
            logger.error(f"播放MP3文件失败: {e}")
    
    async def _play_mp3_with_pygame(self, mp3_path: str):
        """使用pygame播放MP3"""
        try:
            import pygame
            
            def play_in_thread():
                try:
                    # 初始化pygame mixer
                    pygame.mixer.init()
                    
                    # 加载并播放音频文件
                    pygame.mixer.music.load(mp3_path)
                    pygame.mixer.music.play()
                    
                    # 等待播放完成
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                    
                    # 清理
                    pygame.mixer.quit()
                    
                except Exception as e:
                    logger.error(f"pygame播放MP3失败: {e}")
                    raise
            
            # 在线程中播放，避免阻塞
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, play_in_thread)
            
        except ImportError:
            logger.warning("pygame未安装，尝试其他播放方式")
            await self._play_mp3_with_system(mp3_path)
        except Exception as e:
            logger.error(f"pygame播放失败: {e}")
            # 回退到系统播放器
            await self._play_mp3_with_system(mp3_path)
    
    async def _play_mp3_with_system(self, mp3_path: str):
        """使用系统命令播放MP3"""
        try:
            import platform
            import subprocess
            
            system_name = platform.system().lower()
            
            def play_in_thread():
                try:
                    if system_name == "linux":
                        # Linux: 尝试使用 mpg123, mpv, 或 ffplay
                        for player in ["mpg123", "mpv", "ffplay"]:
                            try:
                                subprocess.run([player, mp3_path], 
                                             check=True, 
                                             stdout=subprocess.DEVNULL, 
                                             stderr=subprocess.DEVNULL,
                                             timeout=10)
                                return
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                continue
                        
                        # 如果都不可用，尝试 aplay (需要先转换)
                        logger.warning("未找到合适的MP3播放器，建议安装 mpg123 或 mpv")
                        
                    elif system_name == "darwin":  # macOS
                        subprocess.run(["afplay", mp3_path], check=True, timeout=10)
                        
                    elif system_name == "windows":
                        import winsound
                        winsound.PlaySound(mp3_path, winsound.SND_FILENAME)
                        
                    else:
                        logger.warning(f"不支持的操作系统: {system_name}")
                        
                except Exception as e:
                    logger.error(f"系统播放MP3失败: {e}")
            
            # 在线程中执行
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, play_in_thread)
            
        except Exception as e:
            logger.error(f"系统播放失败: {e}")
    
    async def play_wake_up_mp3(self, mp3_filename: str = "wake_up.mp3"):
        """播放语音唤醒MP3提示音"""
        mp3_path = self.assets_audio_dir / mp3_filename
        await self.play_mp3_file(str(mp3_path))
    
    def get_available_mp3_files(self) -> list:
        """获取可用的MP3文件列表"""
        try:
            if not self.assets_audio_dir.exists():
                return []
            
            mp3_files = list(self.assets_audio_dir.glob("*.mp3"))
            return [f.name for f in mp3_files]
        except Exception as e:
            logger.error(f"获取MP3文件列表失败: {e}")
            return []


# 全局单例实例
_beep_generator: Optional[BeepGenerator] = None


def get_beep_generator() -> BeepGenerator:
    """获取全局beep生成器实例"""
    global _beep_generator
    if _beep_generator is None:
        _beep_generator = BeepGenerator()
    return _beep_generator


# 便利函数
async def play_wake_up_beep(frequency: float = 800.0, duration: float = 0.3, volume: float = 0.3):
    """播放语音唤醒beep音"""
    generator = get_beep_generator()
    await generator.play_wake_up_beep(frequency, duration, volume)


async def play_wake_up_mp3(mp3_filename: str = "wake_up.mp3"):
    """播放语音唤醒MP3提示音"""
    generator = get_beep_generator()
    await generator.play_wake_up_mp3(mp3_filename)


async def play_double_beep():
    """播放双声beep"""
    generator = get_beep_generator()
    await generator.play_double_beep()
