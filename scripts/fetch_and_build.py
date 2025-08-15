#!/usr/bin/env python3
import csv, json, os, time, urllib.request, sys

# Preferir SHEET_ID desde variable de entorno; si no, usar el hardcode de backup
SHEET_ID = os.getenv("SHEET_ID", "1Sia7krk2Mts6w-H1zvG88jWIQhpm5zUHf_COXI2Ab9s")
SHEETS = {
  "general": "1462115415",
  "sub-9": "1106797410",
  "sub-11": "1925253457",
  "sub-14": "1979916640",
  "sub-17": "255628422",
  "primera": "1643111789",
  "damas": "11359234",
  "sabado": "1525215119",
  "domingo": "761656977",
  "femenino": "0",
  "home": "970777381"
}

OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

def fetch_csv(sheet_id: str, gid: str) -> list[dict]:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        # Soporte de compresión lo maneja urllib automáticamente si el server la ofrece
        content = resp.read().decode("utf-8", errors="replace")
    rows = list(csv.DictReader(content.splitlines()))
    return rows

def _to_number(val: str):
    # Intenta castear a int/float de forma segura
    if val is None:
        return None
    s = str(val).strip()
    if s == "":
        return ""
    if s.isdigit():
        try:
            return int(s)
        except Exception:
            return s
    try:
        # Soporta "12.34" y "12,34"
        s_dot = s.replace(",", ".")
        if s_dot.count(".") <= 1 and all(ch.isdigit() or ch == "." for ch in s_dot):
            return float(s_dot)
    except Exception:
        pass
    return s

def normalize_rows(rows: list[dict]) -> list[dict]:
    norm = []
    for r in rows:
        clean = {}
        for k, v in r.items():
            key = (k or "").strip()
            val = (v if v is not None else "").strip()
            clean[key] = _to_number(val)
        norm.append(clean)
    return norm

def write_json(path: str, payload: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

def main():
    if not SHEET_ID or SHEET_ID.strip() == "":
        print("ERROR: SHEET_ID vacío. Configura la variable de entorno SHEET_ID o edita el script.", file=sys.stderr)
        sys.exit(1)

    generated_at = int(time.time())
    bundle = {"_meta": {"generated_at": generated_at, "sheet_id": SHEET_ID}, "data": {}}

    for name, gid in SHEETS.items():
        print(f"Descargando hoja {name} (gid={gid})...")
        rows = fetch_csv(SHEET_ID, gid)
        norm = normalize_rows(rows)
        bundle["data"][name] = norm
        write_json(os.path.join(OUT_DIR, f"{name}.json"), {"_meta": {"generated_at": generated_at}, "data": norm})

    write_json(os.path.join(OUT_DIR, "data.json"), bundle)
    print("OK: archivos en ./data")

if __name__ == "__main__":
    main()
