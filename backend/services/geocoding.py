import httpx
import asyncio
from typing import Optional, Dict, Tuple
from config.settings import get_settings
from config.redis import RedisCache

settings = get_settings()
cache = RedisCache(ttl=86400)  # 24 hours cache


class GeocodingService:
    """Naver Maps Geocoding Service"""
    
    def __init__(self):
        self.client_id = settings.NAVER_MAP_CLIENT_ID
        self.client_secret = settings.NAVER_MAP_CLIENT_SECRET
        self.geocode_url = settings.NAVER_MAP_GEOCODE_URL
        
    async def geocode_address(self, address: str) -> Optional[Dict]:
        """
        Convert address to coordinates using Naver Maps Geocoding API
        
        Args:
            address: Address string to geocode
            
        Returns:
            Dict with status, latitude, longitude, formatted_address
        """
        # Check cache first
        cache_key = f"geocode:{address}"
        cached = await cache.get_json(cache_key)
        if cached:
            return cached
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "X-NCP-APIGW-API-KEY-ID": self.client_id,
                    "X-NCP-APIGW-API-KEY": self.client_secret,
                }
                params = {"query": address}
                
                response = await client.get(
                    self.geocode_url,
                    headers=headers,
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "OK" and data.get("addresses"):
                        address_data = data["addresses"][0]
                        
                        result = {
                            "status": "success",
                            "latitude": float(address_data["y"]),
                            "longitude": float(address_data["x"]),
                            "formatted_address": address_data.get("roadAddress") or address_data.get("jibunAddress"),
                            "address_type": address_data.get("addressType"),
                        }
                        
                        # Cache the result
                        await cache.set_json(cache_key, result)
                        
                        return result
                    else:
                        return {
                            "status": "not_found",
                            "error": "No addresses found for the given query",
                            "latitude": None,
                            "longitude": None,
                        }
                else:
                    return {
                        "status": "error",
                        "error": f"API returned status code {response.status_code}",
                        "latitude": None,
                        "longitude": None,
                    }
                    
        except httpx.TimeoutException:
            return {
                "status": "error",
                "error": "Geocoding request timed out",
                "latitude": None,
                "longitude": None,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "latitude": None,
                "longitude": None,
            }
    
    async def reverse_geocode(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Convert coordinates to address using Naver Maps Reverse Geocoding
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict with status, address information
        """
        # Check cache first
        cache_key = f"reverse_geocode:{latitude}:{longitude}"
        cached = await cache.get_json(cache_key)
        if cached:
            return cached
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "X-NCP-APIGW-API-KEY-ID": self.client_id,
                    "X-NCP-APIGW-API-KEY": self.client_secret,
                }
                params = {
                    "coords": f"{longitude},{latitude}",  # Note: lon,lat order
                    "output": "json",
                    "orders": "roadaddr,addr"
                }
                
                # Use reverse geocoding endpoint
                url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
                
                response = await client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status", {}).get("code") == 0 and data.get("results"):
                        result_data = data["results"][0]
                        region = result_data.get("region", {})
                        land = result_data.get("land", {})
                        
                        result = {
                            "status": "success",
                            "address": result_data.get("name", ""),
                            "road_address": land.get("name", ""),
                            "area1": region.get("area1", {}).get("name", ""),
                            "area2": region.get("area2", {}).get("name", ""),
                            "area3": region.get("area3", {}).get("name", ""),
                            "area4": region.get("area4", {}).get("name", ""),
                        }
                        
                        # Cache the result
                        await cache.set_json(cache_key, result)
                        
                        return result
                    else:
                        return {
                            "status": "not_found",
                            "error": "No address found for the given coordinates",
                        }
                else:
                    return {
                        "status": "error",
                        "error": f"API returned status code {response.status_code}",
                    }
                    
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
            }
    
    async def batch_geocode(self, addresses: list[str], delay: float = 0.1) -> list[Dict]:
        """
        Batch geocode multiple addresses with rate limiting
        
        Args:
            addresses: List of addresses to geocode
            delay: Delay between requests in seconds
            
        Returns:
            List of geocoding results
        """
        results = []
        
        for address in addresses:
            result = await self.geocode_address(address)
            results.append({"address": address, **result})
            
            # Rate limiting
            if delay > 0:
                await asyncio.sleep(delay)
        
        return results
