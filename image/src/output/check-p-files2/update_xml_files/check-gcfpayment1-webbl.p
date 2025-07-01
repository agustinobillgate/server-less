

DEFINE INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER gastnr         AS INTEGER. 
DEFINE INPUT  PARAMETER rechnr         AS INTEGER.
DEFINE INPUT  PARAMETER resnr          AS INTEGER.
DEFINE INPUT  PARAMETER reslinnr       AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER payment  AS INTEGER. 
DEFINE OUTPUT PARAMETER msg-str        AS CHAR.
DEFINE OUTPUT PARAMETER msg-str2       AS CHAR.
DEFINE OUTPUT PARAMETER htparam-fchar  AS CHAR.
DEFINE OUTPUT PARAMETER htparam-fchar1 AS CHAR.
DEFINE OUTPUT PARAMETER guest-kreditlimit AS DECIMAL.
DEFINE OUTPUT PARAMETER enter-passwd1 AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER enter-passwd2 AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER voucher-number AS CHAR.

/*MT
DEF VAR pvILanguage AS INTEGER NO-UNDO INIT 1.
DEF VAR gastnr AS INTEGER INIT 2722.
DEF VAR payment AS INTEGER INIT 20.
DEF VAR msg-str AS CHAR.
DEF VAR msg-str2 AS CHAR.
DEF VAR htparam-fchar AS CHAR.
DEF VAR htparam-fchar1 AS CHAR.
DEF VAR guest-kreditlimit AS INT.
DEF VAR enter-passwd1 AS LOGICAL INIT NO.
DEF VAR enter-passwd2 AS LOGICAL INIT NO.*/

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "check-gcfpayment".

DEFINE VARIABLE zahlungsart AS INTEGER INITIAL 0. 
DEFINE VARIABLE outstand    AS DECIMAL. 
DEFINE VARIABLE i           AS INTEGER NO-UNDO.
DEFINE VARIABLE str         AS CHAR    NO-UNDO.

FIND FIRST artikel WHERE artikel.artnr = payment AND 
  artikel.departement = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE artikel AND artikel.artart = 2 THEN 
DO:
  
  /* unallocated A/R deposit */  
  FIND FIRST htparam WHERE htparam.paramnr = 116 NO-LOCK.
  IF artikel.zwkum = htparam.finteger THEN RETURN.

  FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE guest THEN zahlungsart = guest.zahlungsart. 
  IF zahlungsart = 0 THEN 
  DO: 
    FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
    IF htparam.fchar NE "" THEN 
    DO: 
      enter-passwd1 = YES.
      htparam-fchar = htparam.fchar.
      /*MTRUN enter-passwd.p("CL", gastnr, "", htparam.fchar, 
          0, 0, OUTPUT passwd-ok). 
      IF NOT passwd-ok THEN 
      DO: 
        payment = 0. 
        RETURN. 
      END. */
    END. 
    ELSE 
    DO: 
      msg-str = msg-str + CHR(2) + "&W"
              + translateExtended ("No C/L Payment Articles have been defined for this Guest.",lvCAREA,"").
    END. 
  END.
  ELSE IF guest.zahlungsart NE payment THEN 
  DO: 
    FIND FIRST artikel WHERE artikel.departement = 0 
      AND artikel.artnr = guest.zahlungsart NO-LOCK NO-ERROR. 
    IF AVAILABLE artikel THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("C/L Payment Article for this guest is",lvCAREA,"")
              + CHR(10)
              + STRING(artikel.artnr) + " - " + artikel.bezeich.
      payment = 0. 
      RETURN. 
    END. 
  END. 

  /*FDL Oct 24, 2024: Ticket 30C467*/
  IF guest.karteityp EQ 2 THEN
  DO:
      FIND FIRST res-line WHERE res-line.resnr EQ resnr
        AND res-line.reslinnr EQ reslinnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,7) = "voucher" THEN 
              DO:
                  ASSIGN
                      voucher-number = SUBSTR(str,8)
                      i = 9999
                  .
              END.            
          END.
      END.
  END.
   
  IF guest.karteityp GE 1 AND guest.kreditlimit GT 0 
      /*AND NOT passwd-ok*/ THEN 
  DO: 
      /*ITA 270418 --> add calculate outstanding from bill*/
      FOR EACH bill-line WHERE bill-line.rechnr = rechnr NO-LOCK:
          ASSIGN outstand = outstand + bill-line.betrag.
      END.

      FOR EACH debitor WHERE debitor.gastnr = guest.gastnr 
          AND debitor.opart LE 1 NO-LOCK, 
          FIRST artikel WHERE artikel.artnr = debitor.artnr 
          AND artikel.departement = 0 AND artikel.artart = 2 NO-LOCK: 
          outstand = outstand + debitor.saldo. 
      END. 

      IF outstand GT guest.kreditlimit THEN 
      DO: 
          
          FIND FIRST htparam WHERE paramnr = 320 NO-LOCK. 
          IF htparam.flogical THEN 
          DO: 
              msg-str2 = msg-str2 + CHR(2)
                     + translateExtended ("Over Credit Limit:",lvCAREA,"")
                     + " " + TRIM(STRING(outstand,"->,>>>,>>>,>>>,>>9")) /*" >> " */
                     + TRIM(STRING(guest.kreditlimit,"->>>,>>>,>>>,>>9")).
              FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
              IF htparam.fchar NE "" THEN 
              DO:
                enter-passwd2 = YES.
                htparam-fchar1 = htparam.fchar.
                guest-kreditlimit = guest.kreditlimit.
                /*MTRUN enter-passwd.p("AR", gastnr, "",
                    htparam.fchar, 
                    outstand, guest.kreditlimit, OUTPUT passwd-ok). 
                IF NOT passwd-ok THEN DO: 
                    payment = 0. 
                    RETURN. 
                END. */
              END. 
          END. 
          ELSE 
          DO: 
            msg-str2 = msg-str2 + CHR(2) + "&Q"
                    + translateExtended ("Credit Limit overdrawn:",lvCAREA,"")
                    + " " + TRIM(STRING(outstand,"->,>>>,>>>,>>>,>>9")) /*" >> " */
                    + TRIM(STRING(guest.kreditlimit,"->>>,>>>,>>>,>>9"))
                    + CHR(10)
                    + translateExtended ("Cancel the C/L Payment?", lvCAREA,"").
            /*MTIF answer THEN DO: 
                payment = 0. 
                RETURN. 
            END. */
          END. 
      END. 
  END. 
END.
