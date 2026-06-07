import pandas as pd
import psycopg2

print("--- Iniciando proceso de ETL ---")

# 1. Lectura de datos
print("1. Leyendo datos crudos...")
df = pd.read_csv("data/ventas_raw.csv")
print("Datos originales:")
print(df)

# 2. Limpieza de datos
print("\n2. Limpiando datos...")

# Eliminar duplicados
df = df.drop_duplicates()
print(f"- Duplicados eliminados. Quedan {len(df)} registros")

# Llenar nulos en precio_unitario con 0
df['precio_unitario'] = df['precio_unitario'].fillna(0)
print("- Valores nulos en precio reemplazados por 0")

# Estandarizar fechas
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.strftime('%Y-%m-%d')

# Eliminar filas donde la fecha no se pudo corregir
df = df.dropna(subset=['fecha'])
print(f"- Fechas inválidas eliminadas. Quedan {len(df)} registros")

print("\nDatos limpios:")
print(df)

# 3. Carga a PostgreSQL
print("\n3. Guardando en Base de Datos...")
conn = None
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5434,
        database="ventas_db",
        user="admin",
        password="secret123"
    )
    cursor = conn.cursor()

    # Crear tabla
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INT,
            fecha DATE,
            producto VARCHAR(50),
            cantidad INT,
            precio_unitario FLOAT
        )
    """)
    conn.commit()
    print("- Tabla 'ventas' creada/verificada")
    
    # Limpiar tabla antes de insertar
    cursor.execute("DELETE FROM ventas")
    conn.commit()
    
    # Insertar datos
    for index, row in df.iterrows():
        cursor.execute(
            "INSERT INTO ventas (id, fecha, producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s, %s)",
            (int(row['id']), row['fecha'], row['producto'], int(row['cantidad']), float(row['precio_unitario']))
        )
    
    conn.commit()
    print(f"✅ {len(df)} registros cargados exitosamente en PostgreSQL")
    
    # Validar
    cursor.execute("SELECT COUNT(*) FROM ventas")
    total = cursor.fetchone()[0]
    print(f"Total de registros en la tabla: {total}")
    
except Exception as e:
    print(f" Error: {e}")

finally:
    if conn:
        conn.close()
        print("Conexión cerrada")

print("\n--- Proceso finalizado ---")