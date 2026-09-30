"""힘 단위 변환기.

실행:
	python force_converter.py
"""

import math
import tkinter as tk
from tkinter import ttk


# Each value is the number of newtons represented by one unit.
UNIT_FACTORS = {
	"N": 1.0,
	"kN": 1_000.0,
	"MN": 1_000_000.0,
	"kgf": 9.80665,
	"lbf": 4.4482216152605,
	"ozf": 0.27801385095378125,
	"dyn": 0.00001,
}
UNIT_NAMES = tuple(UNIT_FACTORS)
OUTPUT_UNITS = UNIT_NAMES


def convert_force(value, from_unit, to_unit):
	"""Convert a numeric force value between supported units."""
	if from_unit not in UNIT_FACTORS or to_unit not in UNIT_FACTORS:
		raise ValueError("지원하지 않는 단위입니다.")
	if not math.isfinite(value):
		raise ValueError("유한한 숫자만 입력할 수 있습니다.")
	return value * UNIT_FACTORS[from_unit] / UNIT_FACTORS[to_unit]


def format_value(value):
	"""Show the result with exactly two decimal places."""
	return f"{value:.2f}"


class ForceConverterApp:
	def __init__(self, root):
		self.root = root
		root.title("힘 단위 변환기")
		root.geometry("420x280")
		root.resizable(False, False)

		main = ttk.Frame(root, padding=20)
		main.pack(fill="both", expand=True)

		ttk.Label(main, text="힘 단위 변환기", font=("Malgun Gothic", 16, "bold")).pack(
			anchor="w", pady=(0, 16)
		)

		input_row = ttk.Frame(main)
		input_row.pack(fill="x", pady=4)
		tk.Label(input_row, text="입력값", width=12).pack(side="left")
		self.value_var = tk.StringVar(value="1")
		value_entry = ttk.Entry(input_row, textvariable=self.value_var, width=18)
		value_entry.pack(side="left", padx=(0, 8))
		self.from_var = tk.StringVar(value="kN")
		ttk.Combobox(
			input_row, textvariable=self.from_var, values=UNIT_NAMES,
			state="readonly", width=8
		).pack(side="left")

		output_row = ttk.Frame(main)
		output_row.pack(fill="x", pady=4)
		tk.Label(output_row, text="출력 단위", width=12).pack(side="left")
		self.to_var = tk.StringVar(value="N")
		ttk.Combobox(
			output_row, textvariable=self.to_var, values=OUTPUT_UNITS,
			state="readonly", width=8
		).pack(side="left")
		button_row = ttk.Frame(main)
		button_row.pack(pady=(16, 10))
		ttk.Button(button_row, text="변환", command=self.convert).pack(side="left", padx=4)
		ttk.Button(button_row, text="초기화", command=self.reset).pack(side="left", padx=4)
		self.result_var = tk.StringVar(value="결과가 여기에 표시됩니다.")
		ttk.Label(main, textvariable=self.result_var, font=("Malgun Gothic", 12, "bold")).pack(
			pady=4
		)
		self.status_var = tk.StringVar()
		ttk.Label(main, textvariable=self.status_var, foreground="#b00020").pack()

		value_entry.bind("<Return>", lambda event: self.convert())
		value_entry.focus_set()

	def convert(self):
		try:
			value = float(self.value_var.get().strip().replace(",", ""))
			result = convert_force(value, self.from_var.get(), self.to_var.get())
		except (TypeError, ValueError, OverflowError):
			self.result_var.set("입력을 확인해 주세요.")
			self.status_var.set("숫자와 지원 단위를 입력해야 합니다.")
			return

		self.result_var.set(f"{format_value(result)} {self.to_var.get()}")
		self.status_var.set("")

	def reset(self):
		self.value_var.set("")
		self.result_var.set("")
		self.status_var.set("")


def main():
	root = tk.Tk()
	ForceConverterApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()


