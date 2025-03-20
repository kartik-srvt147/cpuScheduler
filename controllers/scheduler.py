from algorithms.scheduling import fcfs, optimized_sjf, srtf, optimized_round_robin, priority_scheduling
from algorithms.metrics import calculate_metrics

def run_scheduling_algorithm(algorithm, processes, time_quantum=None):
    """
    Run the selected scheduling algorithm and return the schedule and metrics.
    
    Args:
        algorithm: String name of the scheduling algorithm to use
        processes: List of process dictionaries
        time_quantum: Integer for Round Robin algorithm (default=None)
        
    Returns:
        schedule: List of tuples (pid, start_time, end_time)
        summary_metrics: Dictionary of summary performance metrics
        detailed_metrics: List of dictionaries with per-process metrics
    """
    # Check if there are processes to schedule
    if not processes:
        return [], None, None
    
    # Run the selected algorithm
    if algorithm == "FCFS":
        schedule = fcfs(processes)
    elif algorithm == "SJF":
        schedule = optimized_sjf(processes)
    elif algorithm == "SRTF":
        schedule = srtf(processes)
    elif algorithm == "Round Robin":
        quantum = time_quantum if time_quantum else 2
        schedule = optimized_round_robin(processes, quantum)
    elif algorithm == "Priority":
        schedule = priority_scheduling(processes)
    else:
        return [], None, None
    
    # Calculate performance metrics
    summary_metrics, detailed_metrics = calculate_metrics(schedule, processes)
    
    return schedule, summary_metrics, detailed_metrics
