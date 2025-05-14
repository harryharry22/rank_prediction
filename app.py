from flask import Flask, jsonify
import predictor

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

# 전역 변수로 데이터 저장
cached_data = {
    'win_probability_df': None
}

@app.route('/')
def home():
    """인자 없이 호출 시 예상 순위 리스트 반환"""
    try:
        if cached_data['win_probability_df'] is None:
            win_probability_df = predictor.get_win_probability_df(cached_data)
            cached_data['win_probability_df'] = win_probability_df
        else:
            win_probability_df = cached_data['win_probability_df']

        df_processed = win_probability_df.replace('-', 0).astype(float)
        df_processed['average_win_prob'] = df_processed.mean(axis=1)
        sorted_df = df_processed.sort_values(by='average_win_prob', ascending=False)
        
        return jsonify(sorted_df.index.tolist())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
