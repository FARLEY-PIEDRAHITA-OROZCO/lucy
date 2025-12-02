#!/bin/bash
# Demo de la API REST de LUCY

echo ""
echo "======================================================================"
echo "           🚀 DEMO API REST - LUCY SPORTS"
echo "======================================================================"
echo ""
echo "⚠️  Asegúrate de que la API esté corriendo:"
echo "   python start_api.py"
echo ""
echo "Presiona Enter para continuar..."
read

BASE_URL="http://localhost:8001"

echo ""
echo "----------------------------------------------------------------------"
echo "1️⃣  ROOT - Información de la API"
echo "----------------------------------------------------------------------"
curl -s $BASE_URL/ | python -m json.tool
echo ""

echo "----------------------------------------------------------------------"
echo "2️⃣  HEALTH CHECK - Estado del sistema"
echo "----------------------------------------------------------------------"
curl -s $BASE_URL/api/health | python -m json.tool
echo ""

echo "----------------------------------------------------------------------"
echo "3️⃣  STATS - Estadísticas generales"
echo "----------------------------------------------------------------------"
curl -s $BASE_URL/api/stats | python -m json.tool 2>/dev/null || echo "MongoDB no disponible"
echo ""

echo "----------------------------------------------------------------------"
echo "4️⃣  LEAGUES - Primeras 5 ligas"
echo "----------------------------------------------------------------------"
curl -s "$BASE_URL/api/leagues?page=1&limit=5" | python -m json.tool 2>/dev/null || echo "MongoDB no disponible"
echo ""

echo "----------------------------------------------------------------------"
echo "5️⃣  FILTER BY COUNTRY - Ligas de England"
echo "----------------------------------------------------------------------"
curl -s "$BASE_URL/api/leagues/country/England?limit=3" | python -m json.tool 2>/dev/null || echo "MongoDB no disponible"
echo ""

echo "----------------------------------------------------------------------"
echo "6️⃣  PIPELINE STATUS - Estado del pipeline"
echo "----------------------------------------------------------------------"
curl -s $BASE_URL/api/pipeline/status | python -m json.tool
echo ""

echo "======================================================================"
echo "✅ Demo completada"
echo "======================================================================"
echo ""
echo "📚 Documentación interactiva disponible en:"
echo "   Swagger: $BASE_URL/docs"
echo "   ReDoc:   $BASE_URL/redoc"
echo ""
