from swagger_server.API_main import main

application = main()

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8080)
