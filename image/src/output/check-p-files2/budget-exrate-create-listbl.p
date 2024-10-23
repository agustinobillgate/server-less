DEFINE TEMP-TABLE g-list 
  FIELD monat AS INTEGER FORMAT "99" LABEL "Month" 
  FIELD wert  AS DECIMAL FORMAT ">>>,>>9.99" COLUMN-LABEL "Exchange Rate"
  FIELD datum AS DATE
. 

DEF INPUT  PARAMETER curr-year AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR g-list.

RUN create-list.

PROCEDURE create-list: 
DEFINE VARIABLE i          AS INTEGER   NO-UNDO. 
DEFINE VARIABLE curr-date  AS DATE      NO-UNDO.
   FOR EACH g-list:
       DELETE g-list.
   END.
   DO i = 1 TO 12: 
     ASSIGN
         curr-date = DATE(i, 1, curr-year) + 35
         curr-date = DATE(MONTH(curr-date), 1, curr-year) - 1
     .
     CREATE g-list. 
     ASSIGN g-list.monat = i
            g-list.wert  = 1
            g-list.datum = curr-date
     .
     FIND FIRST exrate WHERE exrate.artnr = 99998
         AND exrate.datum = curr-date NO-LOCK NO-ERROR.
     IF AVAILABLE exrate THEN g-list.wert = exrate.betrag.
   END.
END. 
