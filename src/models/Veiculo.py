from src.services.DatabaseService import DatabaseService

class Veiculo:
    def __init__(self, id, marca, modelo, ano, preco_referencia):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.preco_referencia = preco_referencia

    @staticmethod
    def get_todas_marcas():
        """Retorna uma lista com todas as marcas cadastradas (sem repetir)"""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT marca FROM veiculos ORDER BY marca")
            # Transforma o resultado [(Fiat,), (Honda,)] em uma lista simples ['Fiat', 'Honda']
            marcas = [row[0] for row in cursor.fetchall()]
            return marcas
        except Exception as e:
            print(f"Erro ao buscar marcas: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def buscar_por_filtro(marca, modelo=None, ano=None):
        """Busca veículos baseados nos filtros preenchidos"""
        conn = DatabaseService.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, marca, modelo, ano, preco_referencia FROM veiculos WHERE marca = ?"
        params = [marca]

        if modelo:
            query += " AND modelo LIKE ?"
            params.append(f"%{modelo}%")
        
        if ano:
            query += " AND ano = ?"
            params.append(ano)

        try:
            cursor.execute(query, params)
            resultados = []
            for row in cursor.fetchall():
                resultados.append(Veiculo(row[0], row[1], row[2], row[3], row[4]))
            return resultados
        finally:
            conn.close()