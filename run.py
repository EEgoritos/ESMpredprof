from app import create_app

# Создаем экземпляр приложения
app = create_app()

if __name__ == '__main__':
    # Запускаем приложение в режиме отладки
    app.run(debug=True)