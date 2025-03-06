from abc import ABC, abstractmethod
from typing import Any, Dict, ClassVar, Type, Union
from ..models import ToolMetadata, ToolError

class BaseTool(ABC):
    """Base class for all tools"""
    
    # Tool metadata as class variables
    metadata: ClassVar[Type[ToolMetadata]]
    
    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        """Get tool metadata for planning"""
        # Create an instance of the metadata class
        return cls.metadata()  # This will use the default values defined in the metadata class
    
    @abstractmethod
    async def execute(self, **inputs: Any) -> Union[Dict[str, Any], ToolError]:
        """Execute the tool with given inputs"""
        pass 