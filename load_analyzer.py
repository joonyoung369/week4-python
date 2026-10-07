from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


DATA_FILE = Path(__file__).with_name("load_data.csv")
RESULT_FILE = Path(__file__).with_name("load_result.csv")
PLOT_FILE = Path(__file__).with_name("stress_plot.png")
REQUIRED_COLUMNS = {"time_s", "force_N"}


def main():
    raw_data = pd.read_csv(DATA_FILE)
    missing_columns = REQUIRED_COLUMNS.difference(raw_data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV에 필요한 열이 없습니다: {missing}")
    data = raw_data.copy()
    invalid_rows = {}
    for column in ("time_s", "force_N"):
        numeric_values = pd.to_numeric(raw_data[column], errors="coerce")
        for row_index in numeric_values[numeric_values.isna()].index:
            raw_value = raw_data.at[row_index, column]
            if pd.isna(raw_value) or str(raw_value).strip() == "":
                reason = f"{column}=<빈칸> (빈칸)"
            else:
                reason = f"{column}={raw_value!r} (숫자가 아님)"
            invalid_rows.setdefault(row_index, []).append(reason)
        data[column] = numeric_values

    for row_index, reasons in invalid_rows.items():
        time_value = raw_data.at[row_index, "time_s"]
        csv_row = row_index + 2
        print(
            f"경고: CSV {csv_row}행 (time_s={time_value}) 제외: "
            f"{', '.join(reasons)}"
        )

    data = data.dropna(subset=["time_s", "force_N"]).copy()
    print(f"데이터 개수: {len(raw_data)}개")
    print(f"제외한 행 수: {len(invalid_rows)}개")
    print(f"유효한 데이터 수: {len(data)}개")
    if data.empty:
        print("유효한 데이터가 없어 계산과 그래프 생성을 중단합니다.")
        return

    area_mm2 = 100
    data["stress_MPa"] = data["force_N"] / area_mm2
    data.to_csv(RESULT_FILE, index=False)

    maximum_index = data["force_N"].idxmax()
    maximum_row = data.loc[maximum_index]
    maximum_stress_index = data["stress_MPa"].idxmax()
    maximum_stress_row = data.loc[maximum_stress_index]
    above_threshold_count = int((data["stress_MPa"] > 6).sum())

    plt.plot(data["time_s"], data["stress_MPa"], marker="o", linestyle="-")
    plt.scatter(
        maximum_stress_row["time_s"],
        maximum_stress_row["stress_MPa"],
        color="red",
        s=70,
        zorder=3,
    )
    plt.annotate(
        f"{maximum_stress_row['stress_MPa']:g} MPa",
        xy=(maximum_stress_row["time_s"], maximum_stress_row["stress_MPa"]),
        xytext=(8, 8),
        textcoords="offset points",
        color="red",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Stress (MPa)")
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    plt.close()

    print(f"최대 하중: {maximum_row['force_N']} N")
    print(f"해당 시간: {maximum_row['time_s']} S")
    print(f"최대 응력: {maximum_stress_row['stress_MPa']} MPa")
    print(f"최대 응력 해당 시간: {maximum_stress_row['time_s']} S")
    print(f"기준 응력 6 MPa 초과 데이터 개수: {above_threshold_count}개")


if __name__ == "__main__":
    main()