from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# --- LISTA DE ACCIONES PARA EL ESCÁNER ---
TICKERS_A_ESCANEAR = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'JPM', 'JNJ', 'V',
    'PG', 'META', 'XOM', 'WMT', 'KO', 'DIS', 'MELI', 'PYPL', 'CRM', 'NFLX', 'BABA'
]

# ==============================================================================
# FUNCIÓN 1: ANÁLISIS TÉCNICO GENERAL (LARGO PLAZO)
# ==============================================================================
def analizar_largo_plazo(simbolo: str):
    try:
        accion = yf.Ticker(simbolo)
        historial = accion.history(period="1y")

        if len(historial) < 200: return None

        historial['SMA50'] = historial['Close'].rolling(window=50).mean()
        historial['SMA200'] = historial['Close'].rolling(window=200).mean()
        delta = historial['Close'].diff()
        ganancia = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        perdida = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        rs = 100 if perdida.iloc[-1] == 0 else ganancia.iloc[-1] / perdida.iloc[-1]
        rsi_actual = 100 - (100 / (1 + rs))

        puntuacion = 0
        if rsi_actual < 35: puntuacion += 1
        if historial['SMA50'].iloc[-1] > historial['SMA200'].iloc[-1]: puntuacion += 1
        if historial['Close'].iloc[-1] > historial['SMA50'].iloc[-1]: puntuacion += 1

        if puntuacion >= 3: recomendacion, clase_css = "COMPRA FUERTE", "strong-buy"
        elif puntuacion == 2: recomendacion, clase_css = "CONSIDERAR COMPRA", "consider-buy"
        else: recomendacion, clase_css = "NO COMPRAR / ESPERAR", "no-buy"
            
        return {
            'simbolo': simbolo.upper(), 'ultimo_precio_raw': historial['Close'].iloc[-1],
            'ultimo_precio': f"${historial['Close'].iloc[-1]:,.2f}",
            'rsi_actual': f"{rsi_actual:.2f}",
            'sma50_actual': f"${historial['SMA50'].iloc[-1]:,.2f}",
            'sma200_actual': f"${historial['SMA200'].iloc[-1]:,.2f}",
            'puntuacion_raw': puntuacion, 'puntuacion_texto': f"{puntuacion} / 3",
            'recomendacion': recomendacion, 'clase_css': clase_css
        }
    except Exception:
        return None

# ==============================================================================
# FUNCIÓN 2: NUEVO PLANIFICADOR DE ESTRATEGIAS (3-6 MESES)
# ==============================================================================
def analizar_mediano_plazo(historial):
    """Realiza un diagnóstico técnico específico para 3-6 meses."""
    historial['SMA20'] = historial['Close'].rolling(window=20).mean()
    historial['SMA50'] = historial['Close'].rolling(window=50).mean()
    precio_actual = historial['Close'].iloc[-1]
    sma20 = historial['SMA20'].iloc[-1]
    sma50 = historial['SMA50'].iloc[-1]
    tendencia_ok = precio_actual > sma20 and sma20 > sma50

    precio_hace_3_meses = historial['Close'].iloc[-63]
    momentum_3m = ((precio_actual / precio_hace_3_meses) - 1) * 100
    momentum_ok = momentum_3m > 5

    historial['Bollinger_Upper'] = historial['SMA20'] + (historial['Close'].rolling(window=20).std() * 2)
    
    delta = historial['Close'].diff()
    ganancia = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    perdida = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = 100 if perdida.iloc[-1] == 0 else ganancia.iloc[-1] / perdida.iloc[-1]
    rsi_actual = 100 - (100 / (1 + rs))

    if rsi_actual < 30: rsi_diag, rsi_css = f"{rsi_actual:.2f} (Sobrevendido)", "gain"
    elif rsi_actual < 55: rsi_diag, rsi_css = f"{rsi_actual:.2f} (Saludable)", "text-primary"
    elif rsi_actual < 70: rsi_diag, rsi_css = f"{rsi_actual:.2f} (Fuerte)", "text-warning"
    else: rsi_diag, rsi_css = f"{rsi_actual:.2f} (Sobrecomprado)", "loss"
    
    condiciones_aptas = tendencia_ok and momentum_ok and rsi_actual < 70

    return {
        "diagnostico_tendencia": "Positiva" if tendencia_ok else "Neutra/Negativa",
        "diagnostico_momentum": f"{momentum_3m:.2f}% (Positivo)" if momentum_ok else f"{momentum_3m:.2f}% (Débil/Negativo)",
        "diagnostico_rsi": rsi_diag,
        "rsi_clase_css": rsi_css,
        "banda_superior_bollinger": historial['Bollinger_Upper'].iloc[-1],
        "condiciones_aptas": condiciones_aptas
    }

def planificar_estrategia(simbolo: str):
    try:
        accion = yf.Ticker(simbolo)
        historial = accion.history(period="1y")

        # <-- CORRECCIÓN: Se añade esta validación para prevenir el error.
        # Se necesitan al menos 63 días de trading (aprox. 3 meses) para los cálculos.
        if len(historial) < 65: # Se usa 65 como margen de seguridad
            return {'error': f"No hay suficientes datos históricos para {simbolo.upper()} (mínimo 3 meses) para generar un plan."}

        info = accion.info
        precio_actual = historial['Close'].iloc[-1]

        diagnostico = analizar_mediano_plazo(historial)
        if not diagnostico["condiciones_aptas"]:
            return {'error': f"Las condiciones de mediano plazo para {simbolo.upper()} no son óptimas. Tendencia: {diagnostico['diagnostico_tendencia']}, Momentum 3M: {diagnostico['diagnostico_momentum']}, RSI: {diagnostico['diagnostico_rsi']}."}

        obj1_conservador = diagnostico["banda_superior_bollinger"]
        obj2_moderado = historial['High'].tail(126).max()
        obj3_optimista = info.get('targetMeanPrice')
        stop_loss = historial['Low'].tail(63).min()

        return {
            'simbolo': simbolo.upper(), 'precio_actual': f"${precio_actual:,.2f}",
            'diagnostico': diagnostico,
            'objetivos': {
                'conservador': f"${obj1_conservador:,.2f} (Potencial: {((obj1_conservador / precio_actual) - 1) * 100:.2f}%)",
                'moderado': f"${obj2_moderado:,.2f} (Potencial: {((obj2_moderado / precio_actual) - 1) * 100:.2f}%)",
                'optimista': f"${obj3_optimista:,.2f} (Potencial: {((obj3_optimista / precio_actual) - 1) * 100:.2f}%)" if obj3_optimista else "No disponible"
            },
            'stop_loss': f"${stop_loss:,.2f} (Riesgo: {((stop_loss / precio_actual) - 1) * 100:.2f}%)",
            'error': None
        }
    except Exception as e:
        return {'error': f"Ocurrió un error inesperado: {e}"}

# ==============================================================================
# RUTAS DE LA APLICACIÓN FLASK (sin cambios)
# ==============================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar_individual_route():
    ticker = request.form['ticker']
    resultado = analizar_largo_plazo(ticker)
    if resultado is None:
        return render_template('index.html', error_individual=f"No se pudo analizar '{ticker}'.")
    return render_template('index.html', resultado_individual=resultado)

@app.route('/buscar', methods=['POST'])
def buscar_oportunidades_route():
    candidatas = [res for ticker in TICKERS_A_ESCANEAR if (res := analizar_largo_plazo(ticker)) is not None]
    oportunidades = sorted(candidatas, key=lambda x: x['puntuacion_raw'], reverse=True)
    return render_template('index.html', oportunidades=oportunidades[:3])

@app.route('/estrategia', methods=['POST'])
def estrategia_route():
    ticker = request.form['ticker']
    plan = planificar_estrategia(ticker)
    if plan.get('error'):
        return render_template('index.html', error_estrategia=plan['error'])
    return render_template('index.html', plan_estrategia=plan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)