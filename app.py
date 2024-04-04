from website import create_app

# commenting to test git hub actions
app = create_app()
app.run(host='0.0.0.0',port=8080)
