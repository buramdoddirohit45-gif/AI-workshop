import os
from flask import Flask, send_from_directory, send_file, jsonify

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'linguaai-localstorage-key'

    @app.route('/')
    def index():
        """Serve the modern LocalStorage-powered single-page application."""
        return send_file('index.html')

    @app.route('/api/status')
    def status():
        return jsonify({
            'status': 'online',
            'storage_engine': 'localStorage',
            'cloud_database': None,
            'message': 'Superbase/remote database removed. All data stored directly in browser localStorage.'
        })

    @app.route('/<path:path>')
    def catch_all(path):
        """Serve static files or fall back to index.html for SPA client-side routing."""
        if os.path.exists(path):
            return send_file(path)
        if os.path.exists(os.path.join('static', path)):
            return send_from_directory('static', path)
        return send_file('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print(" LinguaAI — Personalized AI Language Tutor")
    print(f" Running at: http://127.0.0.1:{port}")
    print(" Storage: Browser LocalStorage (Zero Supabase/Cloud DB dependencies)")
    print("=" * 60)
    app.run(host='127.0.0.1', port=port, debug=True)
