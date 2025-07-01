DEF TEMP-TABLE tt-s1
    FIELD curr-i AS INTEGER
    FIELD s1     AS CHAR
.

DEF TEMP-TABLE tt-s2
    FIELD curr-i AS INTEGER
    FIELD s2     AS CHAR
.

DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER curr-month AS INT.
DEF INPUT PARAMETER curr-year AS INT.
DEF INPUT PARAMETER all-flag AS LOGICAL.

DEF OUTPUT PARAMETER TABLE FOR tt-s1.
DEF OUTPUT PARAMETER TABLE FOR tt-s2.

DEF VAR s1 AS CHAR EXTENT 42.
DEF VAR s2 AS CHAR EXTENT 42.

DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER FORMAT "99".
DEFINE VARIABLE start-ind   as integer.
DEFINE VARIABLE anz-day     as integer.
DEFINE VARIABLE first-day   as date.
DEFINE VARIABLE last-day    as date.
DEFINE VARIABLE month1      as integer.
DEFINE VARIABLE year1       as integer.
DEFINE VARIABLE lname       AS CHAR.

i = 1.
do while i LE 42:
    s1[i] = "  ".
    s2[i] = "  ".
    i = i + 1.
end.
first-day = date(curr-month, 1, curr-year).
start-ind = weekday(first-day) - 1.
if start-ind = 0 then start-ind = 7.
month1 = curr-month + 1.
year1 = curr-year.
if month1 = 13 then
do:
    month1 = 1.
    year1 = year1 + 1.
end.
last-day = date(month1, 1, year1) - 1.
i = start-ind.
j = 1.
do while j LE day(last-day):
      IF all-flag = NO THEN
      DO:
       FOR EACH akt-line WHERE akt-line.flag = 0 AND akt-line.userinit = user-init AND DAY(akt-line.datum) = j AND  MONTH(akt-line.datum) = curr-month AND YEAR(akt-line.datum) = curr-year ,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK:

          FIND FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK NO-ERROR.
          IF AVAILABLE guest THEN
            lname = guest.NAME + ", " + guest.anredefirma.

         s2[i] = STRING(akt-code.bezeich) + CHR(10)
               + "<" + STRING(akt-line.kontakt) + "/" 
               + STRING(lname) + ">"  + CHR(10) + CHR(10) + s2[i].
       END.
       
      END.
      ELSE 
      DO:
          FOR EACH akt-line WHERE akt-line.flag = 0  AND DAY(akt-line.datum) = j AND  MONTH(akt-line.datum) = curr-month AND YEAR(akt-line.datum) = curr-year ,
             FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK:

             FIND FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK NO-ERROR.
             IF AVAILABLE guest THEN
               lname = guest.NAME + ", " + guest.anredefirma.

            s2[i] = STRING(akt-code.bezeich) + CHR(10)
                  + "<" + STRING(akt-line.kontakt) + "/" 
                  + STRING(lname) + ">"  + CHR(10) + CHR(10) + s2[i] .  
          END.
      END.
    s1[i] = STRING(j,"99").
    if subSTRING(s1[i],1,1) = "0" then s1[i] = " " + subSTRING(s1[i], 2, 1).
    i = i + 1.
    j = j + 1.
end.

DO  i = 1 TO 42:
    CREATE tt-s1.
    ASSIGN
        tt-s1.curr-i = i
        tt-s1.s1     = s1[i]
    .
END.

DO  i = 1 TO 42:
    CREATE tt-s2.
    ASSIGN
        tt-s2.curr-i = i
        tt-s2.s2     = s2[i]
    .
END.
