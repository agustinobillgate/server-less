
DEFINE TEMP-TABLE b-list 
  FIELD k       AS INTEGER 
  FIELD monat   AS CHARACTER 
  FIELD wert    AS DECIMAL. 

DEF INPUT PARAMETER fibukonto AS CHARACTER.
DEF OUTPUT PARAMETER TABLE FOR b-list.

RUN create-b-list.

PROCEDURE create-b-list: 
   DEFINE VARIABLE i AS INTEGER. 
   DEFINE VARIABLE mon AS CHAR FORMAT "x(3)" EXTENT 12 INITIAL 
       ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", 
        "AUG", "SEP", "OCT", "NOV", "DEC"]. 
   FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto NO-LOCK. 
   DO i = 1 TO 12: 
      create b-list. 
      b-list.k = i. 
      b-list.monat = mon[i]. 
      b-list.wert = gl-acct.actual[i]. 
   END. 
END. 
