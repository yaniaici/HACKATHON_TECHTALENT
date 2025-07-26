# 🤖 Guía del Chatbot - Marketplace Tarragona

## 📋 Índice
1. [Introducción](#introducción)
2. [Arquitectura del Chatbot](#arquitectura-del-chatbot)
3. [Detección de Intenciones](#detección-de-intenciones)
4. [Tipos de Preguntas Soportadas](#tipos-de-preguntas-soportadas)
5. [Flujo de Datos](#flujo-de-datos)
6. [Endpoints del Chatbot](#endpoints-del-chatbot)
7. [Ejemplos de Uso](#ejemplos-de-uso)
8. [Configuración y Optimización](#configuración-y-optimización)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

El chatbot del Marketplace Tarragona es un asistente inteligente que combina **detección automática de intenciones** con **consultas a la base de datos** y **respuestas naturales** generadas por un LLM (Large Language Model).

### Características principales:
- ✅ **Detección automática**: Analiza la pregunta para identificar la intención
- ✅ **Búsqueda inteligente**: Consulta la base de datos según la intención detectada
- ✅ **Respuestas naturales**: Usa Ollama (LLM) para redactar respuestas en lenguaje natural
- ✅ **Datos reales**: Siempre responde con información actualizada del marketplace
- ✅ **Respuestas rápidas**: Optimizado para respuestas < 1 minuto

---

## 🏗️ Arquitectura del Chatbot

```
Usuario → Pregunta → ChatbotService → Detección de Intención → Base de Datos → Ollama LLM → Respuesta
```

### Componentes principales:

1. **ChatbotService** (`project/server/app/services/chatbot.py`)
   - Analiza la pregunta del usuario
   - Detecta la intención (productos, pedidos, estadísticas)
   - Consulta la base de datos
   - Genera la respuesta

2. **OllamaClient** (`project/server/app/utils/ollama_client.py`)
   - Cliente para comunicarse con Ollama
   - Configuración optimizada para respuestas rápidas
   - Generación de respuestas naturales

3. **Base de Datos MySQL**
   - Almacena datos reales de usuarios, productos y pedidos
   - Consultas optimizadas para búsquedas rápidas

---

## 🔍 Detección de Intenciones

El chatbot analiza la pregunta del usuario y detecta automáticamente si es sobre:

### 1. **Productos por tipo**
- Palabras clave: `"fruta"`, `"lácteo"`, `"panadería"`, `"verdura"`, `"aceite"`, `"huevos"`, `"miel"`, `"carne"`
- Ejemplo: `"¿Qué productos de fruta tienes?"`

### 2. **Productos por origen**
- Palabras clave: `"Tarragona"`, `"origen"`
- Ejemplo: `"¿Qué productos son de Tarragona?"`

### 3. **Productos sin alérgenos**
- Palabras clave: `"sin alérgenos"`, `"no alérgenos"`
- Ejemplo: `"¿Tienes productos sin alérgenos?"`

### 4. **Búsqueda por nombre**
- Palabras clave: `"manzana"`, `"naranja"`, `"pera"`, `"leche"`, `"pan"`
- Ejemplo: `"¿Tienes manzanas?"`

### 5. **Estadísticas del marketplace**
- Preguntas sobre pedidos, usuarios, productos
- Ejemplo: `"¿Cuántos pedidos hay pendientes?"`

### 6. **Creación de pedidos**
- Solicitudes de compra
- Ejemplo: `"Hazme un pedido de 2kg de manzanas"`

---

## 📝 Tipos de Preguntas Soportadas

### ✅ **Preguntas sobre Productos**

#### Por Tipo:
- `"¿Qué productos de fruta tienes disponibles?"`
- `"Muéstrame productos lácteos"`
- `"¿Qué hay en panadería?"`
- `"¿Tienes productos de verdura?"`

#### Por Origen:
- `"¿Qué productos son de Tarragona?"`
- `"¿Qué productos vienen de Valencia?"`
- `"Muéstrame productos locales"`

#### Sin Alérgenos:
- `"¿Tienes productos sin alérgenos?"`
- `"¿Qué productos no tienen alérgenos?"`
- `"Muéstrame productos seguros para alérgicos"`

#### Por Nombre:
- `"¿Tienes manzanas?"`
- `"¿Hay naranjas disponibles?"`
- `"¿Tienes leche?"`
- `"¿Hay pan fresco?"`

### ✅ **Preguntas sobre Pedidos**

#### Estado de Pedidos:
- `"¿Cuántos pedidos hay pendientes?"`
- `"¿Qué pedidos están enviados?"`
- `"Muéstrame pedidos entregados"`

#### Creación de Pedidos:
- `"Hazme un pedido de 2kg de manzanas"`
- `"Quiero comprar 1L de leche"`
- `"Necesito 3 barras de pan"`

### ✅ **Preguntas sobre Estadísticas**

#### Generales:
- `"¿Cuántos usuarios hay registrados?"`
- `"¿Cuántos productos tienes?"`
- `"¿Cuántos pedidos se han hecho?"`

#### Específicas:
- `"¿Qué tipos de productos tienes?"`
- `"¿Cuáles son los productos más populares?"`
- `"¿Qué estados tienen los pedidos?"`

---

## 🔄 Flujo de Datos

### 1. **Recepción de la Pregunta**
```
POST /chatbot/query
{
  "query": "¿Qué productos de fruta tienes disponibles?"
}
```

### 2. **Análisis de la Intención**
El sistema analiza la pregunta y detecta:
- Palabra clave: `"fruta"`
- Intención: **Productos por tipo**
- Tipo: `"fruta"`

### 3. **Consulta a la Base de Datos**
```sql
SELECT id, nombre, tipo, paradero, origen, alergenos 
FROM producto 
WHERE tipo = 'fruta'
```

### 4. **Construcción del Contexto**
```
Contexto: Usuarios:10 Productos:11 Pedidos:11 Tipos:fruta(3), lácteo(2), panadería(1), verdura(1), aceite(1), huevos(1), miel(1), carne de ternera(1) | Productos de tipo fruta: Manzanas, Naranjas, Pera
```

### 5. **Generación de Respuesta**
El LLM recibe:
- **Pregunta original**: `"¿Qué productos de fruta tienes disponibles?"`
- **Lista de productos**: `"Manzanas, Naranjas, Pera"`
- **Contexto del marketplace**

### 6. **Respuesta Final**
```json
{
  "productos": [
    {
      "id": 12,
      "nombre": "Manzanas",
      "tipo": "fruta",
      "paradero": "Mercado Central",
      "origen": "Tarragona",
      "alergenos": "A1"
    },
    {
      "id": 13,
      "nombre": "Naranjas",
      "tipo": "fruta",
      "paradero": "Mercado Central",
      "origen": "Valencia",
      "alergenos": "A2"
    },
    {
      "id": 21,
      "nombre": "Pera",
      "tipo": "fruta",
      "paradero": "Mercado Central",
      "origen": "Lleida",
      "alergenos": "A1"
    }
  ],
  "response": "Tengo disponibles una variedad de productos de fruta: Manzanas (de Tarragona), Naranjas (de Valencia) y Pera (de Lleida). Todos están disponibles en el Mercado Central."
}
```

---

## 🌐 Endpoints del Chatbot

### 1. **Consulta Principal**
```
POST /chatbot/query
```
- **Descripción**: Endpoint principal del chatbot
- **Funcionalidad**: Detecta intención y responde con datos reales
- **Tiempo de respuesta**: < 1 minuto

### 2. **Búsqueda de Productos**
```
GET /chatbot/search?q={término}
```
- **Descripción**: Búsqueda directa de productos
- **Ejemplo**: `GET /chatbot/search?q=manzana`

### 3. **Productos por Tipo**
```
GET /chatbot/products/{tipo}
```
- **Descripción**: Obtiene productos por tipo específico
- **Ejemplo**: `GET /chatbot/products/fruta`

### 4. **Productos por Origen**
```
GET /chatbot/products/origin/{origen}
```
- **Descripción**: Obtiene productos por origen
- **Ejemplo**: `GET /chatbot/products/origin/Tarragona`

### 5. **Productos Sin Alérgenos**
```
GET /chatbot/products/no-allergens
```
- **Descripción**: Obtiene productos sin alérgenos

### 6. **Pedidos por Estado**
```
GET /chatbot/orders/{estado}
```
- **Descripción**: Obtiene pedidos por estado
- **Ejemplo**: `GET /chatbot/orders/pendiente`

### 7. **Estadísticas del Marketplace**
```
GET /chatbot/stats
```
- **Descripción**: Obtiene estadísticas completas

### 8. **Crear Pedido**
```
POST /chatbot/create-order
```
- **Descripción**: Crea un pedido desde el chatbot

### 9. **Probar Conexión**
```
GET /chatbot/test-connection
```
- **Descripción**: Verifica conexión con Ollama

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Productos por Tipo
```bash
curl -X POST http://localhost:5000/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Qué productos de fruta tienes disponibles?"
  }'
```

**Respuesta esperada:**
```json
{
  "productos": [
    {
      "id": 12,
      "nombre": "Manzanas",
      "tipo": "fruta",
      "paradero": "Mercado Central",
      "origen": "Tarragona",
      "alergenos": "A1"
    }
  ],
  "response": "Tengo disponibles productos de fruta como Manzanas de Tarragona..."
}
```

### Ejemplo 2: Productos por Origen
```bash
curl -X POST http://localhost:5000/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Qué productos son de Tarragona?"
  }'
```

### Ejemplo 3: Productos Sin Alérgenos
```bash
curl -X POST http://localhost:5000/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Tienes productos sin alérgenos?"
  }'
```

### Ejemplo 4: Estadísticas
```bash
curl -X POST http://localhost:5000/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Cuántos pedidos hay pendientes?"
  }'
```

---

## ⚙️ Configuración y Optimización

### Configuración de Ollama

#### 1. **Instalar Ollama**
```bash
# Descargar e instalar Ollama desde https://ollama.ai
```

#### 2. **Descargar Modelo**
```bash
ollama pull llama2
```

#### 3. **Verificar Conexión**
```bash
curl http://localhost:11434/api/tags
```

### Optimización de Rendimiento

#### 1. **Parámetros del LLM**
```python
options={
    'num_predict': 100,    # Tokens de respuesta limitados
    'temperature': 0.3,     # Respuestas más determinísticas
    'top_p': 0.7,          # Control de diversidad
    'num_ctx': 512,         # Contexto limitado
    'num_thread': 4,        # Usar 4 threads
    'num_gpu': 1,           # Usar GPU si está disponible
    'stop': ["\n\n", "###"] # Parar en saltos de línea
}
```

#### 2. **Contexto Optimizado**
- Contexto mínimo pero informativo
- Prompts ultra-concisos
- Detección rápida de intenciones

#### 3. **Base de Datos**
- Consultas optimizadas
- Índices en campos de búsqueda
- Conexiones eficientes

---

## 🔧 Troubleshooting

### Problema: Respuesta muy lenta (> 1 minuto)
**Solución:**
1. Verificar que Ollama esté corriendo: `ollama list`
2. Usar modelo más rápido: `ollama pull llama2`
3. Reducir parámetros de tokens y contexto

### Problema: Respuestas genéricas sin datos
**Solución:**
1. Verificar que la base de datos tenga datos
2. Comprobar que la detección de intenciones funcione
3. Revisar logs del servidor

### Problema: Error de conexión con Ollama
**Solución:**
1. Verificar que Ollama esté corriendo: `ollama serve`
2. Comprobar puerto 11434: `curl http://localhost:11434/api/tags`
3. Reiniciar Ollama si es necesario

### Problema: No detecta intenciones correctamente
**Solución:**
1. Revisar palabras clave en `ChatbotService`
2. Agregar más patrones de detección
3. Probar con diferentes formulaciones de preguntas

---

## 📊 Métricas de Rendimiento

### Tiempos de Respuesta Objetivo:
- **Detección de intención**: < 100ms
- **Consulta a base de datos**: < 500ms
- **Generación de respuesta LLM**: < 30s
- **Tiempo total**: < 1 minuto

### Capacidades del Sistema:
- **Preguntas simultáneas**: 10+ usuarios
- **Tipos de productos**: 8 categorías
- **Orígenes soportados**: 6 regiones
- **Estados de pedidos**: 4 estados

---

## 🚀 Próximas Mejoras

### Funcionalidades Planificadas:
1. **Detección de intenciones más avanzada** usando NLP
2. **Soporte para más idiomas** (catalán, inglés)
3. **Integración con voz** para comandos hablados
4. **Análisis de sentimientos** en las preguntas
5. **Recomendaciones personalizadas** basadas en historial
6. **Integración con Power BI** para análisis avanzado

### Optimizaciones Técnicas:
1. **Caché de respuestas** frecuentes
2. **Búsqueda semántica** más avanzada
3. **Modelos de LLM** más rápidos
4. **Microservicios** para escalabilidad

---

## 📞 Soporte

Para problemas técnicos o preguntas sobre el chatbot:

1. **Revisar logs**: `python run.py`
2. **Probar conexión**: `GET /chatbot/test-connection`
3. **Verificar Swagger**: `http://localhost:5000/docs`
4. **Consultar documentación**: Este archivo

---

*Última actualización: Diciembre 2024*
*Versión del chatbot: 1.0.0* 