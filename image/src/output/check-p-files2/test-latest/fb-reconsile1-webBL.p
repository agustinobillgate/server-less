DEFINE TEMP-TABLE output-list 
  FIELD curr-counter AS INTEGER 
  FIELD nr           AS INTEGER INITIAL 0 
  FIELD store        AS INTEGER INITIAL 0 
  FIELD amount       AS DECIMAL INITIAL 0 
  FIELD bezeich      AS CHAR 
  FIELD s            AS CHAR.

DEFINE TEMP-TABLE fb-list
  FIELD curr-counter AS INTEGER
  FIELD str1         AS CHARACTER
  FIELD str2         AS CHARACTER
  FIELD str3         AS CHARACTER
  FIELD str4         AS CHARACTER
  FIELD str5         AS CHAR.

DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER from-grp    AS INT.
DEF INPUT PARAMETER food        AS INT.
DEF INPUT PARAMETER bev         AS INT.

DEF INPUT PARAMETER from-date   AS DATE.
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER date1       AS DATE. 
DEF INPUT PARAMETER date2       AS DATE. 


DEF INPUT PARAMETER mi-opt-chk AS LOGICAL.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER exchg-rate AS DECIMAL .
DEF INPUT PARAMETER foreign-nr AS INT.

DEF OUTPUT PARAMETER done      AS LOGICAL INITIAL NO. 
DEF OUTPUT PARAMETER TABLE FOR fb-list.


RUN fb-reconsile1bl.p
        (pvILanguage, from-grp, food, bev, from-date, to-date, date1,
                   date2, mi-opt-chk, double-currency,
                   exchg-rate, foreign-nr,
                   OUTPUT done, OUTPUT TABLE output-list).

FOR EACH output-list BY output-list.curr-counter:
    CREATE fb-list.
    ASSIGN 
        fb-list.curr-counter = output-list.curr-counter
        fb-list.str1 = SUBSTR(output-list.s,1,24)
        fb-list.str2 = SUBSTR(output-list.s,25,33)
        fb-list.str3 = SUBSTR(output-list.s,58,15)
        fb-list.str4 = SUBSTR(output-list.s,73,15)
        fb-list.str5 = SUBSTR(output-list.s,88,23)
    .                                
END.
