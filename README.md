**ANALISIS INDIVIDUAL**

**Desglose por Indicador**
- Medias Móviles Simples (SMA 50 y SMA 200): Son el corazón de la estrategia. Estos indicadores no reaccionan a la volatilidad diaria, sino que suavizan los datos de precios para mostrar la tendencia subyacente del mercado.
-- SMA 200 (Largo Plazo): Es el indicador de tendencia a largo plazo más observado. Si el precio está por encima, la acción se considera en una tendencia alcista estructural.
-- SMA 50 (Mediano Plazo): Representa la tendencia de mediano plazo. La relación entre la SMA de 50 y la de 200 (el "Cruce Dorado" o Golden Cross) es una de las señales más potentes de un cambio de tendencia hacia el alza a largo plazo.
- Índice de Fuerza Relativa (RSI de 14 días): Aunque este es un indicador de más corto plazo, en esta estrategia no se usa de forma aislada. Su función es encontrar un punto de entrada oportuno dentro de una tendencia alcista ya confirmada por las medias móviles. Busca responder a la pregunta: "Dado que la acción está en una buena tendencia a largo plazo, ¿está actualmente 'sobrevendida' o en un buen precio para entrar?".

**En Resumen**
Puedes pensar en la lógica del script de esta manera:

- Estrategia (Largo Plazo): Primero, usa las medias móviles de 50 y 200 días para confirmar que la acción tiene una tendencia alcista sólida y sostenida. Esta es la condición principal.
- Táctica (Corto Plazo): Una vez confirmada la tendencia general, usa el RSI para identificar un buen momento para la compra, idealmente cuando el precio ha tenido una caída temporal (RSI bajo) dentro de esa gran tendencia alcista.

**ESCANER DE MERCADO**
Dada una lista finita de tickers hace el **analisis individual** para cada una y devuelve un top 3 recomendado

**PLANIFICADOR (3/6 MESES)**
**Indicadores**
- Medias Móviles de 20 y 50 días (Tendencia): Nos dicen la dirección general del precio (¿va hacia arriba?).
- Momentum: Se calcula el rendimiento de los últimos 3 meses para medir la fuerza reciente. Nos dice la fuerza de esa dirección (¿está subiendo con ganas?).
- RSI (Impulso/Timing): Nos dice la temperatura actual del precio (¿está sobrecomprado o sobrevendido ahora mismo?).

Diagnóstico de Mediano Plazo: Antes de darte un plan, la herramienta te dice si las condiciones son aptas.
Revisa si la tendencia, el momentum, impulso y timing son positivos. Si no lo son, te lo advertirá y no sugerirá la inversión.

**Plan de Inversión Propuesto**
- Objetivo Conservador: Es el primer objetivo a alcanzar, basado en la volatilidad actual. Podrías considerar tomar una parte de tus ganancias aquí.
-- Basado en la Banda de Bollinger superior (un objetivo de volatilidad a corto plazo).
- Objetivo Moderado: Un objetivo más ambicioso, basado en barreras de precios (resistencias) históricas.
-- Basado en el máximo de los últimos 6 meses (un nivel de resistencia clave).
- Objetivo Optimista: El escenario ideal según el consenso de los analistas.
-- Basado en el consenso de los analistas (si está disponible).
- Stop-Loss: Tu red de seguridad. Si el precio cae a este nivel, la estrategia sugiere vender para limitar tus pérdidas.
