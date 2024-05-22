from django.http import FileResponse
from pdv.models import Empresa

def serve_logo(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    return FileResponse(empresa.logo, as_attachment=True, filename='logo.png')