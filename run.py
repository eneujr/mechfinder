from app import create_app

app = create_app()

if __name__ == '__main__':
    # host='0.0.0.0' permite acesso de outros dispositivos na mesma rede
    # Para acessar do celular, use: http://SEU_IP:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
