#!/usr/bin/env python3
import subprocess, time, re, sys

BSSID = "84:FC:E6:00:FC:05"
end = time.time() + 30

hex_re = re.compile(r'\b[0-9A-Fa-f]{2}(?:\s+[0-9A-Fa-f]{2})+\b')

def scan_block():
    p = subprocess.run(["iw","dev","wlp3s0","scan"], capture_output=True, text=True)
    if p.returncode != 0: return None
    txt = p.stdout
    m = re.search(rf"^BSS\s+{re.escape(BSSID)}\b.*?(?=^BSS\s|\Z)", txt, flags=re.S|re.M)
    return m.group(0) if m else None

def extract_vendor_ie(block):
    out = []
    for line in block.splitlines():
        line=line.strip()
        if line.startswith("IE:") or line.startswith("RSN:") or line.startswith("SSID:"):
            # iw often prints vendor IE as "IE: Unknown: dd xx xx ..."
            m = re.search(r"Unknown:\s*(.*)$", line)
            if m:
                hexs = m.group(1).strip()
                if re.fullmatch(hex_re, hexs):
                    out.append(hexs.replace(" ","").lower())
    return out

def decode_opendroneid(hexstr):
    # Minimal heuristic: vendor IE starts with dd (element id) then len, then OUI+type.
    # iw already strips leading dd & len sometimes; we'll try both.
    s = hexstr
    if s.startswith("dd"):
        s = s[2:]  # drop 'dd'
    # skip len if present
    if len(s) >= 2:
        s = s[2:]
    # OUI(3)+type(1)
    if len(s) < 8: return None
    oui = s[:6]
    typ = s[6:8]
    payload = s[8:]
    return {"oui":oui,"type":typ,"payload_len":len(payload)//2}

while time.time() < end:
    blk = scan_block()
    ts = time.strftime("%H:%M:%S")
    if not blk:
        print(f"{ts} | not seen")
        sys.stdout.flush()
        time.sleep(1)
        continue
    last = re.search(r"^\s*last seen:\s*(.*)$", blk, flags=re.M)
    ssid = re.search(r"^\s*SSID:\s*(.*)$", blk, flags=re.M)
    vendors = extract_vendor_ie(blk)
    print(f"{ts} | last seen: {last.group(1) if last else 'unknown'} | SSID: {ssid.group(1) if ssid else 'unknown'}")
    printed = False
    for v in vendors:
        dec = decode_opendroneid(v)
        if dec:
            print(f"  vendor IE: OUI={dec['oui']} type={dec['type']} payload_bytes={dec['payload_len']}")
            printed = True
    if not printed and vendors:
        for v in vendors:
            print(f"  vendor IE raw: {v[:32]}... ({len(v)//2} bytes)")
    sys.stdout.flush()
    time.sleep(1)







