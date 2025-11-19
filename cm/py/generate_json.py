# generate_json.py
#--------------------------------------------------------------------
# Rd, 18/11/2025
# Extract Push Allot + Push Rate in one JSON
#
# PUSH ALLOT:
# - Queasy KEY 171 logi3 = TRUE
# - qty = total_room - occ - ooo
# - LOS from KEY 2
# - statnr from KEY 174 / 175
# - rmtype + bezeich from queasy 152 / zimkateg
#
# PUSH RATE:
# - Queasy KEY 170 logi3 = TRUE
# - rmtype + bezeich from queasy 152 / zimkateg
#--------------------------------------------------------------------

import json
import sys
from db import connect_to_schema
from sqlalchemy import text
import datetime
import uuid

#=======================================================
# # Check perubahan data avail/rate
# ROOM OCCUPANCY berubah
# number2 (occ) berbeda dari sebelumnya
# OOO (Out of Order) berubah
# number3 (ooo) berbeda dari sebelumnya
# Total rooms (rmcat) berubah
# jumlah kamar per zikatnr berubah
# Restriction CTA/CTD/CLOSE berubah (queasy 174)
# Override restriction berubah (queasy 175)
# Ratecode mapping berubah (char1 rcode)
# Ada rcode baru untuk room type ini
# Ada record baru (tidak ada sebelumnya)
# perlu ditandai untuk push
# Ada merging dari allocation-of-derived rcode
#=======================================================

def log_change(text):
    """
    Append log text to push_changes.log with timestamp.
    """
    with open("push_changes.log", "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts}] {text}\n")


# Get Queasy 160, hotelcode etc =========================
def get_hotel_info_q160(cur):
    cur.execute("""
        SELECT char1 
        FROM queasy
        WHERE key = 160
        LIMIT 1
    """)

    hotel_info = {}
    row = cur.fetchone()
    str_char1 = row["char1"] if row else ""
    tmp_data = str_char1.split(";")
    if len(tmp_data) >= 1:
        for part in tmp_data:
            if part.startswith("$autostart$"):
                hotel_info["autostart"] = (part.replace("$autostart$", ""))
            if part.startswith("$period$"):
                hotel_info["period"] = int(part.replace("$period$", ""))
            if part.startswith("$delay$"):
                hotel_info["delay"] = int(part.replace("$delay$", ""))
            if part.startswith("$defcurr$"):
                hotel_info["defcurr"] = part.replace("$defcurr$", "") 
            if part.startswith("$defchild$"):
                hotel_info["defchild"] = int(part.replace("$defchild$", ""))
            if part.startswith("$workpath$"):
                hotel_info["workpath"] = part.replace("$workpath$", "")
            if part.startswith("$progname$"):
                hotel_info["progname"] = part.replace("$progname$", "")
            if part.startswith("$htlcode$"):
                hotel_info["hotelcode"] = part.replace("$htlcode$", "")
            if part.startswith("$username$"):
                hotel_info["username"] = part.replace("$username$", "")
            if part.startswith("$password$"):
                hotel_info["password"] = part.replace("$password$", "")
            if part.startswith("$pushrate$"):
                hotel_info["pushrateflag"] =(part.replace("$pushrate$", ""))
            if part.startswith("$pullbook$"):
                hotel_info["pullbookflag"] = (part.replace("$pullbook$", ""))
            if part.startswith("$pushavail$"):
                hotel_info["pushavailflag"] = (part.replace("$pushavail$", ""  ))
    return hotel_info
# =======================================================


# Generate t_list dari bookeng_id ======================
def get_t_push_list(cur, booking_id):
    sql = """
        SELECT * FROM queasy where key=161 AND number1 = %s
    """
    cur.execute(sql, (booking_id,))
    rows = cur.fetchall()
    t_push_list_data = []
    for row in rows:
        char1 = row.get("char1") or ""
        parts = char1.split(";")

        t_list = {
            "rcodevhp":  parts[0] if len(parts) > 0 else "",
            "rcodebe":   parts[1] if len(parts) > 1 else "",
            "rmtypevhp": parts[2] if len(parts) > 2 else "",
            "rmtypebe":  parts[3] if len(parts) > 3 else "",
            "argtvhp":   parts[4] if len(parts) > 4 else "",
        }

        t_push_list_data.append(t_list)
    return t_push_list_data

# END OF get_hotel_info_q160

#=======================================================     
def check_changes_171(prev, curr, rest174_prev, rest174_curr, rest175_prev, rest175_curr):
    """
    prev  → dict: availability sebelumnya (dari DB)
    curr  → dict: availability terbaru hasil kalkulasi
    rest174_prev  → dict old restriction (CTA, CTD, CLOSE)
    rest174_curr  → dict new restriction
    rest175_prev  → dict old override restriction
    rest175_curr  → dict new override
    """

    # 1. NEW RECORD (tidak ada sebelumnya)
    if prev is None:
        return True

    # 2. Availability changed
    if prev["occ"] != curr["occ"]:
        return True

    if prev["ooo"] != curr["ooo"]:
        return True

    if prev["qty"] != curr["qty"]:
        return True

    # 3. Ratecode for room-type changed
    if prev["rcode"] != curr["rcode"]:
        return True

    # 4. LOS changed
    if prev["minlos"] != curr["minlos"]:
        return True

    if prev["maxlos"] != curr["maxlos"]:
        return True

    # 5. Restriction 174 changed
    if (rest174_prev or rest174_curr) and rest174_prev != rest174_curr:
        return True

    # 6. Restriction 175 changed (override)
    if (rest175_prev or rest175_curr) and rest175_prev != rest175_curr:
        return True

    # 7. statnr changed (Open/Close/CTA/CTD)
    if prev["statnr"] != curr["statnr"]:
        return True

    # 8. bezeich / rmtype changed
    if prev["bezeich"] != curr["bezeich"]:
        return True

    return False

def check_changes_170(prev, curr):
    """
    Yang membandingkan:
    rmrate berubah
    pax berubah
    child berubah
    currency berubah
    dynamic rate (char2) berubah
    arrangement berubah
    markup/discount berubah
    rcode berubah
    bezeich berubah

    Membandingkan record RATE (KEY 170) lama (prev) dan baru (curr).
    Jika ada perbedaan → return True (perlu logi3 = TRUE)
    """

    # NEW record (tidak ada prev)
    if prev is None:
        return True

    # Perbandingan field-field penting RATE 170
    fields = [
        "pax",
        "child",
        "rmrate",
        "currency",
        "rcode",
        "bezeich"
    ]

    for f in fields:
        if prev.get(f) != curr.get(f):
            return True

    # Tidak ada perubahan
    return False

# END OF check_changes
#=======================================================


#=======================================================
# Get Current Data
def build_curr_170(pax, child, rmrate, currency, rcode, bezeich):
    """
    Menghasilkan curr rate KEY 170.
    Digunakan untuk membandingkan dengan prev di check_changes_170().
    """
    return {
        "pax": pax,
        "child": child,
        "rmrate": rmrate,
        "currency": currency,
        "rcode": rcode,
        "bezeich": bezeich
    }

def build_curr_171(total_room, occ, ooo, rcode, minlos, maxlos, statnr, bezeich):
    """
    Menghasilkan curr availability KEY 171.
    Digunakan untuk membandingkan dengan prev di check_changes_171().
    """
    # Hitung qty = total_room - occ - ooo
    qty = total_room - occ - ooo
    qty = max(qty, 0)

    return {
        "occ": occ,
        "ooo": ooo,
        "qty": qty,
        "rcode": rcode,
        "minlos": minlos,
        "maxlos": maxlos,
        "statnr": statnr,
        "bezeich": bezeich
    }
# END OF build_curr functions
#=======================================================


#=======================================================
# Get Prev Data
def get_prev_171(cur, rcode, zikatnr, date1, los, rest, rmnames):
    """
    Mengambil prev KEY 171 yang sudah lengkap (occ, ooo, qty, rcode, minlos, maxlos, statnr, bezeich)
    """

    # 1. Ambil data dasar dari queasy
    sql = """
        SELECT 
            number2 AS occ,
            number3 AS ooo,
            deci1   AS qty,
            char1   AS rcode
        FROM queasy
        WHERE key = 171
          AND char1 = %s
          AND number1 = %s
          AND date1 = %s
        LIMIT 1
    """
    cur.execute(sql, (rcode, zikatnr, date1))
    row = cur.fetchone()

    if not row:
        return None

    # 2. LOS lama (dari KEY 2)
    los_info = los.get(rcode, {"minlos": 0, "maxlos": 0})
    minlos_prev = los_info["minlos"]
    maxlos_prev = los_info["maxlos"]

    # 3. Restriction lama (174/175)
    key = (rcode, zikatnr, date1)
    r174_prev = rest.get(key, {}).get(174)
    r175_prev = rest.get(key, {}).get(175)
    statnr_prev = calc_statnr(r174_prev, r175_prev)

    # 4. Nama room lama
    bezeich_prev = rmnames.get(zikatnr, "")

    # 5. Gabungkan jadi prev penuh
    prev = {
        "occ": row["occ"],
        "ooo": row["ooo"],
        "qty": row["qty"],
        "rcode": row["rcode"],
        "minlos": minlos_prev,
        "maxlos": maxlos_prev,
        "statnr": statnr_prev,
        "bezeich": bezeich_prev
    }

    return prev


def get_prev_170(cur, rcode, zikatnr, date1, pax, child, roomnames):
    """
    Mengambil prev KEY 170 dengan struktur lengkap:
    { pax, child, rmrate, currency, rcode, bezeich }
    """

    sql = """
        SELECT
            number2 AS pax,
            number3 AS child,
            deci1   AS rmrate,
            char1   AS rcode,
            char3   AS currency
        FROM queasy
        WHERE key = 170
          AND char1 = %s
          AND number1 = %s
          AND date1 = %s
          AND number2 = %s
          AND number3 = %s
        LIMIT 1
    """

    cur.execute(sql, (rcode, zikatnr, date1, pax, child))
    row = cur.fetchone()

    if not row:
        return None

    # --- Nama room lama (bezeich dari queasy 152 / zimkateg mapping) ---
    bezeich_prev = roomnames.get(zikatnr, "")

    # --- Gabungkan jadi prev lengkap ---
    prev = {
        "pax": row["pax"],
        "child": row["child"],
        "rmrate": row["rmrate"],
        "currency": row["currency"],
        "rcode": row["rcode"],
        "bezeich": bezeich_prev
    }

    return prev


# END OF get_prev functions
#=======================================================


#=======================================================
# DIff Functions
#=======================================================
def diff_171(prev, curr):
    """
    Membandingkan prev vs curr dan mengembalikan dict berisi field yang berubah.
    Jika prev = None → seluruh field dianggap baru.
    """
    changes = {}

    if prev is None:
        for k, v in curr.items():
            changes[k] = {"old": None, "new": v}
        return changes

    for key in curr:
        old = prev.get(key)
        new = curr.get(key)
        if old != new:
            changes[key] = {"old": old, "new": new}

    return changes

def diff_170(prev, curr):
    changes = {}

    if prev is None:
        for k, v in curr.items():
            changes[k] = {"old": None, "new": v}
        return changes

    for key in curr:
        old = prev.get(key)
        new = curr.get(key)
        if old != new:
            changes[key] = {"old": old, "new": new}

    return changes

# END OF diff functions
#=======================================================


# ======================================================
# SUPPORTING — AVAILABILITY
# ======================================================
def fetch_rmcat_list(cur):
    cur.execute("""
        SELECT 
            CASE WHEN zk.typ != 0 THEN zk.typ ELSE zk.zikatnr END AS zikatnr,
            COUNT(*) AS total_room
        FROM zimmer z
        JOIN zimkateg zk ON zk.zikatnr = z.zikatnr
        WHERE z.sleeping = TRUE
        GROUP BY 1
    """)
    return {r["zikatnr"]: r["total_room"] for r in cur.fetchall()}


def fetch_los(cur):
    cur.execute("""
        SELECT char1 AS rcode, number2 AS minlos, deci2 AS maxlos
        FROM queasy
        WHERE key = 2
    """)
    return {r["rcode"]: {"minlos": r["minlos"], "maxlos": r["maxlos"]} for r in cur.fetchall()}


def fetch_restrictions(cur):
    cur.execute("""
        SELECT key, char1 AS rcode, number1 AS zikatnr, date1, char2, number2
        FROM queasy
        WHERE key IN (174,175)
    """)
    rest = {}
    for r in cur.fetchall():
        k = (r["rcode"], r["zikatnr"], r["date1"])
        rest.setdefault(k, {})
        rest[k][r["key"]] = r
    return rest


def calc_statnr(r174, r175):
    if r175:
        if r175["char2"] == "Close":
            return 1 if r175["number2"] == 1 else 0
        if r175["char2"] == "CTA":
            return 2 if r175["number2"] == 1 else 5
        if r175["char2"] == "CTD":
            return 3 if r175["number2"] == 1 else 6

    if r174:
        x = list(map(int, r174["char2"].split(";")))
        if x[0] == 1:
            return 1
        if x[1] == 1 and x[2] == 0:
            return 2
        if x[2] == 1 and x[1] == 0:
            return 3
        if x[1] == 1 and x[2] == 1:
            return 4

    return 0


def fetch_room_names_avail(cur):
    # get rmtype
    cur.execute("""
        SELECT number1 AS zikatnr, char1 AS rmtype
        FROM queasy
        WHERE key = 152
    """)
    q152 = {r["zikatnr"]: r["rmtype"] for r in cur.fetchall()}

    # fallback from zimkateg
    cur.execute("""
        SELECT zikatnr, kurzbez AS rmtype
        FROM zimkateg
        WHERE active = TRUE
    """)
    zim = {r["zikatnr"]: r["rmtype"] for r in cur.fetchall()}

    res = zim.copy()
    res.update(q152)
    return res


# ======================================================
# SUPPORTING — RATE
# (room names, but different field alias)
# ======================================================
def fetch_room_names_rate(cur):
    cur.execute("""
        SELECT number1 AS zikatnr, char1 AS bezeich
        FROM queasy
        WHERE key = 152
    """)
    q152 = {r["zikatnr"]: r["bezeich"] for r in cur.fetchall()}

    cur.execute("""
        SELECT zikatnr, kurzbez AS bezeich
        FROM zimkateg
        WHERE active = TRUE
    """)
    zim = {r["zikatnr"]: r["bezeich"] for r in cur.fetchall()}

    res = zim.copy()
    res.update(q152)
    return res


# ======================================================
# PUSH RATE extraction
# ======================================================
def extract_push_rate_list(schema):
    conn, cur = connect_to_schema(schema)

    try:
        roomnames = fetch_room_names_rate(cur)

        sql = """
            SELECT 
                date1,
                number1 AS zikatnr,
                number2 AS pax,
                number3 AS child,
                deci1 AS rmrate,
                char1 AS rcode,
                char3 AS currency
            FROM queasy
            WHERE key = 170
              AND logi3 = TRUE
            ORDER BY date1, number1, rcode, pax
        """

        cur.execute(sql)
        q = cur.fetchall()

        out = []

        for r in q:
            z = r["zikatnr"]
            out.append({
                "startperiode": str(r["date1"]),
                "endperiode": str(r["date1"]),
                "zikatnr": z,
                "rcode": r["rcode"],
                "pax": r["pax"],
                "child": r["child"],
                "rmrate": float(r["rmrate"]),
                "currency": r["currency"] or "IDR",
                "bezeich": roomnames.get(z, "")
            })

        return out

    finally:
        cur.close()
        conn.close()


# ======================================================
# MAIN (PUSH ALLOT + RATE)
# ======================================================
# ======================================================
# MAIN (PUSH ALLOT + RATE) with FULL INTEGRATION
# ======================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_json.py <schema>")
        sys.exit(1)

    schema = sys.argv[1]
    becode = sys.argv[2]

    conn, cur = connect_to_schema(schema)

    try:
        print("Connected to schema:", schema)

        # Availability support data
        rmcat = fetch_rmcat_list(cur)
        los = fetch_los(cur)
        rest_prev = fetch_restrictions(cur)   # previous restrictions
        rest_curr = rest_prev                 # (in Python version, assume same source)
        rmnames = fetch_room_names_avail(cur)

        # Counter logs
        changes_171 = 0
        changes_170 = 0

        # ---------------------------
        # AVAILABILITY (KEY 171)
        # ---------------------------
        cur.execute("""
            SELECT date1, number1 AS zikatnr, number2 AS occ, number3 AS ooo, char1 AS rcode
            FROM queasy
            WHERE key = 171
            ORDER BY date1, zikatnr
        """)
        rows = cur.fetchall()

        push_allot = []
        counter = 0

        for r in rows:

            key_tuple = (r["rcode"], r["zikatnr"], r["date1"])
            r174_new = rest_curr.get(key_tuple, {}).get(174)
            r175_new = rest_curr.get(key_tuple, {}).get(175)

            # Build new statnr
            statnr = calc_statnr(r174_new, r175_new)

            # basic calculation
            total_room = rmcat.get(r["zikatnr"], 0)

            los_info = los.get(r["rcode"], {"minlos": 0, "maxlos": 0})
            minlos, maxlos = los_info["minlos"], los_info["maxlos"]

            # Build CURR
            curr = build_curr_171(
                total_room=total_room,
                occ=r["occ"],
                ooo=r["ooo"],
                rcode=r["rcode"],
                minlos=minlos,
                maxlos=maxlos,
                statnr=statnr,
                bezeich=rmnames.get(r["zikatnr"], "")
            )

            # PREV
            prev = get_prev_171(cur, r["rcode"], r["zikatnr"], r["date1"], los, rest_prev, rmnames)

            # restrictions comparison
            r174_prev = rest_prev.get(key_tuple, {}).get(174)
            r175_prev = rest_prev.get(key_tuple, {}).get(175)

            # check changes
            need_push = check_changes_171(prev, curr, r174_prev, r174_new, r175_prev, r175_new)
            changes = diff_171(prev, curr)

            if need_push:
                # UPDATE logi3=TRUE
                cur.execute("""
                    UPDATE queasy
                    SET logi3 = TRUE
                    WHERE key = 171
                    AND char1 = %s
                    AND number1 = %s
                    AND date1 = %s
                """, (r["rcode"], r["zikatnr"], r["date1"]))

                changes_171 += 1
                header = f"[171] date={r['date1']} zikatnr={r['zikatnr']} rcode={r['rcode']}"
                # print(header)
                log_change(header)
                for field, change in changes.items():
                    line = f"    - {field}: {change['old']} → {change['new']}"
                    # print(line)
                    log_change(line)

            counter += 1
            push_allot.append({
                "startperiode": str(r["date1"]),
                "endperiode": str(r["date1"]),
                "zikatnr": r["zikatnr"],
                "rcode": r["rcode"],
                "counter": counter,
                "qty": curr["qty"],
                "minlos": curr["minlos"],
                "maxlos": curr["maxlos"],
                "statnr": curr["statnr"],
                "bezeich": curr["bezeich"],
                "rmtype": curr["bezeich"],
                "str-date1": str(r["date1"]),
                "str-date2": str(r["date1"]),
                "need_push": need_push
            })


        # ---------------------------
        # RATE (KEY 170)
        # ---------------------------
        cur.execute("""
            SELECT 
                date1,
                number1 AS zikatnr,
                number2 AS pax,
                number3 AS child,
                deci1 AS rmrate,
                char1 AS rcode,
                char3 AS currency
            FROM queasy
            WHERE key = 170
            ORDER BY date1, number1, rcode, pax
        """)
        rows_170 = cur.fetchall()

        roomnames = fetch_room_names_rate(cur)
        push_rate = []

        for r in rows_170:
            curr_rate = build_curr_170(
                pax=r["pax"],
                child=r["child"],
                rmrate=r["rmrate"],
                currency=r["currency"] or "IDR",
                rcode=r["rcode"],
                bezeich=roomnames.get(r["zikatnr"], "")
            )

            prev_rate = get_prev_170(cur, r["rcode"], r["zikatnr"], r["date1"], r["pax"], r["child"], roomnames)
            need_push = check_changes_170(prev_rate, curr_rate)
            changes = diff_170(prev_rate, curr_rate)

            if need_push:
                cur.execute("""
                    UPDATE queasy
                    SET logi3 = TRUE
                    WHERE key = 170
                    AND char1 = %s
                    AND number1 = %s
                    AND date1 = %s
                    AND number2 = %s
                    AND number3 = %s
                """, (r["rcode"], r["zikatnr"], r["date1"], r["pax"], r["child"]))

                changes_170 += 1
                header = (f"[170] date={r['date1']} zikatnr={r['zikatnr']} "
                        f"rcode={r['rcode']} pax={r['pax']} child={r['child']}")
                # print(header)
                log_change(header)

                for field, change in changes.items():
                    line = f"    - {field}: {change['old']} → {change['new']}"
                    # print(line)
                    log_change(line)

            push_rate.append({
                "startperiode": str(r["date1"]),
                "endperiode": str(r["date1"]),
                "zikatnr": r["zikatnr"],
                "rcode": r["rcode"],
                "pax": curr_rate["pax"],
                "child": curr_rate["child"],
                "rmrate": curr_rate["rmrate"],
                "currency": curr_rate["currency"],
                "bezeich": curr_rate["bezeich"],
                "need_push": need_push
            })


        # ---------------------------
        # SUMMARY & WRITE JSON
        # ---------------------------
        # print("\nSUMMARY:")
        # print(" - Availability changed:", changes_171)
        # print(" - Rate changed:", changes_170)
        
        hotel_schema = schema
        hotel_info = get_hotel_info_q160(cur)
        booking_id = sys.argv[2]
        t_push_list = get_t_push_list(cur, booking_id)
        echo_token = uuid.uuid4().hex
        final_json = {
            "hotel_schema": hotel_schema,
            "bookeng_id": booking_id,
            "echotoken": echo_token,
            "timestamp": datetime.datetime.now().isoformat(),
            "hotel_info": hotel_info,
            # "t_push_list": t_push_list,
            "push_allot_list": push_allot,
            "push_rate_list": push_rate
        }

        with open("push_data.json", "w") as f:
            json.dump(final_json, f, indent=2)

        print("Generated push_data.json")

    finally:
        conn.commit()
        cur.close()
        conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
