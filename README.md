# 🖥️ CPU Scheduler Simulator

A visual, interactive CPU scheduling algorithm simulator built with Python and Tkinter.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)

## 📋 Overview

This application demonstrates various CPU scheduling algorithms with an intuitive graphical interface. It provides real-time visualization of process execution and detailed performance metrics to help understand the behavior of different scheduling algorithms.

## ✨ Features

- **Multiple Scheduling Algorithms**:
  - First-Come-First-Serve (FCFS)
  - Shortest Job First (SJF)
  - Shortest Remaining Time First (SRTF)
  - Round Robin (with configurable time quantum)
  - Priority Scheduling

- **Interactive Process Management**:
  - Add processes with customizable parameters (PID, arrival time, burst time, priority)
  - Delete or reset process entries
  - Dynamic process table view

- **Visual Representation**:
  - Color-coded Gantt charts for process execution visualization
  - Clear process identification and timing information

- **Comprehensive Performance Metrics**:
  - Average waiting time
  - Average turnaround time
  - CPU utilization percentage
  - Process throughput
  - Detailed per-process statistics

## 🚀 Installation & Setup

### Prerequisites
- Python 3.6+
- tkinter
- ttkbootstrap
- matplotlib

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/kartik-srvt147/cpuScheduler.py.git
   cd cpuScheduler.py
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python cpuscheduler.py
   ```

## 🛠️ Usage

1. **Adding Processes**:
   - Enter the Process ID, Arrival Time, Burst Time, and Priority
   - Click "Add Process" to add it to the table

2. **Selecting a Scheduling Algorithm**:
   - Choose from the dropdown menu (FCFS, SJF, SRTF, Round Robin, Priority)
   - For Round Robin, specify a Time Quantum

3. **Running the Scheduler**:
   - Click "Run Scheduler" to execute the selected algorithm
   - View the Gantt chart and performance metrics below

4. **Managing Processes**:
   - Select a process and click "Delete" to remove it
   - Click "Reset" to clear all processes

## 🧮 Algorithms Explained

- **FCFS**: First-Come-First-Serve - Non-preemptive, processes scheduled in arrival order
- **SJF**: Shortest Job First - Non-preemptive, processes with shortest burst time first
- **SRTF**: Shortest Remaining Time First - Preemptive version of SJF
- **Round Robin**: Time-sliced scheduling with a quantum
- **Priority**: Non-preemptive scheduling based on priority values (lower number = higher priority)

## 📊 Performance Metrics

- **Average Waiting Time**: Average time processes spend waiting in the ready queue
- **Average Turnaround Time**: Average time from process arrival to completion
- **CPU Utilization**: Percentage of time the CPU is busy processing
- **Throughput**: Number of processes completed per unit time

## 📝 Note

Currently, all code is contained in a single file. A proper code file structure will be implemented in upcoming updates.

## 📸 Screenshots

A simple Round-Robin Scheduling algorithm based gantt chart along with the perfromance metrics.

## 🔜 Future Enhancements

- Improved code organization with proper file structure
- Additional scheduling algorithms (MFQ, Lottery Scheduling)
- Export functionality for metrics and charts
- Animation of process execution
- Batch process import/generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Kartik - [@kartik-srvt147](https://github.com/kartik-srvt147)

Project Link: [https://github.com/kartik-srvt147/cpuScheduler.py](https://github.com/kartik-srvt147/cpuScheduler.py)
