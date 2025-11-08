"""
Flask API Server for Multi-Agent Mental Health System
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from demo.core.llm_client import LLMClient
from demo.agents.router_agent import RouterAgent
from demo.agents.anxiety_specialist import AnxietySpecialistAgent
from demo.agents.judge_agent import JudgeAgent

app = Flask(__name__)
CORS(app)

llm = LLMClient()
router = RouterAgent(llm)
anxiety_specialist = AnxietySpecialistAgent(llm)
judge = JudgeAgent(llm)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        routing = router.process(user_message)
        specialist_type = routing.get('specialist', 'anxiety')
        
        if specialist_type == 'anxiety':
            specialist_response = anxiety_specialist.process(user_message)
            response_text = specialist_response.get('response', '')
            
            evaluation = judge.process(user_message, response_text)
            
            return jsonify({
                'success': True,
                'response': response_text,
                'specialist': specialist_type,
                'evaluation': {
                    'approved': evaluation.get('approved', False),
                    'overall_score': evaluation.get('scores', {}).get('overall', 0),
                    'decision': evaluation.get('scores', {}).get('decision', ''),
                    'reasoning': evaluation.get('scores', {}).get('reasoning', '')
                }
            })
        else:
            return jsonify({
                'success': True,
                'response': 'I understand you need support. Let me connect you with the right specialist.',
                'specialist': specialist_type,
                'evaluation': None
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
