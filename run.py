from app import create_app, socket_io

app = create_app()

if __name__ == '__main__':
    print('[INFO] Starting server at http://localhost:5000')
    socket_io.run(app, host='0.0.0.0', port=5000)
