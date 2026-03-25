


![전기차 이미지](./image/free-icon-electric-car-4833984.png)



# 프로젝트명: 전기차 충전소 인프라 분석

---

## 1. 프로젝트 개요

본 프로젝트는 지역별 전기차 등록 대수와 충전소 수를 비교해  
전기차 1,000대당 충전소 수를 분석하는 것을 목표로 한다.

또한 추가적으로 인구 데이터를 활용해  
인구 대비 충전소 수(인구 10만명당 충전소 수)를 분석하고,  
충전기 유형(급속/완속) 비율까지 함께 분석했다.

추가로 지역 검색 기반 충전소 조회 기능과  
지도 기반 충전소 위치 시각화 기능을 구현해  
사용자가 특정 지역의 충전소 분포를 직관적으로 확인할 수 있도록 구성했다.

이를 통해 지역 간 전기차 충전 인프라 수준의 차이를  
정량적·시각적으로 비교했다.

---

## 2. 폴더 구조

- `data` : 원본 공공데이터 파일 저장
- `code` : 데이터 전처리, 분석, 검색 및 지도 시각화 코드 저장
- `output` : 전처리 결과, 최종 분석 결과, 검색 결과, 지도 html 저장

---

## 3. 사용 데이터

- `한국교통안전공단_전국_전기차_차종별_용도별_차량_등록대수(운행차량기준)_20250407.csv`  
  : 지역별 전기차 등록 대수 분석용 데이터

- `한국환경공단_전기차 충전소 위치 및 운영정보_20221027.csv`  
  : 지역 검색 기반 충전소 조회 기능용 데이터

- `한국전력공사_충전소의 위치 및 현황 정보_20250630.csv`  
  : 위도/경도 포함 지도 시각화용 데이터

- `202512_202512_연령별인구현황_연간.csv`  
  : 지역별 인구 분석용 데이터

---

## 4. 코드 파일 설명

- `car_by_region.py`  
  : 전기차 등록 데이터를 읽어 전기차만 필터링하고,  
  지역명을 정규화한 뒤 지역별 전기차 수를 집계한다.  
  → 결과: `output/car_by_region.csv`

- `elec_car.py`  
  : 충전소 데이터를 읽어 지역명을 통일하고,  
  중복 충전소를 제거한 뒤 지역별 충전소 수를 집계한다.  
  또한 급속/완속 충전기 유형별 개수도 함께 생성한다.  
  → 결과:  
  - `output/regional_charger_status.csv`  
  - `output/charger_type_status.csv`

- `merge_and_visualize.py`  
  : 전기차 데이터와 충전소 데이터를 병합해  
  전기차 1,000대당 충전소 수를 계산하는 핵심 분석 파일이다.  
  → 결과: `output/ev_infra_analysis_result.csv`

- `ev_infra_visualization.py`  
  : 최종 분석 결과(전기차 1,000대당 충전소 수)를  
  지역별 막대그래프로 시각화한다.

- `population_by_region.py`  
  : 인구 데이터를 전처리하여 시도 단위의 지역별 인구수를 추출한다.  
  → 결과: `output/population_by_region.csv`

- `population_charger_analysis.py`  
  : 인구 데이터와 충전소 데이터를 병합해  
  인구 10만명당 충전소 수를 계산하는 보조 분석 파일이다.  
  → 결과: `output/population_charger_analysis.csv`

- `charger_type_visualize.py`  
  : 급속/완속 충전기 비율을 시각화하는 그래프를 생성한다.  
  → 입력: `output/charger_type_status.csv`

- `ev_charger_search.py`  
  : 사용자가 입력한 지역명을 기반으로 충전소 데이터를 조회하고,  
  조건(전체/급속/완속)에 맞는 충전소 목록을 CSV 파일로 저장한다.  
  → 결과: `output/{지역명}_{충전기종류}_search_result.csv`  
  예) `output/광명시_all_search_result.csv`

- `charger_map.py`  
  : 위경도 데이터를 기반으로 전국 충전소 위치를 지도에 시각화한다.  
  → 결과: `output/charger_map.html`

- `charger_map_search.py`  
  : 지역 검색 결과 파일과 위경도 데이터를 병합해  
  특정 지역 충전소를 지도에 표시하는 통합 기능 파일이다.  
  현재 코드는 광명시 검색 결과 파일을 기준으로 동작하도록 작성했다.  
  → 결과: `output/광명시_charger_map.html`

---

## 5. 생성 파일

- `output/car_by_region.csv`  
  : 지역별 전기차 등록 대수

- `output/regional_charger_status.csv`  
  : 지역별 충전소 수

- `output/charger_type_status.csv`  
  : 충전기 유형(급속/완속)별 개수

- `output/ev_infra_analysis_result.csv`  
  : 전기차 1,000대당 충전소 수 분석 결과 (핵심 결과)

- `output/population_by_region.csv`  
  : 지역별 인구수

- `output/population_charger_analysis.csv`  
  : 인구 10만명당 충전소 수 분석 결과

- `output/{지역명}_{충전기종류}_search_result.csv`  
  : 특정 지역/조건 충전소 조회 결과  
  예) `output/광명시_all_search_result.csv`

- `output/charger_map.html`  
  : 전국 충전소 지도 시각화 결과

- `output/광명시_charger_map.html`  
  : 광명시 조회 결과 기반 지도 시각화 결과

---

## 6. 실행 방법

프로젝트 루트 폴더 기준으로 아래 순서대로 실행한다.

### [분석 파트]

```bash
python code/car_by_region.py
python code/elec_car.py
python code/merge_and_visualize.py
python code/ev_infra_visualization.py
python code/population_by_region.py
python code/population_charger_analysis.py
python code/charger_type_visualize.py

### [기능 파트]

```bash
python code/ev_charger_search.py
python code/charger_map.py
python code/charger_map_search.py

## 7. 분석 지표
지역별 전기차 등록 대수
지역별 충전소 수
전기차 1,000대당 충전소 수
인구 10만명당 충전소 수
급속 / 완속 충전기 비율

## 8. 핵심 기능
지역 검색 기반 충전소 조회
: 사용자가 입력한 지역명을 기준으로 충전소 정보를 검색하고,
검색 결과를 CSV 파일로 저장한다.
지도 기반 충전소 위치 표시
: 위경도 데이터를 활용하여 전국 충전소 또는
검색 결과에 해당하는 특정 지역 충전소를 지도에 시각화한다.

## 9. 주의사항
모든 실행은 프로젝트 루트 폴더 기준으로 수행해야 한다.
원본 데이터 파일은 반드시 data 폴더에 위치해야 한다.
코드 내부 경로는 현재 폴더 구조에 맞게 설정해야 한다.
전기차 등록 데이터는 cp949 인코딩을 사용한다.
한국환경공단 충전소 데이터는 utf-8-sig 우선, 필요 시 cp949로 처리한다.
한국전력공사 위경도 포함 지도 데이터는 cp949 인코딩을 사용한다.
지역명(서울특별시 → 서울 등)이 통일되지 않으면 병합 시 데이터가 누락될 수 있다.
matplotlib 사용 시 한글 깨짐 방지를 위해 Malgun Gothic 폰트 설정이 필요하다.
지도 HTML 파일은 브라우저 환경에서 열어야 정상적으로 표시된다.
charger_map_search.py는 현재 광명시 검색 결과 파일 기준으로 연결되어 있으므로,
다른 지역으로 확장하려면 입력 파일명/출력 파일명을 함께 수정해야 한다.
