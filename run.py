from waitress import serve
import app

if __name__ == '__main__':
    serve(app.app, host='127.0.0.1', port=8000)