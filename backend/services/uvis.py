import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from config.settings import get_settings
from config.redis import RedisCache

settings = get_settings()
cache = RedisCache(ttl=settings.UVIS_POLL_INTERVAL)


class UVISService:
    """Samsung UVIS GPS Tracking Service"""
    
    def __init__(self):
        self.api_url = settings.UVIS_API_URL
        self.api_key = settings.UVIS_API_KEY
        self.poll_interval = settings.UVIS_POLL_INTERVAL
        
    async def get_vehicle_location(self, device_id: str) -> Optional[Dict]:
        """
        Get current location of a vehicle by UVIS device ID
        
        Args:
            device_id: UVIS device identifier
            
        Returns:
            Dict with GPS data (latitude, longitude, speed, temperature, etc.)
        """
        # Check cache first
        cache_key = f"uvis:location:{device_id}"
        cached = await cache.get_json(cache_key)
        if cached:
            return cached
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                
                # NOTE: This is a placeholder URL structure
                # Actual UVIS API endpoint should be verified
                url = f"{self.api_url}/vehicles/{device_id}/location"
                
                response = await client.get(
                    url,
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    result = {
                        "status": "success",
                        "device_id": device_id,
                        "timestamp": data.get("timestamp"),
                        "latitude": data.get("latitude"),
                        "longitude": data.get("longitude"),
                        "altitude": data.get("altitude"),
                        "speed_kmh": data.get("speed"),
                        "heading": data.get("heading"),
                        "compartment1_temp": data.get("temperature1"),
                        "compartment2_temp": data.get("temperature2"),
                        "engine_on": data.get("engineOn"),
                        "door_open": data.get("doorOpen"),
                        "refrigerator_on": data.get("refrigeratorOn"),
                        "odometer_km": data.get("odometer"),
                    }
                    
                    # Cache the result
                    await cache.set_json(cache_key, result, ttl=self.poll_interval)
                    
                    return result
                else:
                    return {
                        "status": "error",
                        "error": f"UVIS API returned status code {response.status_code}",
                    }
                    
        except httpx.TimeoutException:
            return {
                "status": "error",
                "error": "UVIS API request timed out",
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"UVIS API error: {str(e)}",
            }
    
    async def get_multiple_vehicles(self, device_ids: List[str]) -> List[Dict]:
        """
        Get locations for multiple vehicles
        
        Args:
            device_ids: List of UVIS device identifiers
            
        Returns:
            List of GPS data for each vehicle
        """
        tasks = [self.get_vehicle_location(device_id) for device_id in device_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            result if not isinstance(result, Exception) else {
                "status": "error",
                "device_id": device_ids[idx],
                "error": str(result)
            }
            for idx, result in enumerate(results)
        ]
    
    async def check_temperature_alarm(self, device_id: str, target_temp: float, tolerance: float = 3.0) -> bool:
        """
        Check if vehicle temperature is within acceptable range
        
        Args:
            device_id: UVIS device identifier
            target_temp: Target temperature in Celsius
            tolerance: Acceptable temperature deviation
            
        Returns:
            True if temperature alarm should be triggered
        """
        location_data = await self.get_vehicle_location(device_id)
        
        if location_data and location_data.get("status") == "success":
            temp = location_data.get("compartment1_temp")
            if temp is not None:
                deviation = abs(temp - target_temp)
                return deviation > tolerance
        
        return False
    
    def parse_gps_data(self, raw_data: Dict) -> Dict:
        """
        Parse and normalize GPS data from UVIS format
        
        Args:
            raw_data: Raw GPS data from UVIS API
            
        Returns:
            Normalized GPS data dict
        """
        return {
            "timestamp": raw_data.get("timestamp") or datetime.now().isoformat(),
            "latitude": float(raw_data.get("latitude", 0)),
            "longitude": float(raw_data.get("longitude", 0)),
            "altitude": float(raw_data.get("altitude", 0)) if raw_data.get("altitude") else None,
            "speed_kmh": float(raw_data.get("speed", 0)),
            "heading": float(raw_data.get("heading", 0)),
            "compartment1_temp": float(raw_data.get("temperature1")) if raw_data.get("temperature1") else None,
            "compartment2_temp": float(raw_data.get("temperature2")) if raw_data.get("temperature2") else None,
            "engine_on": bool(raw_data.get("engineOn", False)),
            "door_open": bool(raw_data.get("doorOpen", False)),
            "refrigerator_on": bool(raw_data.get("refrigeratorOn", False)),
            "odometer_km": float(raw_data.get("odometer", 0)),
        }
