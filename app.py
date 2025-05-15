from flask import Flask, request, jsonify
import crawler
import data_processor
import predictor
import pandas as pd  # pandas 추가 임포트

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

cached_data = {
    'hitter_data': None,
    'pitcher_data': None,
    'win_probability_df': None,
    'last_update': None
}

@app.route('/')
def home():
    return "KBO 야구 승률 예측 API. '/ranking_predict' 엔드포인트를 사용하세요."


@app.route('/ranking_predict', methods=['GET'])
def predict_ranking():
    try:
        win_probability_df = predictor.get_win_probability_df(cached_data)
        
        if win_probability_df is None or win_probability_df.empty:
            return jsonify({'error': '데이터가 아직 준비되지 않았습니다.'}), 503

        # 숫자 변환 및 평균 승률 계산
        df_numeric = win_probability_df.apply(pd.to_numeric, errors='coerce')
        sorted_teams = df_numeric.mean(axis=1).sort_values(ascending=False).index.tolist()

        return jsonify({
            'ranking': sorted_teams
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
