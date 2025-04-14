from src.algorithms.dpdptl import DPDPTL

class CWSaving(DPDPTL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_savings(self):
        """
        Implement the Clarke-Wright savings calculation logic here.
        """
        # Tính toán giá trị tiết kiệm giữa các cặp điểm
        savings = []
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                if i != j:
                    # Giả sử nodes[i] và nodes[j] là hai điểm cần tính toán
                    # saving = time[i] + time[j] - time[i][j]
                    saving = self.time_matrix[i][0] + self.time_matrix[j][0] - self.time_matrix[i][j]
                    savings.append((saving, i, j))
        pass

    def solve(self):
        """
        Override the solve method to use the Clarke-Wright savings approach.
        """
        self.calculate_savings()
        # Add logic to construct routes based on savings
        pass