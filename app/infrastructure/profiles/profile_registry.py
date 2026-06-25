from typing import Dict, Any
from app.infrastructure.profiles.lenart_profile import PROFILE as lenart_prof

# Centralna baza konfiguracji dostawców, odizolowana od logiki biznesowej
_REGISTRY: Dict[str, Dict[str, Any]] = {
    "LENART": lenart_prof,
  #  "HELVETICA": helvetica_prof,
   # "MEBLOSIEK": meblosiek_prof
}

def get_active_profiles() -> Dict[str, Dict[str, Any]]:
    """Funkcja zwracająca kopię rejestru dostawców, chroniąca oryginalne dane przed modyfikacją."""
    return _REGISTRY.copy()