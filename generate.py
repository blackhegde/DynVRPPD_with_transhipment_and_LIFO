import numpy as np
import pandas as pd
import os
from scipy.spatial.distance import cdist
from typing import List, Dict
from dataclasses import dataclass

# Seed để đảm bảo reproducibility
np.random.seed(42)

# Thư mục lưu dataset
output_dir = "Dataset"
os.makedirs(output_dir, exist_ok=True)
#large scale dataset dir
output_dir_large = "Dataset/large_scale"
os.makedirs(output_dir_large, exist_ok=True)
#small scale dataset dir
output_dir_small = "Dataset/small_scale"
os.makedirs(output_dir_small, exist_ok=True)

# CẤU HÌNH LỚP DATASET
class DPDPTL_Dataset:
    def __init__(self):
        self.speed = 60  # km/h
        self.min_vehicles = 3
        self.max_vehicles = 8
        self.max_time = 480  # phút (8 tiếng)
        self.transfer_capacity_range = (10, 30)  # Giới hạn hàng tại transshipment

    def generate(self, dataset_id, scale="smallscale"):
        #  TẠO NODES 
        if scale == "largescale":
            n_customers = np.random.randint(70, 100)  # Số lượng khách hàng lớn
            output_dir_scale = output_dir_large
        else:
            n_customers = np.random.randint(30, 50)  # Số lượng khách hàng nhỏ
            output_dir_scale = output_dir_small

        n_transshipments = np.random.randint(3, 6)  # Số lượng transshipment
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
            "ready_time": 0, "due_time": self.max_time, "service_time": 0,
            "order_id": -1, "is_dynamic": 0, "dynamic_appear_time": -1
        }]

        # Transshipment nodes
        for i in range(1, 1 + n_transshipments):
            nodes.append({
                "node_id": i, "x": coords[i][0], "y": coords[i][1],
                "demand": 0, "is_transshipment": 1, "is_depot": 0,
                "ready_time": 0, "due_time": self.max_time,
                "service_time": np.random.randint(5, 15),  # Thời gian bốc/dỡ
                "order_id": -1, "is_dynamic": 0, "dynamic_appear_time": -1,
                "transfer_capacity": np.random.randint(*self.transfer_capacity_range)
            })

        # Customer nodes (pickup/delivery)       
        # Tạo danh sách các cặp pickup và delivery
        pickup_indices = np.random.choice(range(1 + n_transshipments, n_nodes), size=(n_nodes - 1 - n_transshipments) // 2, replace=False)
        delivery_indices = [i for i in range(1 + n_transshipments, n_nodes) if i not in pickup_indices]

        # Tạo các cặp pickup và delivery với order_id
        order_id = 1
        for pickup, delivery in zip(pickup_indices, delivery_indices):
            # Pickup node
            ready_time = np.random.randint(0, self.max_time - 120)
            demand = np.random.randint(-4, -1)  # Âm: pickup
            nodes.append({
                "node_id": pickup, "x": coords[pickup][0], "y": coords[pickup][1],
                "demand": demand, "is_transshipment": 0, "is_depot": 0,
                "ready_time": ready_time,
                "due_time": ready_time + np.random.randint(60, 180),
                "service_time": np.random.randint(5, 20),
                "order_id": order_id  # Gán order_id
            })

            # Delivery node
            ready_time = np.random.randint(0, self.max_time - 120)
            nodes.append({
                "node_id": delivery, "x": coords[delivery][0], "y": coords[delivery][1],
                "demand": -demand,  # Dương: delivery
                "is_transshipment": 0, "is_depot": 0,
                "ready_time": ready_time,
                "due_time": ready_time + np.random.randint(60, 180),
                "service_time": np.random.randint(5, 20),
                "order_id": order_id  # Gán order_id
            })

            order_id += 1  # Tăng order_id cho cặp tiếp theo

        #  TẠO VEHICLES 
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
            })

        #  LƯU DỮ LIỆU 
        # Lưu nodes
        df_nodes = pd.DataFrame(nodes)
        df_nodes.to_csv(f"{output_dir_scale}/dataset_{dataset_id}_nodes.csv", index=False)

        # Lưu ma trận thời gian
        pd.DataFrame(time_matrix).to_csv(
            f"{output_dir_scale}/dataset_{dataset_id}_time_matrix.csv",
            index=False, header=False
        )

        # Lưu vehicles
        df_vehicles = pd.DataFrame(vehicles)
        df_vehicles.to_csv(f"{output_dir_scale}/dataset_{dataset_id}_vehicles.csv", index=False)

        # # Lưu orders (tách từ nodes)
        # df_orders = df_nodes[(df_nodes["demand"] != 0)].copy()
        # df_orders["order_id"] = range(1, len(df_orders) + 1)
        # df_orders.to_csv(f"{output_dir_scale}/dataset_{dataset_id}_orders.csv", index=False)

#  SINH DATASET 
if __name__ == "__main__":
    generator = DPDPTL_Dataset()
    for dataset_id in range(1, 100):  # Sinh 100 dataset nhỏ
        generator.generate(dataset_id, scale="smallscale")
    for dataset_id in range(1, 100):  # Sinh 50 dataset lớn
        generator.generate(dataset_id, scale="largescale")
    
    print(f"Đã sinh 100 dataset nhỏ vào thư mục {output_dir_small}/")
    print(f"Đã sinh 100 dataset lớn vào thư mục {output_dir_large}/")