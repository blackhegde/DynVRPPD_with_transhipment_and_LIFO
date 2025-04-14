import numpy as np
import pandas as pd
import os
from scipy.spatial.distance import cdist

# Seed để đảm bảo reproducibility
np.random.seed(42)

# Thư mục lưu dataset
output_dir = "DPDPTL_Dataset"
os.makedirs(output_dir, exist_ok=True)

# ========================= CẤU HÌNH LỚP DATASET =========================
class DPDPTL_Dataset:
    def __init__(self):
        self.speed = 60  # km/h
        self.min_vehicles = 3
        self.max_vehicles = 8
        self.max_time = 480  # phút (8 tiếng)
        self.transfer_capacity_range = (10, 30)  # Giới hạn hàng tại transshipment

    def generate(self, dataset_id):
        # --------------------- PHẦN 1: TẠO NODES ---------------------
        n_customers = np.random.randint(30, 50)
        n_transshipments = np.random.randint(3, 6)
        n_nodes = 1 + n_customers + n_transshipments  # +1 cho depot

        # Tọa độ ngẫu nhiên (km)
        coords = np.random.uniform(0, 100, (n_nodes, 2))
        
        # Ma trận thời gian di chuyển (phút)
        distance_matrix = cdist(coords, coords, metric='euclidean')
        time_matrix = (distance_matrix / (self.speed / 60)).astype(int)  # km -> phút

        # Depot (node 0)
        nodes = [{
            "node_id": 0, "x": coords[0][0], "y": coords[0][1],
            "demand": 0, "is_transshipment": 0, "is_depot": 1,
            "ready_time": 0, "due_time": self.max_time, "service_time": 0
        }]

        # Transshipment nodes
        for i in range(1, 1 + n_transshipments):
            nodes.append({
                "node_id": i, "x": coords[i][0], "y": coords[i][1],
                "demand": 0, "is_transshipment": 1, "is_depot": 0,
                "ready_time": 0, "due_time": self.max_time,
                "service_time": np.random.randint(5, 15),  # Thời gian bốc/dỡ
                "transfer_capacity": np.random.randint(*self.transfer_capacity_range)
            })

        # Customer nodes (pickup/delivery)
        for i in range(1 + n_transshipments, n_nodes):
            demand = np.random.choice([-3, -2, -1, 1, 2, 3])  # Âm: pickup, Dương: delivery
            ready_time = np.random.randint(0, self.max_time - 120)  # Đảm bảo có đủ time window
            nodes.append({
                "node_id": i, "x": coords[i][0], "y": coords[i][1],
                "demand": demand, "is_transshipment": 0, "is_depot": 0,
                "ready_time": ready_time,
                "due_time": ready_time + np.random.randint(60, 180),
                "service_time": np.random.randint(5, 20),
                "is_dynamic": np.random.choice([0, 1], p=[0.7, 0.3]),  # 30% đơn động
                "dynamic_appear_time": np.random.randint(30, self.max_time - 60) if np.random.rand() > 0.7 else -1
            })

        # --------------------- PHẦN 2: TẠO VEHICLES ---------------------
        n_vehicles = np.random.randint(self.min_vehicles, self.max_vehicles + 1)
        vehicles = []
        for vehicle_id in range(1, n_vehicles + 1):
            capacity = np.random.choice([30, 50, 70])
            vehicles.append({
                "vehicle_id": vehicle_id,
                "capacity": capacity,
                "lifo_capacity": int(capacity * 0.6),  # 60% của tổng capacity
                "start_node": 0,  # Xuất phát từ depot
                "end_node": 0,    # Kết thúc tại depot
                "fixed_cost": 100 + capacity * 2  # Chi phí cố định phụ thuộc capacity
            })

        # --------------------- PHẦN 3: LƯU DỮ LIỆU ---------------------
        # Lưu nodes
        df_nodes = pd.DataFrame(nodes)
        df_nodes.to_csv(f"{output_dir}/dataset_{dataset_id}_nodes.csv", index=False)

        # Lưu ma trận thời gian
        pd.DataFrame(time_matrix).to_csv(
            f"{output_dir}/dataset_{dataset_id}_time_matrix.csv",
            index=False, header=False
        )

        # Lưu vehicles
        df_vehicles = pd.DataFrame(vehicles)
        df_vehicles.to_csv(f"{output_dir}/dataset_{dataset_id}_vehicles.csv", index=False)

        # Lưu orders (tách từ nodes)
        df_orders = df_nodes[(df_nodes["demand"] != 0)].copy()
        df_orders["order_id"] = range(1, len(df_orders) + 1)
        df_orders.to_csv(f"{output_dir}/dataset_{dataset_id}_orders.csv", index=False)

# ========================= SINH DATASET =========================
if __name__ == "__main__":
    generator = DPDPTL_Dataset()
    for dataset_id in range(1, 101):  # Sinh 100 dataset
        generator.generate(dataset_id)
    print(f"Đã sinh 100 dataset vào thư mục {output_dir}/")