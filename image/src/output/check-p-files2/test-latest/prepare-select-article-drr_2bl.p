DEFINE TEMP-TABLE str-list 
    FIELD nr       AS INTEGER
    FIELD bezeich  AS CHAR
    FIELD used     AS LOGICAL
    FIELD descr    AS CHAR.

DEFINE TEMP-TABLE stat-list
    FIELD artnr    AS INTEGER
    FIELD used     AS LOGICAL
    FIELD descr    AS CHAR
    FIELD zwkum    AS INTEGER
    FIELD flag     AS CHAR.

DEFINE VARIABLE str2  AS CHAR.
DEFINE VARIABLE str3  AS CHAR.

DEFINE VARIABLE st1   AS CHAR.
DEFINE VARIABLE st2   AS CHAR.
DEFINE VARIABLE st3   AS CHAR.
DEFINE VARIABLE st4   AS CHAR.

DEFINE VARIABLE n     AS INT.
DEFINE VARIABLE n1    AS INT.
DEFINE VARIABLE n2    AS INT.
DEFINE VARIABLE n3    AS INT.
DEFINE VARIABLE n4    AS INT.


DEFINE INPUT  PARAMETER case-type AS INT.
DEFINE INPUT  PARAMETER nr AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.

/*
DEF VAR case-type AS INT INITIAL 1.
DEF VAR nr AS INT INITIAL 10. */

DEF VAR zwkum AS INTEGER.

FIND FIRST queasy WHERE queasy.KEY EQ 265 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
   ASSIGN
       str2  = queasy.char2
       str3  = queasy.char3.
END.

DO n1 = 1 TO NUM-ENTRIES(str2,";"):
   st1 = ENTRY(n1,str2,";").

   IF SUBSTR(st1,1,11)  = "$statistic$" AND SUBSTR(st1,12,3) EQ "YES" THEN DO:
    ASSIGN st2 = SUBSTR(st1,16).

    DO n2 = 1 TO NUM-ENTRIES(st2,"/"):
        st3 = ENTRY(n2,st2,"/").
        
        IF n2 EQ 1 AND st3 NE "" THEN ASSIGN zwkum = INTEGER(st3).
        ELSE IF st3 NE "" AND n2 GT 1 THEN DO:
            DO n3 = 1 TO NUM-ENTRIES(st3,","):
                st4 = ENTRY(n3,st3,",").
                CREATE stat-list.
                ASSIGN stat-list.zwkum = zwkum
                       stat-list.used  = YES 
                       stat-list.artnr = INT(ENTRY(1,st4,"-"))
                       stat-list.descr = ENTRY(2,st4,"-") 
                       stat-list.flag  = "Statistic".
            END.
        END.
    END.
   END.
END.

IF case-type EQ 1 THEN DO:
    FOR EACH artikel WHERE artikel.artnr GE 4000 AND artikel.zwkum EQ nr AND artikel.departement EQ 0 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST stat-list WHERE stat-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE stat-list THEN DO: 
             ASSIGN str-list.used = YES
                    str-list.descr = stat-list.descr.
        END.
            
    END.
END.

