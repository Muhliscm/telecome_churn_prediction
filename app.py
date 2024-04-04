from website import create_app

# running app
app = create_app()
app.run(host='0.0.0.0',port=8080)
