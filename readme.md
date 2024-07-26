# K3LAR: Your K3 Solution (Back End)

K3LAR adalah alat pemantau kualitas ruangan berbasis ESP32 yang ditujukan untuk lingkungan perkantoran. Tujuan dari K3LAR adalah untuk membantu meningkatkan kualitas K3 di lingkungan perkantoran.

Project ini berisi source code backend yang diintegrasikan ke K3LAR Mobile App.

Pada project ini, kami menggunakan Firebase Firestore sebagai database. Ada beberapa endpoint:
- Sensor: `/api/sensors` merupakan request POST yang mengirimkan data sensor ke dalam Firestore. Endpoint ini dijalankan di alat IoT K3LAR ketika data sensor didapatkan.
- Prediksi: `/api/predict` merupakan request POST yang mengembalikan klasifikasi data kualitas ruangan dan saran tindakan yang bisa dilakukan. Pada endpoint ini, harus mengirimkan data berupa tanggal, kelembaban, suhu, CO, CO2, dan PM2.5. Endpoint ini dijalankan di K3LAR Mobile App.
- Forecast: `/api/forecast` merupakan request GET yang mengembalikan data prediksi kualitas ruangan di masa depan. Endpoint ini dijalankan di K3LAR Mobile App.

## Installation
- Clone project ini.
- Buka project dengan text editor spepe Visual Studio Code.
- Buka terminal dan jalankan `python app.py`
- Project berhasil dijalankan.
