import pandas as pd
import folium

print("1. 프로그램 시작")

# CSV 파일 읽기
df = pd.read_csv(
    "../data/한국전력공사_충전소의 위치 및 현황 정보_20250630.csv",
    encoding="cp949"
)

print("2. CSV 읽기 완료")

# 컬럼명 공백 제거
df.columns = df.columns.str.strip()

# 위도/경도 결측 제거
df = df.dropna(subset=["위도", "경도"])

# 숫자형 변환
df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

# 다시 결측 제거
df = df.dropna(subset=["위도", "경도"])

print("3. 데이터 정리 완료")
print("총 데이터 수:", len(df))

# 지도 중심 좌표
center_lat = df["위도"].mean()
center_lon = df["경도"].mean()

# 지도 생성
charger_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=7
)

print("4. 지도 생성 완료")

# 마커 추가
for _, row in df.iterrows():
    popup_text = f"""
    <b>충전소명:</b> {row['충전소명']}<br>
    <b>주소:</b> {row['충전소주소']}<br>
    <b>상세주소:</b> {row['상세주소']}<br>
    <b>이용가능시간:</b> {row['이용가능시간']}<br>
    <b>연락처:</b> {row['연락처']}
    """

    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=row["충전소명"]
    ).add_to(charger_map)

print("5. 마커 추가 완료")

# html 저장
charger_map.save("../output/charger_map.html")

print("6. 지도 생성 완료")
print("charger_map.html 파일을 열어서 지도를 확인하세요.")
