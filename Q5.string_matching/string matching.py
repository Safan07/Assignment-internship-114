import tkinter as tk
from tkinter import scrolledtext, ttk
from difflib import SequenceMatcher

# --- Core function ---
def string_similarity_alignment(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    ratio = matcher.ratio()
    similarity_percentage = ratio * 100
    
    match_report = []
    aligned_str1 = []
    aligned_str2 = []
    alignment_line = []
    match_count = 0
    mismatch_count = 0
    color_info = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for c1, c2 in zip(str1[i1:i2], str2[j1:j2]):
                match_report.append(f"Match: {c1} == {c2}")
                aligned_str1.append(c1)
                aligned_str2.append(c2)
                alignment_line.append('|')
                match_count += 1
                color_info.append('match')
        elif tag == 'replace':
            for c1, c2 in zip(str1[i1:i2], str2[j1:j2]):
                match_report.append(f"Mismatch: {c1} != {c2}")
                aligned_str1.append(c1)
                aligned_str2.append(c2)
                alignment_line.append('.')
                mismatch_count += 1
                color_info.append('mismatch')
        elif tag == 'insert':
            for c in str2[j1:j2]:
                match_report.append(f"Inserted in str2: {c}")
                aligned_str1.append('-')
                aligned_str2.append(c)
                alignment_line.append('.')
                mismatch_count += 1
                color_info.append('mismatch')
        elif tag == 'delete':
            for c in str1[i1:i2]:
                match_report.append(f"Deleted from str1: {c}")
                aligned_str1.append(c)
                aligned_str2.append('-')
                alignment_line.append('.')
                mismatch_count += 1
                color_info.append('mismatch')

    return (similarity_percentage, match_report,
            ''.join(aligned_str1), ''.join(aligned_str2),
            ''.join(alignment_line), match_count + mismatch_count,
            match_count, mismatch_count, color_info)

# --- GUI Function ---
def run_similarity():
    str1 = entry1.get()
    str2 = entry2.get()
    
    if not str1 or not str2:
        for tab in [similarity_text, visual_text, report_text, summary_text]:
            tab.configure(state='normal')
            tab.delete('1.0', tk.END)
            tab.insert(tk.END, "Please enter both strings.")
            tab.configure(state='disabled')
        return
    
    (similarity, report, a_str1, a_str2, alignment, total_chars,
     match_count, mismatch_count, color_info) = string_similarity_alignment(str1, str2)

    # ---- Similarity Tab ----
    similarity_text.configure(state='normal')
    similarity_text.delete('1.0', tk.END)
    similarity_text.tag_configure('heading', font=('Helvetica', 16, 'bold'), foreground="#00BFFF")
    similarity_text.tag_configure('value', font=('Consolas', 18, 'bold'), foreground="#00FFCC")
    similarity_text.insert(tk.END, "Similarity Percentage:\n", 'heading')
    similarity_text.insert(tk.END, f"{similarity:.2f}%\n", 'value')
    similarity_text.configure(state='disabled')

    # ---- Visual Alignment Tab ----
    visual_text.configure(state='normal')
    visual_text.delete('1.0', tk.END)
    visual_text.tag_configure('match', foreground='#00FFCC', font=('Consolas', 14, 'bold'))
    visual_text.tag_configure('mismatch', foreground='#FF5555', font=('Consolas', 14, 'bold'))
    visual_text.insert(tk.END, "Visual Alignment:\n\n", 'match')
    for idx, char in enumerate(a_str1):
        visual_text.insert(tk.END, char, color_info[idx])
    visual_text.insert(tk.END, "\n")
    for idx, char in enumerate(alignment):
        visual_text.insert(tk.END, char, color_info[idx])
    visual_text.insert(tk.END, "\n")
    for idx, char in enumerate(a_str2):
        visual_text.insert(tk.END, char, color_info[idx])
    visual_text.configure(state='disabled')

    # ---- Match Report Tab ----
    report_text.configure(state='normal')
    report_text.delete('1.0', tk.END)
    report_text.tag_configure('heading', font=('Helvetica', 16, 'bold'), foreground="#00BFFF")
    report_text.tag_configure('line', font=('Consolas', 14))
    report_text.insert(tk.END, "Match Report:\n\n", 'heading')
    for line in report:
        report_text.insert(tk.END, line + "\n", 'line')
    report_text.configure(state='disabled')

    # ---- Summary Tab ----
    summary_text.configure(state='normal')
    summary_text.delete('1.0', tk.END)
    summary_text.tag_configure('heading', font=('Helvetica', 16, 'bold'), foreground="#00BFFF")
    summary_text.tag_configure('value', font=('Consolas', 16, 'bold'), foreground="#00FFCC")
    summary_text.insert(tk.END, "Summary:\n\n", 'heading')
    summary_text.insert(tk.END, f"Total characters compared: {total_chars}\n", 'value')
    summary_text.insert(tk.END, f"Matching characters: {match_count}\n", 'value')
    summary_text.insert(tk.END, f"Mismatched characters: {mismatch_count}\n", 'value')
    summary_text.configure(state='disabled')

# --- Exit Function ---
def exit_app(event=None):
    root.destroy()
    exit()

# --- GUI Setup ---
root = tk.Tk()
root.title("String Similarity Checker")
root.configure(bg="#2e2e2e")
root.geometry("950x650")
root.resizable(True, True)
root.bind('<q>', exit_app)  # Press Q to quit

# Fonts
label_font = ('Helvetica', 12, 'bold')
entry_font = ('Helvetica', 12)
button_font = ('Helvetica', 13, 'bold')

# Input Frame
input_frame = tk.Frame(root, bg="#1a1a1a", padx=15, pady=15)
input_frame.pack(fill='x', padx=10, pady=10)

tk.Label(input_frame, text="Enter first string:", bg="#1a1a1a", fg="#00BFFF", font=label_font).grid(row=0, column=0, sticky="w", pady=5)
entry1 = tk.Entry(input_frame, width=70, font=entry_font, bg="#333333", fg="white", insertbackground="white")
entry1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Enter second string:", bg="#1a1a1a", fg="#00BFFF", font=label_font).grid(row=1, column=0, sticky="w", pady=5)
entry2 = tk.Entry(input_frame, width=70, font=entry_font, bg="#333333", fg="white", insertbackground="white")
entry2.grid(row=1, column=1, padx=5, pady=5)

run_button = tk.Button(input_frame, text="Check Similarity", command=run_similarity,
                       bg="#00BFFF", fg="black", font=button_font, padx=10, pady=5)
run_button.grid(row=2, column=0, columnspan=2, pady=15)

# --- Notebook for Tabs ---
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook', background="#2e2e2e", borderwidth=0)
style.configure('TNotebook.Tab', background="#1a1a1a", foreground="#00BFFF", padding=[10,5], font=('Helvetica', 12, 'bold'))
style.map('TNotebook.Tab', background=[('selected', '#00BFFF')], foreground=[('selected', 'black')])

# ---- Tabs ----
similarity_tab = tk.Frame(notebook, bg="#1a1a1a")
visual_tab = tk.Frame(notebook, bg="#1a1a1a")
report_tab = tk.Frame(notebook, bg="#1a1a1a")
summary_tab = tk.Frame(notebook, bg="#1a1a1a")

notebook.add(similarity_tab, text="Similarity")
notebook.add(visual_tab, text="Visual Alignment")
notebook.add(report_tab, text="Match Report")
notebook.add(summary_tab, text="Summary")

# ---- Text Widgets in Tabs ----
similarity_text = scrolledtext.ScrolledText(similarity_tab, font=('Consolas', 18), bg="#333333", fg="white", insertbackground="white", state='disabled')
similarity_text.pack(fill='both', expand=True, padx=5, pady=5)

visual_text = scrolledtext.ScrolledText(visual_tab, font=('Consolas', 14), bg="#333333", fg="white", insertbackground="white", state='disabled')
visual_text.pack(fill='both', expand=True, padx=5, pady=5)

report_text = scrolledtext.ScrolledText(report_tab, font=('Consolas', 14), bg="#333333", fg="white", insertbackground="white", state='disabled')
report_text.pack(fill='both', expand=True, padx=5, pady=5)

summary_text = scrolledtext.ScrolledText(summary_tab, font=('Consolas', 16), bg="#333333", fg="white", insertbackground="white", state='disabled')
summary_text.pack(fill='both', expand=True, padx=5, pady=5)

root.mainloop()
