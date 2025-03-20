import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_gantt_chart(schedule, frame):
    """
    Create and display a Gantt chart in the specified frame.
    
    Args:
        schedule: List of tuples (pid, start_time, end_time)
        frame: Tkinter frame to display the chart in
    """
    if not schedule or all(task[2] - task[1] == 0 for task in schedule):
        return None
    
    # Clear previous chart
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Define color palette for processes
    color_palette = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#A833FF', '#FFC300', '#008080', '#800080']
    process_colors = {}
    
    # Plot each task in the schedule
    y_pos = 0
    for i, task in enumerate(schedule):
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
    ax.set_xlabel("Time", color="white")
    ax.set_yticks([])
    ax.set_xticks([task[1] for task in schedule] + [schedule[-1][2]])
    
    # Display the chart in the frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()
    
    return canvas
