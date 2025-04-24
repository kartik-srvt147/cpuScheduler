# visualization/comparison_display.py

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def create_comparison_window(parent, comparison_results):
    """
    Create a new window to display algorithm comparison results.
    
    Args:
        parent: Parent Tkinter window
        comparison_results: Dictionary with results for each algorithm
    """
    # Create a new top-level window
    comparison_window = tk.Toplevel(parent)
    comparison_window.title("Algorithm Comparison")
    comparison_window.geometry("900x700")
    
    # Create notebook for tabbed interface
    notebook = ttk.Notebook(comparison_window)
    notebook.pack(fill='both', expand=True)
    
    # Summary tab - shows all metrics in one view
    summary_frame = ttk.Frame(notebook)
    notebook.add(summary_frame, text="Summary")
    
    # Charts tab - shows visualizations
    charts_frame = ttk.Frame(notebook)
    notebook.add(charts_frame, text="Charts")
    
    # Gantt charts tab - shows all Gantt charts
    gantt_frame = ttk.Frame(notebook)
    notebook.add(gantt_frame, text="Gantt Charts")
    
    # Populate the summary tab with a table
    create_summary_table(summary_frame, comparison_results)
    
    # Create comparative charts
    create_comparison_charts(charts_frame, comparison_results)
    
    # Create Gantt charts for each algorithm
    create_all_gantt_charts(gantt_frame, comparison_results)

def create_summary_table(frame, comparison_results):
    """Create a table showing all algorithms and their metrics side by side"""
    # Create a frame for the table
    table_frame = ttk.Frame(frame)
    table_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Define the columns for the table
    columns = ["Metric"] + list(comparison_results.keys())
    
    # Create the table
    table = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Set column headings
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=120, anchor="center")
    
    # Set the first column width differently
    table.column("Metric", width=180, anchor="w")
    
    # Add the metrics data
    metrics = ["avg_waiting_time", "avg_turnaround_time", "cpu_utilization", "throughput"]
    metric_names = {
        "avg_waiting_time": "Average Waiting Time",
        "avg_turnaround_time": "Average Turnaround Time",
        "cpu_utilization": "CPU Utilization (%)",
        "throughput": "Throughput (proc/time)"
    }
    
    for metric in metrics:
        row_data = [metric_names[metric]]
        for algo in comparison_results.keys():
            if comparison_results[algo]["summary"]:
                value = comparison_results[algo]["summary"][metric]
                if metric == "cpu_utilization" or metric == "throughput":
                    formatted_value = f"{value:.2f}"
                else:
                    formatted_value = f"{value:.2f}"
                row_data.append(formatted_value)
            else:
                row_data.append("N/A")
        
        table.insert("", "end", values=row_data)
    
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    table.pack(fill="both", expand=True)
    
    # Add a "Best Algorithm" section
    best_frame = ttk.LabelFrame(frame, text="Best Algorithm Based On:")
    best_frame.pack(fill="x", padx=10, pady=10)
    
    # Find the best algorithms
    best_algorithms = find_best_algorithms(comparison_results)
    
    # Display the best algorithms
    for metric, algo in best_algorithms.items():
        text = f"{metric_names[metric]}: {algo}"
        ttk.Label(best_frame, text=text).pack(anchor="w", padx=5, pady=2)

def find_best_algorithms(comparison_results):
    """Find the best algorithm for each metric"""
    best = {}
    metrics = ["avg_waiting_time", "avg_turnaround_time", "cpu_utilization", "throughput"]
    
    for metric in metrics:
        best_value = None
        best_algo = None
        
        for algo, data in comparison_results.items():
            if data["summary"] and metric in data["summary"]:
                value = data["summary"][metric]
                
                # For waiting and turnaround times, lower is better
                # For CPU utilization and throughput, higher is better
                is_better = False
                
                if best_value is None:
                    is_better = True
                elif metric in ["avg_waiting_time", "avg_turnaround_time"]:
                    is_better = value < best_value
                else:  # cpu_utilization, throughput
                    is_better = value > best_value
                
                if is_better:
                    best_value = value
                    best_algo = algo
        
        best[metric] = best_algo
    
    return best

def create_comparison_charts(frame, comparison_results):
    """Create bar charts comparing metrics across algorithms"""
    # Create figure with subplots
    fig = Figure(figsize=(8, 6))
    
    # Create 2x2 grid of subplots for the 4 metrics
    ax1 = fig.add_subplot(221)  # Waiting Time
    ax2 = fig.add_subplot(222)  # Turnaround Time
    ax3 = fig.add_subplot(223)  # CPU Utilization
    ax4 = fig.add_subplot(224)  # Throughput
    
    algorithms = list(comparison_results.keys())
    
    # Waiting Time
    waiting_times = [comparison_results[algo]["summary"]["avg_waiting_time"] 
                     if comparison_results[algo]["summary"] else 0 for algo in algorithms]
    ax1.bar(algorithms, waiting_times)
    ax1.set_title("Avg. Waiting Time")
    ax1.tick_params(axis='x', rotation=45)
    
    # Turnaround Time
    turnaround_times = [comparison_results[algo]["summary"]["avg_turnaround_time"] 
                         if comparison_results[algo]["summary"] else 0 for algo in algorithms]
    ax2.bar(algorithms, turnaround_times)
    ax2.set_title("Avg. Turnaround Time")
    ax2.tick_params(axis='x', rotation=45)
    
    # CPU Utilization
    cpu_utils = [comparison_results[algo]["summary"]["cpu_utilization"] 
                 if comparison_results[algo]["summary"] else 0 for algo in algorithms]
    ax3.bar(algorithms, cpu_utils)
    ax3.set_title("CPU Utilization (%)")
    ax3.tick_params(axis='x', rotation=45)
    
    # Throughput
    throughputs = [comparison_results[algo]["summary"]["throughput"] 
                   if comparison_results[algo]["summary"] else 0 for algo in algorithms]
    ax4.bar(algorithms, throughputs)
    ax4.set_title("Throughput (proc/time)")
    ax4.tick_params(axis='x', rotation=45)
    
    fig.tight_layout()
    
    # Create canvas
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def create_all_gantt_charts(frame, comparison_results):
    """Create a Gantt chart for each algorithm"""
    # Create a canvas with scrollbar for the Gantt charts
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Add Gantt charts for each algorithm
    for i, (algo_name, data) in enumerate(comparison_results.items()):
        # Create a frame for this algorithm
        algo_frame = ttk.LabelFrame(scrollable_frame, text=algo_name)
        algo_frame.pack(fill="x", padx=10, pady=10, anchor="n")
        
        # Create the Gantt chart
        fig, ax = plt.subplots(figsize=(8, 2))
        
        schedule = data["schedule"]
        if not schedule or all(task[2] - task[1] == 0 for task in schedule):
            ttk.Label(algo_frame, text="No valid schedule to display").pack()
            continue
        
        # Define color palette for processes
        color_palette = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#A833FF', '#FFC300', '#008080', '#800080']
        process_colors = {}
        
        # Plot each task in the schedule
        y_pos = 0
        for task in schedule:
            pid, start, end = task
            
            # Assign colors to processes
            if pid not in process_colors:
                process_colors[pid] = color_palette[len(process_colors) % len(color_palette)]
            
            # Create the bar for this task
            ax.barh(y=y_pos, left=start, width=end - start, color=process_colors[pid], edgecolor="black")
            
            # Add process ID label
            ax.text(start + (end - start) / 2, y_pos, f"P{pid}", va='center', ha='center', 
                    color='white', fontsize=10, fontweight='bold')
            
            y_pos += 1
        
        # Configure chart appearance
        ax.set_xlabel("Time")
        ax.set_yticks([])
        ax.set_title(f"{algo_name} Schedule")
        
        # Add time markers
        ax.set_xticks([task[1] for task in schedule] + [schedule[-1][2]])
        
        canvas_widget = FigureCanvasTkAgg(fig, master=algo_frame)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill="both", expand=True)