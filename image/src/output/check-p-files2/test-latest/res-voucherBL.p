DEF TEMP-TABLE r-list LIKE res-line
     FIELD rsvName  AS CHAR FORMAT "x(24)" LABEL "Company / TA"
     FIELD voucher  AS CHAR FORMAT "x(16)" LABEL "Voucher No"
     FIELD currency AS CHAR FORMAT "x(4)"  LABEL "Curr"
.

DEF INPUT PARAMETER fr-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR r-list.

RUN disp-it.

PROCEDURE disp-it: 
DEF VAR i   AS INTEGER NO-UNDO.
DEF VAR str AS CHAR    NO-UNDO.
  FOR EACH r-list:
      DELETE r-list.
  END.
  FOR EACH res-line WHERE res-line.ankunft GE fr-date
    AND res-line.ankunft LE to-date
    AND res-line.resstatus NE 12 
    AND res-line.resstatus NE 99    /*FD July 14, 2021*/
    AND res-line.zimmer-wunsch MATCHES ("*Voucher*") NO-LOCK:
      CREATE r-list.
      BUFFER-COPY res-line TO r-list.
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
      ASSIGN r-list.rsvName = guest.NAME + "," + guest.anredefirma.
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr
          NO-LOCK NO-ERROR.
      IF AVAILABLE waehrung THEN r-list.currency = waehrung.wabkurz.
      DO i = 1 TO NUM-ENTRIES(r-list.zimmer-wunsch,";") - 1:
        str = ENTRY(i, r-list.zimmer-wunsch, ";").
        IF SUBSTR(str,1,7) = "voucher" THEN 
        ASSIGN
          r-list.voucher = SUBSTR(str,8)
          i = 9999
        .
      END.
  END.
END. 
