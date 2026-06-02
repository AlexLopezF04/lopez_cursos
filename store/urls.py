# store/urls.py
from rest_framework_nested import routers
from store.views import (
    UsuarioViewSet,
    CategoriaViewSet,
    CursoViewSet,
    LeccionViewSet,
    MatriculaViewSet,
    ProgresoViewSet,
    ResenaViewSet,
)

# Router principal
router = routers.DefaultRouter()
router.register(r'usuarios',   UsuarioViewSet,   basename='usuario')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'cursos',     CursoViewSet,     basename='curso')
router.register(r'matriculas', MatriculaViewSet, basename='matricula')
router.register(r'progresos',  ProgresoViewSet,  basename='progreso')

# Rutas anidadas: /api/cursos/{curso_pk}/lecciones/
cursos_router = routers.NestedDefaultRouter(router, r'cursos', lookup='curso')
cursos_router.register(r'lecciones', LeccionViewSet, basename='curso-leccion')
cursos_router.register(r'resenas',   ResenaViewSet,  basename='curso-resena')

urlpatterns = router.urls + cursos_router.urls