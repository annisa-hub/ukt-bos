from flask_login_app import Flask, render_template, request, redirect, url_for, flash, session
# Import 'session' untuk manajemen sesi pengguna

app = Flask(__name__)
# KUNCI RAHASIA INI PENTING!
# Ganti dengan string yang unik, panjang, dan acak untuk produksi.
# Ini digunakan untuk mengamankan sesi pengguna dan pesan flash.
# Contoh: app.secret_key = 'os.urandom(24)' (gunakan di lingkungan produksi)
app.secret_key = 'super_secret_key_yang_sangat_aman_dan_unik_anda_ganti_ini'




# --- Data Pengguna Dummy (untuk contoh, di dunia nyata gunakan database) ---
# PENTING: Dalam aplikasi nyata, password HARUS di-hash (misalnya dengan bcrypt)
# dan disimpan di database, BUKAN dalam kode seperti ini.
users = {
    "admin": "password123", # Contoh: Password ini harus di-hash
    "user": "rahasia"     # Contoh: Password ini harus di-hash
}

# --- Rute Aplikasi ---

# Rute utama ('/') akan dialihkan ke halaman login
@app.route('/')
def index():
    # Mengarahkan pengguna ke rute 'login'
    return redirect(url_for('login'))

# Rute untuk halaman login
# Menerima permintaan GET (untuk menampilkan formulir login)
# dan permintaan POST (untuk memproses data formulir yang dikirim)
@app.route('login', methods=['GET', 'POST'])
def login():
    
    # Jika permintaan adalah POST (formulir login disubmit)
    if request.method == 'POST':
        # Mengambil nilai 'username' dan 'password' dari data formulir
        username = request.form['username']
        password = request.form['password']

        # Memeriksa kredensial pengguna
        # PENTING: Dalam aplikasi nyata, bandingkan password yang di-hash
        if username in users and users[username] == password:
            # Jika kredensial benar:
            # Setel sesi pengguna untuk menandai bahwa mereka telah login
            session['logged_in'] = True
            session['username'] = username
            # Menampilkan pesan sukses menggunakan flash
            flash(f'Selamat datang, {username}!', 'success')
            # Mengarahkan pengguna ke halaman dashboard
            return redirect(url_for('dashboard'))
        else:
            # Jika kredensial salah:
            # Menampilkan pesan error menggunakan flash
            flash('Username atau password salah.', 'danger')

    # Untuk permintaan GET (saat halaman login pertama kali dimuat)
    # atau jika login gagal (setelah pesan flash ditampilkan),
    # tampilkan kembali halaman login.
    return render_template("login.html")
    

# Rute untuk halaman dashboard
# Ini adalah halaman yang hanya bisa diakses setelah login berhasil
@app.route('/dashboard')
def dashboard():
    # Memeriksa apakah pengguna sudah login melalui sesi
    if 'logged_in' not in session or not session['logged_in']:
        # Jika belum login, alihkan kembali ke halaman login dengan pesan error
        flash('Anda harus login terlebih dahulu untuk mengakses halaman ini.', 'danger')
        return redirect(url_for('login'))

    # Jika sudah login, tampilkan halaman dashboard
    current_username = session.get('username', 'Pengguna') # Ambil username dari sesi
    return f"""
    <h1>Login Berhasil!</h1>
    <p>Selamat datang di dashboard, {current_username}.</p>
    <p>Ini adalah halaman dashboard Anda.</p>
    <a href="{url_for('logout')}">Logout</a> | <a href="{url_for('login')}">Kembali ke Login</a>
    """

# Rute untuk logout
@app.route('/logout')
def logout():
    # Hapus semua data dari sesi untuk logout pengguna
    session.pop('logged_in', None)
    session.pop('username', None)
    # Menampilkan pesan logout
    flash('Anda telah berhasil logout.', 'info')
    # Mengarahkan kembali ke halaman login
    return redirect(url_for('login'))

# --- Menjalankan Aplikasi ---
if __name__ == '__main__':
    # app.run(debug=True) akan otomatis me-reload server jika ada perubahan kode
    # dan menampilkan pesan error yang lebih detail.
    # PENTING: Nonaktifkan 'debug=True' di lingkungan produksi karena alasan keamanan.
    app.run(debug=True)
