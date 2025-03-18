# 🖥️ CPU Scheduler Simulator

![GitHub stars](https://img.shields.io/github/stars/yourusername/cpuScheduler?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/cpuScheduler?style=social)
![License](https://img.shields.io/badge/license-MIT-blue)

> An interactive CPU scheduling algorithm simulator with visualizations and performance metrics.

![CPU Scheduler](https://github.com/yourusername/cpuScheduler/raw/main/screenshot.png)

## ✨ Features

### Supported Scheduling Algorithms

- **First-Come-First-Serve (FCFS)**  
  Non-preemptive scheduling based on arrival time

- **Shortest Job First (SJF)**  
  Non-preemptive scheduling prioritizing shortest burst time

- **Shortest Remaining Time First (SRTF)**  
  Preemptive version of SJF, dynamically switching to shorter processes

- **Round Robin**  
  Time-sliced scheduling with customizable quantum value

- **Priority Scheduling**  
  Non-preemptive scheduling based on priority values

### User Interface

- **Intuitive Process Management**  
  Easy-to-use controls to add, delete, and reset processes

- **Real-time Visualization**  
  Color-coded Gantt charts showing process execution timelines

- **Comprehensive Metrics**  
  Detailed statistics and performance analysis

- **Modern Design**  
  Clean UI with the ttkbootstrap "solar" theme

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Libraries:
  ```
  tkinter
  ttkbootstrap
  matplotlib
  ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cpuScheduler.git
   cd cpuScheduler
   ```

2. **Install dependencies**
   ```bash
   pip install matplotlib ttkbootstrap
   ```

3. **Launch the application**
   ```bash
   python cpu_scheduler.py
   ```

## 📖 How to Use

### 1. Add Process Details
- Enter process ID, arrival time, burst time, and priority
- Click "Add Process" to include in the simulation

### 2. Select Algorithm
- Choose from the dropdown menu
- For Round Robin, set your desired time quantum

### 3. Run Simulation
- Click "Run Scheduler" to execute
- View the scheduling visualization in the Gantt chart

### 4. Analyze Results
- Review performance metrics:
  - Average Waiting Time
  - Average Turnaround Time
  - CPU Utilization
  - Throughput
- Examine per-process statistics in the detailed table

## 📊 Performance Metrics Explained

| Metric | Description |
|--------|-------------|
| **Average Waiting Time** | Mean time processes spend in the ready queue |
| **Average Turnaround Time** | Mean time from arrival to completion |
| **CPU Utilization** | Percentage of time CPU is actively processing |
| **Throughput** | Number of processes completed per unit time |

## Algorithm Comparison

| Algorithm | Preemptive | Advantages | Best For |
|-----------|------------|------------|----------|
| FCFS | No | Simple, easy to implement | Batch systems |
| SJF | No | High throughput | Known burst times |
| SRTF | Yes | Optimal average waiting time | Interactive systems |
| Round Robin | Yes | Fair CPU distribution | Time-sharing systems |
| Priority | No | Important tasks first | Systems with varied task importance |

## Project Structure

```
cpuScheduler/
├── cpu_scheduler.py    # Main application file
├── README.md           # Project documentation
├── screenshot.png      # Application screenshot
└── LICENSE             # License information
```

## 👥 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Operating Systems theory for the algorithm implementations
- The tkinter and matplotlib communities
- All contributors and users of this educational tool

---

<p align="center">
  Made with ❤️ for OS enthusiasts and Computer Science students
</p>

<p align="center">
  <a href="https://github.com/yourusername">GitHub</a> •
  <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
</p>
