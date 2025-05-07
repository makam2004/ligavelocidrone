from flask import Flask, render_template_string, request, redirect, url_for, flash
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import os
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "clave-secreta"

def leer_jugadores_desde_txt(ruta="jugadores.txt"):
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def escribir_jugador(nombre, ruta="jugadores.txt"):
    jugadores = leer_jugadores_desde_txt(ruta)
    if nombre not in jugadores:
        try:
            with open(ruta, "a+", encoding="utf-8") as f:
                f.seek(0, 2)
                if f.tell() > 0:
                    f.seek(f.tell() - 1)
                    if f.read(1) != "\n":
                        f.write("\n")
                f.write(nombre + "\n")
            return True
        except Exception:
            return False
    return False

def tiempo_a_segundos(tiempo_str):
    try:
        if ':' in tiempo_str:
            mins, secs = tiempo_str.split(':')
            return int(mins) * 60 + float(secs)
        return float(tiempo_str)
    except:
        return float('inf')

def obtener_resultados(url, jugadores_objetivos):
    resultados = []
    nombre_track = "Track desconocido"
    escenario = "Escenario desconocido"

    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        escenario_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.text-center")))
        escenario = escenario_elem.text.strip()

        encabezado = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.container h3")))
        nombre_track = encabezado.text.strip()

        race_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Race Mode')]")))
        race_tab.click()

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
        time.sleep(1.5)

        filas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

        for fila in filas[:50]:
            columnas = fila.find_elements(By.TAG_NAME, "td")
            if len(columnas) >= 3:
                tiempo = columnas[1].text.strip()
                jugador = columnas[2].text.strip()
                if jugador in jugadores_objetivos:
                    resultados.append((tiempo_a_segundos(tiempo), tiempo, jugador))

    except Exception as e:
        resultados.append((float('inf'), f"Error: {e}", ""))

    finally:
        driver.quit()

    return escenario, nombre_track, resultados

@app.route('/', methods=["GET", "POST"])
def mostrar_resultados():
    if request.method == "POST":
        nuevo_piloto = request.form.get("nuevo_piloto", "").strip()
        recaptcha_simulado = request.form.get("soy_humano")

        if not nuevo_piloto:
            flash("Nombre de piloto vacío.", "error")
        elif recaptcha_simulado != "on":
            flash("Debes marcar que no eres un robot.", "error")
        else:
            if escribir_jugador(nuevo_piloto):
                flash(f"Piloto '{nuevo_piloto}' añadido correctamente.", "success")
            else:
                flash(f"El piloto '{nuevo_piloto}' ya está en la lista.", "error")
        return redirect(url_for("mostrar_resultados"))

    jugadores = leer_jugadores_desde_txt()
    semana_actual = datetime.date.today().isocalendar()[1]

    urls = [
        "https://www.velocidrone.com/leaderboard/16/1777/All",
        "https://www.velocidrone.com/leaderboard/16/1780/All"
    ]

    todos_resultados = []
    ranking = defaultdict(int)

    puntos_posicion = [10, 8, 6, 4, 5]
    puntos_default = 1

    for url in urls:
        escenario, nombre_track, resultados = obtener_resultados(url, jugadores)
        resultados.sort()
        formateados = []
        for i, (_, tiempo, jugador) in enumerate(resultados):
            formateados.append(f"{i + 1}\t{tiempo}\t{jugador}")
            if jugador:
                puntos = puntos_posicion[i] if i < len(puntos_posicion) else puntos_default
                ranking[jugador] += puntos
        todos_resultados.append((escenario, nombre_track, formateados))

    ranking_ordenado = sorted(ranking.items(), key=lambda x: -x[1])
    ranking_formateado = [f"{i + 1}. {nombre} - {puntos} pts" for i, (nombre, puntos) in enumerate(ranking_ordenado)]

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>LIGA VELOCIDRONE SEMANA {{ semana }}</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #f2f2f2;
                padding: 40px;
                margin: 0;
            }
            .top-bar {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 30px;
            }
            .top-bar img {
                height: 50px;
                margin: 0 20px;
            }
            h1 {
                font-size: 40px;
                color: white;
                text-align: center;
                background-color: #333;
                padding: 10px;
                border-radius: 8px;
            }
            .tracks {
                display: flex;
                gap: 40px;
                margin-bottom: 30px;
            }
            .card {
                flex: 1;
                background: #fff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                min-width: 300px;
            }
            h2, h3 {
                color: #333;
                margin-bottom: 10px;
            }
            .resultado {
                font-size: 16px;
                white-space: pre;
                font-family: monospace;
                margin-top: 10px;
            }
            .formulario {
                background: #fff;
                padding: 15px;
                border-radius: 12px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                width: 250px;
                margin-left: auto;
            }
            .formulario input[type="text"] {
                width: 100%;
                padding: 6px;
                margin-bottom: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .formulario input[type="submit"] {
                padding: 8px 16px;
                background-color: #007bff;
                border: none;
                color: white;
                cursor: pointer;
                border-radius: 5px;
            }
            .mensaje {
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .success { background-color: #d4edda; color: #155724; }
            .error { background-color: #f8d7da; color: #721c24; }
            .ranking {
                background: #fff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                margin: 30px 0;
            }
        </style>
    </head>
    <body>
        <div class="top-bar">
            <img src="https://www.velocidrone.com/assets/images/VelocidroneLogoWeb.png" alt="Logo">
            <h1>LIGA VELOCIDRONE SEMANA {{ semana }}</h1>
            <img src="https://www.velocidrone.com/assets/images/VelocidroneLogoWeb.png" alt="Logo">
        </div>

        <div class="tracks">
            {% for escenario, nombre_track, resultados in todos_resultados %}
            <div class="card">
                <h2>{{ escenario }} - {{ nombre_track }}</h2>
                <div class="resultado">{{ resultados|join('\\n') }}</div>
            </div>
            {% endfor %}
        </div>

        <div class="ranking">
            <h2>Ranking semanal</h2>
            <div class="resultado">{{ ranking_formateado|join('\\n') }}</div>
        </div>

        <div class="formulario">
            <h3>Alta Piloto</h3>
            {% with messages = get_flashed_messages(with_categories=true) %}
              {% if messages %}
                {% for category, message in messages %}
                  <div class="mensaje {{ category }}">{{ message }}</div>
                {% endfor %}
              {% endif %}
            {% endwith %}
            <form method="post">
                <input type="text" name="nuevo_piloto" placeholder="Nombre del piloto">
                <label><input type="checkbox" name="soy_humano"> No soy un robot</label><br><br>
                <input type="submit" value="Añadir">
            </form>
        </div>
    </body>
    </html>
    """

    return render_template_string(html,
                                  semana=semana_actual,
                                  todos_resultados=todos_resultados,
                                  ranking_formateado=ranking_formateado)

if __name__ == '__main__':
    app.run(debug=True)
