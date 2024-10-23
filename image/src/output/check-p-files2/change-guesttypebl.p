DEFINE TEMP-TABLE t-guest LIKE guest.

DEFINE INPUT PARAMETER gastno   AS INTEGER. 
DEFINE INPUT PARAMETER new-type AS INTEGER. 
DEFINE INPUT PARAMETER user-init AS CHAR. 
DEFINE OUTPUT PARAMETER mess-str AS CHAR. 

DEFINE VARIABLE success-flag AS LOGICAL INIT NO NO-UNDO.

RUN read-guestbl.p (1, gastno, "", "", OUTPUT TABLE t-guest).

IF new-type NE t-guest.karteityp THEN
DO:
    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    CREATE res-history. 
    ASSIGN 
    res-history.nr = bediener.nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME
    res-history.action = "CHG CardType"
    res-history.aenderung = "CHG CardType GuestNo " 
      + STRING(t-guest.gastnr) + " - " + t-guest.NAME 
      + " " + STRING(t-guest.karteityp) + "->" + STRING(new-type).

    RUN write-guestbl.p (1, INPUT TABLE t-guest, OUTPUT success-flag).
    mess-str = "Cardtype change successfull!".
END.
ELSE DO:
    mess-str = "Guest type can not be same type!".
    RETURN.
END.
