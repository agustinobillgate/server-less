DEF TEMP-TABLE hbill
    FIELD kellner-nr LIKE h-bill.kellner-nr.

DEF INPUT  PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR hbill.

FOR EACH h-bill WHERE h-bill.departement = curr-dept
    AND h-bill.flag = 0 NO-LOCK:
    CREATE hbill.
    ASSIGN
      hbill.kellner-nr = h-bill.kellner-nr.
END.
