# build_avail.py

def build_availability_json(avail_rows, hotel_code="VHP-HOTEL"):
    """
    avail_rows harus sudah berupa list dict:
    {
       "startperiode": date,
       "endperiode": date,
       "rmtype": str,
       "rcode": str or None,
       "qty": int,
       "status": "Open"/"Close",
       "restrictions": list optional
    }
    """
    return {
        "OTA_HotelAvailNotifRQ": {
            "AvailStatusMessages": {
                "HotelCode": hotel_code,
                "Messages": [
                    {
                        "Start": str(r["startperiode"]),
                        "End": str(r["endperiode"]),
                        "InvTypeCode": r["rmtype"],
                        "RatePlanCode": r["rcode"],
                        "AvailStatus": {"Status": r["status"]},
                        "Restrictions": r.get("restrictions", [])
                    }
                    for r in avail_rows
                ]
            }
        }
    }
