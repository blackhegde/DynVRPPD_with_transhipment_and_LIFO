#import problem models từ thư mục src/models, là thư mục cha của algorithms
from ..models.problem import DPDPTL
from models import problem


class CWSaving(DPDPTL):
    def __init__(self, problem: DPDPTL):
        self.problem = problem
        self.time_matrix = problem.time_matrix
        self.orders = problem.orders
        self.vehicles = problem.vehicles

    def calculate_savings(self):
        """
        Implement the Clarke-Wright savings calculation logic here.
        """
        # Tính toán giá trị tiết kiệm giữa các cặp điểm
        savings = []
        for i in range(len(self.orders)):
            for j in range(i + 1, len(self.orders)):
                if i != j:
                    # Giả sử orders[i] và orders[j] là hai điểm cần tính toán
                    # saving = time[i] + time[j] - time[i][j]
                    saving = self.time_matrix[self.orders[i].pickup][self.orders[j].pickup] + \
                    savings.append((saving, i, j))
        pass

        # Sắp xếp các giá trị tiết kiệm theo thứ tự giảm dần
        return sorted(savings, reverse=True, key=lambda x: x[0])
    
    # xây dưng intial solution từ saving
    def build_initial_solution(self):
        # Tính toán giá trị tiết kiệm
        savings = self.calculate_savings()

        # Khởi tạo các lộ trình
        routes = [[o.pickup_node, o.delivery_node] for o in self.orders]  # Mỗi order là một lộ trình riêng

        # Thêm các cặp điểm vào các lộ trình dựa trên giá trị tiết kiệm
        for saving, i, j in savings:
            # Logic để thêm i và j vào các lộ trình
            route_i = self.find_route(routes, i)
            route_j = self.find_route(routes, j)

            # Kiểm tra hợp lệ, không trùng route, không vượt quá capacity, không vi phạm LIFO
            if (route_i != route_j and
                self.check_capacity(route_i, route_j) and
                self.check_lifo(route_i) and
                self.check_lifo(route_j)):

                # Hợp nhất route i và j
                new_route = self.merge_routes(route_i, route_j)
                # Xóa route cũ
                routes.remove(route_i)
                routes.remove(route_j)
                # Thêm route mới vào danh sách
                routes.append(new_route)
            pass # pass để không bị lỗi indent

        return routes
    # kiểm tra tổng demand không vượt quá capacity
    def check_capacity(self, route1, route2):
        total_demand = sum(self.problem.nodes[i].demand for i in route1) + sum(self.problem.nodes[i].demand for i in route2)
        return total_demand <= self.capacity
    
    # kiểm tra rang buoc LIFO constraint
    def check_lifo (self, route):
        stack = []
        for node in route:
            if node.demand < 0: # pickup
                stack.append(node)
            else: # delivery
                if not stack or stack[-1].id != node.id:    # kiểm tra xem có node nào trong stack không
                    return False
                stack.pop()
        return True
    
    # Tìm route có chứa order có index order_idx
    def find_route(self, routes, order_idx):
        target_pickup = self.orders[order_idx].pickup
        for route in routes:
            if target_pickup in route:
                return route
        return None
    
    # Hợp nhất hai route thành một route mới
    def merge_routes(self, route1, route2):
        # Hợp nhất tại pickup node
        pickup_node = self.orders[route1[-1]].pickup
        delivery_node = self.orders[route2[-1]].delivery
        new_route = route1 + [pickup_node] + route2 + [delivery_node]
        return new_route
