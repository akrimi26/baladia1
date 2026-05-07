from django.urls import path
from .views import demandes, update_statut, dashboard , form_page, mes_demandes_page,admin_demandes_page, login_page, dashboard_page, suivi_page, suivi_demande
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('demandes/', demandes),

    # 🔐 JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('demandes/<int:id>/statut/', update_statut),
    path('dashboard/', dashboard),  # 👈 الجديد
    path('form/', form_page),
    path('mes-demandes/', mes_demandes_page),
    path('login-page/', login_page),
    path('dashboard-page/', dashboard_page),
    path('suivi/', suivi_demande),
    path('suivi-page/', suivi_page),
    path('admin-demandes/', admin_demandes_page),
]