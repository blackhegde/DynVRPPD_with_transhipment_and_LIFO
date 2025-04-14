# Mô hình bài toán DPDP-TL
# Định nghĩa các lớp và phương thức cần thiết cho bài toán DPDP-TL
class DPDPTL:
    def __init__(self, nodes, vehicles, time_matrix):
        self.nodes = nodes          # Danh sách nodes
        self.vehicles = vehicles    # Danh sách xe
        self.time_matrix = time_matrix  # Ma trận thời gian
        self.transshipments = [n for n in nodes if n.is_transshipment]
    
    def check_lifo(self, route):
        """Kiểm tra ràng buộc LIFO"""
        stack = []
        for node in route:
            if node.is_pickup:
                stack.append(node)
            else:
                if not stack or stack.pop().paired_node != node.id:
                    return False
        return True
   