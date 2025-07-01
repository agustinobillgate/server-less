DEFINE TEMP-TABLE str-list 
    FIELD nr       AS INTEGER
    FIELD bezeich  AS CHAR FORMAT "x(35)"
    FIELD used     AS LOGICAL.

DEFINE TEMP-TABLE pay-list
    FIELD artnr    AS INTEGER
    FIELD flag     AS LOGICAL.

DEFINE TEMP-TABLE outlet-list 
    FIELD artnr         AS INTEGER
    FIELD departement   AS INTEGER
    FIELD flag          AS CHAR
    FIELD flag-used     AS LOGICAL.

DEFINE TEMP-TABLE stat-list 
    FIELD artnr    AS INTEGER
    FIELD zwkum    AS INTEGER
    FIELD flag     AS LOGICAL.


DEFINE VARIABLE c-862 AS INTEGER NO-UNDO.
DEFINE VARIABLE c-892 AS INTEGER NO-UNDO.
DEFINE VARIABLE str1  AS CHAR.
DEFINE VARIABLE str2  AS CHAR.
DEFINE VARIABLE str3  AS CHAR.
DEFINE VARIABLE dept  AS INTEGER.
DEFINE VARIABLE dept1  AS INTEGER.
DEFINE VARIABLE food  AS CHAR.
DEFINE VARIABLE bev   AS CHAR.

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
DEFINE VARIABLE st13   AS CHAR.
DEFINE VARIABLE st14   AS CHAR.
DEFINE VARIABLE st15   AS CHAR.
DEFINE VARIABLE st16   AS CHAR.
DEFINE VARIABLE st17   AS CHAR.
DEFINE VARIABLE st18   AS CHAR.
DEFINE VARIABLE st19   AS CHAR.
DEFINE VARIABLE st20  AS CHAR.
DEFINE VARIABLE st21  AS CHAR.
DEFINE VARIABLE st22  AS CHAR.

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
DEFINE VARIABLE n11    AS INT.
DEFINE VARIABLE n12    AS INT.
DEFINE VARIABLE n13    AS INT.
DEFINE VARIABLE n14    AS INT.
DEFINE VARIABLE n15    AS INT.
DEFINE VARIABLE n16    AS INT.
DEFINE VARIABLE n17    AS INT.
DEFINE VARIABLE n18    AS INT.
DEFINE VARIABLE n19    AS INT.
DEFINE VARIABLE n20    AS INT.
DEFINE VARIABLE n21    AS INT.

DEFINE INPUT  PARAMETER case-type AS INT.
DEFINE INPUT  PARAMETER departement AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.
/*
DEFINE VARIABLE case-type AS INT INITIAL 14.
DEFINE VARIABLE departement AS INT INITIAL 14.*/

DEFINE VARIABLE zwkum AS INT.
zwkum = departement.
DEFINE VARIABLE zwkum1 AS INT.

FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
c-862 = htparam.finteger.
FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
c-892 = htparam.finteger.

FIND FIRST queasy WHERE queasy.KEY EQ 265 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
   ASSIGN 
       str1  = queasy.char1
       str2  = queasy.char2
       str3  = queasy.char3.
END.

FIND FIRST pay-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE pay-list THEN DO:
    DO n = 1 TO NUM-ENTRIES(str1,";"):
        st1 = ENTRY(n,str1,";").
    
        IF SUBSTR(st1,1,9)  = "$payment$" AND SUBSTR(st1,10,3) EQ "YES" THEN DO:
            st2 = SUBSTR(st1,14).
            DO n1 = 1 TO NUM-ENTRIES(st2,","):
                CREATE pay-list.
                pay-list.artnr = INTEGER(ENTRY(n1,st2,",")).
                pay-list.flag  = YES.
            END.
        END.
    
        ELSE IF SUBSTR(st1,1,8) EQ "$ledger$" AND SUBSTR(st1,9,3) EQ "YES"  THEN DO:
            st3 = SUBSTR(st1,13).
            DO n2 = 1 TO NUM-ENTRIES(st3,","):
                CREATE pay-list.
                pay-list.artnr = INTEGER(ENTRY(n2,st3,",")).
                pay-list.flag  = YES.
            END.
        END.
        
        ELSE IF SUBSTR(st1,1,6) EQ "$cash$" AND SUBSTR(st1,7,3) EQ "YES"  THEN DO:
            st4 = SUBSTR(st1,11).
            DO n3 = 1 TO NUM-ENTRIES(st4,","):
                CREATE pay-list.
                pay-list.artnr = INTEGER(ENTRY(n3,st4,",")).
                pay-list.flag  = YES.
            END.  
        END.
        
        ELSE IF SUBSTR(st1,1,9) EQ "$foreign$" AND SUBSTR(st1,10,3) EQ "YES"  THEN DO:
            st5 = SUBSTR(st1,14).
            DO n4 = 1 TO NUM-ENTRIES(st5,","):
                CREATE pay-list.
                pay-list.artnr = INTEGER(ENTRY(n4,st5,",")).
                pay-list.flag  = YES.
            END.        
        END.
            
        ELSE IF SUBSTR(st1,1,9) EQ "$deposit$" AND SUBSTR(st1,10,3) EQ "YES"  THEN DO:
            st6 = SUBSTR(st1,14).
            DO n5 = 1 TO NUM-ENTRIES(st6,","):
                CREATE pay-list.
                pay-list.artnr = INTEGER(ENTRY(n5,st6,",")).
                pay-list.flag  = YES.
            END.
        END.
        
        ELSE IF SUBSTR(st1,1,10) EQ "$otherPay$" AND SUBSTR(st1,11,3) EQ "YES"  THEN DO:
            st7 = SUBSTR(st1,15).
            DO n6 = 1 TO NUM-ENTRIES(st7,","):
                CREATE pay-list.
                pay-list.artnr = INTEGER(ENTRY(n6,st7,",")).
                pay-list.flag  = YES.
            END.
        END.
    END.   
END.

DO n7 = 1 TO NUM-ENTRIES(str3,"*"):
   st8 = ENTRY(n7,str3,"*").

   /*IF SUBSTR(st8,1,16) = "$revenueOutlets$" AND SUBSTR(st8,17,3) EQ "YES" THEN DO:
       ASSIGN st9 = SUBSTR(st8, 20).
           
           DO n8 = 1 TO NUM-ENTRIES (st9,";") :
                st10 = ENTRY(n8,st9,";").
                DO n9 = 1 TO NUM-ENTRIES (st10,"|"):
                   st11 = ENTRY (n9,st10,"|").

                   IF n9 EQ 1 AND st11 NE "" AND ENTRY(2,st10,"|") NE "" THEN ASSIGN dept = INTEGER(st11).
                   ELSE IF st11 NE "" AND n9 GT 1 THEN DO:
                       DO n10 = 1 TO NUM-ENTRIES(st11, ","):
                           st12 = ENTRY(n10, st11, ",").
                           IF st12 NE "" THEN DO:
                                CREATE outlet-list.
                                ASSIGN outlet-list.departement = dept
                                       outlet-list.artnr       =  INTEGER(ENTRY(1,st12,","))
                                       outlet-list.flag        = "Outlet"
                                       outlet-list.flag-used   = YES.
                           END.
                       END.
                   END.                             
                END.
        
            END.
   END.*/

   IF SUBSTR(st8,1,9) = "$FBcover$" AND SUBSTR(st8,10,3) EQ "YES" THEN DO:
   ASSIGN st13 = SUBSTR(st8,13).   
        DO n11 = 1 TO NUM-ENTRIES (st13,";"):
        st14 = ENTRY(n11,st13,";").
            DO n12 = 1 TO NUM-ENTRIES(st14,"|"):
            st15 = ENTRY(n12,st14,"|").
                IF n12 EQ 1 AND st15 NE "" THEN ASSIGN dept1 = INTEGER(st15).
                ELSE IF st15 NE "" AND n12 GT 1 THEN DO:
                   
                   DO n13 = 1 TO NUM-ENTRIES(st15,"-"):
                      st16 = ENTRY(n13,st15,"-").
                      st17 = SUBSTR(st16,2).
                      
                      DO n14 = 1 TO NUM-ENTRIES(st17,","):
                         CREATE outlet-list.
                         ASSIGN outlet-list.departement = dept1
                                outlet-list.artnr       = INTEGER(ENTRY(n14,st17,","))
                                outlet-list.flag        = "FBcover"
                                outlet-list.flag-used   = YES.
                      END.
                   END.
                END.
            END.
        END.
   END. 
   IF SUBSTR(st8,1,9) = "$FBsales$" AND SUBSTR(st8,10,3) EQ "YES" THEN DO:
      ASSIGN st18 = SUBSTR(st8,13).
          DO n15 = 1 TO NUM-ENTRIES(st18,","):
          CREATE outlet-list.
          ASSIGN outlet-list.departement = INTEGER(ENTRY(n15,st18,","))
                 outlet-list.flag        = "FBsales"
                 outlet-list.flag-used   = YES.
          END.    
   END.
END.

/*DO n16 = 1 TO NUM-ENTRIES(str2,";"):
   st19 = ENTRY(n16,str2,";").

   IF SUBSTR(st19,1,11)  = "$statistic$" AND SUBSTR(st19,12,3) EQ "YES" THEN DO:
    ASSIGN st20 = SUBSTR(st19,16). 
    DO n20 = 1 TO NUM-ENTRIES(st20,"/"):
        st21 = ENTRY(n20,st20,"/").
        
        IF n20 EQ 1 AND st21 NE "" THEN ASSIGN zwkum1 = INTEGER(st21).
        ELSE IF st21 NE "" AND n20 GT 1 THEN DO:
            DO n21 = 1 TO NUM-ENTRIES(st21,","):
                st22 = ENTRY(n21,st21,",").
                CREATE stat-list.
                ASSIGN stat-list.zwkum = zwkum1
                       stat-list.artnr = INT(st22)
                       stat-list.flag  = YES.
            END.
        END.
    END.
   END.
END.*/

IF case-type EQ 1 THEN DO:
    FOR EACH artikel WHERE artikel.artart EQ 7 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST pay-list WHERE pay-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE pay-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 2 THEN DO:
    FOR EACH artikel WHERE artikel.artart EQ 2 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST pay-list WHERE pay-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE pay-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 3 THEN DO:
    FOR EACH artikel WHERE artikel.artart EQ 6 AND artikel.umsatzart EQ 0 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST pay-list WHERE pay-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE pay-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 4 THEN DO:
    FOR EACH artikel WHERE artikel.artart EQ 6 AND artikel.umsatzart EQ 4 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST pay-list WHERE pay-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE pay-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 5 THEN DO:
    FOR EACH artikel WHERE artikel.artart EQ 5 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST pay-list WHERE pay-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE pay-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 6 THEN DO:
    FOR EACH hoteldpt NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = hoteldpt.num
               str-list.bezeich = hoteldpt.depart.

        FIND FIRST outlet-list WHERE outlet-list.flag EQ "FBsales" AND outlet-list.departement EQ hoteldpt.num NO-LOCK NO-ERROR.
        IF AVAILABLE outlet-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 7 THEN DO:
    FOR EACH artikel WHERE artikel.departement EQ departement NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST outlet-list WHERE outlet-list.flag EQ "Outlet" AND outlet-list.artnr EQ artikel.artnr AND outlet-list.departemen EQ departement NO-LOCK NO-ERROR.
        IF AVAILABLE outlet-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 8 THEN DO:
    FOR EACH artikel WHERE artikel.endkum EQ c-862 AND artikel.departement EQ departement AND artikel.umsatzart = 5 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST outlet-list WHERE outlet-list.flag EQ "FBcover" AND outlet-list.artnr EQ artikel.artnr AND outlet-list.departemen EQ departement NO-LOCK NO-ERROR.
        IF AVAILABLE outlet-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 9 THEN DO:
    FOR EACH artikel WHERE artikel.endkum EQ c-892 AND artikel.departement EQ departement AND artikel.umsatzart = 6 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST outlet-list WHERE outlet-list.flag EQ "FBcover" AND outlet-list.artnr EQ artikel.artnr AND outlet-list.departemen EQ departement NO-LOCK NO-ERROR.
        IF AVAILABLE outlet-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 10 THEN DO:
    FOR EACH artikel WHERE (artikel.artart EQ 0 OR artikel.artart EQ 8) AND artikel.umsatzart EQ 1 AND artikel.departement EQ departement NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.
    END.
END.

ELSE IF case-type EQ 11 THEN DO:
    FOR EACH artikel WHERE (artikel.artart EQ 0 OR artikel.artart EQ 8) AND artikel.umsatzart EQ 4 AND artikel.departement EQ departement NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.
    END.
END.

ELSE IF case-type EQ 12 THEN DO:
    FOR EACH artikel WHERE artikel.zwkum EQ 26 AND artikel.endkum EQ 36 AND artikel.departement EQ departement NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST pay-list WHERE pay-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE pay-list THEN str-list.used = YES.
    END.
END.

ELSE IF case-type EQ 13 THEN DO:
    FOR EACH artikel WHERE artikel.zwkum EQ zwkum AND artikel.departement EQ 0 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST stat-list WHERE stat-list.artnr EQ artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE stat-list THEN str-list.used = YES.
    END.
END.

 
ELSE IF case-type EQ 14 THEN DO:
    FOR EACH artikel WHERE artikel.artnr LT 3000 AND artikel.departement EQ departement AND artikel.umsatzart LT 5 NO-LOCK:
        CREATE str-list.
        ASSIGN str-list.nr      = artikel.artnr
               str-list.bezeich = artikel.bezeich.

        FIND FIRST outlet-list WHERE outlet-list.flag EQ "FBcover" AND outlet-list.artnr EQ artikel.artnr AND outlet-list.departemen EQ departement NO-LOCK NO-ERROR.
        IF AVAILABLE outlet-list THEN str-list.used = YES.
    END.
END.

