import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 1. 파일 읽기
charger_df = pd.read_csv("../output/regional_charger_status.csv", encoding="utf-8-sig")
population_df = pd.read_csv("../output/population_by_region.csv", encoding="utf-8-sig")

# 2. 컬럼 공백 제거
charger_df.columns = charger_df.columns.str.strip()
population_df.columns = population_df.columns.str.strip()

# 3. 데이터 확인
print("=== 충전소 데이터 ===")
print(charger_df.to_string(index=False))

print("\n=== 인구 데이터 ===")
print(population_df.to_string(index=False))

# 4. 지역 기준 병합
merged_df = pd.merge(charger_df, population_df, on="지역", how="inner")

# 5. 인구 10만명당 충전소 수 계산
merged_df["인구10만명당충전소수"] = (
    merged_df["충전소수"] / merged_df["인구수"] * 100000
).round(2)

# 6. 정렬
merged_df = merged_df.sort_values(by="인구10만명당충전소수", ascending=False)

# 7. 결과 출력
print("\n=== 인구 대비 충전소 분석 결과 ===")
print(merged_df.to_string(index=False))

# 8. CSV 저장
merged_df.to_csv("../output/population_charger_analysis.csv", index=False, encoding="utf-8-sig")

# 9. 그래프 출력
plt.figure(figsize=(12, 6))
plt.bar(merged_df["지역"], merged_df["인구10만명당충전소수"])
plt.xticks(rotation=45)
plt.xlabel("지역")
plt.ylabel("인구 10만명당 충전소 수")
plt.title("지역별 인구 10만명당 충전소 수 비교")
plt.tight_layout()
plt.show()
