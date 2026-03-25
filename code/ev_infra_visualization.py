import pandas as pd
import matplotlib.pyplot as plt

# 한글 깨짐 방지
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 최종 결과 파일 읽기
df = pd.read_csv(
    "../output/ev_infra_analysis_result.csv",
    encoding="utf-8-sig"
)

# 2. 컬럼 공백 제거
df.columns = df.columns.str.strip()

# 3. 그래프 생성
plt.figure(figsize=(12, 6))
plt.bar(df["지역"], df["전기차1000대당충전소수"])

# 4. 제목과 축 이름
plt.title("지역별 전기차 1000대당 충전소 수")
plt.xlabel("지역")
plt.ylabel("충전소 수")

# 5. x축 글자 회전
plt.xticks(rotation=45)

# 6. 여백 자동 조정
plt.tight_layout()

# 7. 그래프 출력
plt.show()
