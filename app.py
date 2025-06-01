from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret-key-unik-123'  # wajib untuk session

@app.route('/')
def home():
    return redirect(url_for('ruangan'))

@app.route('/ruangan', methods=['GET', 'POST'])
def ruangan():
    if request.method == 'POST':
        session['panjang_ruangan'] = float(request.form['panjang_ruangan'])
        session['lebar_ruangan'] = float(request.form['lebar_ruangan'])
        return redirect(url_for('ubin'))
    return render_template('ruangan.html')

@app.route('/ubin', methods=['GET', 'POST'])
def ubin():
    if 'panjang_ruangan' not in session or 'lebar_ruangan' not in session:
        return redirect(url_for('ruangan'))

    if request.method == 'POST':
        session['panjang_ubin'] = float(request.form['panjang_ubin'])
        session['lebar_ubin'] = float(request.form['lebar_ubin'])
        return redirect(url_for('harga'))
    return render_template('ubin.html')

@app.route('/harga', methods=['GET', 'POST'])
def harga():
    if 'panjang_ubin' not in session or 'lebar_ubin' not in session:
        return redirect(url_for('ubin'))

    if request.method == 'POST':
        session['harga_per_ubin'] = float(request.form['harga_per_ubin'])
        return redirect(url_for('hasil'))
    return render_template('harga.html')

@app.route('/hasil')
def hasil():
    if not all(k in session for k in ('panjang_ruangan', 'lebar_ruangan', 'panjang_ubin', 'lebar_ubin', 'harga_per_ubin')):
        return redirect(url_for('ruangan'))

    luas_ruangan = session['panjang_ruangan'] * session['lebar_ruangan']
    luas_ubin = session['panjang_ubin'] * session['lebar_ubin']
    jumlah_ubin = int(luas_ruangan / luas_ubin)
    total_harga = jumlah_ubin * session['harga_per_ubin']

    return render_template('hasil.html', jumlah_ubin=jumlah_ubin, total_harga=total_harga)

if __name__ == '__main__':
    app.run(debug=True)
