# Ajustar nombres de columnas que coincidan con el ERXCEL, revisar los FKs, verificar los campos oblñigatorios y no nulos
# Instalar pip install pandas psycopg2 openpyxl


import pandas as pd
import psycopg2

# Configura tu conexión a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="tu_base_de_datos",
    user="tu_usuario",
    password="tu_contraseña",
)

cursor = conn.cursor()

# Carga el Excel
df = pd.read_excel(
    "datos_DISAHP.xlsx", sheet_name="Hoja1"
)  # Ajusta nombre si es necesario

# 1. Insertar tipo_equipo
tipo_equipo_unicos = df["tipo_equipo"].dropna().unique()

for tipo in tipo_equipo_unicos:
    cursor.execute(
        "INSERT INTO tipo_equipo (nombre) VALUES (%s) ON CONFLICT DO NOTHING;", (tipo,)
    )

# 2. Insertar unidad_admin
unidad_admin_df = df[
    ["id_unidad", "nombre_unidad", "ubicacion", "piso", "siglas", "responsable"]
].drop_duplicates()

for _, row in unidad_admin_df.iterrows():
    cursor.execute(
        """
        INSERT INTO unidad_admin (id_uni_admin, nombre, ubicacion, piso, siglas, responsable)
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id_uni_admin) DO NOTHING;
    """,
        tuple(row),
    )

# 3. Insertar usuarios
usuarios_df = df[
    ["id_usuario", "nombre_usuario", "correo", "rol", "password", "activo"]
].drop_duplicates()

for _, row in usuarios_df.iterrows():
    cursor.execute(
        """
        INSERT INTO usuario (id_usuario, nombre, correo, rol, password, activa)
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id_usuario) DO NOTHING;
    """,
        tuple(row),
    )

# (Opcional) 4. Insertar empleados si no tienen FK dependiente
empleados_df = df[
    ["No_empleado", "Nombres", "a_paterno", "a_materno", "cargo"]
].drop_duplicates()

for _, row in empleados_df.iterrows():
    cursor.execute(
        """
        INSERT INTO empleado (No_empleado, Nombres, a_paterno, a_materno, cargo)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (No_empleado) DO NOTHING;
    """,
        tuple(row),
    )

# Finalizar
conn.commit()
cursor.close()
conn.close()
print("Datos insertados correctamente 🚀")
