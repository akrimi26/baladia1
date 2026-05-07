from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Demande
from .serializers import DemandeSerializer
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# Create your views here.
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_statut(request, id):

    if not request.user.is_staff:
        return Response({"error": "غير مسموح"}, status=403)

    try:
        demande = Demande.objects.get(id=id)
    except Demande.DoesNotExist:
        return Response({"error": "غير موجود"}, status=404)

    statut = request.data.get('statut')

    if statut not in ['acceptee', 'refusee']:
        return Response({"error": "statut غير صحيح"}, status=400)

    demande.statut = statut
    demande.save()

    return Response({"message": "تم التحديث بنجاح", "statut": statut})

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def demandes(request):

    # 🧑‍💼 admin يشوف الكل
    if request.method == 'GET':

        if not request.user.is_authenticated:
            return Response({"error": "غير مسموح"}, status=403)

        if request.user.is_staff:
            demandes = Demande.objects.all()
        else:
            demandes = Demande.objects.filter(utilisateur=request.user)

        serializer = DemandeSerializer(demandes, many=True)
        return Response(serializer.data)

    # 👤 المواطن يرسل مطلب بدون login
    if request.method == 'POST':

        serializer = DemandeSerializer(data=request.data)

        if serializer.is_valid():

            # ✅ إذا user متصل
            if request.user.is_authenticated:
                serializer.save(utilisateur=request.user)

            # ✅ مواطن عادي بدون login
            else:
                serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):

    # 🧑‍💼 admin فقط يشوف الإحصائيات
   
    if not request.user.is_staff:
        return Response({"error": "غير مسموح"}, status=403)

    total = Demande.objects.count()
    en_attente = Demande.objects.filter(statut='en_attente').count()
    acceptee = Demande.objects.filter(statut='acceptee').count()
    refusee = Demande.objects.filter(statut='refusee').count()
    eau = Demande.objects.filter(type_service='eau').count()
    electricite = Demande.objects.filter(type_service='electricite').count()
    
    return Response({
        "total": total,
        "en_attente": en_attente,
        "acceptee": acceptee,
        "refusee": refusee,
        "eau": eau,
        "electricite": electricite,
    })
def form_page(request):
    return render(request, 'form.html')

def mes_demandes_page(request):
    return render(request, 'mes_demandes.html')
def login_page(request):
    return render(request, 'login.html')
def dashboard_page(request):
    return render(request, 'dashboard.html')
@api_view(['POST'])
def suivi_demande(request):

    cin = request.data.get('cin', '').strip()
    id_demande = request.data.get('id')

    try:

        demande = Demande.objects.get(
            id=id_demande,
            cin__iexact=cin
        )

        return Response({
            "id": demande.id,
            "nom": demande.nom,
            "prenom": demande.prenom,
            "statut": demande.statut,
            "type_service": demande.type_service,
            "date_demande": demande.date_demande
        })

    except Demande.DoesNotExist:

        return Response({
            "error": "الطلب غير موجود"
        }, status=404)
def suivi_page(request):
    return render(request, 'suivi.html')
def admin_demandes_page(request):
    return render(request, 'admin_demandes.html')