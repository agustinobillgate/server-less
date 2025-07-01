
DEFINE TEMP-TABLE t-salesbud LIKE salesbud
    FIELD rec-id AS INT.

DEF INPUT PARAMETER mm AS INT.
DEF INPUT PARAMETER yy AS INT.
DEF INPUT PARAMETER room AS INT.
DEF INPUT PARAMETER lodging AS DECIMAL.
DEF INPUT PARAMETER fb AS DECIMAL.
DEF INPUT PARAMETER sonst AS DECIMAL.
DEF INPUT PARAMETER bediener-nr AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-salesbud.

FIND FIRST salesbud WHERE salesbud.monat = mm AND salesbud.jahr = yy 
    AND salesbud.bediener-nr = bediener-nr NO-ERROR. 
IF NOT AVAILABLE salesbud THEN 
DO: 
    create salesbud. 
    salesbud.monat = mm. 
    salesbud.jahr = yy. 
    salesbud.bediener-nr = bediener-nr. 
END. 
salesbud.room-nights = room. 
salesbud.argtumsatz = lodging. 
salesbud.f-b-umsatz = fb. 
salesbud.sonst-umsatz = sonst. 
salesbud.gesamtumsatz = lodging + fb + sonst. 
salesbud.id = user-init.

FOR EACH salesbud:
    CREATE t-salesbud.
    BUFFER-COPY salesbud TO t-salesbud.
    ASSIGN t-salesbud.rec-id = RECID(salesbud).
END.
