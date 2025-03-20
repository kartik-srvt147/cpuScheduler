from queue import PriorityQueue

def fcfs(processes):
    """
    First-Come-First-Serve scheduling algorithm.
    Processes are scheduled in order of arrival.
    """
    processes.sort(key=lambda x: x['arrival'])
    start_time, result = 0, []
    for process in processes:
        start_time = max(start_time, process['arrival'])
        result.append((process['pid'], start_time, start_time + process['burst']))
        start_time += process['burst']
    return result


def optimized_sjf(processes):
    """
    Optimized Shortest Job First using a priority queue for better performance.
    """
    if not processes:
        return []

    # Create a copy of processes to avoid modifying the original data
    processes = [p.copy() for p in processes]

    # Sort by arrival time
    processes.sort(key=lambda x: x['arrival'])

    result = []
    time = processes[0]['arrival']
    pq = PriorityQueue()  # Priority queue for ready processes
    next_process_idx = 0

    while next_process_idx < len(processes) or not pq.empty():
        # Add all processes that have arrived to the priority queue
        while next_process_idx < len(processes) and processes[next_process_idx]['arrival'] <= time:
            # Queue contains (burst_time, arrival_time, process_id)
            # Arrival time is used as a tie-breaker
            p = processes[next_process_idx]
            pq.put((p['burst'], p['arrival'], p['pid']))
            next_process_idx += 1

        if pq.empty():
            # If no process is ready, jump to the next arrival
            if next_process_idx < len(processes):
                time = processes[next_process_idx]['arrival']
                continue
            else:
                break

        # Get the process with the shortest burst time
        burst, arrival, pid = pq.get()

        # Add to result
        result.append((pid, time, time + burst))

        # Update time
        time += burst

    return result


def srtf(processes):
    """
    Shortest Remaining Time First (Preemptive SJF) algorithm implementation.
    Fixed to correctly handle process preemption and Gantt chart creation.
    """
    if not processes:
        return []

    # Create a copy of processes to avoid modifying the original data
    processes = [p.copy() for p in processes]

    # Sort processes by arrival time
    processes.sort(key=lambda x: x['arrival'])

    # Initialize variables
    n = len(processes)
    current_time = processes[0]['arrival']
    completed = 0
    remaining_time = {p['pid']: p['burst'] for p in processes}

    # To track if a process is in the result already
    last_scheduled = None
    result = []

    while completed < n:
        # Find the process with minimum remaining time among the arrived processes
        min_remaining = float('inf')
        selected_pid = None

        for process in processes:
            if process['arrival'] <= current_time and remaining_time[process['pid']] > 0:
                if remaining_time[process['pid']] < min_remaining:
                    min_remaining = remaining_time[process['pid']]
                    selected_pid = process['pid']

        # If no process is available, jump to the next arrival time
        if selected_pid is None:
            next_arrival = float('inf')
            for process in processes:
                if process['arrival'] > current_time and remaining_time[process['pid']] > 0:
                    next_arrival = min(next_arrival, process['arrival'])

            if next_arrival == float('inf'):
                break  # No more processes to execute

            current_time = next_arrival
            continue

        # If there's a context switch, end the previous process's execution segment
        if last_scheduled is not None and last_scheduled != selected_pid and result and result[-1][0] == last_scheduled:
            result[-1] = (result[-1][0], result[-1][1], current_time)

        # If starting a new process or resuming after preemption
        if last_scheduled != selected_pid:
            result.append((selected_pid, current_time, None))  # End time will be filled later

        # Determine how long this process will run
        next_event_time = float('inf')

        # Check if another process will arrive before this one finishes
        for process in processes:
            if process['arrival'] > current_time and process['arrival'] < current_time + remaining_time[selected_pid]:
                next_event_time = min(next_event_time, process['arrival'])

        # Calculate execution time for this segment
        execution_time = min(remaining_time[selected_pid],
                             next_event_time - current_time if next_event_time != float('inf') else remaining_time[
                                 selected_pid])

        # Update current time and remaining time
        current_time += execution_time
        remaining_time[selected_pid] -= execution_time

        # If the process just finished
        if remaining_time[selected_pid] == 0:
            completed += 1
            # Complete the last entry
            result[-1] = (result[-1][0], result[-1][1], current_time)
            last_scheduled = None
        else:
            last_scheduled = selected_pid
            # If we're approaching a new arrival, we need to close this segment
            if next_event_time != float('inf'):
                result[-1] = (result[-1][0], result[-1][1], current_time)

    # Make sure all segments have end times
    for i in range(len(result)):
        if result[i][2] is None:
            result[i] = (result[i][0], result[i][1], current_time)

    # Merge consecutive segments for the same process
    merged_result = []
    for pid, start, end in result:
        if merged_result and merged_result[-1][0] == pid and merged_result[-1][2] == start:
            merged_result[-1] = (pid, merged_result[-1][1], end)
        else:
            merged_result.append((pid, start, end))

    return merged_result


def optimized_round_robin(processes, quantum):
    """
    Optimized Round Robin scheduling algorithm that avoids unnecessary iterations
    by jumping to the next event (arrival or quantum completion) rather than
    incrementing time one by one.
    """
    if not processes:
        return []

    # Create a copy of processes to avoid modifying the original data
    processes = [p.copy() for p in processes]

    # Sort processes by arrival time
    processes.sort(key=lambda x: x['arrival'])

    # Initialize variables
    result = []
    ready_queue = []  # Processes that have arrived and are waiting for CPU
    time = processes[0]['arrival']  # Start time is the earliest arrival
    remaining_burst = {p['pid']: p['burst'] for p in processes}
    remaining_processes = len(processes)
    next_arrival_idx = 0

    while remaining_processes > 0:
        # Add newly arrived processes to the ready queue
        while next_arrival_idx < len(processes) and processes[next_arrival_idx]['arrival'] <= time:
            ready_queue.append(processes[next_arrival_idx])
            next_arrival_idx += 1

        if not ready_queue:
            # If no process is in the ready queue, jump to the next arrival time
            if next_arrival_idx < len(processes):
                time = processes[next_arrival_idx]['arrival']
                continue
            else:
                break  # No more processes to execute

        # Get the next process from the ready queue
        current_process = ready_queue.pop(0)
        pid = current_process['pid']

        # Calculate actual execution time (either quantum or remaining burst time)
        exec_time = min(quantum, remaining_burst[pid])

        # Add to result
        result.append((pid, time, time + exec_time))

        # Update time and remaining burst
        time += exec_time
        remaining_burst[pid] -= exec_time

        # Check if process is completed
        if remaining_burst[pid] == 0:
            remaining_processes -= 1
        else:
            # Process still has work to do, check if any new processes have arrived
            # before adding it back to the ready queue
            arrived_during_execution = []
            while next_arrival_idx < len(processes) and processes[next_arrival_idx]['arrival'] <= time:
                arrived_during_execution.append(processes[next_arrival_idx])
                next_arrival_idx += 1

            # Add the preempted process back to the ready queue after newly arrived processes
            ready_queue.extend(arrived_during_execution)
            ready_queue.append(current_process)

    return result if result else [(0, 0, 0)]  # Ensure non-empty result to avoid plotting errors


def priority_scheduling(processes):
    """
    Non-preemptive Priority Scheduling with fixed handling of arrival times.
    Lower priority value indicates higher priority.
    """
    if not processes:
        return []

    # Create a copy of processes to avoid modifying the original data
    processes = [p.copy() for p in processes]

    # Sort by arrival time initially
    processes.sort(key=lambda x: x['arrival'])

    result = []
    time = processes[0]['arrival']
    remaining = len(processes)
    completed = set()

    while remaining > 0:
        # Find available processes that have arrived
        available = [p for p in processes if p['arrival'] <= time and p['pid'] not in completed]

        if not available:
            # Jump to next process arrival
            next_arrival = min([p['arrival'] for p in processes if p['pid'] not in completed])
            time = next_arrival
            continue

        # Find process with highest priority (lowest priority number)
        selected = min(available, key=lambda x: x['priority'])

        # Schedule the process
        result.append((selected['pid'], time, time + selected['burst']))

        # Update time and mark process as completed
        time += selected['burst']
        completed.add(selected['pid'])
        remaining -= 1

    return result
