# ====================================================================
#  File: sdk/manager.py
#  Plugin Manager: 플러그인 발견, 로드, 활성화
# ====================================================================

from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, plugins_dir: str, config: Dict[str, Any]):
        self.plugins_dir = Path(plugins_dir)
        self.config = config or {}
        self.discovered: Dict[str, Path] = {}
        self.loaded: Dict[str, Any] = {}
        self.enabled: set[str] = set()
        
        logger.info(f"[L.U.N.A. PluginManager] 초기화: {self.plugins_dir}")

    def discover_plugins(self) -> List[str]:
        self.discovered.clear()
        
        if not self.plugins_dir.exists():
            logger.warning(f"[L.U.N.A. PluginManager] 플러그인 디렉토리 없음: {self.plugins_dir}")
            return []
        
        discovered = []
        for item in self.plugins_dir.iterdir():
            if not item.is_dir():
                continue
            
            name = item.name
            
            has_init = (item / "__init__.py").exists()
            has_server = (item / "server.py").exists()
            
            if has_init or has_server:
                self.discovered[name] = item
                discovered.append(name)
                logger.debug(f"[L.U.N.A. PluginManager] 플러그인 발견: {name}")
        
        logger.info(f"[L.U.N.A. PluginManager] 총 {len(discovered)}개 플러그인 발견")
        return discovered

    def load_plugin(self, name: str) -> Optional[Any]:
        if name in self.loaded:
            logger.debug(f"[L.U.N.A. PluginManager] 이미 로드됨: {name}")
            return self.loaded[name]
        
        if name not in self.discovered:
            logger.error(f"[L.U.N.A. PluginManager] 플러그인 없음: {name}")
            return None
        
        plugin_path = self.discovered[name]
        
        try:
            server_file = plugin_path / "server.py"
            init_file = plugin_path / "__init__.py"
            
            target_file = server_file if server_file.exists() else init_file
            
            if not target_file.exists():
                logger.error(f"[L.U.N.A. PluginManager] 플러그인 파일 없음: {target_file}")
                return None
            
            spec = importlib.util.spec_from_file_location(
                f"plugins.{name}",
                target_file
            )
            
            if spec is None or spec.loader is None:
                logger.error(f"[L.U.N.A. PluginManager] 스펙 생성 실패: {name}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"plugins.{name}"] = module
            spec.loader.exec_module(module)
            
            self.loaded[name] = module
            logger.info(f"[L.U.N.A. PluginManager] 플러그인 로드 완료: {name}")
            
            return module
            
        except Exception as e:
            logger.error(f"[L.U.N.A. PluginManager] 플러그인 로드 실패 ({name}): {e}")
            import traceback
            traceback.print_exc()
            return None

    def enable_plugin(self, name: str) -> bool:
        if name not in self.loaded:
            logger.error(f"[L.U.N.A. PluginManager] 로드되지 않은 플러그인: {name}")
            return False
        
        try:
            self.enabled.add(name)
            logger.info(f"[L.U.N.A. PluginManager] 플러그인 활성화: {name}")
            return True
            
        except Exception as e:
            logger.error(f"[L.U.N.A. PluginManager] 플러그인 활성화 실패 ({name}): {e}")
            return False

    def disable_plugin(self, name: str) -> bool:
        if name not in self.loaded:
            logger.error(f"[L.U.N.A. PluginManager] 로드되지 않은 플러그인: {name}")
            return False
        
        try:
            self.enabled.discard(name)
            logger.info(f"[L.U.N.A. PluginManager] 플러그인 비활성화: {name}")
            return True
            
        except Exception as e:
            logger.error(f"[L.U.N.A. PluginManager] 플러그인 비활성화 실패 ({name}): {e}")
            return False

    def get_enabled(self) -> List[str]:
        return list(self.enabled)

    def get_loaded(self) -> List[str]:
        return list(self.loaded.keys())

    def get_discovered(self) -> List[str]:
        return list(self.discovered.keys())
