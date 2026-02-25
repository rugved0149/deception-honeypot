from core.risk_engine import risk_engine
from utils.paths import DB_PATH

HONEYPOT_RISK_WEIGHT = 70

def analyze_honeypot_hit(ip):
    risk_engine.add_score(ip, HONEYPOT_RISK_WEIGHT)
    return risk_engine.get_score(ip)
