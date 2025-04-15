import sys
from pathlib import Path
from algorithms.cw_saving import CWSaving
from src.models.problem import DPDPTL

# Thêm thư mục gốc vào PATH
sys.path.append(str(Path(__file__).parent.parent))

# Tạo dữ liệu test
def create_test_problem():
    nodes = [
        {"node_id": 0, "is_depot": True},
        {"node_id": 1, "demand": -3, "is_pickup": True, "paired_node": 4},  # P1 -> D1 (id 4)
        {"node_id": 2, "demand": -2, "is_pickup": True, "paired_node": 5},  # P2 -> D2
        {"node_id": 3, "is_transshipment": True},
        {"node_id": 4, "demand": 3, "is_delivery": True},
        {"node_id": 5, "demand": 2, "is_delivery": True}
    ]
    
    vehicles = [{"vehicle_id": 1, "capacity": 10, "lifo_capacity": 6}]
    time_matrix = [[0, 10, 15, 20, 30, 40],
                   [10, 0, 5, 10, 20, 30],
                   [15, 5, 0, 5, 15, 25],
                   [20, 10, 5, 0, 10, 20],
                   [30, 20, 15, 10, 0, 10],
                   [40, 30, 25, 20, 10, 0]]
    
    return DPDPTL(nodes, vehicles, time_matrix)

def test_cw_saving():
    problem = create_test_problem()
    solver = CWSaving(problem)
    routes = solver.build_initial_solution()
    
    print("Initial routes:")
    for route in routes:
        print(route)
    
    assert len(routes) <= len(problem.vehicles), "Số route vượt quá số xe"
    print("✅ Test passed!")

if __name__ == "__main__":
    test_cw_saving()