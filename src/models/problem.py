# Mô hình bài toán DPDP-TL
# Định nghĩa các lớp và phương thức cần thiết cho bài toán DPDP-TL
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Node:
    id: int
    type: str  # 'pickup', 'delivery', 'transshipment'
    x: float   # x coordinate
    y: float   # y coordinate

@dataclass
class Order:
    id: int
    pickup_node: int
    delivery_node: int
    start_time: float
    end_time: float
    weight: float
    items: List[Dict] 

@dataclass
class Vehicle:
    id: int
    capacity: float
    current_load: float = 0
    current_location: int = None  # node id
    route: List[int] = None       # list of node ids
    arrival_times: List[float] = None
    departure_times: List[float] = None
    
class DPDPTL:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.orders: Dict[int, Order] = {}
        self.vehicles: Dict[int, Vehicle] = {}
        self.transshipment_nodes: List[int] = []
        self.time_horizon: float = 24 * 60  
        self.current_time: float = 0
        self.distance_matrix: Dict[Tuple[int, int], float] = {}
        self.travel_time_matrix: Dict[Tuple[int, int], float] = {}
   