import pandas as pd

# 1. 데이터 읽기
df = pd.read_csv("../data/202512_202512_연령별인구현황_연간.csv", encoding="cp949")

# 2. 컬럼 정리
df.columns = df.columns.str.strip()

# 3. 행정구역 이름 추출
df["행정구역명"] = df["행정구역"].astype(str).apply(lambda x: x.split("(")[0].strip())

# 4. 시도만 남기기
df = df[df["행정구역명"].str.count(" ") == 0]

# 5. 출장소 제거 (핵심 추가)
df = df[~df["행정구역명"].str.contains("출장소")]

# 6. 지역 정규화
def normalize_region(region):
    if region.startswith("서울"):
        return "서울"
    elif region.startswith("부산"):
        return "부산"
    elif region.startswith("대구"):
        return "대구"
    elif region.startswith("인천"):
        return "인천"
    elif region.startswith("광주"):
        return "광주"
    elif region.startswith("대전"):
        return "대전"
    elif region.startswith("울산"):
        return "울산"
    elif region.startswith("세종"):
        return "세종"
    elif region.startswith("경기"):
        return "경기"
    elif region.startswith("강원"):
        return "강원"
    elif region.startswith("충청북도"):
        return "충북"
    elif region.startswith("충청남도"):
        return "충남"
    elif region.startswith("전북"):
        return "전북"
    elif region.startswith("전라남도"):
        return "전남"
    elif region.startswith("경상북도"):
        return "경북"
    elif region.startswith("경상남도"):
        return "경남"
    elif region.startswith("제주"):
        return "제주"
    return region

# 7. 지역 생성
df["지역"] = df["행정구역명"].apply(normalize_region)

# 8. 인구수 변환
df["인구수"] = (
    df["2025년_계_총인구수"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)

# 9. 최종 결과
region_population = df[["지역", "인구수"]].drop_duplicates().reset_index(drop=True)

print(region_population.to_string(index=False))

# 10. 저장
region_population.to_csv("../output/population_by_region.csv", index=False, encoding="utf-8-sig")
