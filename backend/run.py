from app import app

if __name__ == "__main__":
    print("Starting AWE-Store Backend Server...")
    print(app.url_map)
    app.run(debug=True, port=5000) 