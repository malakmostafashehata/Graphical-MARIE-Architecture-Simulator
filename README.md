# Graphical MARIE Architecture Simulator

## 📌 Project Overview
The **Graphical MARIE Architecture Simulator** is an educational tool built using Python and Tkinter to simulate the MARIE (Machine Architecture that is Really Intuitive and Easy) computer architecture. It helps users understand how a CPU executes instructions, manages memory, and interacts with registers through a visual and interactive interface.

---

## 🎯 Features

### 📝 Assembly Code Editor
- Built-in text editor for writing MARIE assembly programs
- Supports multiline editing and scrolling

### ⚙️ Assembler (Two-Pass)
- Converts assembly code into machine code (hexadecimal)
- **Pass 1:** Detects labels and builds symbol table
- **Pass 2:** Translates instructions into machine code
- Supports:
  - LOAD, STORE, ADD, SUBT
  - INPUT, OUTPUT, SKIPCOND
  - JUMP, HALT
  - DEC, HEX data declarations

### 🧠 CPU Simulation
- Simulates MARIE instruction cycle:
  - Fetch
  - Decode
  - Execute
  - PC Increment
- Step-by-step execution support

### 💾 Memory System
- 4096 memory locations
- Grid-based memory visualization
- Highlights modified memory cells during execution

### 📊 Registers
Simulates core MARIE registers:
- AC (Accumulator)
- IR (Instruction Register)
- MAR (Memory Address Register)
- MBR (Memory Buffer Register)
- PC (Program Counter)
- IN (Input Register)
- OUT (Output Register)

### 🎮 Control Panel
- **Assemble & Load:** Compile and load program into memory
- **Step Instruction:** Execute one instruction at a time
- **Reset CPU:** Reset system state

### 🖥️ Output System
- Displays output using dialog messages
- Shows results from OUTPUT instruction

### 🎨 GUI
- Built using Tkinter
- User-friendly layout with:
  - Code editor
  - Memory view
  - Register dashboard
  - Control buttons

---

## 🛠️ Technologies Used
- Python 3.x
- Tkinter (GUI Library)

---

## 🚀 How to Run

1. Install Python 3.x
2. Clone the repository:
```bash
git clone https://github.com/your-username/Graphical-MARIE-Architecture-Simulator.git
