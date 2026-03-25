import pandas as pd

# 1. 1번 결과 파일 읽기 (지역별 충전소 수)
charger_df = pd.read_csv("../output/regional_charger_status.csv", encoding="utf-8-sig")

# 2. 2번 결과 파일 읽기 (지역별 전기차 수)
car_df = pd.read_csv("../output/car_by_region.csv", encoding="utf-8-sig")

# 3. 컬럼 공백 제거
charger_df.columns = charger_df.columns.str.strip()
car_df.columns = car_df.columns.str.strip()

# 4. 데이터 확인
print("=== 충전소 데이터 ===")
print(charger_df.to_string(index=False))

print("\n=== 전기차 데이터 ===")
print(car_df.to_string(index=False))

# 5. 지역 기준으로 병합
merged_df = pd.merge(charger_df, car_df, on="지역", how="inner")

# 6. 전기차 1000대당 충전소 수 계산
merged_df["전기차1000대당충전소수"] = (
    merged_df["충전소수"] / merged_df["전기차수"] * 1000
).round(2)

# 7. 보기 좋게 정렬
merged_df = merged_df.sort_values(by="전기차1000대당충전소수", ascending=False)

# 8. 결과 출력
print("\n=== 최종 병합 결과 ===")
print(merged_df.to_string(index=False))

# 9. CSV 저장
merged_df.to_csv("../output/ev_infra_analysis_result.csv", index=False, encoding="utf-8-sig")
