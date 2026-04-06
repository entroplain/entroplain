"""
Shared state for real-time data sharing between proxy and dashboard.
"""

import asyncio
import json
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SharedState:
    """
    Shared state between proxy and dashboard.
    
    Usage:
        state = SharedState()
        
        # In proxy:
        await state.update({
            "trajectory": [...],
            "token_count": 10,
            ...
        })
        
        # In dashboard:
        data = await state.get_update()
    """
    _data: Dict[str, Any] = field(default_factory=dict)
    _subscribers: List[Callable] = field(default_factory=list)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    _last_update: Optional[datetime] = None
    
    async def update(self, data: Dict[str, Any]) -> None:
        """Update state and notify subscribers."""
        async with self._lock:
            self._data = data
            self._last_update = datetime.utcnow()
        
        # Notify all subscribers
        for callback in self._subscribers:
            try:
                await callback(data)
            except Exception:
                pass
    
    async def get(self) -> Dict[str, Any]:
        """Get current state."""
        async with self._lock:
            return self._data.copy()
    
    def subscribe(self, callback: Callable) -> None:
        """Subscribe to state updates."""
        self._subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable) -> None:
        """Unsubscribe from state updates."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)


# Global shared state instance
_shared_state: Optional[SharedState] = None


def get_shared_state() -> SharedState:
    """Get or create the global shared state."""
    global _shared_state
    if _shared_state is None:
        _shared_state = SharedState()
    return _shared_state
