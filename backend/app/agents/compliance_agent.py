from typing import Dict, Any, List, Tuple
from app.models.schemas import ComplianceStatus

# Thai FDA (อย.) and Consumer Protection Board (สคบ.) Banned / High-Risk Advertising Terms
BANNED_THAI_CLAIMS = [
    {
        "pattern": "รักษาหายขาด",
        "replacement": "ช่วยดูแลและฟื้นบำรุงให้ดีขึ้น",
        "severity": "CRITICAL",
        "law": "พ.ร.บ. เครื่องสำอาง / พ.ร.บ. ยา"
    },
    {
        "pattern": "ขาวทันที",
        "replacement": "ช่วยให้ผิวแลดูกระจ่างใสขึ้นอย่างเป็นธรรมชาติ",
        "severity": "HIGH",
        "law": "ประกาศ อย. เรื่องการโฆษณาเครื่องสำอาง"
    },
    {
        "pattern": "ลดน้ำหนัก 10 กิโลใน 7 วัน",
        "replacement": "ช่วยคุมหิว อิ่มนาน สุขภาพดี",
        "severity": "CRITICAL",
        "law": "พ.ร.บ. อาหาร พ.ศ. 2522"
    },
    {
        "pattern": "เห็นผล 100%",
        "replacement": "เห็นผลลัพธ์พึงพอใจอย่างชัดเจน",
        "severity": "MEDIUM",
        "law": "พ.ร.บ. คุ้มครองผู้บริโภค (สคบ.)"
    },
    {
        "pattern": "อันดับ 1 ของโลก",
        "replacement": "ไอเทมยอดฮิตติดเทรนด์",
        "severity": "MEDIUM",
        "law": "พ.ร.บ. คุ้มครองผู้บริโภค เรื่องการอวดอ้างเกินจริง"
    }
]

def check_and_sanitize_thai_script(script_text: str) -> Tuple[ComplianceStatus, str, List[Dict[str, Any]]]:
    flags = []
    sanitized_script = script_text
    highest_severity = ComplianceStatus.PASS

    for rule in BANNED_THAI_CLAIMS:
        if rule["pattern"] in sanitized_script:
            flags.append({
                "detected_term": rule["pattern"],
                "suggested_replacement": rule["replacement"],
                "severity": rule["severity"],
                "law_reference": rule["law"]
            })
            # Auto-replace to create compliant version
            sanitized_script = sanitized_script.replace(rule["pattern"], rule["replacement"])
            if rule["severity"] == "CRITICAL":
                highest_severity = ComplianceStatus.WARNING  # Auto-mitigated to warning
            elif highest_severity == ComplianceStatus.PASS:
                highest_severity = ComplianceStatus.WARNING

    # Ensure affiliate disclosure hashtag
    if "#affiliate" not in sanitized_script and "#นายหน้า" not in sanitized_script:
        sanitized_script += "\n#นายหน้าtiktokshop #affiliate"

    return highest_severity, sanitized_script, flags
