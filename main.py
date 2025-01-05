import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib

# 1. 한글 폰트 설정 (윈도우용 '맑은 고딕' 사용)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우에서 맑은 고딕 사용
matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 기호가 깨지지 않도록 설정

# 2. 파일 경로 설정 및 데이터 불러오기
file_path = r"C:\src\CARD_SUBWAY_MONTH_202411.csv"

if not os.path.exists(file_path):
    print("파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
else:
    try:
        # CSV 파일 읽기
        df = pd.read_csv(file_path, encoding='utf-8')  # 인코딩 오류 방지

        # 2. 데이터 확인
        print(df.head())
        print(df.info())

        # 3. 컬럼명 변경 및 필요 데이터 추출
        if len(df.columns) == 6:
            df.columns = ['연월', '호선명', '역명', '승차총승객수', '하차총승객수', '기타']
            df.drop(columns=['기타'], inplace=True)  # 추가적인 '기타' 열 제거
        elif len(df.columns) == 5:
            df.columns = ['연월', '호선명', '역명', '승차총승객수', '하차총승객수']
        else:
            print("열의 수가 예상과 맞지 않습니다. 데이터 구조를 확인해 주세요.")
            raise ValueError("열의 수가 예상과 맞지 않음")

        
        df['역명'] = df['역명'].astype(str).str.strip()
        df['호선명'] = df['호선명'].astype(str).str.strip()

        # 4. 데이터 전처리 (총 승하차 인원 계산)
        df['총승객수'] = df['승차총승객수'] + df['하차총승객수']

        # 5. 노선별 승하차 인원 분석
        line_usage = df.groupby('호선명')['총승객수'].sum().reset_index()
        line_usage = line_usage.sort_values(by='총승객수', ascending=False)

        # 6. 역별 승하차 인원 분석
        station_usage = df.groupby(['역명', '호선명'])['총승객수'].sum().reset_index()
        station_usage = station_usage.sort_values(by='총승객수', ascending=False)

        # 7. 시각화 (노선별 승하차 인원 그래프)
        plt.figure(figsize=(12, 6))
        sns.barplot(x='호선명', y='총승객수', data=line_usage, palette='viridis')
        plt.title('노선별 지하철 승하차 인원 (2024년 11월)')
        plt.xticks(rotation=45)
        plt.show()

        # 8. 상위 10개 역 시각화
        plt.figure(figsize=(12, 8))
        top10_stations = station_usage.head(10)
        sns.barplot(x='총승객수', y='역명', data=top10_stations, hue='호선명', dodge=False, palette='muted')
        plt.title('상위 10개 역 지하철 승하차 인원 (2024년 11월)')
        plt.show()

        # 9. 분석 결과 CSV 저장 (타블로 시각화용)
        line_usage.to_csv(r"C:\src\line_usage_202411.csv", index=False, encoding='utf-8-sig')
        station_usage.to_csv(r"C:\src\station_usage_202411.csv", index=False, encoding='utf-8-sig')
    
    except Exception as e:
        print(f"데이터 처리 중 오류가 발생했습니다: {e}")
