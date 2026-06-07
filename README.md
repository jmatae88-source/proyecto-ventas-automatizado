# Sistema de Automatización de Reportes de Ventas

## Descripción
Proyecto DevOps/DataOps que automatiza la limpieza y carga de datos de ventas en PostgreSQL.

## Estructura del Proyecto
proyecto-ventas-automatizado/
├── data/
│ └── ventas_raw.csv
├── scripts/
│ └── procesar_ventas.py
├── terraform/
│ └── main.tf
├── Jenkinsfile
└── README.md


## Tecnologías
- Git y GitHub
- Docker
- Terraform
- Python (Pandas, Psycopg2)
- PostgreSQL
- Jenkins

## Cómo Ejecutar
1. Clonar el repositorio
2. Ejecutar `terraform apply` en la carpeta terraform
3. Ejecutar `python scripts/procesar_ventas.py`