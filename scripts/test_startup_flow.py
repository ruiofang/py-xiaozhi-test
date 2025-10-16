#!/usr/bin/env python3
"""
模拟测试自动对话模式启动流程
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application import Application
from src.utils.config_manager import ConfigManager

class MockProtocol:
    """模拟协议类"""
    def __init__(self):
        self.session_id = "test-session"
        self.connected = False
        self._on_audio_channel_opened = None
        
    def on_network_error(self, callback):
        pass
        
    def on_incoming_json(self, callback):
        pass
        
    def on_incoming_audio(self, callback):
        pass
        
    def on_audio_channel_opened(self, callback):
        self._on_audio_channel_opened = callback
        
    def on_audio_channel_closed(self, callback):
        pass
        
    def is_audio_channel_opened(self):
        return self.connected
        
    async def send_start_listening(self, mode):
        print(f"模拟发送监听命令: {mode}")
        
    async def send_text(self, message):
        print(f"模拟发送文本: {message}")
        
    async def open_audio_channel(self):
        print("模拟打开音频通道")
        self.connected = True
        if self._on_audio_channel_opened:
            await self._on_audio_channel_opened()
        return True
        
    async def close_audio_channel(self):
        print("模拟关闭音频通道")
        self.connected = False

async def test_auto_conversation_startup():
    """测试自动对话启动流程"""
    print("=" * 60)
    print("自动对话模式启动流程测试")
    print("=" * 60)
    
    # 读取配置
    config = ConfigManager.get_instance()
    auto_start = config.get_config("SYSTEM_OPTIONS.AUTO_START_CONVERSATION", True)
    
    print(f"配置检查:")
    print(f"  自动启动对话: {auto_start}")
    
    if not auto_start:
        print("\n⚠️  自动对话模式已禁用，测试将模拟手动模式")
    
    # 创建应用实例 (不通过单例，避免冲突)
    app = Application.__new__(Application)
    app.__init__()
    
    # 模拟初始化
    app.running = True
    app._main_loop = asyncio.get_event_loop()
    app._initialize_async_objects()
    
    # 使用模拟协议
    app.protocol = MockProtocol()
    app._setup_protocol_callbacks()
    
    print(f"\n应用状态:")
    print(f"  自动启动配置: {app.auto_start_conversation}")
    print(f"  当前设备状态: {app.device_state}")
    print(f"  保持监听: {app.keep_listening}")
    print(f"  监听模式: {app.listening_mode}")
    
    # 模拟协议连接建立
    print(f"\n模拟协议连接建立...")
    await app.protocol.open_audio_channel()
    
    # 等待状态稳定
    await asyncio.sleep(0.1)
    
    print(f"\n连接建立后状态:")
    print(f"  设备状态: {app.device_state}")
    print(f"  保持监听: {app.keep_listening}")
    print(f"  协议已连接: {app.protocol.is_audio_channel_opened()}")
    
    # 验证预期行为
    if app.auto_start_conversation:
        if app.keep_listening and str(app.device_state) == "listening":
            print(f"\n✅ 自动对话模式启动成功!")
            print(f"   - 应用已进入持续监听状态")
            print(f"   - 用户可以直接开始语音对话")
        else:
            print(f"\n❌ 自动对话模式启动失败")
            print(f"   - 预期: keep_listening=True, state=listening")
            print(f"   - 实际: keep_listening={app.keep_listening}, state={app.device_state}")
    else:
        if not app.keep_listening and str(app.device_state) == "listening":
            print(f"\n✅ 手动模式工作正常!")
            print(f"   - 应用处于待机监听状态")
            print(f"   - 需要用户手动激活对话")
        else:
            print(f"\n❌ 手动模式状态异常")
    
    print(f"\n测试完成!")

async def main():
    """主函数"""
    try:
        await test_auto_conversation_startup()
    except Exception as e:
        print(f"\n测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())