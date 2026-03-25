import os
import pandas as pd


def normalize_region(region):
    region = str(region).strip()

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
    elif region.startswith("충북") or region.startswith("충청북도"):
        return "충북"
    elif region.startswith("충남") or region.startswith("충청남도"):
        return "충남"
    elif region.startswith("전북") or region.startswith("전라북도"):
        return "전북"
    elif region.startswith("전남") or region.startswith("전라남도"):
        return "전남"
    elif region.startswith("경북") or region.startswith("경상북도"):
        return "경북"
    elif region.startswith("경남") or region.startswith("경상남도"):
        return "경남"
    elif region.startswith("제주"):
        return "제주"

    return region


def main():
    # 1. CSV 파일 읽기
    df = pd.read_csv(
        "../data/한국교통안전공단_전국_전기차_차종별_용도별_차량_등록대수(운행차량기준)_20250407.csv",
        encoding="cp949"
    )

    # 2. 컬럼 공백 제거
    df.columns = df.columns.str.strip()

    # 3. 전기차 데이터만 필터링
    df = df[df["연료별"] == "전기"].copy()

    # 4. 숫자형 변환
    df["계"] = pd.to_numeric(df["계"], errors="coerce")

    # 5. 지역 컬럼 생성
    df["지역"] = df["시군구별"].apply(normalize_region)

    # 6. 지역별 전기차 수 집계
    car_by_region = df.groupby("지역", as_index=False)["계"].sum()

    # 7. 컬럼명 변경
    car_by_region = car_by_region.rename(columns={"계": "전기차수"})

    # 8. 정렬
    car_by_region = car_by_region.sort_values("지역").reset_index(drop=True)

    # 9. 결과 출력
    print(car_by_region.to_string(index=False))

    # 10. output 폴더 생성 후 저장
    os.makedirs("../output", exist_ok=True)
    car_by_region.to_csv("../output/car_by_region.csv", index=False, encoding="utf-8-sig")

    print("\n지역별 전기차 수 저장 완료")


if __name__ == "__main__":
    main()
