
DEFINE TEMP-TABLE depo-list  
    FIELD resnr         LIKE reservation.resnr COLUMN-LABEL "ResNr" FORMAT ">>>>>>9"  
    FIELD reserve-name  LIKE reservation.NAME   
    FIELD grpname       LIKE reservation.groupname  
    FIELD guestname     LIKE res-line.NAME  
    FIELD ankunft       LIKE res-line.ankunft
    FIELD deposit-type  LIKE reservation.deposit-type  
    FIELD depositgef    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"  
    FIELD bal           AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL "Balance"  
    FIELD depo1         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL ""  
    FIELD datum1        LIKE reservation.zahldatum  
    FIELD depo2         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL ""   
    FIELD datum2        LIKE reservation.zahldatum2
    FIELD deposit-type2 LIKE reservation.deposit-type
    FIELD deposit-paid  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    .
DEFINE input parameter fdate AS DATE NO-UNDO.
DEFINE INPUT PARAMETER sortype AS INTEGER.
define output parameter table for depo-list.
DEFINE output parameter total-saldo   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".  /*bernatd*/


DEF TEMP-TABLE out-list
    FIELD deposit AS DECI FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD deposit2 AS DECI FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD datum AS DATE
    FIELD datum2 AS DATE
    FIELD resno AS INTEGER .

DEFINE VARIABLE depo-foreign LIKE artikel.pricetab.
DEFINE VARIABLE depo-curr LIKE artikel.betriebsnr.
DEFINE VARIABLE depo-artnr as INTEGER.
DEFINE VARIABLE str-resnr as CHARACTER.
DEFINE VARIABLE resnr as INTEGER.
DEFINE VARIABLE bill-date AS DATE.
DEFINE VARIABLE exchg-rate AS DECIMAL NO-UNDO.
DEFINE VARIABLE found-it AS LOGICAL INITIAL YES NO-UNDO.
DEFINE VARIABLE resno AS INTEGER.
DEF VAR tot-depo1 AS DECI NO-UNDO FORMAT "->>>,>>>,>>>,>>9.99".
DEF VAR tot-depo2 AS DECI NO-UNDO FORMAT "->>>,>>>,>>>,>>9.99".
DEF VAR tot AS DECI FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE curr-name AS CHARACTER.
DEFINE VARIABLE curr-date AS DATE.
DEFINE VARIABLE subtotal AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99".
DEFINE VARIABLE str-resnr2 AS CHARACTER.
DEFINE VARIABLE str-resnr3 AS CHARACTER.

FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK NO-ERROR.
FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
    AND artikel.departement = 0 NO-LOCK.
depo-artnr = htparam.finteger.
depo-foreign = artikel.pricetab.
depo-curr  = artikel.betriebsnr.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.
bill-date = htparam.fdate.

DEFINE VARIABLE grpstr      AS CHAR FORMAT "x(1)" EXTENT 2 
  INITIAL [" ", "G"] LABEL "   ". 

FOR EACH depo-list:
    DELETE depo-list.
END.

/*
IF depo-foreign THEN
  RUN create-depo.
ELSE RUN create-depo1. */


FUNCTION extractDigits RETURNS CHARACTER ( INPUT pcString AS CHARACTER ):  
  DEFINE VARIABLE iChar AS INTEGER NO-UNDO.
  DEFINE VARIABLE iAsc AS INTEGER NO-UNDO.

  DEFINE VARIABLE cTemp AS CHARACTER NO-UNDO.
  DEFINE VARIABLE cChar AS CHARACTER NO-UNDO.

  DO iChar = 1 TO LENGTH(pcString):
      ASSIGN cChar = SUBSTRING(pcString,iChar,1)
                      iAsc = ASC(cChar).

      IF iAsc GT 47 AND
           iAsc LT 58 THEN
         cTemp = cTemp + cChar.
  END.

  IF (cTemp GT "") EQ TRUE THEN
      RETURN cTemp.
  ELSE
      RETURN ?. /* If no integers in the string return the unknown value. */
END FUNCTION.

  IF sortype = 1 THEN
  DO:
    RUN create-depo1.
  END.

  IF sortype = 2 THEN
  DO:
    RUN create-depo2.
  END.

  IF sortype = 3 THEN
  DO:
    RUN create-depo3.
  END.


procedure create-depo1: 
  FOR EACH billjournal WHERE billjournal.artnr EQ depo-artnr and billjournal.bill-datum LE fdate
    AND YEAR(billjournal.bill-datum) EQ YEAR(fdate) /*bernatd B9DB6E 2025 */
    AND (billjournal.bezeich matches "*Reservation*" or billjournal.bezeich matches "*#*") NO-LOCK
    BY billjournal.bill-datum:
      
      IF billjournal.bezeich MATCHES "*Reservation*" THEN
      DO:
        str-resnr = ENTRY(1, billjournal.bezeich, "]"). /*bernatd*/
        str-resnr2 = ENTRY(1, str-resnr, "[" ).
        resno = INT(extractDigits(str-resnr2)).  

      END.
      ELSE 
      DO:
        str-resnr = ENTRY(1, billjournal.bezeich, "]"). /*bernatd*/
        str-resnr2 = ENTRY(2, str-resnr, "[" ).
        str-resnr3 = ENTRY(1, str-resnr2, " " ).
        resno = INT(extractDigits(str-resnr3)).

      END.

    FIND FIRST out-list WHERE out-list.resno = resno NO-ERROR.
    IF NOT AVAILABLE out-list THEN DO:
        CREATE out-list.
        ASSIGN out-list.resno = resno.
    END.

    IF out-list.deposit = 0 THEN 
      ASSIGN 
          out-list.deposit = billjournal.betrag
          out-list.datum  = billjournal.bill-datum.
    ELSE 
      ASSIGN 
          out-list.deposit2 = out-list.deposit2 + billjournal.betrag
          out-list.datum2  = billjournal.bill-datum.
  END.
  tot = 0.
  tot-depo2 = 0.
  tot-depo1 = 0.

  FOR EACH out-list NO-LOCK,
    FIRST res-line where res-line.resnr EQ out-list.resno,
    FIRST reservation where reservation.resnr EQ out-list.resno by out-list.resno:
        IF out-list.deposit2 GE 0 THEN
        DO:
            create depo-list.
            assign
              depo-list.resnr         = reservation.resnr
              depo-list.reserve-name  = reservation.name
              depo-list.grpname       = reservation.groupname
              depo-list.guestname     = res-line.NAME
              depo-list.ankunft       = res-line.ankunft
              depo-list.deposit-type  = reservation.deposit-type
              depo-list.depositgef    = reservation.depositgef
              depo-list.depo1         = out-list.deposit
              depo-list.datum1        = out-list.datum
              depo-list.depo2         = out-list.deposit2
              depo-list.datum2        = out-list.datum2
              depo-list.deposit-type2 = reservation.deposit-type
              depo-list.deposit-paid  = out-list.deposit + out-list.deposit2
            .
            tot-depo2 = tot-depo2 + out-list.deposit2.
            tot-depo1 = tot-depo1 + out-list.deposit.
        END.
  END. 
  tot = tot-depo2 + tot-depo1.
  total-saldo = tot.
          
end procedure.


procedure create-depo2:
  FOR EACH billjournal WHERE billjournal.artnr EQ depo-artnr and billjournal.bill-datum LE fdate
    AND YEAR(billjournal.bill-datum) EQ YEAR(fdate) /*bernatd B9DB6E 2025 */
    AND (billjournal.bezeich matches "*Reservation*" or billjournal.bezeich matches "*#*") NO-LOCK
    BY billjournal.bill-datum:
      IF billjournal.bezeich MATCHES "*Reservation*" THEN
      DO:
        
        str-resnr = ENTRY(1, billjournal.bezeich, "]"). /*bernatd*/
        str-resnr2 = ENTRY(1, str-resnr, "[" ).
        resno = INT(extractDigits(str-resnr2)).  

      END.
      ELSE 
      DO:
        str-resnr = ENTRY(1, billjournal.bezeich, "]"). /*bernatd*/
        str-resnr2 = ENTRY(2, str-resnr, "[" ).
        str-resnr3 = ENTRY(1, str-resnr2, " " ).
        resno = INT(extractDigits(str-resnr3)).

      END.

    FIND FIRST out-list WHERE out-list.resno = resno NO-ERROR.
    IF NOT AVAILABLE out-list THEN DO:
        CREATE out-list.
        ASSIGN out-list.resno = resno.
    END.

    IF out-list.deposit = 0 THEN 
      ASSIGN 
          out-list.deposit = billjournal.betrag
          out-list.datum  = billjournal.bill-datum.
    ELSE 
      ASSIGN 
          out-list.deposit2 = out-list.deposit2 + billjournal.betrag
          out-list.datum2  = billjournal.bill-datum.
  END.
  tot = 0.
  tot-depo2 = 0.
  tot-depo1 = 0.
  curr-name = "".

  FOR EACH out-list NO-LOCK,
    FIRST res-line where res-line.resnr EQ out-list.resno,
    FIRST reservation where reservation.resnr EQ out-list.resno by reservation.NAME:
      
        
        IF out-list.deposit2 GE 0 THEN
        DO:
            IF curr-name NE "" AND curr-name NE reservation.name THEN
            DO:
              create depo-list.
              assign
              depo-list.resnr         = ?
              depo-list.reserve-name  = ""
              depo-list.grpname       = "TOTAL"
              depo-list.guestname     = ""
              depo-list.ankunft       = ?
              depo-list.deposit-type  = ?
              depo-list.depositgef    = subtotal
              depo-list.depo1         = ?
              depo-list.datum1        = ?
              depo-list.depo2         = ?
              depo-list.datum2        = ?
              depo-list.deposit-type2 = ?
              depo-list.deposit-paid  = ?
              . 

              subtotal = 0.
            END.

            create depo-list.
            assign
              depo-list.resnr         = reservation.resnr
              depo-list.reserve-name  = reservation.name
              depo-list.grpname       = reservation.groupname
              depo-list.guestname     = res-line.NAME
              depo-list.ankunft       = res-line.ankunft
              depo-list.deposit-type  = reservation.deposit-type
              depo-list.depositgef    = reservation.depositgef
              depo-list.depo1         = out-list.deposit
              depo-list.datum1        = out-list.datum
              depo-list.depo2         = out-list.deposit2
              depo-list.datum2        = out-list.datum2
              depo-list.deposit-type2 = reservation.deposit-type
              depo-list.deposit-paid  = out-list.deposit + out-list.deposit2
            .
            tot-depo2 = tot-depo2 + out-list.deposit2.
            tot-depo1 = tot-depo1 + out-list.deposit.
            curr-name = reservation.NAME.
            subtotal = subtotal + depo-list.depositgef.
        END.
  END. 
  tot = tot-depo2 + tot-depo1.
  total-saldo = tot.

end procedure.

procedure create-depo3:
  FOR EACH billjournal WHERE billjournal.artnr EQ depo-artnr and billjournal.bill-datum LE fdate
    AND YEAR(billjournal.bill-datum) EQ YEAR(fdate) /*bernatd B9DB6E 2025 */
    AND (billjournal.bezeich matches "*Reservation*" or billjournal.bezeich matches "*#*") NO-LOCK
    BY billjournal.bill-datum:
      
      IF billjournal.bezeich MATCHES "*Reservation*" THEN
      DO:
        
        str-resnr = ENTRY(1, billjournal.bezeich, "]"). /*bernatd*/
        str-resnr2 = ENTRY(1, str-resnr, "[" ).
        resno = INT(extractDigits(str-resnr2)).  

      END.
      ELSE 
      DO:
        str-resnr = ENTRY(1, billjournal.bezeich, "]"). /*bernatd*/
        str-resnr2 = ENTRY(2, str-resnr, "[" ).
        str-resnr3 = ENTRY(1, str-resnr2, " " ).
        resno = INT(extractDigits(str-resnr3)).

      END.

    FIND FIRST out-list WHERE out-list.resno = resno NO-ERROR.
    IF NOT AVAILABLE out-list THEN DO:
        CREATE out-list.
        ASSIGN out-list.resno = resno.
    END.

    IF out-list.deposit = 0 THEN 
      ASSIGN 
          out-list.deposit = billjournal.betrag
          out-list.datum  = billjournal.bill-datum.
    ELSE 
      ASSIGN 
          out-list.deposit2 = out-list.deposit2 + billjournal.betrag
          out-list.datum2  = billjournal.bill-datum.
  END.
  tot = 0.
  tot-depo2 = 0.
  tot-depo1 = 0.

  FOR EACH out-list NO-LOCK,
    FIRST res-line where res-line.resnr EQ out-list.resno,
    FIRST reservation where reservation.resnr EQ out-list.resno by res-line.ankunft:
      
      
        IF out-list.deposit2 GE 0 THEN
        DO:
            
            IF curr-date NE ? AND curr-date NE res-line.ankunft THEN
              DO:
                create depo-list.
                assign
                depo-list.resnr         = ?
                depo-list.reserve-name  = ""
                depo-list.grpname       = "TOTAL"
                depo-list.guestname     = ""
                depo-list.ankunft       = ?
                depo-list.deposit-type  = ?
                depo-list.depositgef    = subtotal
                depo-list.depo1         = ?
                depo-list.datum1        = ?
                depo-list.depo2         = ?
                depo-list.datum2        = ?
                depo-list.deposit-type2 = ?
                depo-list.deposit-paid  = ?
                . 

                subtotal = 0.
              END.

            create depo-list.
            assign
              depo-list.resnr         = reservation.resnr
              depo-list.reserve-name  = reservation.name
              depo-list.grpname       = reservation.groupname
              depo-list.guestname     = res-line.NAME
              depo-list.ankunft       = res-line.ankunft
              depo-list.deposit-type  = reservation.deposit-type
              depo-list.depositgef    = reservation.depositgef
              depo-list.depo1         = out-list.deposit
              depo-list.datum1        = out-list.datum
              depo-list.depo2         = out-list.deposit2
              depo-list.datum2        = out-list.datum2
              depo-list.deposit-type2 = reservation.deposit-type
              depo-list.deposit-paid  = out-list.deposit + out-list.deposit2
            .
            tot-depo2 = tot-depo2 + out-list.deposit2.
            tot-depo1 = tot-depo1 + out-list.deposit.
            curr-date = res-line.ankunft.
            subtotal  = subtotal + depo-list.depositgef. 

        END.
  END. 
  tot = tot-depo2 + tot-depo1.
  total-saldo = tot.
  
end procedure.


