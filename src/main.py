from src.models.problem import DPDPTL
from algorithms.cw_saving import CWSaving
from src.algorithms.alns_q_learning import ALNS_Q_Learning
from src.algorithms.dynamic_adjustment import DynamicAdjustment
from src.utils.data_loader import load_data
from src.utils.simulation import (
    get_new_orders,
    get_unfinished_orders,
    get_key_points,
    execute_solution
)

def main():
    # Khởi tạo bài toán
    problem = DPDPTL()
    
    # Load data (nodes, orders, vehicles, distance matrix)
    load_data(problem)
    
    # khởi tạo solution ban đầu
    cw = CWSaving(problem)
    initial_solution = cw.generate_initial_solution()
    
    # Cải thiện kết quả với ALNS Q-Learning
    alns = ALNS_Q_Learning(problem)
    optimized_solution = alns.run(initial_solution)
    
    # Xử lý dynamic với timélice
    time_slices = [5, 10, 15, 20]  # hours
    current_time = 0
    current_solution = optimized_solution
    
    for t in time_slices:
        # Advance time
        current_time = t
        problem.current_time = current_time
        
        # Lấy đơn hàng mới trong timeslice này
        new_orders = get_new_orders(problem, current_time)
        
        # Lấy đơn hàng chưa hoàn thành
        unfinished_orders = get_unfinished_orders(problem, current_solution, current_time)
        
        # Lấy vị chí vehicle hiện tại(key points)
        key_points = get_key_points(problem, current_solution, current_time)
        
        # Điều chỉnh solution với các chiến thuật
        da = DynamicAdjustment(problem)
        current_solution = da.adjust_solution(
            current_solution, new_orders, unfinished_orders, key_points
        )
        
        # Thực hiện solution hiện tại
        execute_solution(problem, current_solution, current_time)
    
    print("Final solution cost:", alns.calculate_cost(current_solution))

if __name__ == "__main__":
    main()