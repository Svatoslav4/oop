from fastapi import FastAPI
from pydantic import BaseModel

# Імпортуємо фасад та його підсистеми
from facade import SmartHomeFacade
from settings_manager import SettingsManager, EnergyManager

# Ініціалізація системи розумного дому
app = FastAPI()
home = SmartHomeFacade()
settings = SettingsManager()

# Модель для запитів
class LightingRequest(BaseModel):
    action: str  # "on" або "off"
    brightness: int = None  

class ClimateRequest(BaseModel):
    temperature: int

# Роут для управління освітленням
@app.post("/lighting")
def control_lighting(request: LightingRequest):
    home.control_lighting(request.action, request.brightness)
    return {"status": "Lighting controlled", "action": request.action, "brightness": request.brightness}

# Роут для управління кліматом
@app.post("/climate")
def set_climate(request: ClimateRequest):
    settings.set_setting("preferred_temperature", request.temperature)
    home.set_climate_control(settings.get_setting("preferred_temperature"))
    return {"status": "Climate controlled", "temperature": request.temperature}

# Роут для активації системи безпеки
@app.post("/security/activate")
def activate_security():
    home.activate_security_system()
    return {"status": "Security system activated"}

# Роут для моніторингу енергії
@app.get("/energy/monitor")
def monitor_energy():
    EnergyManager().monitor_usage()
    return {"status": "Energy usage monitored"}

# Роут для оптимізації енергії
@app.post("/energy/optimize")
def optimize_energy():
    EnergyManager().optimize_energy()
    return {"status": "Energy usage optimized"}