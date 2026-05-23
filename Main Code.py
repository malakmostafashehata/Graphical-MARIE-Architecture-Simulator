import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class MarieSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("MARIE.js Python Simulator")
        self.root.geometry("1100x850")
        self.root.configure(bg="#f5f5f5")

        # CPU State & Memory
        self.memory = ["0000"] * 4096
        self.registers = {
            "AC": 0, "IR": "0000", "MAR": 0, 
            "MBR": "0000", "PC": 0, "IN": 0, "OUT": 0
        }
        
        self.opcodes = {
            "LOAD": "1", "STORE": "2", "ADD": "3", "SUBT": "4",
            "INPUT": "5", "OUTPUT": "6", "HALT": "7", "SKIPCOND": "8", "JUMP": "9"
        }
        self.symbol_table = {}
        self.is_halted = False
        self.setup_ui()

    def setup_ui(self):
        # --- Top: Assembly Editor ---
        tk.Label(self.root, text="Assembly Editor", bg="#f5f5f5", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.editor = scrolledtext.ScrolledText(self.root, height=10, font=("Consolas", 12))
        self.editor.pack(fill=tk.BOTH, padx=10, pady=5)
        
    
        # --- Middle: Register Dashboard ---
        self.reg_frame = tk.Frame(self.root, bg="#ffffff", relief=tk.GROOVE, borderwidth=1)
        self.reg_frame.pack(fill=tk.X, padx=10, pady=10)
        self.reg_widgets = {}
        
        for reg in self.registers.keys():
            container = tk.Frame(self.reg_frame, bg="#ffffff")
            container.pack(side=tk.LEFT, expand=True, padx=5, pady=10)
            tk.Label(container, text=reg, bg="#ffffff", font=("Arial", 9, "bold")).pack()
            
            bg_color = "#e8f5e9" if reg == "PC" else "#f1f3f4"
            val_box = tk.Label(container, text="0000", bg=bg_color, width=10, relief="sunken", 
                               font=("Consolas", 11, "bold"), fg="#1a73e8")
            val_box.pack()
            self.reg_widgets[reg] = val_box

        # --- Control Buttons ---
        btn_frame = tk.Frame(self.root, bg="#f5f5f5")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Assemble & Load", command=self.assemble, bg="#1a73e8", fg="white", padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Step Instruction", command=self.step, bg="#34a853", fg="white", padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset CPU", command=self.reset_cpu, bg="#ea4335", fg="white", padx=15).pack(side=tk.LEFT, padx=5)

        # --- Bottom: Memory Grid ---
        self.canvas = tk.Canvas(self.root, bg="white")
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.grid_frame = tk.Frame(self.canvas, bg="white")
        
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")
        
        self.cells = {}
        self.create_grid()
        self.update_reg_display()

    def create_grid(self):
        for i in range(16):
            tk.Label(self.grid_frame, text=f"+{hex(i)[2:].upper()}", width=6, font=("Arial", 8, "bold"), bg="#eee").grid(row=0, column=i+1)
        for r in range(32): 
            tk.Label(self.grid_frame, text=f"{r*16:03X}", width=5, font=("Arial", 8, "bold"), bg="#eee").grid(row=r+1, column=0)
            for c in range(16):
                cell = tk.Label(self.grid_frame, text="0000", width=6, relief="ridge", font=("Consolas", 9))
                cell.grid(row=r+1, column=c+1)
                self.cells[r*16 + c] = cell

    def update_reg_display(self):
        for reg, val in self.registers.items():
            if isinstance(val, str):
                display_val = val.upper()
            else:
                fmt = "03X" if reg in ["PC", "MAR"] else "04X"
                display_val = f"{(val & 0xFFFF):{fmt}}"
            self.reg_widgets[reg].config(text=display_val)

    def assemble(self):
        self.memory = ["0000"] * 4096
        for cell in self.cells.values():
            cell.config(text="0000", fg="black", bg="white")
        self.symbol_table = {}
        self.is_halted = False

        raw_lines = self.editor.get("1.0", tk.END).strip().split('\n')
        clean_instructions = []
        for line in raw_lines:
            content = line.split('/')[0].strip()
            if content: clean_instructions.append(content)

        # Pass 1: Labels
        for i, line in enumerate(clean_instructions):
            if ',' in line:
                label = line.split(',')[0].strip().upper()
                self.symbol_table[label] = i

        # Pass 2: Machine Code
        for i, line in enumerate(clean_instructions):
            if i >= 4096: break
            main_part = line.split(',')[1].strip() if ',' in line else line
            parts = main_part.split()
            cmd = parts[0].upper()

            if cmd in ["DEC", "HEX"]:
                val = int(parts[1]) if cmd == "DEC" else int(parts[1], 16)
                self.memory[i] = f"{val & 0xFFFF:04X}"
            else:
                opcode = self.opcodes.get(cmd, "0")
                if cmd == "SKIPCOND":
                    addr_part = parts[1] if len(parts) > 1 else "000"
                else:
                    target = parts[1].upper() if len(parts) > 1 else ""
                    addr_val = self.symbol_table.get(target, 0)
                    addr_part = f"{addr_val:03X}"
                self.memory[i] = f"{opcode}{addr_part}"
            self.cells[i].config(text=self.memory[i], fg="#1a73e8")
        
        self.reset_cpu()
        messagebox.showinfo("Assembler", "Loaded Successfully.")

    def step(self):
        if self.is_halted: return

        # --- FETCH CYCLE ---
        # MAR <- PC
        # MBR <- M[MAR], IR <- MBR
        # PC <- PC + 1
        pc_val = self.registers["PC"]
        self.registers["MAR"] = pc_val
        self.registers["MBR"] = self.memory[pc_val]
        self.registers["IR"] = self.registers["MBR"]
        self.registers["PC"] += 1 
        
        instr = self.registers["IR"]
        opcode = instr[0]
        operand_addr = int(instr[1:], 16)

        # --- EXECUTE CYCLE ---
        if opcode == "1": # LOAD
            val = int(self.memory[operand_addr], 16)
            self.registers["AC"] = val if val <= 0x7FFF else val - 0x10000
        elif opcode == "2": # STORE
            self.memory[operand_addr] = f"{self.registers['AC'] & 0xFFFF:04X}"
            self.cells[operand_addr].config(text=self.memory[operand_addr], bg="#fff9c4")
        elif opcode == "3": # ADD
            self.registers["AC"] += int(self.memory[operand_addr], 16)
        elif opcode == "4": # SUBT
            val = int(self.memory[operand_addr], 16)
            if val > 0x7FFF: val -= 0x10000
            self.registers["AC"] -= val
        elif opcode == "6": # OUTPUT
            messagebox.showinfo("Output", f"Accumulator: {self.registers['AC']}")
        elif opcode == "7": # HALT
            self.is_halted = True
            self.update_reg_display()
            messagebox.showinfo("MARIE", "Halted.")
            return # Exit; PC is already incremented to match web simulator
        elif opcode == "8": # SKIPCOND
            cond = instr[1:]
            ac = self.registers["AC"]
            if (cond == "000" and ac < 0) or (cond == "400" and ac == 0) or (cond == "800" and ac > 0):
                self.registers["PC"] += 1
        elif opcode == "9": # JUMP
            self.registers["PC"] = operand_addr

        self.update_reg_display()

    def reset_cpu(self):
        self.is_halted = False
        for k in self.registers:
            self.registers[k] = "0000" if k in ["IR", "MBR"] else 0
        self.update_reg_display()

if __name__ == "__main__":
    root = tk.Tk()
    MarieSimulator(root)
    root.mainloop()