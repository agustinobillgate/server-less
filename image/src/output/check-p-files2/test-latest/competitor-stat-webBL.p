DEFINE TEMP-TABLE b1-list
    FIELD datum         LIKE zinrstat.datum
    FIELD betriebsnr    LIKE zinrstat.betriebsnr
    FIELD bezeich       LIKE akt-code.bezeich
    FIELD zimmeranz     LIKE zinrstat.zimmeranz
    FIELD personen      LIKE zinrstat.personen
    /*FIELD logisumsatz   LIKE zinrstat.logisumsatz*/
    FIELD logisumsatz   AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"
    FIELD argtumsatz    AS INTEGER
    .

DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR  b1-list.

FOR EACH zinrstat WHERE zinrstat.zinr = "Competitor"
    AND zinrstat.datum GE from-date AND zinrstat.datum LE to-date
    NO-LOCK /*M , FIRST queasy WHERE queasy.number1 = zinrstat.betriebsnr
AND queasy.KEY = 136 NO-LOCK . */,
    FIRST akt-code WHERE akt-code.aktionscode = zinrstat.betriebsnr
    AND akt-code.aktiongrup = 4 NO-LOCK:
    CREATE b1-list.
    ASSIGN
      b1-list.datum         = zinrstat.datum
      b1-list.betriebsnr    = zinrstat.betriebsnr
      b1-list.bezeich       = akt-code.bezeich
      b1-list.zimmeranz     = zinrstat.zimmeranz
      b1-list.personen      = zinrstat.personen
      b1-list.logisumsatz   = zinrstat.logisumsatz
      b1-list.argtumsatz    = INT(zinrstat.argtumsatz)
      .
END.
