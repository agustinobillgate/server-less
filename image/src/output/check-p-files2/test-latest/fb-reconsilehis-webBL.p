DEFINE TEMP-TABLE output-list 
  FIELD nr AS INTEGER 
  FIELD code AS INTEGER 
  FIELD bezeich AS CHAR 
  FIELD s AS CHAR.
DEFINE TEMP-TABLE s-list
    FIELD col1 AS CHARACTER FORMAT "x(24)"
    FIELD col2 AS CHARACTER FORMAT "x(50)"
    FIELD col3 AS CHARACTER FORMAT "x(15)"
    FIELD col4 AS CHARACTER FORMAT "x(15)"
    FIELD col5 AS CHARACTER FORMAT "x(34)"
.

DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER from-grp AS INT.
DEF INPUT PARAMETER food AS INT.
DEF INPUT PARAMETER bev AS INT.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER ldry AS INTEGER. 
DEF INPUT PARAMETER dstore AS INTEGER. 
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER foreign-nr AS INT.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER mi-opt-chk AS LOGICAL.
DEF INPUT PARAMETER date1 AS DATE.
DEF INPUT PARAMETER date2 AS DATE.
DEF OUTPUT PARAMETER done AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER TABLE FOR s-list.


RUN fb-reconsilehis-cldbl.p
    (pvILanguage, from-grp, food, bev, from-date, to-date, ldry,
     dstore, double-currency, foreign-nr, exchg-rate,mi-opt-chk, date1, date2,
     OUTPUT done, OUTPUT TABLE output-list).

FOR EACH output-list:
    CREATE s-list.
    /* Naufal Afthar - BDFB55 -> adjust substring length*/
    ASSIGN
        s-list.col1 = SUBSTRING(output-list.s,1,24)
        s-list.col2 = SUBSTRING(output-list.s,25,50)
        s-list.col3 = SUBSTRING(output-list.s,75,18)
        s-list.col4 = SUBSTRING(output-list.s,93,18)
        s-list.col5 = SUBSTRING(output-list.s,110,36).
END.

