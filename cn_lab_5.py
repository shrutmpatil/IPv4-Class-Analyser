"""
CN Lab 5 — IPv4 Address Classification
Computer Networks Lab, VIT
Classful IPv4 analyzer (RFC 791) — stdlib only, no pip installs required.
"""

import tkinter as tk
from tkinter import messagebox

# ─── Classification Data ──────────────────────────────────────────────────────

CLASS_DATA = {
    "A": {
        "net_bits":  8,
        "host_bits": 24,
        "networks":  2**7 - 2,   # 126  (excludes 0.x and 127.x)
        "hosts":     2**24 - 2,  # subtract network & broadcast addresses
        "start":     "1.0.0.0",
        "end":       "126.255.255.255",
        "mask":      "255.0.0.0",
    },
    "B": {
        "net_bits":  16,
        "host_bits": 16,
        "networks":  2**14,      # first 2 bits fixed (10), 14 bits free
        "hosts":     2**16 - 2,
        "start":     "128.0.0.0",
        "end":       "191.255.255.255",
        "mask":      "255.255.0.0",
    },
    "C": {
        "net_bits":  24,
        "host_bits": 8,
        "networks":  2**21,      # first 3 bits fixed (110), 21 bits free
        "hosts":     2**8 - 2,
        "start":     "192.0.0.0",
        "end":       "223.255.255.255",
        "mask":      "255.255.255.0",
    },
}

SPECIAL_MESSAGES = {
    "D":        ("Multicast",    "Class D — Reserved for Multicast groups.\nRange: 224.0.0.0 – 239.255.255.255\nNo host/network assignment."),
    "E":        ("Experimental", "Class E — Reserved for Experimental use.\nRange: 240.0.0.0 – 255.255.255.255\nNo host/network assignment."),
    "Loopback": ("Loopback",     "127.x.x.x — Loopback / localhost address.\nNever routed; used for local stack testing.\nRFC 1122 §3.2.1.3"),
    "Invalid":  ("Reserved",     "First octet 0 is reserved ('This' network).\nNot classifiable under RFC 791."),
}

# ─── Classification Logic ─────────────────────────────────────────────────────

def get_ip_class(first_octet: int) -> str:
    """Return the RFC 791 class label for a given first octet."""
    if first_octet == 0:
        return "Invalid"
    if first_octet == 127:
        return "Loopback"
    if 1   <= first_octet <= 126:
        return "A"
    if 128 <= first_octet <= 191:
        return "B"
    if 192 <= first_octet <= 223:
        return "C"
    if 224 <= first_octet <= 239:
        return "D"
    if 240 <= first_octet <= 255:
        return "E"
    return "Invalid"


def classify(ip_str: str) -> str:
    """
    Validate and classify an IPv4 address string.

    Returns a formatted multi-line result string.
    Raises ValueError with a human-readable message on bad input.
    """
    parts = ip_str.strip().split(".")
    if len(parts) != 4:
        raise ValueError("Must be exactly 4 octets separated by dots.\nExample: 192.168.1.1")

    try:
        octets = [int(p) for p in parts]
    except ValueError:
        raise ValueError("Each octet must be an integer (no letters or symbols).")

    if not all(0 <= o <= 255 for o in octets):
        raise ValueError("Each octet must be in the range 0 – 255.")

    first    = octets[0]
    ip_class = get_ip_class(first)

    SEP = "─" * 42
    lines = [
        f"  IP Address    : {ip_str}",
        f"  IP Class      : {ip_class}",
        SEP,
    ]

    if ip_class in SPECIAL_MESSAGES:
        label, msg = SPECIAL_MESSAGES[ip_class]
        for line in msg.split("\n"):
            lines.append(f"  {line}")
        return "\n".join(lines)

    d = CLASS_DATA[ip_class]
    lines += [
        f"  NetID bits    : {d['net_bits']}",
        f"  HostID bits   : {d['host_bits']}",
        f"  Subnet Mask   : {d['mask']}",
        SEP,
        f"  Networks      : {d['networks']:,}",
        f"  Hosts/network : {d['hosts']:,}",
        SEP,
        f"  Class start   : {d['start']}",
        f"  Class end     : {d['end']}",
    ]
    return "\n".join(lines)


def is_valid_format(val: str) -> bool:
    """Return True only if val is a well-formed IPv4 (4 octets, each 0–255)."""
    parts = val.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False


# ─── Colour Palette ───────────────────────────────────────────────────────────

BG       = "#1e1e2e"   # dark navy background
SURFACE  = "#2a2a3d"   # card / widget surface
ACCENT   = "#7c6af7"   # purple accent (buttons, title)
FG       = "#cdd6f4"   # primary text
FG_DIM   = "#6c7086"   # muted / hint text
GREEN    = "#a6e3a1"   # valid-format indicator
RED      = "#f38ba8"   # invalid-format indicator

FONT_TITLE  = ("Consolas", 15, "bold")
FONT_SUB    = ("Consolas",  9)
FONT_LABEL  = ("Consolas", 10)
FONT_ENTRY  = ("Consolas", 12)
FONT_OUTPUT = ("Consolas", 10)
FONT_BTN    = ("Consolas", 10, "bold")
FONT_BTN2   = ("Consolas", 10)


# ─── GUI ──────────────────────────────────────────────────────────────────────

def build_gui():
    root = tk.Tk()
    root.title("IPv4 Class Analyzer — CN Lab 5")
    root.configure(bg=BG)
    root.resizable(False, False)

    # ── Title ────────────────────────────────────────────────────────────────
    tk.Label(
        root, text="IPv4 Address Classifier",
        bg=BG, fg=ACCENT, font=FONT_TITLE
    ).grid(row=0, column=0, columnspan=2, pady=(20, 2))

    tk.Label(
        root, text="Classful Addressing  ·  RFC 791",
        bg=BG, fg=FG_DIM, font=FONT_SUB
    ).grid(row=1, column=0, columnspan=2, pady=(0, 16))

    # ── Input ────────────────────────────────────────────────────────────────
    tk.Label(
        root, text="IPv4 Address:", bg=BG, fg=FG, font=FONT_LABEL
    ).grid(row=2, column=0, padx=(24, 8), sticky="e")

    entry_var = tk.StringVar()
    entry = tk.Entry(
        root, textvariable=entry_var, width=26,
        font=FONT_ENTRY, bg=SURFACE, fg=FG,
        insertbackground=FG, relief="flat",
        highlightthickness=1,
        highlightcolor=ACCENT,
        highlightbackground=FG_DIM,
    )
    entry.grid(row=2, column=1, padx=(0, 24), pady=4, sticky="w")
    entry.focus_set()

    hint = tk.Label(
        root, text="e.g. 192.168.1.1",
        bg=BG, fg=FG_DIM, font=FONT_SUB
    )
    hint.grid(row=3, column=1, sticky="w", padx=(0, 24), pady=(0, 4))

    # Live border + hint update on every keystroke
    def on_key(*_):
        val = entry_var.get()
        if val == "":
            hint.config(fg=FG_DIM, text="e.g. 192.168.1.1")
            entry.config(highlightbackground=FG_DIM)
        elif is_valid_format(val):
            entry.config(highlightbackground=GREEN)
            hint.config(fg=GREEN, text="✓ Valid format")
        else:
            entry.config(highlightbackground=RED)
            hint.config(fg=RED, text="✗  Use format A.B.C.D  (0–255 each)")

    entry_var.trace_add("write", on_key)

    # ── Buttons ──────────────────────────────────────────────────────────────
    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=12)

    def run_classify(_event=None):
        result_box.config(state="normal")
        result_box.delete(1.0, tk.END)
        try:
            output = classify(entry_var.get())
            result_box.insert(tk.END, "\n" + output + "\n")
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
        result_box.config(state="disabled")

    def copy_result():
        content = result_box.get(1.0, tk.END).strip()
        if content:
            root.clipboard_clear()
            root.clipboard_append(content)
            copy_btn.config(text="Copied ✓")
            root.after(1600, lambda: copy_btn.config(text="Copy"))

    def clear_all():
        entry_var.set("")
        entry.config(highlightbackground=FG_DIM)
        hint.config(fg=FG_DIM, text="e.g. 192.168.1.1")
        result_box.config(state="normal")
        result_box.delete(1.0, tk.END)
        result_box.config(state="disabled")
        entry.focus_set()

    PRIMARY_BTN = dict(
        bg=ACCENT, fg="#ffffff", font=FONT_BTN,
        relief="flat", cursor="hand2",
        padx=16, pady=6, bd=0,
        activebackground="#6a59d1", activeforeground="#ffffff",
    )
    SECONDARY_BTN = dict(
        bg=SURFACE, fg=FG, font=FONT_BTN2,
        relief="flat", cursor="hand2",
        padx=16, pady=6, bd=0,
        activebackground="#3a3a55", activeforeground=FG,
    )

    tk.Button(
        btn_frame, text="Classify  [↵]",
        command=run_classify, **PRIMARY_BTN
    ).pack(side="left", padx=6)

    copy_btn = tk.Button(
        btn_frame, text="Copy",
        command=copy_result, **SECONDARY_BTN
    )
    copy_btn.pack(side="left", padx=6)

    tk.Button(
        btn_frame, text="Clear",
        command=clear_all, **SECONDARY_BTN
    ).pack(side="left", padx=6)

    # ── Output box ───────────────────────────────────────────────────────────
    result_box = tk.Text(
        root, height=11, width=54,
        font=FONT_OUTPUT, bg=SURFACE, fg=FG,
        relief="flat", padx=10, pady=8,
        state="disabled", cursor="arrow",
        spacing1=2, spacing3=2,
    )
    result_box.grid(row=5, column=0, columnspan=2, padx=24, pady=(0, 8))

    # ── Footer ───────────────────────────────────────────────────────────────
    tk.Label(
        root,
        text="Press Enter to classify  ·  stdlib only, no pip required",
        bg=BG, fg=FG_DIM, font=FONT_SUB
    ).grid(row=6, column=0, columnspan=2, pady=(0, 18))

    # ── Key bindings ─────────────────────────────────────────────────────────
    root.bind("<Return>",  run_classify)
    root.bind("<Escape>",  lambda _: clear_all())

    root.mainloop()


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_gui()
