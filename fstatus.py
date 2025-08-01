# analyzer.py
import yfinance as yf
import pandas as pd
import google.generativeai as genai
import os
import sys

# --- Configuración de la API de Gemini (igual que antes) ---
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Error: La variable de entorno GEMINI_API_KEY no está configurada.")
    sys.exit(1)

model = genai.GenerativeModel('gemini-2.5-flash')

def obtener_estados_financieros(ticker_symbol):
    """
    Obtiene los balances, estados de resultados y flujos de caja de una empresa
    utilizando yfinance y los devuelve como un diccionario de DataFrames.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        balance_sheet = ticker.balance_sheet
        income_stmt = ticker.income_stmt
        cash_flow = ticker.cashflow
        
        if balance_sheet.empty or income_stmt.empty or cash_flow.empty:
            return None
            
        return {
            "balance_sheet": balance_sheet,
            "income_stmt": income_stmt,
            "cash_flow": cash_flow
        }
    except Exception:
        return None

def analizar_con_gemini(ticker_symbol):
    """
    Usa la API de Gemini para analizar los estados financieros y devolver una conclusión
    como una cadena de texto.
    """
    datos_financieros = obtener_estados_financieros(ticker_symbol)

    if not datos_financieros:
        return "No se pudieron obtener datos financieros para el análisis."
        
    prompt = f"""
    Eres un analista financiero. Aquí tienes los últimos estados financieros anuales de la empresa {ticker_symbol}.
    Tu tarea es analizar estos datos para determinar la "salud" financiera de la empresa y ofrecer una conclusión clara.
    Considera aspectos como la rentabilidad, la liquidez, el endeudamiento y el crecimiento.
    
    Responde en español y de una manera estructurada y fácil de entender.

    Balance General (últimos años):
    {datos_financieros['balance_sheet'].to_string()}

    Estado de Resultados (últimos años):
    {datos_financieros['income_stmt'].to_string()}
    
    Estado de Flujo de Caja (últimos años):
    {datos_financieros['cash_flow'].to_string()}
    
    Análisis y Conclusión:
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "Ocurrió un error al interactuar con la API de Gemini. Verifique la conexión o la clave de API."
