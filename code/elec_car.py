import os
import pandas as pd

# 1. 데이터 불러오기
file_path = "../data/한국환경공단_전기차 충전소 위치 및 운영정보_20221027.csv"

try:
    df = pd.read_csv(file_path, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="cp949", encoding_errors="replace")

# 2. output 폴더 보장
os.makedirs("../output", exist_ok=True)

# 3. 지역명 매핑
region_map = {
    "서울특별시": "서울", "경기도": "경기", "인천광역시": "인천", "강원도": "강원",
    "충청북도": "충북", "충청남도": "충남", "대전광역시": "대전", "세종특별자치시": "세종",
    "경상북도": "경북", "대구광역시": "대구", "전라북도": "전북", "전라남도": "전남",
    "광주광역시": "광주", "경상남도": "경남", "부산광역시": "부산", "울산광역시": "울산",
    "제주특별자치도": "제주"
}

# 4. 컬럼명 변경 및 지역명 변환
df.rename(columns={"시도": "지역"}, inplace=True)
df["지역"] = df["지역"].map(region_map)

# 5. 충전소 기준 집계
df_station = df.drop_duplicates(subset=["지역", "군구", "주소", "충전소명"])
region_station_counts = df_station.groupby("지역").size().reset_index(name="충전소수")

# 6. 급속/완속 비율용 데이터 생성
# 실제 파일에서 충전기 구분 컬럼은 '기종(대)' 사용
type_counts = df["기종(대)"].value_counts().reset_index()
type_counts.columns = ["충전기타입", "개수"]

# 7. 출력
print("--- [지역별 충전소 수 현황] ---")
print(region_station_counts.sort_values(by="충전소수", ascending=False).to_string(index=False))

print("\n--- [급속/완속 구성 현황] ---")
print(type_counts.to_string(index=False))

# 8. CSV 저장
region_station_counts.to_csv("../output/regional_charger_status.csv", index=False, encoding="utf-8-sig")
type_counts.to_csv("../output/charger_type_status.csv", index=False, encoding="utf-8-sig")
