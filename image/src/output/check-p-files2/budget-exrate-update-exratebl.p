DEFINE TEMP-TABLE g-list 
  FIELD monat AS INTEGER FORMAT "99" LABEL "Month" 
  FIELD wert  AS DECIMAL FORMAT ">>>,>>9.99" COLUMN-LABEL "Exchange Rate"
  FIELD datum AS DATE
. 

DEF INPUT PARAMETER TABLE FOR g-list.

RUN update-exrate.

PROCEDURE update-exrate: 
DEFINE VARIABLE i          AS INTEGER   NO-UNDO. 
DEFINE VARIABLE curr-date  AS DATE      NO-UNDO.
   FOR EACH g-list:
     FIND FIRST exrate WHERE exrate.artnr = 99998
         AND exrate.datum = g-list.datum EXCLUSIVE-LOCK NO-ERROR.
     IF NOT AVAILABLE exrate THEN 
     DO:
         CREATE exrate.
         ASSIGN
             exrate.artnr  = 99998
             exrate.datum  = g-list.datum
             exrate.betrag = 1
         .
     END.
     IF g-list.wert NE 0 THEN ASSIGN exrate.betrag = g-list.wert.
   END. 
   
END. 
