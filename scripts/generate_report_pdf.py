from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

report_text = '''Informe rápido — Estado y recomendaciones

Resumen:
La app arranca y responde; ya creé y apliqué migraciones para todas las tablas básicas y guardé cambios en GitHub.

Dependencias:
- Mantener: fastapi, uvicorn, sqlalchemy, jinja2, openpyxl, passlib.
- Revisar/posible remover: bcrypt (no se usa directamente), psycopg2-binary (solo para Postgres), itsdangerous (no encontrado en el código).

Configuración / secretos:
Mover SESSION_SECRET y DATABASE_URL a variables de entorno y añadir .env.example. Archivos clave: app/main.py y app/config.py.

Migraciones:
- alembic/versions/c815f8fba4e6_create_tablas_vivero.py
- alembic/versions/d6ee3648b9f9_add_users_and_ventas_tables.py
Recomendación: usar Alembic en producción (no usar create_all allí).

Seguridad:
- Asegurar SessionMiddleware en producción (https_only=True) y cookies seguras.
- Considerar protección CSRF para formularios POST o usar JWT para API.
- Aplicar verificación de permisos en rutas administrativas (usar dependencia require_login o Depends).

Calidad de código:
- Añadir linters (ruff/flake8) y pre-commit.
- Añadir typing gradual con mypy si se desea.

Tests & CI:
- Crear tests básicos (arranque, rutas públicas, CRUD produtos) y workflow de GitHub Actions para instalar deps, ejecutar linters y tests.

Próximos pasos sugeridos:
1) Limpiar y fijar requirements.txt.
2) Añadir .env.example y documentar variables en README.md.
3) Forzar protección de rutas críticas y ajustar cookies seguras.
4) Añadir tests mínimos + GitHub Actions.
5) Ejecutar auditoría para código no usado y proponer eliminación segura.

Si quieres, empiezo por cualquiera de los pasos anteriores.
'''

output_path = 'reports/kuadra_review.pdf'

c = canvas.Canvas(output_path, pagesize=A4)
width, height = A4

x = 2*cm
y = height - 2*cm

for line in report_text.split('\n'):
    if y < 2*cm:
        c.showPage()
        y = height - 2*cm
    c.drawString(x, y, line)
    y -= 12

c.save()
print('PDF_CREATED:', output_path)
