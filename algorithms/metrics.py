def calculate_metrics(schedule, processes):
    """
    Calculate performance metrics for the given schedule and processes.
    
    Args:
        schedule: List of tuples (pid, start_time, end_time)
        processes: List of dictionaries with process details
        
    Returns:
        Dictionary containing various performance metrics
    """
    if not schedule:
        return None, None

    # Create a dictionary for processes for easy lookup
    process_dict = {p['pid']: p for p in processes}

    # Get the end time of the last process to complete
    max_completion_time = max(task[2] for task in schedule)

    # Dictionary to track completion time for each process
    completion_times = {}

    # Dictionary to calculate total running time for each process
    running_times = {}

    # For each process, find its segments in the schedule
    for pid, start, end in schedule:
        if pid not in running_times:
            running_times[pid] = 0
        running_times[pid] += (end - start)

        # Update completion time (we want the max time when the process finishes)
        completion_times[pid] = max(completion_times.get(pid, 0), end)

    # Calculate waiting and turnaround times for each process
    waiting_times = {}
    turnaround_times = {}

    for pid in completion_times:
        # Turnaround time = completion time - arrival time
        turnaround_times[pid] = completion_times[pid] - process_dict[pid]['arrival']

        # Waiting time = turnaround time - burst time
        waiting_times[pid] = turnaround_times[pid] - process_dict[pid]['burst']

    # Calculate averages
    avg_waiting_time = sum(waiting_times.values()) / len(waiting_times) if waiting_times else 0
    avg_turnaround_time = sum(turnaround_times.values()) / len(turnaround_times) if turnaround_times else 0

    # Calculate CPU utilization
    # Get the first arrival time
    first_arrival = min(p['arrival'] for p in processes)

    # Total time from first arrival to completion
    total_time = max_completion_time - first_arrival

    # Sum of all process execution times
    total_execution_time = sum(end - start for _, start, end in schedule)

    # CPU utilization as a percentage
    cpu_utilization = (total_execution_time / total_time) * 100 if total_time > 0 else 0

    # Calculate throughput (processes per unit time)
    number_of_processes = len(set(pid for pid, _, _ in schedule))
    throughput = number_of_processes / total_time if total_time > 0 else 0

    # Create a summary dictionary
    summary = {
        'avg_waiting_time': avg_waiting_time,
        'avg_turnaround_time': avg_turnaround_time,
        'cpu_utilization': cpu_utilization,
        'throughput': throughput
    }
    
    # Create detailed metrics per process
    detailed_metrics = []
    for pid in sorted(completion_times.keys()):
        detailed_metrics.append({
            'pid': pid,
            'arrival': process_dict[pid]['arrival'],
            'burst': process_dict[pid]['burst'],
            'completion': completion_times[pid],
            'turnaround': turnaround_times[pid],
            'waiting': waiting_times[pid]
        })
    
    return summary, detailed_metrics