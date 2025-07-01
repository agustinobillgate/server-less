DEFINE TEMP-TABLE resto-list
    FIELD deptnr      AS INT    
    FIELD departement AS CHAR FORMAT "x(30)"
    FIELD artikel     AS CHAR FORMAT "x(30)"
    FIELD resto-info  AS CHAR.

DEFINE TEMP-TABLE fbcover-list
    FIELD deptnr      AS INT    
    FIELD departement AS CHAR FORMAT "x(30)"
    FIELD food        AS CHAR FORMAT "x(30)"
    FIELD beverage    AS CHAR FORMAT "x(30)"
    FIELD material    AS CHAR FORMAT "x(30)".

DEFINE TEMP-TABLE paxcover-list
    FIELD deptnr      AS INT    
    FIELD departement AS CHAR FORMAT "x(30)"
    FIELD artikel     AS CHAR FORMAT "x(30)".

DEFINE TEMP-TABLE setup-list
    FIELD payment     AS CHAR FORMAT "x(400)"
    FIELD statistic   AS CHAR FORMAT "x(400)"
    FIELD outlets     AS CHAR FORMAT "x(400)".

DEFINE TEMP-TABLE pay-list
    FIELD payment-flag      AS CHAR INITIAL NO
    FIELD ledger-flag       AS CHAR INITIAL NO
    FIELD cash-flag         AS CHAR INITIAL NO
    FIELD foreign-flag      AS CHAR INITIAL NO
    FIELD deposit-flag      AS CHAR INITIAL NO
    FIELD other-pay-flag    AS CHAR INITIAL NO
    FIELD artnr-payment     AS CHAR
    FIELD artnr-ledger      AS CHAR
    FIELD artnr-cash        AS CHAR
    FIELD artnr-foreign     AS CHAR
    FIELD artnr-deposit     AS CHAR
    FIELD artnr-other-pay   AS CHAR. 

DEFINE TEMP-TABLE statistic-list
    FIELD fo-rev-flag       AS CHAR INITIAL NO
    FIELD other-income-flag AS CHAR INITIAL NO
    FIELD segment-rev-flag  AS CHAR INITIAL NO
    FIELD statistic-flag    AS CHAR INITIAL NO
    FIELD artnr-fo          AS CHAR
    FIELD artnr-other       AS CHAR
    FIELD fo-info           AS CHAR
    FIELD other-info        AS CHAR
    FIELD segmentcode       AS CHAR
    FIELD segment-info      AS CHAR
    FIELD statistic-zwkum   AS CHAR
    FIELD statistic-artnr   AS CHAR
    FIELD statistic-info    AS CHAR.

DEFINE TEMP-TABLE outlets-list
    FIELD outlets-flag     AS CHAR INITIAL NO
    FIELD fbcover-flag     AS CHAR INITIAL NO
    FIELD fbsales-flag     AS CHAR INITIAL NO
    FIELD outlets-info     AS CHAR
    FIELD fbcover-info     AS CHAR
    FIELD fbsales-info     AS CHAR.

DEFINE TEMP-TABLE outlets-info
    FIELD deptnr    AS INT
    FIELD artnr     AS CHAR
    FIELD otls-info AS CHAR.

DEFINE TEMP-TABLE fbcover-info 
    FIELD deptnr    AS INT
    FIELD food      AS CHAR
    FIELD beverage  AS CHAR
    FIELD material  AS CHAR.


DEFINE OUTPUT PARAMETER TABLE FOR resto-list.
DEFINE OUTPUT PARAMETER TABLE FOR fbcover-list.
DEFINE OUTPUT PARAMETER TABLE FOR paxcover-list.
DEFINE OUTPUT PARAMETER TABLE FOR pay-list.
DEFINE OUTPUT PARAMETER TABLE FOR statistic-list.
DEFINE OUTPUT PARAMETER TABLE FOR outlets-list.
DEFINE OUTPUT PARAMETER gsheet-link AS CHAR. 

/*DEFINE VAR gsheet-link AS CHAR.*/


DEFINE VARIABLE str1  AS CHAR.
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
DEFINE VARIABLE st13  AS CHAR.
DEFINE VARIABLE st14  AS CHAR.
DEFINE VARIABLE st15  AS CHAR.
DEFINE VARIABLE st16  AS CHAR.
DEFINE VARIABLE st17  AS CHAR.
DEFINE VARIABLE st18  AS CHAR.
DEFINE VARIABLE st19  AS CHAR.
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
DEFINE VARIABLE n11   AS INT.
DEFINE VARIABLE n12   AS INT.
DEFINE VARIABLE n13   AS INT.
DEFINE VARIABLE n14   AS INT.
DEFINE VARIABLE n15   AS INT.
DEFINE VARIABLE n16   AS INT.
DEFINE VARIABLE n17   AS INT.
DEFINE VARIABLE n18   AS INT.
DEFINE VARIABLE n19   AS INT.
DEFINE VARIABLE n20   AS INT.


FOR EACH hoteldpt WHERE hoteldpt.num NE 0 NO-LOCK:
   CREATE resto-list.
   ASSIGN resto-list.deptnr       = hoteldpt.num
          resto-list.departement  = hoteldpt.depart.
   CREATE fbcover-list.
   ASSIGN fbcover-list.deptnr     = hoteldpt.num
          fbcover-list.departement  = hoteldpt.depart.
   CREATE paxcover-list.
   ASSIGN paxcover-list.deptnr       = hoteldpt.num
          paxcover-list.departement  = hoteldpt.depart.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 265 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
   ASSIGN 
       str1  = queasy.char1
       str2  = queasy.char2
       str3  = queasy.char3.
END. 

FIND FIRST pay-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE pay-list THEN DO:
    CREATE pay-list.
    DO n = 1 TO NUM-ENTRIES(str1,";"):
        st1 = ENTRY(n,str1,";").
    
        IF SUBSTR(st1,1,9)  = "$payment$" AND SUBSTR(st1,10,3) EQ "YES" THEN DO:
            ASSIGN
                pay-list.payment-flag    = SUBSTR(st1,10,3)
                pay-list.artnr-payment  = SUBSTR(st1,14).
        END.
    
        
        ELSE IF SUBSTR(st1,1,8) EQ "$ledger$" AND SUBSTR(st1,9,3) EQ "YES"  THEN DO:
             ASSIGN
                pay-list.ledger-flag  = SUBSTR(st1,9,3)
                pay-list.artnr-ledger = SUBSTR(st1,13).
        END.
           
    
        ELSE IF SUBSTR(st1,1,6) EQ "$cash$" AND SUBSTR(st1,7,3) EQ "YES"  THEN DO:
            ASSIGN
                pay-list.cash-flag  = SUBSTR(st1,7,3)
                pay-list.artnr-cash = SUBSTR(st1,11).
        END.
            
    
        ELSE IF SUBSTR(st1,1,9) EQ "$foreign$" AND SUBSTR(st1,10,3) EQ "YES"  THEN DO:
            ASSIGN
                pay-list.foreign-flag  = SUBSTR(st1,10,3)
                pay-list.artnr-foreign = SUBSTR(st1,14).
        END.
            
    
        ELSE IF SUBSTR(st1,1,9) EQ "$deposit$" AND SUBSTR(st1,10,3) EQ "YES"  THEN DO:
            ASSIGN
                pay-list.deposit-flag  = SUBSTR(st1,10,3)
                pay-list.artnr-deposit = SUBSTR(st1,14).
        END.
            
    
        ELSE IF SUBSTR(st1,1,10) EQ "$otherPay$" AND SUBSTR(st1,11,3) EQ "YES"  THEN DO:
            ASSIGN
                pay-list.other-pay-flag  = SUBSTR(st1,11,3)
                pay-list.artnr-other     = SUBSTR(st1,15).
        END.
        
        ELSE IF SUBSTR(st1,1,8) EQ "$Gsheet$" THEN DO:
            ASSIGN
                gsheet-link  = SUBSTR(st1,9).
        END.

    END.
END.

FIND FIRST statistic-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE statistic-list THEN DO:
   CREATE statistic-list.
   DO n1 = 1 TO NUM-ENTRIES(str2,";"):
   st2 = ENTRY(n1,str2,";").
       IF SUBSTR(st2,1,11)  = "$FOrevenue$" AND SUBSTR(st2,12,3) EQ "YES" THEN DO:
         ASSIGN
            statistic-list.fo-rev-flag   = SUBSTR(st2,12,3)
            statistic-list.fo-info       = SUBSTR(st2,16).

         st3 = SUBSTR(st2,16,9999).
            
         DO n2 = 1 TO NUM-ENTRIES(st3,","):
            st4 = ENTRY(n2,st3,",").
            ASSIGN
                statistic-list.artnr-fo = statistic-list.artnr-fo + ENTRY(1,st4,"-") + ",".
         END.
       END.
       IF SUBSTR(st2,1,13)  = "$otherincome$" AND SUBSTR(st2,14,3) EQ "YES" THEN DO:
         ASSIGN
            statistic-list.other-income-flag   = SUBSTR(st2,14,3)
            statistic-list.other-info          = SUBSTR(st2,18).

         st5 = SUBSTR(st2,18,9999).
         DO n3 = 1 TO NUM-ENTRIES(st5,","):
            st6 = ENTRY(n3,st5,",").
            ASSIGN
                statistic-list.artnr-other = statistic-list.artnr-other + ENTRY(1,st6,"-") + ",".
         END.   
       END.
       IF SUBSTR(st2,1,9)  = "$segment$" AND SUBSTR(st2,10,3) EQ "YES" THEN DO:
        ASSIGN 
            statistic-list.segment-rev-flag = SUBSTR(st2,10,3)
            statistic-list.segment-info = SUBSTR(st2,14).

        st13 = SUBSTR(st2,14).

        DO n11 = 1 TO NUM-ENTRIES(st13,","):
            st14 = ENTRY(n11,st13,",").
            ASSIGN
                statistic-list.segmentcode = statistic-list.segmentcode + ENTRY(1,st14,"-") + ",".
        END.
       END.
       IF SUBSTR(st2,1,11)  = "$statistic$" AND SUBSTR(st2,12,3) EQ "YES" THEN DO:
        ASSIGN 
           statistic-list.statistic-flag = SUBSTR(st2,12,3)
           st16 = SUBSTR(st2,16).
           
           statistic-list.statistic-zwkum = ENTRY(1,st16,"/").
           st17                           = ENTRY(2,st16,"/").
            
           statistic-list.statistic-info  = st17.

           DO n14 = 1 TO NUM-ENTRIES(st17,","):
              st18 = ENTRY(n14,st17,",").
              
              IF ENTRY(1,st18,"-") NE "" THEN
              statistic-list.statistic-artnr = statistic-list.statistic-artnr + ENTRY(1,st18,"-") + ",".

           END.
           
       END.
   END.
END.

FIND FIRST outlets-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE outlets-list THEN DO:
    CREATE outlets-list.
    DO n4 = 1 TO NUM-ENTRIES(str3,"*"):
       st7 = ENTRY(n4,str3,"*").

       IF SUBSTR(st7,1,16) = "$revenueOutlets$" AND SUBSTR(st7,17,3) EQ "YES" THEN DO:
           ASSIGN 
               outlets-list.outlets-flag = SUBSTR(st7,17,3)
               outlets-list.outlets-info = SUBSTR(st7,20).
          
          DO n6 = 1 TO NUM-ENTRIES (outlets-list.outlets-info,";") :
               st8 = ENTRY(n6,outlets-list.outlets-info,";").
                
               DO n7 = 1 TO NUM-ENTRIES (st8,"|"):
                  st9 = ENTRY (n7,st8,"|").
                  IF st9 NE "" AND n7 EQ 1 THEN DO:
                   CREATE outlets-info. 
                   ASSIGN outlets-info.deptnr      = INTEGER(st9).
                  END.
                  ELSE IF st9 NE "" AND n7 NE 1 THEN DO:
                   ASSIGN outlets-info.otls-info = st9. 
                   DO n13 = 1 TO NUM-ENTRIES (st9,","):
                       st15 = ENTRY(n13,st9,",").

                       ASSIGN outlets-info.artnr =  outlets-info.artnr + ENTRY(1,st15,"-") + ",".
                   END.
                   
                  END.
               END.

           END.
       END.

       IF SUBSTR(st7,1,9) = "$FBcover$" AND SUBSTR(st7,10,3) EQ "YES" THEN DO:
        ASSIGN 
            outlets-list.fbcover-flag = SUBSTR(st7,10,3)
            outlets-list.fbcover-info = SUBSTR(st7,13).
            
            DO n8 = 1 TO NUM-ENTRIES (fbcover-info,";"):
                st10 = ENTRY(n8,fbcover-info,";").
                CREATE fbcover-info.
                DO n9 = 1 TO NUM-ENTRIES(st10,"|"):
                    st11 = ENTRY (n9,st10,"|").
                    
                    IF n9 EQ 1 THEN DO:
                        ASSIGN fbcover-info.deptnr = INT(st11). 
                    END.
                    IF n9 NE 1 THEN DO:
                        DO n10 = 1 TO NUM-ENTRIES(st11,"-"):
                            st12 = ENTRY(n10,st11,"-").
                            IF SUBSTR(st12,1,1) EQ "F" THEN ASSIGN fbcover-info.food = SUBSTR(st12,2,9999).
                            ELSE IF SUBSTR(st12,1,1) EQ "B" THEN ASSIGN fbcover-info.beverage = SUBSTR(st12,2,9999).
                            ELSE IF SUBSTR(st12,1,1) EQ "M" THEN ASSIGN fbcover-info.material = SUBSTR(st12,2,9999).
                        END.
                    END.
                   
                END.
            END.
       END. 
       IF SUBSTR(st7,1,9) = "$FBsales$" AND SUBSTR(st7,10,3) EQ "YES" THEN DO:
        ASSIGN   
            outlets-list.fbsales-flag = SUBSTR(st7,10,3)
            outlets-list.fbsales-info = SUBSTR(st7,13).     
       END.
    END.
END.

FOR EACH resto-list NO-LOCK:
    FIND FIRST outlets-info WHERE outlets-info.deptnr EQ resto-list.deptnr NO-LOCK NO-ERROR.
    IF AVAILABLE outlets-info THEN 
        ASSIGN resto-list.artikel     = outlets-info.artnr
               resto-list.resto-info  = outlets-info.otls-info. 
END.

FOR EACH fbcover-list NO-LOCK:
    FIND FIRST fbcover-info WHERE fbcover-info.deptnr EQ fbcover-list.deptnr NO-LOCK NO-ERROR.
    IF AVAILABLE fbcover-info THEN 
        ASSIGN 
            fbcover-list.food        = fbcover-info.food 
            fbcover-list.beverage    = fbcover-info.beverage
            fbcover-list.material    = fbcover-info.material.
END.



