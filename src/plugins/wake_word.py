from typing import Any

from src.constants.constants import AbortReason
from src.plugins.base import Plugin
from src.utils.beep_generator import get_beep_generator
from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger

logger = get_logger(__name__)
from src.utils.beep_generator import get_beep_generator
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class WakeWordPlugin(Plugin):
    name = "wake_word"

    def __init__(self) -> None:
        super().__init__()
        self.app = None
        self.detector = None
        
        # 获取配置管理器
        self.config = ConfigManager.get_instance()
        
        # 提示音相关配置
        self.play_beep_on_wake = self.config.get_config("WAKE_WORD_OPTIONS.PLAY_BEEP_ON_WAKE", True)
        self.use_mp3_sound = self.config.get_config("WAKE_WORD_OPTIONS.USE_MP3_SOUND", True)  # 优先使用MP3
        self.mp3_filename = self.config.get_config("WAKE_WORD_OPTIONS.MP3_FILENAME", "wake_up.mp3")
        self.use_double_beep = self.config.get_config("WAKE_WORD_OPTIONS.USE_DOUBLE_BEEP", True)
        self.beep_frequency = self.config.get_config("WAKE_WORD_OPTIONS.BEEP_FREQUENCY", 800.0)
        self.beep_duration = self.config.get_config("WAKE_WORD_OPTIONS.BEEP_DURATION", 0.3)
        self.beep_volume = self.config.get_config("WAKE_WORD_OPTIONS.BEEP_VOLUME", 0.3)
        
        # 获取提示音生成器
        if self.play_beep_on_wake:
            try:
                self.beep_generator = get_beep_generator()
                logger.debug("提示音生成器初始化成功")
            except Exception as e:
                logger.warning(f"提示音生成器初始化失败: {e}")
                self.beep_generator = None
        else:
            self.beep_generator = None

    async def setup(self, app: Any) -> None:
        self.app = app
        try:
            from src.audio_processing.wake_word_detect import WakeWordDetector

            self.detector = WakeWordDetector()
            if not getattr(self.detector, "enabled", False):
                self.detector = None
                return

            # 绑定回调
            self.detector.on_detected(self._on_detected)
            self.detector.on_error = self._on_error
        except Exception:
            self.detector = None

    async def start(self) -> None:
        if not self.detector:
            return
        try:
            # 需要音频编码器以提供原始PCM数据
            audio_codec = getattr(self.app, "audio_codec", None)
            if audio_codec is None:
                return
            await self.detector.start(audio_codec)
        except Exception:
            pass

    async def stop(self) -> None:
        if self.detector:
            try:
                await self.detector.stop()
            except Exception:
                pass

    async def shutdown(self) -> None:
        if self.detector:
            try:
                await self.detector.stop()
            except Exception:
                pass

    async def _on_detected(self, wake_word, full_text):
        # 检测到唤醒词：切到自动对话（根据 AEC 自动选择实时/自动停）
        try:
            print(wake_word, full_text)
            
            # 播放语音唤醒提示音（如果启用）
            if self.play_beep_on_wake and self.beep_generator:
                try:
                    if self.use_mp3_sound:
                        # 优先播放MP3提示音
                        self.app.spawn(
                            self.beep_generator.play_wake_up_mp3(self.mp3_filename),
                            "wake_word:mp3_sound"
                        )
                        logger.debug(f"已触发MP3语音唤醒提示音: {self.mp3_filename}")
                    elif self.use_double_beep:
                        # 播放双声提示音
                        self.app.spawn(
                            self.beep_generator.play_double_beep(),
                            "wake_word:double_beep"
                        )
                        logger.debug("已触发双声beep语音唤醒提示音")
                    else:
                        # 播放单声提示音
                        self.app.spawn(
                            self.beep_generator.play_wake_up_beep(
                                frequency=self.beep_frequency,
                                duration=self.beep_duration,
                                volume=self.beep_volume
                            ),
                            "wake_word:single_beep"
                        )
                        logger.debug("已触发单声beep语音唤醒提示音")
                    
                except Exception as e:
                    # 提示音播放失败不应影响正常功能
                    logger.warning(f"播放唤醒提示音失败: {e}")
            else:
                logger.debug("唤醒提示音已禁用或生成器不可用")
            
            # 若正在说话，交给应用的打断/状态机处理
            if hasattr(self.app, "device_state") and hasattr(
                self.app, "start_auto_conversation"
            ):
                if self.app.is_speaking():
                    await self.app.abort_speaking(AbortReason.WAKE_WORD_DETECTED)
                else:
                    await self.app.start_auto_conversation()
                # 打断后清理一下队列
                try:
                    audio_plugin = self.app.plugins.get_plugin("audio")
                    if audio_plugin and hasattr(audio_plugin, 'codec'):
                        await audio_plugin.codec.clear_audio_queue()
                except (AttributeError, Exception):
                    # 如果没有plugins属性或清理失败，忽略（比如测试环境）
                    pass
        except Exception as e:
            logger.error(f"处理唤醒词检测失败: {e}", exc_info=True)

    def _on_error(self, error):
        try:
            if hasattr(self.app, "set_chat_message"):
                self.app.set_chat_message("assistant", f"[KWS错误] {error}")
        except Exception:
            pass
