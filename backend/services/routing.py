import httpx
import asyncio
from typing import Optional, Dict, List, Tuple
from config.settings import get_settings
from config.redis import RedisCache

settings = get_settings()
cache = RedisCache(ttl=3600)  # 1 hour cache


class RoutingService:
    """Naver Maps Directions API Service"""
    
    def __init__(self):
        self.client_id = settings.NAVER_MAP_CLIENT_ID
        self.client_secret = settings.NAVER_MAP_CLIENT_SECRET
        self.directions_url = settings.NAVER_MAP_DIRECTIONS_URL
        
    async def get_route(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        waypoints: Optional[List[Tuple[float, float]]] = None,
        option: str = "trafast"  # trafast, tracomfort, traoptimal
    ) -> Optional[Dict]:
        """
        Get route information between two points
        
        Args:
            start_lat: Starting latitude
            start_lon: Starting longitude
            end_lat: Ending latitude
            end_lon: Ending longitude
            waypoints: Optional list of waypoint coordinates [(lat, lon), ...]
            option: Route optimization option (trafast=fastest, tracomfort=comfortable, traoptimal=optimal)
            
        Returns:
            Dict with distance_km, duration_minutes, path, toll_fee, etc.
        """
        # Create cache key
        waypoint_str = ""
        if waypoints:
            waypoint_str = "|".join([f"{lon},{lat}" for lat, lon in waypoints])
        cache_key = f"route:{start_lon},{start_lat}:{end_lon},{end_lat}:{waypoint_str}:{option}"
        
        # Check cache
        cached = await cache.get_json(cache_key)
        if cached:
            return cached
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "X-NCP-APIGW-API-KEY-ID": self.client_id,
                    "X-NCP-APIGW-API-KEY": self.client_secret,
                }
                
                # Naver API uses lon,lat order
                params = {
                    "start": f"{start_lon},{start_lat}",
                    "goal": f"{end_lon},{end_lat}",
                    "option": option,
                }
                
                # Add waypoints if provided
                if waypoints:
                    params["waypoints"] = "|".join([f"{lon},{lat}" for lat, lon in waypoints])
                
                response = await client.get(
                    self.directions_url,
                    headers=headers,
                    params=params,
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("code") == 0 and data.get("route"):
                        route_data = data["route"][option][0]
                        summary = route_data["summary"]
                        
                        result = {
                            "status": "success",
                            "distance_km": summary["distance"] / 1000,  # Convert to km
                            "duration_minutes": summary["duration"] / 60000,  # Convert to minutes
                            "duration_seconds": summary["duration"] / 1000,
                            "toll_fee": summary.get("tollFare", 0),
                            "taxi_fare": summary.get("taxiFare", 0),
                            "fuel_price": summary.get("fuelPrice", 0),
                            "path": route_data.get("path", []),  # List of [lon, lat] coordinates
                            "bbox": summary.get("bbox", []),  # Bounding box
                        }
                        
                        # Cache the result
                        await cache.set_json(cache_key, result, ttl=3600)
                        
                        return result
                    else:
                        return {
                            "status": "error",
                            "error": f"Route not found: {data.get('message', 'Unknown error')}",
                            "distance_km": None,
                            "duration_minutes": None,
                        }
                else:
                    return {
                        "status": "error",
                        "error": f"API returned status code {response.status_code}",
                        "distance_km": None,
                        "duration_minutes": None,
                    }
                    
        except httpx.TimeoutException:
            return {
                "status": "error",
                "error": "Routing request timed out",
                "distance_km": None,
                "duration_minutes": None,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "distance_km": None,
                "duration_minutes": None,
            }
    
    async def get_distance_matrix(
        self,
        origins: List[Tuple[float, float]],
        destinations: List[Tuple[float, float]],
        option: str = "trafast"
    ) -> Dict:
        """
        Calculate distance matrix between multiple origins and destinations
        
        Args:
            origins: List of origin coordinates [(lat, lon), ...]
            destinations: List of destination coordinates [(lat, lon), ...]
            option: Route optimization option
            
        Returns:
            Dict with distance and duration matrices
        """
        n_origins = len(origins)
        n_destinations = len(destinations)
        
        distance_matrix = [[0.0] * n_destinations for _ in range(n_origins)]
        duration_matrix = [[0.0] * n_destinations for _ in range(n_origins)]
        
        # Calculate routes for all origin-destination pairs
        tasks = []
        for i, (o_lat, o_lon) in enumerate(origins):
            for j, (d_lat, d_lon) in enumerate(destinations):
                if i == j and origins == destinations:
                    # Same location, zero distance
                    continue
                tasks.append((i, j, o_lat, o_lon, d_lat, d_lon))
        
        # Process in batches to avoid rate limits
        batch_size = 10
        for batch_start in range(0, len(tasks), batch_size):
            batch = tasks[batch_start:batch_start + batch_size]
            
            batch_results = await asyncio.gather(*[
                self.get_route(o_lat, o_lon, d_lat, d_lon, option=option)
                for i, j, o_lat, o_lon, d_lat, d_lon in batch
            ])
            
            for (i, j, _, _, _, _), result in zip(batch, batch_results):
                if result and result.get("status") == "success":
                    distance_matrix[i][j] = result["distance_km"]
                    duration_matrix[i][j] = result["duration_minutes"]
                else:
                    # Use straight-line distance as fallback
                    distance_matrix[i][j] = self._haversine_distance(
                        origins[i][0], origins[i][1],
                        destinations[j][0], destinations[j][1]
                    )
                    # Estimate duration: 40 km/h average
                    duration_matrix[i][j] = (distance_matrix[i][j] / 40) * 60
            
            # Rate limiting between batches
            await asyncio.sleep(0.5)
        
        return {
            "status": "success",
            "distance_matrix": distance_matrix,
            "duration_matrix": duration_matrix,
            "n_origins": n_origins,
            "n_destinations": n_destinations,
        }
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate straight-line distance between two points using Haversine formula
        
        Returns:
            Distance in kilometers
        """
        import math
        
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    async def get_estimated_arrival_time(
        self,
        current_lat: float,
        current_lon: float,
        dest_lat: float,
        dest_lon: float,
        speed_factor: float = None
    ) -> Optional[Dict]:
        """
        Get estimated arrival time considering current traffic
        
        Args:
            current_lat: Current latitude
            current_lon: Current longitude
            dest_lat: Destination latitude
            dest_lon: Destination longitude
            speed_factor: Speed adjustment factor (default from settings)
            
        Returns:
            Dict with ETA information
        """
        if speed_factor is None:
            speed_factor = settings.SPEED_FACTOR
        
        route = await self.get_route(current_lat, current_lon, dest_lat, dest_lon)
        
        if route and route.get("status") == "success":
            adjusted_duration = route["duration_minutes"] / speed_factor
            
            return {
                "status": "success",
                "distance_km": route["distance_km"],
                "duration_minutes": adjusted_duration,
                "original_duration_minutes": route["duration_minutes"],
                "speed_factor": speed_factor,
            }
        
        return route
