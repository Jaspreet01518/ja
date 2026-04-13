import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import heapq

# ---------------- GRAPH ----------------
graph = {
    "Hospital": {"Sector 17": 4, "Sector 22": 2},
    "Sector 17": {"Hospital": 4, "Patient": 6},
    "Sector 22": {"Hospital": 2, "Patient": 3},
    "Patient": {"Sector 17": 6, "Sector 22": 3}
}

heuristic = {
    "Hospital": 7,
    "Sector 17": 6,
    "Sector 22": 2,
    "Patient": 0
}

emergency_requests = []

# ---------------- SAVE REQUEST ----------------
def save_request():
    patient = patient_entry.get()
    location = location_var.get()
    emergency = emergency_var.get()

    if patient == "":
        messagebox.showerror("Error", "Enter Patient Name")
        return

    emergency_requests.append((patient, location, emergency))
    messagebox.showinfo("Saved", "Emergency Request Saved Successfully")

# ---------------- CLEAR ----------------
def clear_all():
    patient_entry.delete(0, tk.END)
    location_var.set("Sector 22")
    emergency_var.set("Heart Attack")
    output.delete("1.0", tk.END)

# ---------------- BFS ----------------
def bfs():
    output.delete("1.0", tk.END)
    visited = set()
    queue = deque(["Hospital"])

    output.insert(tk.END, "BFS Traversal:\n\n")

    while queue:
        node = queue.popleft()
        if node not in visited:
            output.insert(tk.END, node + "\n")
            visited.add(node)
            queue.extend(graph[node].keys())

# ---------------- DFS ----------------
def dfs_util(node, visited):
    if node not in visited:
        output.insert(tk.END, node + "\n")
        visited.add(node)
        for neighbor in graph[node]:
            dfs_util(neighbor, visited)

def dfs():
    output.delete("1.0", tk.END)
    output.insert(tk.END, "DFS Traversal:\n\n")
    dfs_util("Hospital", set())

# ---------------- A* ----------------
def a_star():
    output.delete("1.0", tk.END)

    open_list = [(0, "Hospital")]
    g_cost = {"Hospital": 0}
    parent = {"Hospital": None}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == "Patient":
            break

        for neighbor, weight in graph[current].items():
            new_cost = g_cost[current] + weight

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                f_cost = new_cost + heuristic[neighbor]
                heapq.heappush(open_list, (f_cost, neighbor))
                parent[neighbor] = current

    path = []
    node = "Patient"
    while node:
        path.append(node)
        node = parent[node]

    path.reverse()

    output.insert(tk.END, "A* Shortest Path:\n\n")
    output.insert(tk.END, " -> ".join(path))
    output.insert(tk.END, f"\nDistance = {g_cost['Patient']} km")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Smart Emergency AI System")
root.geometry("950x700")
root.configure(bg="#e6f2ff")

heading = tk.Label(root, text="Smart Emergency AI System",
                   font=("Arial", 20, "bold"), bg="#e6f2ff", fg="darkblue")
heading.pack(pady=10)

# -------- INPUT FORM --------
form = tk.Frame(root, bg="#e6f2ff")
form.pack(pady=10)

tk.Label(form, text="Patient Name:", bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=5)
patient_entry = tk.Entry(form, width=25)
patient_entry.grid(row=0, column=1)

tk.Label(form, text="Location:", bg="#e6f2ff").grid(row=1, column=0)
location_var = tk.StringVar(value="Sector 22")
ttk.Combobox(form, textvariable=location_var,
             values=["Sector 17", "Sector 22"]).grid(row=1, column=1)

tk.Label(form, text="Emergency Type:", bg="#e6f2ff").grid(row=2, column=0)
emergency_var = tk.StringVar(value="Heart Attack")
ttk.Combobox(form, textvariable=emergency_var,
             values=["Heart Attack", "Accident", "Fire", "Other"]).grid(row=2, column=1)

# -------- BUTTONS --------
btn_frame = tk.Frame(root, bg="#e6f2ff")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Save Request", width=20, command=save_request, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Clear", width=20, command=clear_all, bg="#607D8B", fg="white").grid(row=0, column=1)

tk.Button(btn_frame, text="BFS", width=20, command=bfs, bg="#2196F3", fg="white").grid(row=1, column=0, padx=10)
tk.Button(btn_frame, text="DFS", width=20, command=dfs, bg="#9C27B0", fg="white").grid(row=1, column=1)

tk.Button(btn_frame, text="A* Algorithm", width=20, command=a_star, bg="#F44336", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

# -------- OUTPUT --------
output = tk.Text(root, width=100, height=18)
output.pack(pady=20)

root.mainloop()
