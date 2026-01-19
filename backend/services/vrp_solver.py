from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import math
from config.settings import get_settings

settings = get_settings()


class VRPSolver:
    """Vehicle Routing Problem Solver using Google OR-Tools"""
    
    def __init__(self):
        self.settings = settings
        
    def solve(
        self,
        vehicles: List[Dict],
        orders: List[Dict],
        distance_matrix: List[List[float]],
        time_matrix: List[List[float]],
        depot_location: Tuple[float, float] = None
    ) -> Optional[Dict]:
        """
        Solve VRP problem with multiple constraints
        
        Args:
            vehicles: List of vehicle dicts with capacity and constraints
            orders: List of order dicts with pickup/delivery requirements
            distance_matrix: Matrix of distances between all locations (km)
            time_matrix: Matrix of travel times between all locations (minutes)
            depot_location: Starting depot coordinates (optional)
            
        Returns:
            Dict with optimized routes for each vehicle
        """
        
        # Create routing index manager
        num_vehicles = len(vehicles)
        num_locations = len(distance_matrix)
        
        # Create depot index (0 = depot)
        depot_index = 0
        
        manager = pywrapcp.RoutingIndexManager(
            num_locations,
            num_vehicles,
            depot_index
        )
        
        # Create routing model
        routing = pywrapcp.RoutingModel(manager)
        
        # Create distance callback
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(distance_matrix[from_node][to_node] * 1000)  # Convert to meters
        
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Create time callback
        def time_callback(from_index, to_index):
            """Returns the travel time between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(time_matrix[from_node][to_node])  # Minutes
        
        time_callback_index = routing.RegisterTransitCallback(time_callback)
        
        # Add time dimension (for time windows)
        time_dimension_name = 'Time'
        routing.AddDimension(
            time_callback_index,
            30,  # Allow waiting time up to 30 minutes
            settings.MAX_DRIVING_HOURS_PER_DAY * 60,  # Maximum time per vehicle (minutes)
            False,  # Don't force start cumul to zero
            time_dimension_name
        )
        time_dimension = routing.GetDimensionOrDie(time_dimension_name)
        
        # Add time windows for orders
        for order_idx, order in enumerate(orders):
            # Node index in routing (skip depot at index 0)
            node_index = order_idx + 1
            index = manager.NodeToIndex(node_index)
            
            # Parse time windows
            pickup_start = self._parse_time(order.get('pickup_time_start', '06:00'))
            pickup_end = self._parse_time(order.get('pickup_time_end', '20:00'))
            
            time_dimension.CumulVar(index).SetRange(pickup_start, pickup_end)
        
        # Add capacity dimension (pallets)
        def demand_callback(from_index):
            """Returns the demand of the node."""
            from_node = manager.IndexToNode(from_index)
            if from_node == 0:  # Depot
                return 0
            order_idx = from_node - 1
            if order_idx < len(orders):
                return orders[order_idx].get('required_pallets', 0)
            return 0
        
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # Null capacity slack
            [v['max_pallets'] for v in vehicles],  # Vehicle maximum capacities
            True,  # Start cumul to zero
            'Capacity'
        )
        
        # Add temperature constraints
        def temperature_callback(from_index):
            """Returns temperature type of the node."""
            from_node = manager.IndexToNode(from_index)
            if from_node == 0:  # Depot
                return 0  # Neutral
            order_idx = from_node - 1
            if order_idx < len(orders):
                temp_type = orders[order_idx].get('temperature_type', 'frozen')
                return self._temperature_to_int(temp_type)
            return 0
        
        # Add vehicle-order compatibility constraints
        for vehicle_idx, vehicle in enumerate(vehicles):
            vehicle_temp_type = vehicle['vehicle_type']
            
            for order_idx, order in enumerate(orders):
                node_index = order_idx + 1
                index = manager.NodeToIndex(node_index)
                
                # Check temperature compatibility
                if not self._is_temperature_compatible(order['temperature_type'], vehicle_temp_type):
                    # Disallow this vehicle for this order
                    routing.VehicleVar(index).RemoveValue(vehicle_idx)
        
        # Set search parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = settings.ORTOOLS_TIME_LIMIT_SECONDS
        search_parameters.solution_limit = settings.ORTOOLS_SOLUTION_LIMIT
        
        # Solve the problem
        solution = routing.SolveWithParameters(search_parameters)
        
        if solution:
            return self._extract_solution(
                manager, routing, solution, vehicles, orders, distance_matrix, time_matrix
            )
        else:
            return {
                "status": "failed",
                "error": "No solution found within time limit",
            }
    
    def _extract_solution(
        self,
        manager,
        routing,
        solution,
        vehicles: List[Dict],
        orders: List[Dict],
        distance_matrix: List[List[float]],
        time_matrix: List[List[float]]
    ) -> Dict:
        """Extract solution from OR-Tools solver"""
        
        routes = []
        total_distance = 0
        total_time = 0
        total_load = 0
        
        for vehicle_idx in range(len(vehicles)):
            route = {
                "vehicle_id": vehicles[vehicle_idx]['vehicle_id'],
                "vehicle_type": vehicles[vehicle_idx]['vehicle_type'],
                "stops": [],
                "total_distance_km": 0,
                "total_time_minutes": 0,
                "total_pallets": 0,
                "total_weight_kg": 0,
            }
            
            index = routing.Start(vehicle_idx)
            route_distance = 0
            route_time = 0
            route_load = 0
            
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                
                # Skip depot
                if node_index > 0:
                    order_idx = node_index - 1
                    order = orders[order_idx]
                    
                    route['stops'].append({
                        "order_id": order['order_id'],
                        "stop_type": "pickup",  # Simplified for now
                        "client_id": order['pickup_client_id'],
                        "pallets": order['required_pallets'],
                        "weight_kg": order['weight_kg'],
                        "temperature_type": order['temperature_type'],
                        "sequence": len(route['stops']) + 1,
                    })
                    
                    route_load += order['required_pallets']
                
                # Get next index
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                
                # Calculate distance and time
                if previous_index != index:
                    from_node = manager.IndexToNode(previous_index)
                    to_node = manager.IndexToNode(index)
                    route_distance += distance_matrix[from_node][to_node]
                    route_time += time_matrix[from_node][to_node]
            
            route['total_distance_km'] = round(route_distance, 2)
            route['total_time_minutes'] = round(route_time, 2)
            route['total_pallets'] = route_load
            
            # Only include routes with stops
            if route['stops']:
                routes.append(route)
                total_distance += route_distance
                total_time += route_time
                total_load += route_load
        
        return {
            "status": "success",
            "routes": routes,
            "summary": {
                "total_distance_km": round(total_distance, 2),
                "total_time_hours": round(total_time / 60, 2),
                "total_pallets": total_load,
                "vehicles_used": len(routes),
                "orders_assigned": sum(len(r['stops']) for r in routes),
                "avg_utilization": round(
                    sum(r['total_pallets'] / vehicles[idx]['max_pallets'] 
                        for idx, r in enumerate(routes)) / len(routes) * 100, 2
                ) if routes else 0,
            },
            "objective_value": solution.ObjectiveValue(),
        }
    
    def _parse_time(self, time_str: str) -> int:
        """Convert HH:MM time string to minutes from midnight"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except:
            return 0
    
    def _temperature_to_int(self, temp_type: str) -> int:
        """Convert temperature type to integer for comparison"""
        mapping = {
            'frozen': 1,
            'chilled': 2,
            'ambient': 3,
        }
        return mapping.get(temp_type, 0)
    
    def _is_temperature_compatible(self, order_temp: str, vehicle_temp: str) -> bool:
        """Check if vehicle can carry order based on temperature"""
        # Multi-chamber vehicles can carry any temperature
        if vehicle_temp == 'multi':
            return True
        
        # Exact match
        if order_temp == vehicle_temp:
            return True
        
        # Frozen vehicles can carry chilled (but not optimal)
        if vehicle_temp == 'frozen' and order_temp == 'chilled':
            return True
        
        # Ambient vehicles can only carry ambient
        if vehicle_temp == 'ambient':
            return order_temp == 'ambient'
        
        return False
