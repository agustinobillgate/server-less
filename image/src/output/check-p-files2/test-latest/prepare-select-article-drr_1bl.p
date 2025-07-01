DEFINE TEMP-TABLE str-list 
    FIELD nr       AS INTEGER
    FIELD bezeich  AS CHAR
    FIELD used     AS LOGICAL
    FIELD grup     AS LOGICAL
    FIELD grp-name AS CHAR.

DEFINE TEMP-TABLE stat-list
    FIELD artnr    AS INTEGER
    FIELD used     AS LOGICAL
    FIELD grup     AS LOGICAL
    FIELD grp-name AS CHAR
    FIELD flag     AS CHAR.

DEFINE TEMP-TABLE out-list LIKE stat-list
    FIELD deptnr   AS INTEGER.


DEFINE VARIABLE c-862 AS INTEGER NO-UNDO.
DEFINE VARIABLE c-892 AS INTEGER NO-UNDO.
DEFINE VARIABLE str2  AS CHAR.
DEFINE VARIABLE str3  AS CHAR.

DEFINE VARIABLE st1   AS CHAR.
DEFINE VARIABLE st2   AS CHAR.
DEFINE VARIABLE st3   AS CHAR.
DEFINE VARIABLE st4   AS CHAR.
DEFINE VARIABLE st5   AS CHAR.
DEFINE VARIABLE st6   AS CHAR.
DEFINE VARIABLE st7   AS CHAR.
DEFINE VARIABLE st8   AS CHAR.
DEFINE VARIABLE st9   AS CHAR.
DEFINE VARIABLE st10  AS CHAR.
DEFINE VARIABLE st11  AS CHAR.
DEFINE VARIABLE st12  AS CHAR.

DEFINE VARIABLE n     AS INT.
DEFINE VARIABLE n1    AS INT.
DEFINE VARIABLE n2    AS INT.
DEFINE VARIABLE n3    AS INT.
DEFINE VARIABLE n4    AS INT.
DEFINE VARIABLE n5    AS INT.
DEFINE VARIABLE n6    AS INT.
DEFINE VARIABLE n7    AS INT.
DEFINE VARIABLE n8    AS INT.
DEFINE VARIABLE n9    AS INT.
DEFINE VARIABLE n10   AS INT.

DEFINE VARIABLE dept  AS INT.

DEFINE INPUT  PARAMETER case-type AS INT.
DEFINE INPUT  PARAMETER departement AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.

/*
DEF VAR case-type AS INT INITIAL 2.
DEF VAR departement AS INT INITIAL 0.*/

FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
c-862 = htparam.finteger.
FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
c-892 = htparam.finteger.

FIND FIRST queasy WHERE queasy.KEY EQ 265 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
   ASSIGN
       str2  = queasy.char2
       str3  = queasy.char3.
END.

DO n = 1 TO NUM-ENTRIES(str2,";"):
st1 = ENTRY(n,str2,";").
    IF SUBSTR(st1,1,11)  = "$FOrevenue$" AND SUBSTR(st1,12,3) EQ "YES" THEN DO:
      st2 = SUBSTR(st1,16).

      DO n1 = 1 TO NUM-ENTRIES(st2,","):
        st3 = ENTRY(n1,st2,",").
        CREATE stat-list.
        ASSIGN 
            stat-list.artnr     = INTEGER(ENTRY(1,st3,"-"))
            stat-list.used      = YES
            stat-list.grup      = LOGICAL(ENTRY(2,st3,"-"))
            stat-list.grp-name  = ENTRY(3,st3,"-")
            stat-list.flag      = "FoRev".
      END.
    END.
    IF SUBSTR(st1,1,13)  = "$otherincome$" AND SUBSTR(st1,14,3) EQ "YES" THEN DO:
      st4 = SUBSTR(st1,18).
      DO n2 = 1 TO NUM-ENTRIES(st4,","):
         st5 = ENTRY(n2,st4,",").
         CREATE stat-list.
         ASSIGN 
            stat-list.artnr     = INTEGER(ENTRY(1,st5,"-"))
            stat-list.used      = YES
            stat-list.grup      = LOGICAL(ENTRY(2,st5,"-"))
            stat-list.grp-name  = ENTRY(3,st5,"-")
            stat-list.flag      = "OtherRev".
      END. 
    END.

    IF SUBSTR(st1,1,9)  = "$segment$" AND SUBSTR(st1,10,3) EQ "YES" THEN DO:
      st6 = SUBSTR(st1,14).
      DO n3 = 1 TO NUM-ENTRIES(st6,","):
         st7 = ENTRY(n3,st6,",").
         CREATE stat-list.
         ASSIGN 
            stat-list.artnr     = INTEGER(ENTRY(1,st7,"-"))
            stat-list.used      = YES
            stat-list.grup      = LOGICAL(ENTRY(2,st7,"-"))
            stat-list.grp-name  = ENTRY(3,st7,"-")
            stat-list.flag      = "Segment".
      END. 
    END.
END.

DO n4 =1 TO NUM-ENTRIES (str3,"*"):
   st8 =  ENTRY(n4,str3,"*").

   IF SUBSTR(st8,1,16) = "$revenueOutlets$" AND SUBSTR(st8,17,3) EQ "YES" THEN DO:
    st9 = SUBSTR(st8,20).
    DO n5 = 1 TO NUM-ENTRIES (st9,";"):
        st10 = ENTRY(n5,st9,";").
        DO n6 = 1 TO NUM-ENTRIES (st10,"|"):
           st11 = ENTRY(n6,st10,"|").

           IF n6 EQ 1 AND st11 NE "" AND ENTRY(2,st10,"|") NE "" THEN ASSIGN dept = INTEGER(st11).
           ELSE IF st11 NE "" AND n6 GT 1 THEN DO:
               DO n7 = 1 TO NUM-ENTRIES (st11,","):
                   st12 = ENTRY(n7,st11,",").
                   IF st12 NE "" THEN DO:
                       CREATE out-list.
                       ASSIGN
                           out-list.deptnr      = dept
                           out-list.artnr       = INTEGER(ENTRY(1,st12,"-"))
                           out-list.used        = YES
                           out-list.grup        = LOGICAL(ENTRY(2,st12,"-"))
                           out-list.grp-name    = ENTRY(3,st12,"-").
                   END.
               END.
           END.
        END.
    END.
   END.
END.


IF case-type EQ 1 THEN DO:
    FOR EACH artikel WHERE (artikel.artart EQ 0 OR artikel.artart EQ 8) AND umsatzart EQ 1 AND artikel.departement EQ departement NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST stat-list WHERE stat-list.artnr EQ str-list.nr AND stat-list.flag EQ "FoRev" NO-LOCK NO-ERROR.
        IF AVAILABLE stat-list THEN
            ASSIGN str-list.used        = stat-list.used
                   str-list.grup        = stat-list.grup
                   str-list.grp-name    = stat-list.grp-name.
    END.
END.

ELSE IF case-type EQ 2 THEN DO:
    FOR EACH artikel WHERE (artikel.artart EQ 0 OR artikel.artart EQ 8) AND umsatzart EQ 4 AND zwkum NE 26 AND artikel.departement EQ departement NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST stat-list WHERE stat-list.artnr EQ str-list.nr AND stat-list.flag EQ "OtherRev"  NO-LOCK NO-ERROR.
        IF AVAILABLE stat-list THEN
            ASSIGN str-list.used        = stat-list.used
                   str-list.grup        = stat-list.grup
                   str-list.grp-name    = stat-list.grp-name.
    END.
END.

ELSE IF case-type EQ 3 THEN DO:
    FOR EACH segment NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = segment.segmentcode
               str-list.bezeich = segment.bezeich.

        FIND FIRST stat-list WHERE stat-list.artnr EQ str-list.nr AND stat-list.flag EQ "Segment"  NO-LOCK NO-ERROR.
        IF AVAILABLE stat-list THEN
            ASSIGN str-list.used        = stat-list.used
                   str-list.grup        = stat-list.grup
                   str-list.grp-name    = stat-list.grp-name.
    END.
END.

ELSE IF case-type EQ 4 THEN DO:
   FOR EACH artikel WHERE artikel.departement EQ departement AND artikel.endkum NE 101 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST out-list WHERE out-list.artnr EQ str-list.nr AND out-list.deptnr EQ departement NO-LOCK NO-ERROR.
        IF AVAILABLE out-list THEN
            ASSIGN str-list.used        = out-list.used
                   str-list.grup        = out-list.grup
                   str-list.grp-name    = out-list.grp-name.
    END.
END.
