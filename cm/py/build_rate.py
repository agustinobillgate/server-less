# build_rate.py

def build_rate_json(rate_rows, hotel_code="VHP-HOTEL"):
    """
    rate_rows harus berupa list dict:
    {
       "startperiode": date,
       "endperiode": date,
       "rcode": str,
       "rmtype": str,
       "currency": str,
       "guestAmts": [
          {"amount": dec, "pax": int, "ageCode": int}
       ]
    }
    """
    return {
        "OTA_HotelRateAmountNotifRQ": {
            "RateAmountMessages": [
                {
                    "Start": str(r["startperiode"]),
                    "End": str(r["endperiode"]),
                    "RatePlanCode": r["rcode"],
                    "InvTypeCode": r["rmtype"],
                    "Currency": r["currency"],
                    "BaseByGuestAmts": [
                        {
                            "AmountAfterTax": g["amount"],
                            "NumberOfGuests": g["pax"],
                            "AgeQualifyingCode": g["ageCode"],
                        }
                        for g in r["guestAmts"]
                    ],
                }
                for r in rate_rows
            ]
        }
    }
