import tkinter as tk
from tkinter import ttk

def display_metrics(frame, summary_metrics, detailed_metrics):
    """
    Display performance metrics in the specified frame.
    
    Args:
        frame: Tkinter frame to display metrics in
        summary_metrics: Dictionary containing summary metrics
        detailed_metrics: List of dictionaries with per-process metrics
    """
    # Clear previous content
    for widget in frame.winfo_children():
        widget.destroy()
    
    if not summary_metrics or not detailed_metrics:
        ttk.Label(frame, text="No metrics available.").pack(anchor="w", padx=10)
        return
    
    # Display summary metrics
    metrics_text = f"""
    Performance Metrics:
    - Average Waiting Time: {summary_metrics['avg_waiting_time']:.2f} time units
    - Average Turnaround Time: {summary_metrics['avg_turnaround_time']:.2f} time units
    - CPU Utilization: {summary_metrics['cpu_utilization']:.2f}%
    - Throughput: {summary_metrics['throughput']:.4f} processes/time unit
    """
    
    ttk.Label(frame, text=metrics_text, justify="left").pack(anchor="w", padx=10)
    
    # Create a table for detailed per-process metrics
    process_metrics_frame = ttk.Frame(frame)
    process_metrics_frame.pack(pady=5, fill="x", expand=True)
    
    # Define table columns
    columns = ("Process ID", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time")
    process_metrics_table = ttk.Treeview(process_metrics_frame, columns=columns, show="headings")
    
    # Configure columns
    for col in columns:
        process_metrics_table.heading(col, text=col)
        process_metrics_table.column(col, width=120)
    
    # Add rows for each process
    for process in detailed_metrics:
        process_metrics_table.insert("", "end", values=(
            process['pid'],
            process['arrival'],
            process['burst'],
            process['completion'],
            process['turnaround'],
            process['waiting']
        ))
    
    # Add scrollbar if needed
    scrollbar = ttk.Scrollbar(process_metrics_frame, orient="vertical", command=process_metrics_table.yview)
    process_metrics_table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    process_metrics_table.pack(fill="both", expand=True)