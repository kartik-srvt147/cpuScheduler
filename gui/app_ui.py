import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap.constants import *

from controllers.scheduler import run_scheduling_algorithm
from visualization.gantt_chart import create_gantt_chart
from visualization.metrics_display import display_metrics

def create_ui(root):
    """
    Create the main UI components for the CPU Scheduler application.
    
    Args:
        root: The Tkinter root window
    """
    # Create a main frame with scrollbars
    main_container = ttk.Frame(root)
    main_container.pack(fill="both", expand=True)

    # Add a Canvas that will contain the scrollable content
    canvas = tk.Canvas(main_container)
    scrollbar_y = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(main_container, orient="horizontal", command=canvas.xview)

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Place the scrollbars
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    # Create a frame inside the canvas that will contain all your UI elements
    content_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Define the frames for various components
    frame_title = ttk.Frame(content_frame)
    frame_input = ttk.Frame(content_frame)
    frame_table = ttk.Frame(content_frame)
    frame_controls = ttk.Frame(content_frame)
    frame_chart = ttk.Frame(content_frame)
    frame_metrics = ttk.Frame(content_frame)
    frame_explanation = ttk.Frame(content_frame)

    # Pack frames in order
    frame_title.pack(side="top", pady=(10, 0))
    frame_input.pack(pady=10)
    frame_table.pack()
    frame_controls.pack(pady=10)
    frame_chart.pack(pady=10, fill="both", expand=True)
    frame_metrics.pack(pady=10, padx=10, fill="both", expand=True)
    frame_explanation.pack(pady=10, padx=10, fill="x")

    # Create title
    ttk.Label(frame_title, text="CPU Scheduler", font=("Arial", 16)).pack()

    # Create input fields
    entry_pid = ttk.Entry(frame_input, width=5)
    entry_arrival = ttk.Entry(frame_input, width=5)
    entry_burst = ttk.Entry(frame_input, width=5)
    entry_priority = ttk.Entry(frame_input, width=5)

    entry_pid.grid(row=0, column=1)
    entry_arrival.grid(row=0, column=3)
    entry_burst.grid(row=0, column=5)
    entry_priority.grid(row=0, column=7)

    ttk.Label(frame_input, text="PID").grid(row=0, column=0)
    ttk.Label(frame_input, text="Arrival").grid(row=0, column=2)
    ttk.Label(frame_input, text="Burst").grid(row=0, column=4)
    ttk.Label(frame_input, text="Priority").grid(row=0, column=6)

    # Create process table
    columns = ("PID", "Arrival", "Burst", "Priority")
    table = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=80)
    table.pack()

    # Define algorithm variable and time quantum
    algo_var = tk.StringVar(value="FCFS")
    time_quantum = ttk.Entry(frame_controls, width=5)
    label_quantum = ttk.Label(frame_controls, text="Time Quantum:")

    # Function to add a new process
    def add_process():
        try:
            pid = int(entry_pid.get())
            arrival = int(entry_arrival.get())
            burst = int(entry_burst.get())
            priority = int(entry_priority.get())
            table.insert("", "end", values=(pid, arrival, burst, priority))
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    # Function to delete selected process
    def delete_process():
        selected_item = table.selection()
        if selected_item:
            table.delete(selected_item)

    # Function to reset the table
    def reset_table():
        for row in table.get_children():
            table.delete(row)

    # Function to update time quantum visibility
    def update_time_quantum_visibility(*args):
        if algo_var.get() == "Round Robin":
            label_quantum.pack(side="left", padx=5)
            time_quantum.pack(side="left", padx=5)
        else:
            label_quantum.pack_forget()
            time_quantum.pack_forget()

    # Function to calculate scheduling
    def calculate_scheduling():
        algorithm = algo_var.get()
        try:
            processes = []
            for row in table.get_children():
                values = table.item(row)['values']
                processes.append({
                    'pid': int(values[0]), 
                    'arrival': int(values[1]), 
                    'burst': int(values[2]), 
                    'priority': int(values[3])
                })

            quantum = int(time_quantum.get()) if time_quantum.get() else 2
            
            # Run the scheduler
            schedule, summary_metrics, detailed_metrics = run_scheduling_algorithm(
                algorithm, processes, quantum if algorithm == "Round Robin" else None
            )
            
            # Display results
            create_gantt_chart(schedule, frame_chart)
            display_metrics(frame_metrics, summary_metrics, detailed_metrics)
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    # Add controls
    ttk.Button(frame_input, text="Add Process", command=add_process, bootstyle=INFO).grid(row=0, column=8, padx=5)
    ttk.Button(frame_input, text="Delete", command=delete_process, bootstyle=WARNING).grid(row=0, column=9, padx=5)
    ttk.Button(frame_input, text="Reset", command=reset_table, bootstyle=PRIMARY).grid(row=0, column=10, padx=5)
    
    # Algorithm selection
    algo_var.trace("w", update_time_quantum_visibility)
    algo_menu = ttk.Combobox(frame_controls, textvariable=algo_var,
                           values=["FCFS", "SJF", "SRTF", "Round Robin", "Priority"],
                           state="readonly")
    algo_menu.pack(side="left", padx=5)
    
    # Run button
    ttk.Button(frame_controls, text="Run Scheduler", command=calculate_scheduling, bootstyle=INFO).pack(side="left", padx=5)

    # Add explanation
    explanation_text = """
FCFS: First-Come-First-Serve - Non-preemptive, processes scheduled in arrival order
SJF: Shortest Job First - Non-preemptive, processes with shortest burst time first
SRTF: Shortest Remaining Time First - Preemptive version of SJF
Round Robin: Time-sliced scheduling with a quantum
Priority: Non-preemptive scheduling based on priority values

Performance Metrics:
- Average Waiting Time: Average time processes spend waiting in the ready queue
- Average Turnaround Time: Average time from process arrival to completion
- CPU Utilization: Percentage of time the CPU is busy processing
- Throughput: Number of processes completed per unit time
"""
    ttk.Label(frame_explanation, text=explanation_text, justify="left").pack(anchor="w")

    # Adjust canvas window size when frame size changes
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    content_frame.bind("<Configure>", on_frame_configure)

    # Add mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Initialize UI based on current algorithm
    update_time_quantum_visibility()
