import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
from PIL import Image
from io import BytesIO

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Weather App')
        self.setGeometry(100, 100, 400, 300)

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        # City input
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText('Enter city name...')
        input_layout.addWidget(self.city_input)

        # Search button
        search_button = QPushButton('Search', self)
        search_button.clicked.connect(self.show_weather)
        input_layout.addWidget(search_button)

        # Adding input layout to the main layout
        main_layout.addLayout(input_layout)

        # Labels for displaying weather data
        self.city_label = QLabel('', self)
        self.city_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.city_label)

        self.icon_label = QLabel('', self)
        self.icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.icon_label)

        self.temp_label = QLabel('', self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.temp_label)

        self.weather_label = QLabel('', self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.weather_label)

        self.wind_label = QLabel('', self)
        self.wind_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.wind_label)

        # Set the main layout
        self.setLayout(main_layout)

    def get_weather_data(self, city_name):
        api_key = '8d5fd0b550177ffe0903fd839592e82e'  # Replace with your OpenWeatherMap API key
        base_url = 'https://api.openweathermap.org/data/2.5/weather?'
        complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"

        response = requests.get(complete_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def show_weather(self):
        city_name = self.city_input.text()
        
        if not city_name:
            QMessageBox.warning(self, 'Error', 'Please enter a city name.')
            return

        weather_data = self.get_weather_data(city_name)
        
        if weather_data:
            city = weather_data['name']
            country = weather_data['sys']['country']
            temperature = weather_data['main']['temp']
            weather = weather_data['weather'][0]['description'].capitalize()
            wind_speed = weather_data['wind']['speed']
            icon_code = weather_data['weather'][0]['icon']

            # Update weather details
            self.city_label.setText(f"{city}, {country}")
            self.temp_label.setText(f"Temperature: {temperature}°C")
            self.weather_label.setText(f"Weather: {weather}")
            self.wind_label.setText(f"Wind Speed: {wind_speed} m/s")

            # Fetch and display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_data = icon_response.content
            image = Image.open(BytesIO(icon_data))
            image.save('weather_icon.png')

            pixmap = QPixmap('weather_icon.png')
            self.icon_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        else:
            QMessageBox.warning(self, 'Error', 'City not found or API request failed.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())
