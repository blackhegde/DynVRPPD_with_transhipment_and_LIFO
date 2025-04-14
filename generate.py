import numpy as np
import pandas as pd
import os
from scipy.spatial.distance import cdist

# Seed để đảm bảo reproducibility
np.random.seed(42)

# Thư mục lưu dataset
output_dir = "Dataset"
os.makedirs(output_dir, exist_ok=True)

# Cấu hình
SPEED = 1.0  # Tốc độ di chuyển (km/phút)
VEHICLE_CAPACITY = 50  # Tải trọng mỗi xe (giống nhau)
MIN_VEHICLES = 3  # Số lượng xe tối thiểu
MAX_VEHICLES = 10  # Số lượng xe tối đa

def calculate_travel_time_matrix(coords, speed):
    """Tính ma trận thời gian di chuyển giữa các điểm."""
    distances = cdist(coords, coords, metric='euclidean')
    travel_time = distances / speed
    return travel_time

# Sinh 100 dataset
for dataset_id in range(1, 101):
    # --- Phần 1: Tạo nodes ---
    n_customers = np.random.randint(20, 50)
    n_transshipments = np.random.randint(3, 8)
    n_nodes = 1 + n_customers + n_transshipments

    # Tọa độ ngẫu nhiên
    coords = np.random.uniform(0, 100, (n_nodes, 2))
    x_coords, y_coords = coords[:, 0], coords[:, 1]

    # Ma trận thời gian di chuyển
    travel_time_matrix = calculate_travel_time_matrix(coords, SPEED)

    # Depot (node 0)
    depot = {
        "node_id": 0, "x": x_coords[0], "y": y_coords[0],
        "demand": 0, "is_transshipment": 0, "is_depot": 1,
        "ready_time": 0, "due_time": 1000, "service_time": 0
    }

    # Khách hàng và điểm trung chuyển
    nodes = []
    node_counter = 1

    # Transshipment nodes
    for i in range(n_transshipments):
        nodes.append({
            "node_id": node_counter, "x": x_coords[node_counter], "y": y_coords[node_counter],
            "demand": 0, "is_transshipment": 1, "is_depot": 0,
            "ready_time": 0, "due_time": 1000, "service_time": np.random.randint(5, 15)
        })
        node_counter += 1

    # Customer nodes (pickup/delivery)
    for i in range(n_customers):
        demand = np.random.randint(-5, 6)  # Âm: pickup, Dương: delivery
        ready_time = np.random.uniform(0, 200)
        nodes.append({
            "node_id": node_counter, "x": x_coords[node_counter], "y": y_coords[node_counter],
            "demand": demand, "is_transshipment": 0, "is_depot": 0,
            "ready_time": ready_time, "due_time": ready_time + np.random.uniform(30, 120),
            "service_time": np.random.randint(10, 30)
        })
        node_counter += 1

    # --- Phần 2: Tạo đội xe ---
    n_vehicles = np.random.randint(MIN_VEHICLES, MAX_VEHICLES + 1)
    vehicles = []
    for vehicle_id in range(1, n_vehicles + 1):
        vehicles.append({
            "vehicle_id": vehicle_id,
            "capacity": VEHICLE_CAPACITY,
            "start_node": 0,  # Xuất phát từ depot
            "end_node": 0,    # Kết thúc tại depot
            "fixed_cost": 100  # Chi phí cố định (nếu cần)
        })

    # --- Phần 3: Lưu dữ liệu ---
    # Lưu nodes
    df_nodes = pd.DataFrame([depot] + nodes)
    df_nodes.to_csv(f"{output_dir}/dataset_{dataset_id}_nodes.csv", index=False)

    # Lưu ma trận thời gian
    pd.DataFrame(travel_time_matrix).to_csv(
        f"{output_dir}/dataset_{dataset_id}_travel_time_matrix.csv",
        index=False, header=False
    )

    # Lưu thông tin xe
    df_vehicles = pd.DataFrame(vehicles)
    df_vehicles.to_csv(f"{output_dir}/dataset_{dataset_id}_vehicles.csv", index=False)

print(f"Đã sinh 100 dataset vào thư mục {output_dir}/")