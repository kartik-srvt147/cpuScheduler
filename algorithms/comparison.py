# algorithms/comparison.py

def compare_algorithms(processes, time_quantum=2):
    """
    Compare all scheduling algorithms using the same process set.
    
    Args:
        processes: List of process dictionaries
        time_quantum: Time quantum for Round Robin algorithm
        
    Returns:
        Dictionary containing results for each algorithm
    """
    from algorithms.scheduling import fcfs, optimized_sjf, srtf, optimized_round_robin, priority_scheduling
    from algorithms.metrics import calculate_metrics
    
    algorithms = {
        "FCFS": fcfs(processes),
        "SJF": optimized_sjf(processes),
        "SRTF": srtf(processes),
        "Round Robin": optimized_round_robin(processes, time_quantum),
        "Priority": priority_scheduling(processes)
    }
    
    results = {}
    
    for name, schedule in algorithms.items():
        summary, detailed = calculate_metrics(schedule, processes)
        results[name] = {
            "schedule": schedule,
            "summary": summary,
            "detailed": detailed
        }
    
    return results