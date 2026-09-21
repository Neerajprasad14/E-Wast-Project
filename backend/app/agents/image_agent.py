"""Replaceable image understanding boundary."""
from pathlib import Path
from app.schemas.analysis import Classification


class ImageClassificationAgent:
    """Safe local fallback; a vision-model provider can implement the same interface later."""
    async def analyze(self, image_bytes: bytes, filename: str) -> Classification:
        name = Path(filename).stem.lower()
        hints = {"laptop": ("Laptop", "Computers"), "phone": ("Mobile Phone", "Mobile Phones"), "mobile": ("Mobile Phone", "Mobile Phones"), "battery": ("Battery", "Batteries"), "monitor": ("Monitor", "Monitors"), "tv": ("Television", "Televisions"), "printer": ("Printer", "Printers")}
        for hint, result in hints.items():
            if hint in name:
                return Classification(object=result[0], category=result[1], confidence=0.62)
        return Classification(object="Electronic device", category="Other E-Waste", confidence=0.25)
