# 🏆 LUCY - Sistema de Pronósticos Deportivos

## 📋 Descripción

LUCY es un sistema de extracción, transformación y carga (ETL) de datos deportivos que consume la API de Football API Sports, limpia y normaliza los datos, y los prepara para análisis y pronósticos.

## 🏗️ Arquitectura

```
/app/
├── pipeline.py              # Orquestador principal del ETL
├── main_fetcher.py         # Extractor de datos de API
├── main_cleaner.py         # Limpiador y normalizador de datos
│
├── src/
│   ├── fetcher/            # Módulo de extracción
│   │   ├── rapidapi_client.py  # Cliente HTTP con reintentos
│   │   ├── save_raw.py         # Guardado de datos raw
│   │   ├── config.py           # Configuración
│   │   └── logger.py           # Logging
│   │
│   ├── cleaner/            # Módulo de limpieza
│   │   ├── loader.py           # Carga de archivos raw
│   │   ├── normalizer.py       # Normalización de datos
│   │   ├── validator.py        # Validación de datos
│   │   ├── save_clean.py       # Guardado de datos limpios
│   │   └── logger.py           # Logging
│   │
│   └── common/             # Utilidades compartidas
│       ├── exceptions.py       # Excepciones personalizadas
│       └── retry.py            # Lógica de reintentos
│
├── data/
│   ├── raw/                # Datos sin procesar (JSON)
│   └── clean/              # Datos limpios (CSV)
│
└── logs/                   # Logs del sistema
```

## 🚀 Instalación

### 1. Requisitos Previos

- Python 3.8+
- pip

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita `.env` y agrega tu API key de Football API Sports:
   ```
   API_KEY=tu_api_key_aqui
   ```

3. Obtén tu API key en: https://www.api-football.com/

## 📖 Uso

### Ejecutar Pipeline Completo

Ejecuta el proceso completo de extracción y limpieza:

```bash
python pipeline.py
```

### Ejecutar Solo Extracción

```bash
python main_fetcher.py
```

### Ejecutar Solo Limpieza

```bash
python main_cleaner.py
```

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|----------|
| `API_KEY` | API key de Football API Sports | Requerido |
| `BASE_URL` | URL base de la API | `https://v3.football.api-sports.io` |
| `DEFAULT_COUNTRY` | País por defecto | `england` |
| `DEFAULT_SEASON` | Temporada por defecto | `2023` |
| `MAX_RETRIES` | Reintentos en caso de fallo | `3` |
| `RETRY_DELAY` | Delay entre reintentos (seg) | `2` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

## 📊 Flujo de Datos

1. **Extracción (Fetcher)**:
   - Consume API de Football API Sports
   - Guarda datos raw en `data/raw/` (JSON)
   - Logging completo de operaciones
   - Reintentos automáticos en caso de fallo

2. **Limpieza (Cleaner)**:
   - Carga archivos JSON de `data/raw/`
   - Normaliza estructura de datos
   - Valida integridad
   - Elimina duplicados
   - Guarda en `data/clean/` (CSV)

## 🛡️ Seguridad

- ✅ API keys en variables de entorno (nunca en código)
- ✅ `.env` en `.gitignore` (no se sube a repositorio)
- ✅ Validación de datos de entrada
- ✅ Manejo seguro de excepciones

## 📝 Logs

Los logs se guardan en el directorio `logs/` con el formato:
- `fetch_YYYY_MM_DD.log` - Logs de extracción
- `cleaner_YYYY_MM_DD.log` - Logs de limpieza

## 🐛 Troubleshooting

### Error: "API key no encontrada"
- Verifica que el archivo `.env` exista
- Confirma que `API_KEY` esté configurada

### Error: "API request failed"
- Verifica tu conexión a internet
- Confirma que tu API key sea válida
- Revisa los límites de tu plan en api-football.com

### Error: "No raw files found"
- Ejecuta primero `main_fetcher.py` para generar datos raw
- Verifica que exista el directorio `data/raw/`

## 📈 Próximas Fases

- [✅] **Fase 1**: Seguridad, logging y manejo de errores (COMPLETADA)
- [✅] **Fase 2**: Integración con MongoDB para escalabilidad (COMPLETADA)
- [ ] **Fase 3**: API REST con FastAPI
- [ ] **Fase 4**: Módulo de pronósticos con ML

## 🆕 Fase 2: MongoDB Integration

### Características
- ✅ Almacenamiento dual: Archivos + MongoDB
- ✅ Procesamiento por lotes (1000 registros/lote)
- ✅ Índices optimizados para queries rápidas
- ✅ Paginación completa
- ✅ Filtros por país y temporada
- ✅ Graceful degradation (funciona sin MongoDB)

### Uso con MongoDB

```bash
# Iniciar MongoDB (Docker)
docker run -d -p 27017:27017 --name lucy-mongo mongo:latest

# Ejecutar pipeline (guarda en archivos + MongoDB)
python pipeline.py

# Ver demo de funcionalidades
python demo_mongodb.py

# Tests de Fase 2
python test_phase2.py
```

### Consultas Rápidas

```python
from src.database.repositories import LeagueRepository

repo = LeagueRepository()

# Estadísticas
stats = repo.get_stats()

# Paginación
leagues = repo.get_all_leagues(page=1, limit=50)

# Filtros
england = repo.get_by_country('England')
season_23 = repo.get_by_season(2023)
```

## 📄 Licencia

Proyecto privado - Todos los derechos reservados

## 👤 Autor

Desarrollado para análisis y pronósticos deportivos
