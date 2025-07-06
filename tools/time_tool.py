from datetime import datetime
import pytz
from typing import Dict, Any, Optional
from models.schema import Tool

async def get_time(timezone: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current time, optionally for a specific timezone
    
    Args:
        timezone: Timezone name (optional), e.g., 'America/New_York'
        
    Returns:
        Dictionary containing time information
    """
    try:
        if timezone:
            # Get time for specified timezone
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            timezone_name = timezone
        else:
            # Get UTC time
            current_time = datetime.now(pytz.UTC)
            timezone_name = "UTC"
        
        # Format the time information
        time_info = {
            "timestamp": current_time.timestamp(),
            "iso_format": current_time.isoformat(),
            "date": current_time.strftime("%Y-%m-%d"),
            "time": current_time.strftime("%H:%M:%S"),
            "day_of_week": current_time.strftime("%A"),
            "timezone": timezone_name
        }
        
        return time_info
    except pytz.exceptions.UnknownTimeZoneError:
        return {
            "error": f"Unknown timezone: {timezone}",
            "valid_timezones": "Please use a valid timezone from the IANA Time Zone Database"
        }
    except Exception as e:
        return {"error": f"Error getting time: {str(e)}"}

def register_time_tool(mcp_server):
    """Register the time tool with the MCP server"""
    time_tool = Tool(
        name="get_time",
        description="Get current time, optionally for a specific timezone",
        parameters={
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Timezone name from IANA Time Zone Database (optional), e.g., 'America/New_York', 'Europe/London'"
                }
            },
            "required": []
        },
        function=get_time
    )
    
    mcp_server.register_tool(time_tool)
