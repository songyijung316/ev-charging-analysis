import pandas as pd #빅데이터를 처리하기 좋음
import os #폴더나 파일 위치 같은 컴퓨터 환경관리담당


# -----------------------------------
# 1. 충전소 데이터 불러오기
# -----------------------------------
file_path = "./data/한국환경공단_전기차 충전소 위치 및 운영정보_20221027.csv"

#df = Data Frame
#pandas를 사용할때 표 형태 데이터를 저장하는 객체
#읽어올 파일 인코딩
try:
    df = pd.read_csv(file_path, encoding="utf-8-sig")
except UnicodeDecodeError: #실패시
    df = pd.read_csv(file_path, encoding="cp949") 


# -----------------------------------
# 2. 필요한 컬럼만 선택
# -----------------------------------
# 처음부터 모든 컬럼을 다 쓰면 복잡해지기 때문에
# 조회에 필요한 컬럼만 남겨두기
df = df[["시도", "군구", "주소", "충전소명", "기종(대)", "충전기타입", "이용자제한"]]


# -----------------------------------
# 3. 지역명 보기 좋게 바꾸기
# -----------------------------------
# 검색 편의성을 위해 긴 지역명을 짧게 바꿔주기
region_map = {
    "서울특별시": "서울",
    "부산광역시": "부산",
    "대구광역시": "대구",
    "인천광역시": "인천",
    "광주광역시": "광주",
    "대전광역시": "대전",
    "울산광역시": "울산",
    "세종특별자치시": "세종",
    "경기도": "경기",
    "강원도": "강원",
    "충청북도": "충북",
    "충청남도": "충남",
    "전라북도": "전북",
    "전라남도": "전남",
    "경상북도": "경북",
    "경상남도": "경남",
    "제주특별자치도": "제주"
}

# 원본 시도값을 보기 편한 형태로 변환
df["시도"] = df["시도"].replace(region_map)
#df["시도"]만 꺼내기
#df.haed() -> 위에서 다섯줄 보기
#df.shape -> 행,열 개수 확인




# -----------------------------------
# 4. 지역 검색 함수 만들기
# -----------------------------------
def search_chargers_by_region(dataframe, region, charger_kind=None):
    #"""은 주석이 아니라 문자열 데이터다
    #함수에 사용하면 함수를 설명하는 문자열 데이터가 된다

    """
    region: 시도 또는 군구 검색어
    charger_kind: '급속', '완속' 중 하나를 넣으면 추가 필터링
    """

    # 시도 또는 군구에 입력한 지역명이 들어있는지 확인
    condition = (
        dataframe["시도"].fillna("").str.contains(region, case=False) |
        dataframe["군구"].fillna("").str.contains(region, case=False)
    )

    # 조건에 맞는 데이터만 따로 저장
    result = dataframe[condition].copy()

    # 급속 / 완속 조건이 있으면 추가로 필터링
    if charger_kind:
        result = result[result["기종(대)"] == charger_kind]

    return result

# -----------------------------------
# 5. 사용자 입력 받기
# -----------------------------------
region = input("검색할 지역 또는 충전소명을 입력하세요: ").strip()
charger_kind = input("충전기 종류를 입력하세요(급속/완속, 없으면 엔터): ").strip()

# 빈 문자열이면 None 처리
if charger_kind == "":
    charger_kind = None


# -----------------------------------
# 6. 검색 실행
# -----------------------------------
result = search_chargers_by_region(df, region, charger_kind)


# -----------------------------------
# 7. 결과 출력
# -----------------------------------
if result.empty:
    print("\n검색 결과가 없습니다.")
else:
    # 같은 충전소가 중복될 수 있으므로 주소 + 충전소명 기준으로 중복 제거
    result = result.drop_duplicates(subset=["주소", "충전소명"])

    # 주소 기준 가나다 순 정렬
    result = result.sort_values(by="주소")

    print(f"\n총 {len(result)}개의 충전소가 검색되었습니다.\n")

    # 터미널에서는 핵심 정보만 간단히 출력
    print(
        result[["주소", "충전소명", "기종(대)", "이용자제한"]]
        .to_string(index=False)
    )
# -----------------------------------
# 8. 결과 저장
# -----------------------------------

# output 폴더가 없으면 자동 생성
os.makedirs("./output", exist_ok=True)

# 파일명에 들어가면 안 되는 문자 정리
safe_region = region.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_")

# 충전기 종류를 입력 안 했으면 all 처리
kind_text = charger_kind if charger_kind else "all"

# 지역명 + 충전기종류 기준으로 파일명 만들기
save_path = f"./output/{safe_region}_{kind_text}_search_result.csv"

# CSV 저장
result.to_csv(save_path, index=False, encoding="utf-8-sig")
print(f"\n검색 결과를 {save_path} 파일로 저장했습니다.")

#이용자 제한 충전소는 아파트 입주민 전용, 회사·기관 내부 전용, 특정 회원 전용 등 일반 사용자의 접근이 제한된 경우가 있을 수 있다. 
#따라서 지역별 충전소 수가 많더라도 실제 체감하는 충전 인프라 수준은 다를 수 있다.