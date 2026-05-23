# Graphical MARIE Architecture Simulator

## 📌 Project Overview
The **Graphical MARIE Architecture Simulator** is an educational Python project that simulates the MARIE (Machine Architecture that is Really Intuitive and Easy) CPU architecture.  

The simulator provides a graphical interface using Tkinter to help students understand how a CPU executes instructions, manages memory, and interacts with registers in a step-by-step visual way.

---

## 🎯 Features

### 📝 Assembly Code Editor
- Write MARIE assembly code directly inside the program
- Supports multiline editing

### ⚙️ Assembler (Two-Pass)
- Converts assembly instructions into machine code
- Supports label handling and symbol table creation
- Supports:
  - LOAD, STORE, ADD, SUBT
  - INPUT, OUTPUT, SKIPCOND
  - JUMP, HALT
  - DEC, HEX

### 🧠 CPU Simulation
- Simulates full instruction cycle:
  - Fetch
  - Decode
  - Execute
  - PC Increment
- Step-by-step execution for learning

### 💾 Memory System
- Simulates 4096 memory locations
- Displays memory in a grid view
- Highlights updated memory cells

### 📊 Registers
Simulates MARIE CPU registers:
- AC, IR, MAR, MBR
- PC, IN, OUT

### 🎮 Control Panel
- Assemble & Load program
- Step-by-step execution
- Reset CPU simulation

### 🖥️ Output System
- Displays output using popup messages
- Shows results of OUTPUT instruction

### 🎨 GUI
- Built using Tkinter
- Simple educational interface with:
  - Code editor
  - Memory view
  - Registers panel
  - Control buttons

---

## 🛠️ Technologies Used
- Python 3.x
- Tkinter (built-in GUI library)

---

## 🚀 How to Run

1. Make sure Python 3 is installed  
2. Download the project file:  
   `Main Code.py`

3. Run the program:
```bash
python "Main Code.py"
