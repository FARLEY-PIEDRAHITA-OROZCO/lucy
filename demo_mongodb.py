#!/usr/bin/env python3
"""
Script de demostración de funcionalidades MongoDB - Fase 2
Muestra todas las capacidades implementadas
"""

from src.database.repositories import LeagueRepository

def main():
    print("\n" + "="*70)
    print(" "*15 + "🚀 DEMO MONGODB - FASE 2" + " "*15)
    print("="*70)
    
    repo = LeagueRepository()
    
    if not repo.is_available():
        print("\n⚠️  MongoDB no disponible - Sistema en modo solo archivos")
        return
    
    # 1. Estadísticas generales
    print("\n📊 ESTADÍSTICAS GENERALES")
    print("-" * 70)
    stats = repo.get_stats()
    print(f"  Total de ligas: {stats['total_leagues']}")
    print(f"  Países únicos: {stats['countries']}")
    print(f"  Temporadas: {', '.join(map(str, stats['seasons']))}")
    print(f"  Lista de países: {', '.join(stats['country_list'])}")
    
    # 2. Paginación
    print("\n📄 PAGINACIÓN (5 registros por página)")
    print("-" * 70)
    
    page_1 = repo.get_all_leagues(page=1, limit=5)
    print(f"\n  Página 1:")
    for i, league in enumerate(page_1, 1):
        print(f"    {i}. {league['league_name']} ({league['type']})")
    
    page_2 = repo.get_all_leagues(page=2, limit=5)
    print(f"\n  Página 2:")
    for i, league in enumerate(page_2, 1):
        print(f"    {i}. {league['league_name']} ({league['type']})")
    
    # 3. Filtro por país
    print("\n🌍 FILTRO POR PAÍS")
    print("-" * 70)
    england_leagues = repo.get_by_country('England', page=1, limit=10)
    print(f"  Ligas de England (primeras 10):")
    for i, league in enumerate(england_leagues, 1):
        print(f"    {i}. {league['league_name']}")
    
    # 4. Filtro por temporada
    print("\n📅 FILTRO POR TEMPORADA")
    print("-" * 70)
    season_2023 = repo.get_by_season(2023, page=1, limit=5)
    print(f"  Temporada 2023 (primeras 5):")
    for i, league in enumerate(season_2023, 1):
        print(f"    {i}. {league['league_name']} - {league['start']} a {league['end']}")
    
    # 5. Conteo total
    print("\n🔢 CONTEO TOTAL")
    print("-" * 70)
    total = repo.count_leagues()
    print(f"  Total de documentos en MongoDB: {total}")
    
    # 6. Performance test
    print("\n⚡ TEST DE PERFORMANCE")
    print("-" * 70)
    import time
    
    start = time.time()
    all_leagues = repo.get_all_leagues(page=1, limit=100)
    duration = (time.time() - start) * 1000
    print(f"  Query de 100 registros: {duration:.2f}ms")
    
    start = time.time()
    filtered = repo.get_by_country('England', page=1, limit=50)
    duration = (time.time() - start) * 1000
    print(f"  Query filtrada por país: {duration:.2f}ms")
    
    print("\n" + "="*70)
    print("✅ Demo completada - Todas las funcionalidades MongoDB operativas")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
