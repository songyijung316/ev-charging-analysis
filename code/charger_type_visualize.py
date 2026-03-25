import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("../output/charger_type_status.csv", encoding="utf-8-sig")

plt.figure()
plt.bar(df["충전기타입"], df["개수"])
plt.title("급속 / 완속 충전기 비율")
plt.xlabel("충전기 타입")
plt.ylabel("개수")
plt.tight_layout()
plt.show()
