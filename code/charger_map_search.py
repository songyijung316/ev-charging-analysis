import os
import webbrowser
import pandas as pd
import folium

print("1. 프로그램 시작")

# 1. 팀원이 저장한 조회 결과 파일 읽기
search_df = pd.read_csv(
    "../output/광명시_all_search_result.csv",
    encoding="utf-8-sig"
)

print("2. 조회 결과 파일 읽기 완료")

# 2. 위경도 포함 원본 파일 읽기
location_df = pd.read_csv(
    "../data/한국전력공사_충전소의 위치 및 현황 정보_20250630.csv",
    encoding="cp949"
)

print("3. 위경도 원본 파일 읽기 완료")

# 3. 컬럼 공백 제거
search_df.columns = search_df.columns.str.strip()
location_df.columns = location_df.columns.str.strip()

# 4. 컬럼명 맞추기
search_df = search_df.rename(columns={"주소": "충전소주소"})

# 5. 공백 제거
search_df["충전소명"] = search_df["충전소명"].astype(str).str.strip()
search_df["충전소주소"] = search_df["충전소주소"].astype(str).str.strip()

location_df["충전소명"] = location_df["충전소명"].astype(str).str.strip()
location_df["충전소주소"] = location_df["충전소주소"].astype(str).str.strip()

# 6. 1차 병합: 충전소명 + 주소
merged_df = pd.merge(
    search_df,
    location_df[["충전소명", "충전소주소", "위도", "경도"]],
    on=["충전소명", "충전소주소"],
    how="left"
)

# 7. 1차 병합에서 실패한 행 찾기
unmatched_df = merged_df[merged_df["위도"].isna()].copy()

# 8. 2차 병합: 충전소명만으로 재시도
if len(unmatched_df) > 0:
    retry_df = pd.merge(
        unmatched_df.drop(columns=["위도", "경도"]),
        location_df[["충전소명", "위도", "경도"]],
        on="충전소명",
        how="left"
    )

    matched_df = merged_df[merged_df["위도"].notna()].copy()
    merged_df = pd.concat([matched_df, retry_df], ignore_index=True)

# 9. 위도/경도 숫자형 변환
merged_df["위도"] = pd.to_numeric(merged_df["위도"], errors="coerce")
merged_df["경도"] = pd.to_numeric(merged_df["경도"], errors="coerce")

# 10. 최종 결측 제거
merged_df = merged_df.dropna(subset=["위도", "경도"]).reset_index(drop=True)

print("4. 병합 완료")
print("지도에 표시할 충전소 수:", len(merged_df))

# 11. 병합 결과 없으면 종료
if len(merged_df) == 0:
    print("조회 결과와 위경도 데이터가 매칭되지 않았습니다.")
    print("충전소명 또는 주소 형식이 서로 달라서 병합이 실패한 것입니다.")
    raise SystemExit

# 12. 지도 중심 좌표
center_lat = merged_df["위도"].mean()
center_lon = merged_df["경도"].mean()

# 13. 지도 생성
charger_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11
)

print("5. 지도 생성 완료")

# 14. 마커 추가
for _, row in merged_df.iterrows():
    popup_text = f"""
    <b>충전소명:</b> {row['충전소명']}<br>
    <b>주소:</b> {row['충전소주소']}<br>
    <b>충전기종:</b> {row['기종(대)']}<br>
    <b>충전기타입:</b> {row['충전기타입']}<br>
    <b>이용자제한:</b> {row['이용자제한']}
    """

    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=row["충전소명"]
    ).add_to(charger_map)

print("6. 마커 추가 완료")

# 15. output 폴더 생성
os.makedirs("../output", exist_ok=True)

# 16. html 저장
output_path = "../output/광명시_charger_map.html"
charger_map.save(output_path)

print("7. 지도 저장 완료:", output_path)

# 17. 브라우저 자동 열기
absolute_path = os.path.abspath(output_path)
webbrowser.open("file://" + absolute_path)

print("8. 브라우저에서 지도 열기 완료")
