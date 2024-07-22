# Library yang digunakan
import streamlit.components.v1 as components
import streamlit as st
import face_recognition
from datetime import datetime
from PIL import Image
import pandas as pd
import numpy as np
import cv2
import os
import time

# inisiasi variabel
FRAME_WINDOW = st.image([])

menu = ["HOME", "DETEKSI KEHADIRAN", "REGISTER DATA", "DAFTAR PRESENSI", "HAPUS DATA MAHASISWA"]
st.sidebar.image('static/images/IN.png', width=100)
st.sidebar.title("faceIN")
choice = st.sidebar.selectbox("Menu", menu)

path = 'absensi'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    classNames.append(os.path.splitext(cl)[0])

cap = cv2.VideoCapture(0)

# Face recognition functions
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encode = encodings[0]
            encodeList.append(encode)
        else:
            print(f"Face not found in {img}")
    return encodeList

def faceList(name, selected_course):
    with open('absensi.csv', 'r+') as f:
        myDataList = f.readlines()
        dateToday = datetime.now().strftime('%d-%m-%Y')
        for line in myDataList:
            entry = line.split(',')
            if len(entry) >= 5:
                entryName = entry[0]
                entryDate = entry[3].strip()
                entryCourse = entry[4].strip()
                if entryName == name and entryDate == dateToday and entryCourse == selected_course:
                    return
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        f.writelines(f'\n{name},{dtString},{dateToday},{selected_course}')

# Deteksi Kehadiran
if choice == 'DETEKSI KEHADIRAN': 
    st.markdown("<h2 style='text-align: center; color: white;'>DETEKSI KEHADIRAN</h2>", unsafe_allow_html=True)
    courses = ["Grafik Komputer 2", "Rekayasa Komputasional", "Konsep Data Mining", "Sistem Basis Data 2"]
    selected_course = st.selectbox("Pilih mata kuliah:", courses)
    st.write(f"Anda memilih mata kuliah: {selected_course}")
    run = st.checkbox("Jalankan kamera")

    if run:
        for cl in myList:
            curlImg = cv2.imread(f'{path}/{cl}')
            images.append(curlImg)
        print(classNames)

        encodeListUnknown = findEncodings(images)
        print('Encoding complete!')

        def faceList(filename, selected_course):
            npm, name = os.path.splitext(filename)[0].split('_', 1)
            with open('absensi.csv', 'r+') as f:
                myDataList = f.readlines()
                dateToday = datetime.now().strftime('%d-%m-%Y')
                for line in myDataList:
                    entry = line.split(',')
                    if len(entry) >= 5:
                        entryNPM = entry[0]
                        entryName = entry[1]
                        entryDate = entry[3].strip()
                        entryCourse = entry[4].strip()
                        if entryNPM == npm and entryName == name and entryDate == dateToday and entryCourse == selected_course:
                            return
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{npm},{name},{dtString},{dateToday},{selected_course}')

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListUnknown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListUnknown, encodeFace)

                if len(faceDis) > 0:
                    matchesIndex = np.argmin(faceDis)
                    
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    if matches[matchesIndex]:
                        filename = myList[matchesIndex]
                        name = classNames[matchesIndex].upper()
                        print(name)
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        faceList(filename, selected_course)
                        time.sleep(3)
                    else:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                        cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # mengkonvert warna yang ditampilkan
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            FRAME_WINDOW.image(img)
            cv2.waitKey(1)


# Register data
elif choice == 'REGISTER DATA':
    st.markdown("<h2 style='text-align: center; color: white;'>REGISTER DATA</h2>", unsafe_allow_html=True)
    
    def load_image(image_file):
        img = Image.open(image_file)
        return img

    def capture_image():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        return frame

    def check_existing_npm(npm):
        for file in os.listdir("absensi"):
            if file.startswith(f"{npm}_"):
                return True
        return False

    user_npm = st.text_input("Masukkan NPM:")
    user_npm = str(user_npm)
    user_name = st.text_input("Masukkan nama:")
    st.write("Harap bersiap sebelum mengambil gambar!")
    st.write("Klik tombol dibawah ini untuk mengambil gambar sebagai data wajah")
    capture_btn = st.button("Mengambil Gambar")
    
    if capture_btn:
        if user_npm == "" or user_name == "":
            st.warning("Tolong masukkan NPM dan nama sebelum mengambil gambar.")
        else:
            if check_existing_npm(user_npm):
                st.warning(f"NPM {user_npm} sudah terdaftar. Tolong masukkan NPM yang berbeda.")
            else:
                img = capture_image()
                if img is not None:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img_pil = Image.fromarray(img_rgb)
                    st.image(img_pil, caption="Captured Image")
                    
                    if not os.path.exists("absensi"):
                        os.makedirs("absensi")
                    
                    img_pil.save(os.path.join("absensi", f"{user_npm}_{user_name}.png"))
                    st.success(f"Saved Captured Image as {user_npm}_{user_name}.png")

# Daftar Presensi
elif choice == 'DAFTAR PRESENSI':
    st.markdown("<h2 style='text-align: center; color: white;'>DAFTAR KEHADIRAN</h2>", unsafe_allow_html=True)
    
    df = pd.read_csv('absensi.csv', header=None, names=['NPM', 'NAMA', 'WAKTU HADIR', 'TANGGAL', 'MATA KULIAH'])
    df['NPM'] = df['NPM'].astype(str)

    if df.empty:
        st.write("Tidak ada data kehadiran yang tersedia")
    else:
        df = df.dropna(subset=['TANGGAL'])
        unique_courses = df['MATA KULIAH'].unique()
        
        for course in unique_courses:
            st.write(f"### Daftar Kehadiran Mata Kuliah {course}")
            course_df = df[df['MATA KULIAH'] == course]
            unique_dates = course_df['TANGGAL'].unique()
            
            for date in unique_dates:
                st.write(f"##### Tanggal {date}")
                date_df = course_df[course_df['TANGGAL'] == date]
                st.write(date_df)
                
                # Tombol menghapus tabel
                delete_button = st.button(f"Hapus Data {course} - {date}", key=f"{course}_{date}")
                
                if delete_button:
                    df = df[~((df['MATA KULIAH'] == course) & (df['TANGGAL'] == date))]
                    df.to_csv('absensi.csv', index=False, header=False)
                    st.success(f"Data untuk {course} pada tanggal {date} berhasil dihapus.")
                    st.experimental_rerun()

        # Tombol menghapus semua data
        if st.button("Hapus Semua Data"):
            open('absensi.csv', 'w').close()  # menghapus data file
            st.success("Semua data berhasil dihapus.")
            st.experimental_rerun()

# Home        
elif choice == 'HOME':
    st.title("Selamat datang di faceIN!")
    
    st.write("""
    faceIN adalah sebuah sistem inovatif yang dirancang untuk memudahkan para dosen dalam mengambil kehadiran mahasiswanya. Menggunakan teknologi face recognition, faceIN mampu mengenali wajah dengan akurat dan mencatat data kehadiran secara otomatis.
    """)

    st.subheader("Cara Pemakaian Sistem:")

    st.write("""
    - **Menu HOME** berisikan penjelasan dan cara pemakaian sistem.
    - **Menu DETEKSI KEHADIRAN** digunakan untuk mencatat kehadiran mahasiswa menggunakan kamera.
    - **Menu REGISTER DATA** berfungsi untuk mengambil data mahasiswa, dengan cara masukkan NPM dan Nama kemudian difoto agar data mahasiswa didapatkan.
    - **Menu DAFTAR PRESENSI** merupakan menu yang menampilkan hasil dari pencatatan kehadiran mahasiswa yang dicatat sesuai dengan waktu terdeteksinya, dan dikumpulkan berdasarkan tanggal dan mata kuliahnya. Jika daftar kehadirannya sudah tidak diperlukan dapat dihapus dengan tombol yang disediakan, dapat dihapus tabel yang diinginkan atau keseluruhan tabel yang ada.
    - **Menu HAPUS DATA MAHASISWA** berguna untuk menghapus data mahasiswa yang tersimpan, sekiranya ada kesalahan data saat registrasi atau data tidak diperlukan lagi datanya dapat dihapus.
    """)

    st.write("Dengan faceIN proses absensi menjadi lebih efisien dan akurat, sehingga Anda dapat fokus pada pengajaran dan pembelajaran yang lebih baik. Selamat menggunakan faceIN!")

# Hapus Data Mahasiswa
elif choice == "HAPUS DATA MAHASISWA":
    st.markdown("<h2 style='text-align: center; color: white;'>HAPUS DATA MAHASISWA</h2>", unsafe_allow_html=True)
    
    # function menghapus data wajah
    def delete_face_data(file_name):
        file_path = os.path.join("absensi", file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False
    
    # Menampilkan list data yang ada
    if len(myList) > 0:
        selected_name = st.selectbox("Pilih nama untuk dihapus datanya", classNames)
        delete_btn = st.button("Hapus Data")
        
        if delete_btn:
            file_name = f"{selected_name}.png"
            success = delete_face_data(file_name)
            if success:
                st.success(f"Data wajah untuk {selected_name} berhasil dihapus.")
            else:
                st.error(f"Data wajah untuk {selected_name} tidak ditemukan.")
    else:
        st.write("Tidak ada data wajah yang terdaftar.")
