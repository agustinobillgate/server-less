
DEFINE TEMP-TABLE segm1-list 
    FIELD selected      AS LOGICAL INITIAL NO 
    FIELD segm          AS INTEGER 
    FIELD bezeich       AS CHAR FORMAT "x(24)"
    FIELD bezeich1      AS CHAR FORMAT "x(24)". /* ozhan added */
 
DEFINE TEMP-TABLE argt-list 
    FIELD selected      AS LOGICAL INITIAL NO 
    FIELD argtnr        AS INTEGER
    FIELD argt          AS CHAR 
    FIELD bezeich       AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE zikat-list 
    FIELD selected      AS LOGICAL INITIAL NO 
    FIELD zikatnr       AS INTEGER 
    FIELD kurzbez       AS CHAR 
    FIELD bezeich       AS CHAR FORMAT "x(24)". 
 
DEFINE TEMP-TABLE room-list 
    FIELD nr            AS INTEGER 
    FIELD tag           AS INTEGER 
    FIELD bezeich       AS CHAR FORMAT "x(15)" 
    FIELD room          AS INTEGER EXTENT 12 FORMAT "->>,>>9" 
    FIELD pax           AS INTEGER EXTENT 12 FORMAT "->>,>>9" 
    FIELD coom          AS CHAR EXTENT 12 FORMAT "x(7)" 
    FIELD rstat         AS INTEGER INITIAL 0. 

DEFINE TEMP-TABLE sum-list 
    FIELD bezeich       AS CHAR FORMAT "x(15)" 
    FIELD summe         AS INTEGER EXTENT 12 FORMAT "->>,>>9". 

DEFINE TEMP-TABLE segm-list 
    FIELD segmentcode   AS INTEGER 
    FIELD bezeich       AS CHAR FORMAT "x(15)" 
    FIELD bezeich1      AS CHAR FORMAT "x(15)"  /* ozhan added */
    FIELD segm          AS INTEGER EXTENT 12 FORMAT "->>,>>9". 

DEFINE TEMP-TABLE rev-list
    FIELD bezeich       AS CHAR FORMAT "x(15)"
    FIELD str1          AS CHAR EXTENT 6 FORMAT "x(14)".

DEFINE TEMP-TABLE tt-month-str
    FIELD i-counter     AS INTEGER
    FIELD month-str     AS CHAR.
                                        
DEFINE INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER vhp-limited    AS LOGICAL.
DEFINE INPUT  PARAMETER dlist          AS CHAR FORMAT "x(133)". 
                                    
DEFINE INPUT  PARAMETER op-type        AS INTEGER.
DEFINE INPUT  PARAMETER printer-nr     AS INTEGER.
DEFINE INPUT  PARAMETER call-from      AS INTEGER.
DEFINE INPUT  PARAMETER txt-file       AS CHAR.
                                    
DEFINE INPUT  PARAMETER monthDaySelect AS INTEGER.
DEFINE INPUT  PARAMETER roomPaxSelect  AS INTEGER.
DEFINE INPUT  PARAMETER nationselect   AS CHAR.
DEFINE INPUT  PARAMETER all-segm       AS LOGICAL. 
DEFINE INPUT  PARAMETER all-argt       AS LOGICAL.
DEFINE INPUT  PARAMETER all-zikat      AS LOGICAL. 
            
DEFINE INPUT  PARAMETER from-month     AS CHAR.
DEFINE INPUT  PARAMETER show-rmrev     AS LOGICAL.
DEFINE INPUT  PARAMETER incl-tent      AS LOGICAL.
DEFINE INPUT  PARAMETER incl-wait      AS LOGICAL.
DEFINE INPUT  PARAMETER incl-glob      AS LOGICAL.
              
DEFINE OUTPUT PARAMETER TABLE FOR tt-month-str.

DEFINE OUTPUT PARAMETER TABLE FOR room-list.
DEFINE OUTPUT PARAMETER TABLE FOR rev-list.
DEFINE OUTPUT PARAMETER TABLE FOR sum-list.
DEFINE OUTPUT PARAMETER TABLE FOR segm-list.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR segm1-list.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR argt-list.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR zikat-list.

{supertransBL.i}
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "annual-fcast". 

/*MTDEFINE shared VARIABLE LnLDelimeter AS CHAR.*/

/*MTDEFINE VAR month-str AS CHAR EXTENT 12 .*/
DEFINE VARIABLE rmsharer        AS LOGICAL INITIAL NO.
DEFINE VARIABLE week-list       AS CHAR EXTENT 12 FORMAT "x(5)" 
  INITIAL [" Jan ", " Feb ", " Mar ", " Apr ", " May ", " Jun ", 
           " Jul ", " Aug ", " Sep ", " Oct ", " Nov ", " Dec "]. 
DEFINE VARIABLE wlist           AS CHAR FORMAT "x(133)". 
                      
DEFINE VARIABLE month-str       AS CHAR EXTENT 12 NO-UNDO.
DEFINE VARIABLE rm-serv         AS LOGICAL        NO-UNDO.
DEFINE VARIABLE foreign-rate    AS LOGICAL        NO-UNDO. 
                                        
DEFINE STREAM s1.
DEFINE VARIABLE htl-name        AS CHARACTER FORMAT "x(40)". 
DEFINE VARIABLE htl-adr         AS CHARACTER FORMAT "x(40)". 
DEFINE VARIABLE htl-tel         AS CHARACTER FORMAT "x(24)". 
FIND FIRST paramtext WHERE txtnr = 200 NO-ERROR. 
IF AVAILABLE paramtext THEN htl-name = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 201 NO-ERROR. 
IF AVAILABLE paramtext THEN htl-adr  = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 204 NO-ERROR. 
IF AVAILABLE paramtext THEN htl-tel  = paramtext.ptexte. 

DEFINE VARIABLE out-type    AS CHAR NO-UNDO. 
out-type = translateExtended ("Output By : Rooms", lvCAREA,""). 
 
DEFINE VARIABLE dis-type    AS CHAR NO-UNDO. 
dis-type = translateExtended ("Display : Daily Basis", lvCAREA,""). 
 
DEFINE VARIABLE rm-occ      AS CHAR NO-UNDO. 
rm-occ = translateExtended ("Room Occupied",lvCAREA, ""). 
 
DEFINE VARIABLE pax-occ     AS CHAR NO-UNDO. 
pax-occ = translateExtended( "Person Occupied",lvCAREA,""). 
 
DEFINE VARIABLE avl-rm      AS CHAR NO-UNDO. 
avl-rm =  translateExtended( " Saleable Rooms",lvCAREA,""). 
 
DEFINE VARIABLE occ-proz    AS CHAR NO-UNDO. 
occ-proz = translateExtended( "Occupancy (%)",lvCAREA,""). 

DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE ci-date     AS DATE. 
DEFINE VARIABLE curr-day    AS INTEGER. 
DEFINE VARIABLE tot-room    AS INTEGER. 
DEFINE VARIABLE inactive    AS INTEGER. 
DEFINE VARIABLE mm          AS INTEGER. 
DEFINE VARIABLE yy          AS INTEGER. 
DEFINE VARIABLE diff-one    AS INTEGER INITIAL 0. 
DEFINE VARIABLE ok          AS LOGICAL. 
DEFINE VARIABLE pax         AS INTEGER NO-UNDO. 
DEFINE VARIABLE rev-array   AS DECIMAL EXTENT 12 NO-UNDO.
DEFINE VARIABLE curr-date   AS DATE FORMAT "99/99/9999" LABEL "Date". 
DEFINE VARIABLE date1       AS DATE FORMAT "99/99/9999". 
DEFINE VARIABLE contcode    AS CHAR              NO-UNDO.
DEFINE VARIABLE ct          AS CHAR              NO-UNDO.
DEFINE VARIABLE room-ooo    AS DECIMAL EXTENT 12 NO-UNDO.
DEFINE VARIABLE tmp-room    AS INTEGER EXTENT 12 FORMAT "->>,>>9".                  /* Rulita 281124 | Fixing serverless issue 135 */

FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs AS INTEGER, 
     INPUT kind1   AS INTEGER, 
     INPUT kind2   AS INTEGER). 
    DEFINE VARIABLE rate AS DECIMAL INITIAL 0. 
    IF erwachs GE 1 AND erwachs LE 4 THEN 
        rate = rate + katpreis.perspreis[erwachs]. 
    rate = rate + kind1 * katpreis.kindpreis[1] + kind2 * katpreis.kindpreis[2]. 
    RETURN rate. 
END FUNCTION. 

DEFINE BUFFER kbuff FOR kontline.

/*************MAIN LOGIC***********/
RUN sum-rooms.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
rm-serv = NOT htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 

CASE op-type:
    WHEN 0 THEN
    DO:
        RUN clear-shared.
        RUN create-label11.
        RUN create-browse11. 
        IF show-rmrev THEN
            RUN create-rev.
    END.
    /*MTWHEN 1 THEN
    DO:
        RUN design-lnl.
    END.
    WHEN 2 THEN
    DO:
        RUN print-lnl.
    END.
    WHEN 3 THEN
    DO:
        RUN print-txt.
    END.
    WHEN 4 THEN
        RUN clear-shared1.*/
END CASE.

DO i = 1 TO 12:
    CREATE tt-month-str.
    ASSIGN
        tt-month-str.i-counter = i
        tt-month-str.month-str = month-str[i].
END.

/****************PROCEDURE************/
/*
PROCEDURE create-labels: 
DEFINE VARIABLE datum1 AS CHAR FORMAT "x(5)". 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
  IF monthdayselect = 1 THEN 
  DO: 
    RUN create-label11. 
    RETURN. 
  END. 
  mm = INTEGER(SUBSTR(from-month,1,2)). 
  yy = INTEGER(SUBSTR(from-month,3,4)). 
 
  dlist = "               ". 
 
  DO i = 1 TO 12: 
    curr-day = mm. 
    datum = DATE(mm, 1, yy). 
    datum1 = SUBSTR(STRING(datum),1,5). 
 
    dlist = dlist + "   " + datum1. 
 
    IF i = 1 THEN DO: 
      ASSIGN room-list.room[1]:LABEL IN BROWSE b1 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[1]:label-fgcolor = 0. 
      ASSIGN room-list.room[1]:label-bgcolor = 8. 
      month-str1 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 2 THEN DO: 
      ASSIGN room-list.room[2]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[2]:label-fgcolor = 0. 
      ASSIGN room-list.room[2]:label-bgcolor = 8. 
      month-str2 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
     END. 
    ELSE IF i = 3 THEN DO: 
      ASSIGN room-list.room[3]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[3]:label-fgcolor = 0. 
      ASSIGN room-list.room[3]:label-bgcolor = 8. 
      month-str3 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 4 THEN DO: 
      ASSIGN room-list.room[4]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[4]:label-fgcolor = 0. 
      ASSIGN room-list.room[4]:label-bgcolor = 8. 
      month-str4 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 5 THEN DO: 
      ASSIGN room-list.room[5]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[5]:label-fgcolor = 0. 
      ASSIGN room-list.room[5]:label-bgcolor = 8. 
      month-str5 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,"").  
    END. 
    ELSE IF i = 6 THEN DO: 
      ASSIGN room-list.room[6]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[6]:label-fgcolor = 0. 
      ASSIGN room-list.room[6]:label-bgcolor = 8. 
      month-str6 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 7 THEN DO: 
      ASSIGN room-list.room[7]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[7]:label-fgcolor = 0. 
      ASSIGN room-list.room[7]:label-bgcolor = 8. 
      month-str7 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 8 THEN DO: 
      ASSIGN room-list.room[8]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[8]:label-fgcolor = 0. 
      ASSIGN room-list.room[8]:label-bgcolor = 8. 
      month-str8 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 9 THEN DO: 
      ASSIGN room-list.room[9]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[9]:label-fgcolor = 0. 
      ASSIGN room-list.room[9]:label-bgcolor = 8. 
      month-str9 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 10 THEN DO: 
      ASSIGN room-list.room[10]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[10]:label-fgcolor = 0. 
      ASSIGN room-list.room[10]:label-bgcolor = 8. 
      month-str10 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 11 THEN DO: 
      ASSIGN room-list.room[11]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[11]:label-fgcolor = 0. 
      ASSIGN room-list.room[11]:label-bgcolor = 8. 
      month-str11 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 12 THEN DO: 
      ASSIGN room-list.room[12]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.room[12]:label-fgcolor = 0. 
      ASSIGN room-list.room[12]:label-bgcolor = 8. 
      month-str12 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,"").  
    END. 
    mm = mm + 1. 
    IF mm = 13 THEN 
    DO: 
      mm = 1. 
      yy = yy + 1. 
    END. 
  END. 
END. 
*/

/*MT 22/03/13
PROCEDURE assign-it:
    DEFINE VARIABLE lodging AS DECIMAL NO-UNDO.
    DEFINE VARIABLE qty AS INT.
    DEFINE INPUT PARAMETER j AS INTEGER.
    IF show-rmrev THEN
    DO:
        qty = res-line.zimmeranz.
        lodging = res-line.zipreis.
        RUN calculate-zipreis(datum, INPUT-OUTPUT lodging).
        /*MT*/
        lodging = lodging * qty.
        rev-array[j] = rev-array[j] + lodging.
    END.
END.*/

PROCEDURE assign-it:
    DEFINE INPUT PARAMETER j      AS INTEGER.
    /*DEFINE INPUT PARAMETER datum AS INTEGER.*/
    DEFINE INPUT PARAMETER datum  AS DATE.     /*geral D5F9E2*/ 
    DEFINE INPUT PARAMETER from-date AS DATE. /*geral add from-date D5F9E2*/
    DEFINE VARIABLE net-lodg      AS DECIMAL FORMAT "->,>>>,>>9.99" NO-UNDO INIT 0.
    DEFINE VARIABLE Fnet-lodg     AS DECIMAL FORMAT "->,>>>,>>9.99" NO-UNDO INIT 0.

    DEFINE VARIABLE tot-breakfast AS DECIMAL FORMAT "->,>>>,>>9.99".
    DEFINE VARIABLE tot-lunch     AS DECIMAL FORMAT "->,>>>,>>9.99".
    DEFINE VARIABLE tot-dinner    AS DECIMAL FORMAT "->,>>>,>>9.99".
    DEFINE VARIABLE tot-other     AS DECIMAL FORMAT "->,>>>,>>9.99".
    DEFINE VARIABLE tot-rmrev     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-vat       AS DECIMAL INITIAL 0.
    DEFINE VARIABLE tot-service   AS DECIMAL INITIAL 0.
    
    /*RUN get-room-breakdown.p(RECID(res-line), datum, j, datum,
                             OUTPUT Fnet-lodg, OUTPUT net-lodg,
                             OUTPUT tot-breakfast, OUTPUT tot-lunch,
                             OUTPUT tot-dinner, OUTPUT tot-other,
                             OUTPUT tot-rmrev, OUTPUT tot-vat,
                             OUTPUT tot-service).*/

    /*geral D5F9E2*/ 
    IF datum = res-line.abreise THEN .
    ELSE 
    DO:
      IF res-line.zipreis GT 0 THEN
      RUN get-room-breakdown.p(RECID(res-line), datum, j, from-date,
                               OUTPUT Fnet-lodg, OUTPUT net-lodg,
                               OUTPUT tot-breakfast, OUTPUT tot-lunch,
                               OUTPUT tot-dinner, OUTPUT tot-other,
                               OUTPUT tot-rmrev, OUTPUT tot-vat,
                               OUTPUT tot-service).
      
      /*MT 28/03/13
      RUN calc-lodging2(datum, j, OUTPUT net-lodg).*/
      
      rev-array[j] = rev-array[j] + net-lodg.
    END.
    /*END GERAL*/
END.

PROCEDURE create-browse11: 
DEFINE VARIABLE from-date   AS DATE. 
DEFINE VARIABLE to-date     AS DATE. 
DEFINE VARIABLE datum1      AS DATE. 
DEFINE VARIABLE datum2      AS DATE. 
DEFINE VARIABLE abreise1    AS DATE. 
DEFINE VARIABLE cur-date    AS DATE. 
DEFINE VARIABLE anz         AS INTEGER EXTENT 12 INITIAL 
    [31,28,31,30,31,30,31,31,30,31,30,31]. 
DEFINE VARIABLE tmp-list    AS INTEGER EXTENT 12 FORMAT ">9". 
DEFINE VARIABLE tmp-i       AS INTEGER EXTENT 12 FORMAT "9" INIT 0. 
DEFINE VARIABLE last-resnr  AS INTEGER INITIAL 0. 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE VARIABLE lodging     AS DECIMAL.
DEFINE VARIABLE loop-date   AS DATE.
 
DEFINE BUFFER r1-list  FOR room-list. 
DEFINE BUFFER r2-list  FOR room-list. 
DEFINE BUFFER r3-list  FOR room-list. 
DEFINE BUFFER r4-list  FOR room-list. /*Person Occupied*/
DEFINE BUFFER r5-list  FOR room-list. /*Tentative-Occ %*/
                       
/*DS*/             
DEFINE VARIABLE datum3 AS DATE.
DEFINE BUFFER r6-list  FOR room-list. /*SaleRoom w/ OOO*/
DEFINE BUFFER r7-list  FOR room-list. /*Occupancy w/ OOO(%)*/
DEFINE BUFFER r8-list  FOR room-list. /*OOO*/
DEFINE VARIABLE ooo-room AS INT INITIAL 0 NO-UNDO. 

    FOR EACH room-list: 
        DELETE room-list. 
    END. 
 
    DO i = 1 TO 12:
        rev-array[i] = 0.
    END.

    DO i = 1 TO 31: 
        CREATE room-list. 
        room-list.tag = i. 
        room-list.bezeich = "            " + STRING(i, ">9 "). 
        IF incl-tent OR incl-wait THEN 
        DO: 
            CREATE room-list. 
            room-list.tag = i. 
            room-list.rstat = 1. 
        END. 
    END. 
 
    CREATE room-list. 
    ASSIGN 
        room-list.tag = 32 
        room-list.bezeich = "===============". 
    DO i = 1 TO 12: 
        room-list.coom[i] = "=======". 
    END. 
 
/* IF roompaxselect = 0 THEN */ 
    DO: 
        CREATE room-list. 
        ASSIGN 
            room-list.tag = 33 
            room-list.bezeich = translateExtended( "  Room Occupied",lvCAREA,""). 

        CREATE room-list. 
        ASSIGN 
            room-list.tag = 34 
            room-list.bezeich = translateExtended( " Saleable Rooms",lvCAREA,""). 

        CREATE room-list. 
        ASSIGN 
            room-list.tag = 35 
            room-list.bezeich = "  Occupancy (%)". 
    END. 
    CREATE room-list. 
    ASSIGN 
        room-list.tag = 36 
        room-list.bezeich = translateExtended( "Person Occupied",lvCAREA,""). 
 
    IF incl-tent THEN 
    DO: 
        CREATE room-list. 
        ASSIGN 
            room-list.tag = 37 
            room-list.bezeich = translateExtended( "Tentative-Occ %",lvCAREA,""). 
        FIND FIRST r5-list WHERE r5-list.tag = 37. /*Tentative-Occ %*/
    END. 

    FIND FIRST r1-list WHERE r1-list.tag = 33. /*Room Occupied*/
    FIND FIRST r2-list WHERE r2-list.tag = 34. /*Saleable Rooms*/
    FIND FIRST r3-list WHERE r3-list.tag = 35. /*Occupancy (%)*/
    FIND FIRST r4-list WHERE r4-list.tag = 36. /*Person Occupied*/

    /*DS 120419 - add ooo room for 1 year (F6F5B7)*/
    CREATE room-list.
    ASSIGN 
        room-list.tag = 38
        room-list.bezeich = translateExtended("SaleRoom w/ OOO", lvCAREA, "").
    CREATE room-list.
    ASSIGN 
        room-list.tag = 39
        room-list.bezeich = translateExtended("Occ(%) w/ OOO", lvCAREA, "").
    
    FIND FIRST r6-list WHERE r6-list.tag = 38. /*SaleRoom w/ OOO*/
    FIND FIRST r7-list WHERE r7-list.tag = 39. /*Occupancy w/ OOO(%)*/
    FIND FIRST r8-list WHERE r8-list.tag = 39. /*OOO*/                          /* Rulita 221124 issue git 135 | Fixing r7-list.tag change to r8-list.tag */
    /*end DS*/

    mm = INTEGER(SUBSTR(from-month,1,2)) + diff-one. 
    yy = INTEGER(SUBSTR(from-month,3,4)). 
    IF diff-one = 1 AND mm = 13 THEN 
    DO: 
        mm = 1. 
        yy = yy + 1. 
    END. 
    ELSE IF diff-one = -1 AND mm = 0 THEN 
    DO: 
        mm = 12. 
        yy = yy - 1. 
    END. 
    curr-date  = DATE(mm, 1, yy). 
    from-month = STRING(MONTH(curr-date),"99") + STRING(YEAR(curr-date),"9999"). 
    
    mm = INTEGER(SUBSTR(from-month,1,2)). 
    yy = INTEGER(SUBSTR(from-month,3,4)). 
    j = mm - 1. 
    DO i = 1 TO 12: 
        j = j + 1. 
        IF j GT 12 THEN j = j - 12. 
        tmp-list[i] = anz[j]. 
        IF j = 2 THEN 
        DO: 
            IF mm LE 2 THEN 
            DO: 
                IF (yy MODULO 4) = 0 THEN tmp-list[i] = 29. 
            END. 
            ELSE 
            DO: 
                IF ((yy + 1) MODULO 4) = 0 THEN tmp-list[i] = 29. 
            END. 
        END. 
    END. 

    DEFINE VARIABLE d2 AS DATE.
    DEFINE VARIABLE tmp-yy AS INTEGER.                          /* Rulita 221124 | Fixing for serverless */

    tmp-yy = yy + 1. 

    curr-date = DATE(mm, 1, yy). 
    to-date = DATE(mm, 1, tmp-yy) - 1. 
    
    IF curr-date GE ci-date THEN from-date = curr-date. 
    ELSE from-date = ci-date. 
    
    IF to-date LT (ci-date - 1) THEN datum2 = to-date. 
    ELSE datum2 = ci-date - 1. 

    
    /*ft 30/01/15*/
    IF curr-date LT ci-date THEN
    DO:
        FOR EACH zkstat WHERE zkstat.datum GE curr-date AND zkstat.datum LE datum2 NO-LOCK:
            datum = zkstat.datum.
            j = MONTH(datum) - mm + 1. 
            IF j LE 0 THEN j = j + 12. 
            tmp-i[j] = 1.
            IF MONTH(zkstat.datum) =  MONTH(datum2) THEN tmp-i[j] = 2.
            FIND FIRST r2-list WHERE r2-list.tag = 34 NO-LOCK NO-ERROR.
            IF AVAILABLE r2-list THEN r2-list.room[j] = r2-list.room[j] + zkstat.anz100.
            
        END.
    END.
  
    /**/
    DO i = 1 TO 12:
        IF tmp-i[i] = 0 THEN
            r2-list.room[i] = tot-room * tmp-list[i]. 
        IF tmp-i[i] = 2 THEN
            r2-list.room[i] = r2-list.room[i] + (tot-room * (tmp-list[i] - DAY(datum2))).
    END.
  
    /*DS 120419 - count ooo room*/
    /*datum3 = curr-date + 365.*/
    IF curr-date LT ci-date THEN
    DO:
        FOR EACH zinrstat WHERE zinrstat.datum GE curr-date
            AND zinrstat.datum LE datum2
            AND zinrstat.zinr = "ooo" NO-LOCK:
          
            datum = zinrstat.datum.
            j = MONTH(datum) - mm + 1. 
          
            IF j LE 0 THEN j = j + 12.
            tmp-i[j] = 1.
          
            IF MONTH(zinrstat.datum) =  MONTH(datum3) THEN tmp-i[j] = 2.
                         
            FIND FIRST r6-list WHERE r6-list.tag = 38 NO-LOCK NO-ERROR.
            IF AVAILABLE r6-list THEN r6-list.room[j] = (r6-list.room[j] + zinrstat.zimmeranz).
        END.

        DO loop-date = from-date TO to-date:
            ASSIGN ooo-room = 0.
            FOR EACH outorder WHERE outorder.gespstart LE loop-date
                AND outorder.gespende GE loop-date  AND outorder.betriebsnr LE 1 NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping NO-LOCK: 
                ooo-room = ooo-room + 1.
            END.

            j = MONTH(loop-date) - mm + 1. 
          
            IF j LE 0 THEN j = j + 12.
            tmp-i[j] = 1.
          
            FIND FIRST r6-list WHERE r6-list.tag = 38 NO-LOCK NO-ERROR.
            IF AVAILABLE r6-list THEN DO:
                r6-list.room[j] = (r6-list.room[j] + ooo-room).
            END.
        END.

    END.
    ELSE
    DO:
        /*
        FOR EACH outorder WHERE NOT (outorder.gespstart GT to-date) 
            AND NOT (outorder.gespende LE from-date):
            ooo-room = ooo-room + 1.    
        END.
        FIND FIRST r6-list WHERE r6-list.tag = 38 NO-LOCK NO-ERROR.
        IF AVAILABLE r6-list THEN
            r6-list.room[j] = (r6-list.room[j] + ooo-room). */

        DO loop-date = from-date TO to-date:
            ASSIGN ooo-room = 0.
            FOR EACH outorder WHERE outorder.gespstart LE loop-date
                AND outorder.gespende GE loop-date  AND outorder.betriebsnr LE 1 NO-LOCK, 
            FIRST zimmer WHERE zimmer.zinr = outorder.zinr AND zimmer.sleeping NO-LOCK: 
                ooo-room = ooo-room + 1.
            END.

            j = MONTH(loop-date) - mm + 1. 
          
            IF j LE 0 THEN j = j + 12.
            tmp-i[j] = 1.
          
            FIND FIRST r6-list WHERE r6-list.tag = 38 NO-LOCK NO-ERROR.
            IF AVAILABLE r6-list THEN DO:
                r6-list.room[j] = (r6-list.room[j] + ooo-room).
            END.
        END.
    END.
    /*END DS*/
  
    IF curr-date LT ci-date THEN 
    DO:
        FOR EACH genstat WHERE genstat.datum GE curr-date AND genstat.datum LE datum2
            AND genstat.zinr NE "" AND genstat.res-logic[2] EQ YES NO-LOCK:
            do-it = YES. 
            rmsharer = (genstat.resstatus = 13).
            
            IF vhp-limited THEN do-it = YES.
            DO: 
                IF genstat.res-date[1] LT genstat.datum
                    AND genstat.res-date[2] = genstat.datum 
                    AND genstat.resstatus = 8 AND genstat.logis = 0 THEN do-it = NO.
            END.
            IF do-it AND NOT all-segm THEN 
            DO: 
                FIND FIRST segm1-list WHERE segm1-list.segm = genstat.segmentcode 
                  AND segm1-list.selected NO-LOCK NO-ERROR. 
                do-it = AVAILABLE segm1-list. 
            END.
        
            IF do-it AND NOT all-argt THEN 
            DO: 
                FIND FIRST argt-list WHERE argt-list.argt = genstat.argt 
                  AND argt-list.selected NO-LOCK NO-ERROR. 
                do-it = AVAILABLE argt-list.
            END. 
        
            IF do-it AND NOT all-zikat THEN 
            DO:
                FIND FIRST zikat-list WHERE zikat-list.zikatnr = genstat.zikatnr 
                  AND zikat-list.selected NO-LOCK NO-ERROR.
                do-it = AVAILABLE zikat-list.
            END. 
            
            IF do-it THEN
            DO: 
                datum = genstat.datum. 
                j = MONTH(datum) - mm + 1. 
                IF j LE 0 THEN j = j + 12. 
                FIND FIRST room-list WHERE room-list.tag = day(datum).
                
                IF roompaxselect = 0 THEN 
                DO: 
                    IF nationselect = "" THEN 
                    DO:
                        IF NOT rmSharer THEN
                            ASSIGN
                                room-list.room[j] = room-list.room[j] + 1
                                room-list.pax[j]  = room-list.pax[j]  + genstat.erwachs + genstat.kind1 + 
                                                    genstat.kind2 + genstat.gratis + genstat.kind3.
                        IF show-rmrev THEN
                        DO:
                            rev-array[j] = rev-array[j] + genstat.logis.
                        END.
                    END.
                    ELSE
                    DO:
                        IF NOT rmSharer THEN
                            ASSIGN
                                room-list.room[j] = room-list.room[j] + 1 
                                room-list.pax[j]  = room-list.pax[j] + genstat.erwachs + 
                                                    genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3 .
                    END.
                END.
                ELSE 
                DO:
                    IF nationselect = "" THEN 
                    DO:
                        IF NOT rmSharer THEN
                        DO: 
                            ASSIGN
                                room-list.pax[j]  = room-list.pax[j]  + genstat.erwachs + genstat.kind1 + 
                                                    genstat.kind2 + genstat.gratis + genstat.kind3
                                room-list.room[j] = room-list.room[j] + genstat.erwachs + genstat.kind1 + 
                                                    genstat.kind2 + genstat.gratis + genstat.kind3.
                        END.
                        IF show-rmrev THEN
                        DO:
                            rev-array[j] = rev-array[j] + genstat.logis.
                        END.
                    END.
                    ELSE
                    DO:
                        IF NOT rmSharer THEN
                        ASSIGN
                            room-list.pax[j]  = room-list.pax[j]  + genstat.erwachs + genstat.kind1 + 
                                                genstat.kind2 + genstat.gratis + genstat.kind3
                            room-list.room[j] = room-list.room[j] + genstat.erwachs + genstat.kind1 + 
                                                genstat.kind2 + genstat.gratis + genstat.kind3.
                    END.
                END.
            END.
        END.
    END. /*curr-date LT ci-date*/


    /*FT IF roompaxselect = 0 THEN 
    DO i = 1 TO 12: 
      r2-list.room[i] = tot-room * tmp-list[i]. 
    END.*/ 
    last-resnr = -1. 
    IF to-date GE ci-date THEN 
    DO:
        FOR EACH res-line WHERE ((res-line.resstatus LE 13 
            AND res-line.resstatus NE 4
            AND res-line.resstatus NE 8
            AND res-line.resstatus NE 9 
            AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.active-flag LE 1 
            /*AND NOT (res-line.ankunft GT to-date) FT serverless*/
            AND res-line.ankunft LE to-date
            /*AND NOT (res-line.abreise LT d2)FT serverless*/
            AND res-line.abreise GE from-date)) OR
            ((res-line.active-flag = 2 AND res-line.resstatus = 8
            AND res-line.ankunft = ci-date AND res-line.abreise = ci-date) OR 
            (res-line.active-flag = 2 AND res-line.resstatus = 8 
            AND res-line.abreise = ci-date))
            AND res-line.gastnr GT 0 
            AND res-line.l-zuordnung[3] = 0 NO-LOCK 
            USE-INDEX gnrank_ix BY res-line.resnr:

            FIND FIRST guest NO-LOCK WHERE guest.gastnr = res-line.gastnrmember NO-ERROR. /*ozhan added */
            IF nationselect <> "" THEN IF NOT AVAILABLE guest OR nationselect <> guest.nation1 THEN NEXT.
            
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
            IF last-resnr NE res-line.resnr THEN 
            DO: 
                FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
                last-resnr = res-line.resnr. 
            END. 
            do-it = YES. 
            IF NOT incl-tent  
                AND res-line.resstatus = 3 THEN do-it = NO. 
            IF NOT incl-wait  
                AND res-line.resstatus = 4 THEN do-it = NO. 

            IF do-it AND res-line.resstatus = 8 
                AND res-line.ankunft = ci-date AND res-line.abreise = ci-date THEN
            DO:              
              FIND FIRST arrangement WHERE arrangement.arrangement 
                =  res-line.arrangement NO-LOCK NO-ERROR. 
              FIND FIRST bill-line WHERE bill-line.departement = 0
                AND bill-line.artnr = arrangement.argt-artikelnr
                AND bill-line.bill-datum = ci-date
                AND bill-line.massnr = res-line.resnr
                AND bill-line.billin-nr = res-line.reslinnr
                USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
              do-it = AVAILABLE bill-line.
            END.
            
            /*IF AVAILABLE zimmer AND NOT zimmer.sleeping THEN do-it = NO.*/ 
            IF do-it AND AVAILABLE zimmer THEN 
            DO: 
              FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
                AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
              IF zimmer.sleeping THEN 
              DO: 
                  IF AVAILABLE queasy AND queasy.number3 EQ res-line.gastnr THEN 
                    do-it = NO. 
              END. 
              ELSE 
              DO: 
                IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN . 
                ELSE do-it = NO. 
              END. 
            END. 

            IF do-it AND NOT all-segm THEN 
            DO: 
                FIND FIRST segm1-list WHERE segm1-list.segm = reservation.segmentcode 
                    AND segm1-list.selected NO-LOCK NO-ERROR. 
                do-it = AVAILABLE segm1-list. 
            END. 
        
            IF do-it AND NOT all-argt THEN 
            DO: 
                FIND FIRST argt-list WHERE argt-list.argt = res-line.arrangement 
                    AND argt-list.selected NO-LOCK NO-ERROR. 
                do-it = AVAILABLE argt-list. 
            END. 
            
            IF do-it AND NOT all-zikat THEN 
            DO: 
                FIND FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr 
                    AND zikat-list.selected NO-LOCK NO-ERROR. 
                do-it = AVAILABLE zikat-list. 
            END. 
        
            IF do-it AND (res-line.kontignr LT 0) THEN 
            DO:
                IF all-segm THEN do-it = YES. 
                ELSE 
                DO: 
                    FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK. 
                    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                        AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
                    IF NOT AVAILABLE guestseg THEN 
                        FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                            NO-LOCK NO-ERROR. 
                    IF AVAILABLE guestseg THEN 
                    DO: 
                        FIND FIRST segm1-list WHERE segm1-list.segm = guestseg.segmentcode 
                            AND segm1-list.selected NO-LOCK NO-ERROR. 
                        do-it = NOT AVAILABLE segm1-list. 
                    END. 
                END. 
            END.
        
            IF do-it THEN 
            DO: 
                /*IF res-line.ankunft GT from-date THEN datum1 = res-line.ankunft.
                ELSE datum1 = from-date.
                IF res-line.abreise LT to-date THEN datum2 = res-line.abreise.
                ELSE datum2 = to-date.*/


                /*geral compare with monthly D5F9E2 dicomment karna rmnight tidaksesuai*/
                /*datum1 = from-date.
                IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft.
                datum2 = to-date.
                IF res-line.abreise LE datum2 THEN datum2 = res-line.abreise.*/

                IF res-line.ankunft Gt from-date THEN datum1 = res-line.ankunft.
                ELSE datum1 = from-date.
                
                IF res-line.ankunft = res-line.abreise THEN ASSIGN datum2 = res-line.abreise.
                ELSE DO:                
                    IF res-line.abreise LT to-date THEN datum2 = res-line.abreise - 1.
                    ELSE datum2 = to-date.
                END .

                
                DO datum = datum1 TO datum2: 
                   
                    pax = res-line.erwachs. 
                    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                        AND reslin-queasy.resnr = res-line.resnr 
                        AND reslin-queasy.reslinnr = res-line.reslinnr 
                        AND reslin-queasy.date1 LE datum 
                        AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
                    IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
                        pax = reslin-queasy.number3. 
                    j = MONTH(datum) - mm + 1. 
                    
                    IF j LE 0 THEN j = j + 12. 
        
                    IF res-line.resstatus NE 3 AND res-line.resstatus NE 4 THEN 
                        FIND FIRST room-list WHERE room-list.tag = day(datum) 
                            AND room-list.rstat = 0. 
                    ELSE 
                        FIND FIRST room-list WHERE room-list.tag = day(datum) 
                            AND room-list.rstat = 1. 
                    
                    IF roompaxselect = 0 AND res-line.resstatus NE 11
                       AND res-line.resstatus NE 13 AND NOT res-line.zimmerfix THEN 
                    DO:  
                       room-list.room[j] = room-list.room[j] + res-line.zimmeranz. 
                       room-list.pax[j] = room-list.pax[j] + (pax + res-line.kind1 + res-line.kind2 
                         + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz.
                       RUN assign-it(j, datum, from-date). /*geral add from-date D5F9E2*/
                    END.
                    ELSE IF roompaxselect NE 0 THEN 
                    DO:
                        room-list.room[j] = room-list.room[j] + (pax + res-line.kind1 + res-line.kind2 
                            + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz. 
                        room-list.pax[j] = room-list.pax[j] + (pax + res-line.kind1 + res-line.kind2 
                            + res-line.l-zuordnung[4] + res-line.gratis) * res-line.zimmeranz. 
                        RUN assign-it(j,datum, from-date). /*geral add from-date D5F9E2*/
                    END.
                END. 
            END. 
        END. 
    END.

    IF incl-glob THEN
    DO:
        DO datum = from-date TO to-date: 
            j = MONTH(datum) - mm + 1. 
            IF j LE 0 THEN j = j + 12. 
            FIND FIRST room-list WHERE room-list.tag = day(datum). 
            FOR EACH kontline WHERE kontline.betriebsnr = 1 
                AND kontline.ankunft LE datum AND kontline.abreise GE datum 
                AND kontline.kontstat = 1 NO-LOCK: 
            
                FIND FIRST guest NO-LOCK WHERE guest.gastnr = kontline.gastnr NO-ERROR. /*ozhan added */
                IF nationselect <> "" THEN IF NOT AVAILABLE guest OR nationselect <> guest.nation1 THEN NEXT.
                  
                do-it = YES. 
                IF do-it AND NOT all-argt THEN 
                DO: 
                    FIND FIRST argt-list WHERE argt-list.argt = kontline.arrangement 
                        AND argt-list.selected NO-LOCK NO-ERROR. 
                    do-it = AVAILABLE argt-list. 
                END. 
                IF do-it AND NOT all-zikat THEN 
                DO: 
                    FIND FIRST zikat-list WHERE zikat-list.zikatnr = kontline.zikatnr 
                        AND zikat-list.selected NO-LOCK NO-ERROR. 
                    do-it = AVAILABLE zikat-list. 
                END. 
                IF do-it AND NOT all-segm THEN 
                DO: 
                    FIND FIRST guest WHERE guest.gastnr = kontline.gastnr NO-LOCK. 
                    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                        AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
                    IF NOT AVAILABLE guestseg THEN 
                        FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
                            NO-LOCK NO-ERROR. 
                    IF AVAILABLE guestseg THEN 
                    DO: 
                        FIND FIRST segm1-list WHERE segm1-list.segm = guestseg.segmentcode 
                            AND segm1-list.selected NO-LOCK NO-ERROR. 
                        do-it = AVAILABLE segm1-list. 
                    END. 
                END. 
      
                IF do-it THEN 
                DO: 
                    IF roompaxselect = 0 THEN 
                    DO:
                        room-list.room[j] = room-list.room[j] + kontline.zimmeranz. 
                        /*RUN assign-it(j).*/
                    END.
                    ELSE IF roompaxselect NE 0 THEN 
                    DO: 
                        room-list.room[j] = room-list.room[j] + (kontline.erwachs 
                                            + kontline.kind1 /*+ kontline.kind2*/) * kontline.zimmeranz. 
                        room-list.pax[j]  = room-list.pax[j] + (kontline.erwachs 
                                            + kontline.kind1 /*+ kontline.kind2*/) * kontline.zimmeranz. 
                        /*IF show-rmrev THEN
                        DO:
                            lodging = res-line.zipreis. /* &&& */
                            RUN calculate-zipreis(datum, INPUT-OUTPUT lodging).
                            rev-array[j] = rev-array[j] + lodging.
                        END.*/
                    END.
                END. /*do-it*/
            END. 
            /*&&&&18 Feb 09*/
            FOR EACH res-line WHERE res-line.active-flag LE 1 
                AND res-line.resstatus LE 13 AND res-line.resstatus NE 3 
                AND res-line.resstatus NE 4  AND res-line.resstatus NE 12
                AND res-line.ankunft LE datum AND res-line.abreise GT datum 
                AND res-line.kontignr LT 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
                ASSIGN room-list.room[j] = room-list.room[j] - res-line.zimmeranz.
                
                FIND FIRST kbuff WHERE kbuff.gastnr = res-line.gastnr 
                    AND kbuff.ankunft EQ datum 
                    AND kbuff.zikatnr EQ res-line.zikatnr 
                    AND kbuff.betriebsnr = 1 NO-LOCK NO-ERROR.
                IF AVAILABLE kbuff THEN room-list.pax[j] = room-list.pax[j] - 
                    (kbuff.erwachs + kbuff.kind1) * res-line.zimmeranz.
                ELSE room-list.pax[j] = room-list.pax[j] - res-line.erwachs * res-line.zimmeranz.
            END.
            /*&&&&*/
        END.
    END. 

    FOR EACH room-list WHERE room-list.tag LE 31: 
        DO i = 1 TO 12: 
            IF room-list.room[i] NE 0 OR room-list.tag LE 28 THEN 
                room-list.coom[i] = STRING(room-list.room[i],"->>,>>9"). 
            IF roompaxselect = 0 THEN 
                r1-list.room[i] = r1-list.room[i] + room-list.room[i]. 
            r4-list.room[i] = r4-list.room[i] + room-list.pax[i]. 
            IF incl-tent  AND room-list.rstat = 1 
                THEN r5-list.room[i] = r5-list.room[i] + room-list.room[i]. 
        END. 
    END. 

    FOR EACH room-list WHERE room-list.tag GE 29 AND room-list.tag LE 31: 
        DO i = 1 TO 12: 
            IF room-list.room[i] = 0 AND room-list.tag LE tmp-list[i] THEN 
                room-list.coom[i] = "      0". 
        END. 
    END. 

    DO i = 1 TO 12: 
        IF roompaxselect = 0 THEN 
        DO: 
            r1-list.coom[i] = STRING(r1-list.room[i],"->>,>>9"). 
            IF r2-list.room[i] NE 0 AND r2-list.room[i] NE ? THEN 
            DO: 
                r2-list.room[i] = r2-list.room[i] /*FT 011014- r1-list.room[i]. */.
                r2-list.coom[i] = STRING(r2-list.room[i],"->>,>>9"). 
                
                IF r2-list.room[i] NE 0 AND r2-list.room[i] NE ? THEN                               /* Rulita 221124 | Fixing for serverless */
                DO:
                    r3-list.coom[i] = STRING(r1-list.room[i] / r2-list.room[i] * 100, "->>9.99"). 
                END.
                
                IF incl-tent THEN 
                DO:
                    IF r2-list.room[i] NE 0 AND r2-list.room[i] NE ? THEN                               /* Rulita 221124 | Fixing for serverless */
                    DO:
                        r5-list.coom[i] = STRING(r5-list.room[i] / r2-list.room[i] * 100, "->>9.99"). 
                    END.
                    
                END.
                
                /*DS 120419 - NEW SALEABLE ROOM*/
                IF r6-list.room[i] NE 0 AND r6-list.room[i] NE ? THEN                                   /* Rulita 231124 | Fixing for serverless */
                DO:
                    IF (r2-list.room[i] - r6-list.room[i]) NE 0 AND (r2-list.room[i] - r6-list.room[i]) NE ? THEN      /* Rulita 131224 | Fixing serverless issue git 135 */
                    DO: 
                        r6-list.coom[i] = STRING(r2-list.room[i] - r6-list.room[i], "->>,>>9").
                        room-ooo[i]     = r1-list.room[i] / (r2-list.room[i] - r6-list.room[i]) * 100.
                        r7-list.coom[i] = STRING(room-ooo[i], "->>9.99").
                    END.
                    ELSE
                    DO:
                        r6-list.coom[i] = STRING(r2-list.room[i] - r6-list.room[i], "->>,>>9").
                        room-ooo[i]     = 0.
                        r7-list.coom[i] = STRING(room-ooo[i], "->>9.99").
                    END.
                END.
                /*END DS*/
            END. 
            /*r2-list.room[i] = r2-list.room[i] - r1-list.room[i]. 
            r2-list.coom[i] = STRING(r2-list.room[i],"->>,>>9"). */
        END. 
        r4-list.coom[i] = STRING(r4-list.room[i],"->>,>>9"). 
    END. 
    /*DS*/ 
    /*
    FIND FIRST r1-list WHERE r1-list.tag = 33. /*Room Occupied*/
    FIND FIRST r2-list WHERE r2-list.tag = 34. /*Saleable Rooms*/
    FIND FIRST r3-list WHERE r3-list.tag = 35. /*Occupancy (%)*/
    FIND FIRST r4-list WHERE r4-list.tag = 36. /*Person Occupied*/
    FIND FIRST r5-list WHERE r5-list.tag = 37. /*Tentative-Occ %*/
    FIND FIRST r6-list WHERE r6-list.tag = 38. /*SaleRoom w/ OOO*/
    FIND FIRST r7-list WHERE r7-list.tag = 39. /*Occupancy w/ OOO(%)*/
    FIND FIRST r8-list WHERE r7-list.tag = 39. /*OOO*/
    */
END. 

PROCEDURE calculate-zipreis: 
DEFINE INPUT PARAMETER        bill-date AS DATE.
DEFINE INPUT-OUTPUT PARAMETER roomrate  AS DECIMAL. 
DEFINE VARIABLE rm-rate                 AS DECIMAL. 
DEFINE VARIABLE add-it                  AS LOGICAL INITIAL NO. 
DEFINE VARIABLE qty                     AS INTEGER. 
DEFINE VARIABLE qty2                    AS INTEGER. 
DEFINE VARIABLE it-exist                AS LOGICAL INITIAL NO. /* YES->usr prog exists */ 
DEFINE VARIABLE argt-defined            AS LOGICAL. 
DEFINE VARIABLE exrate1                 AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2                     AS DECIMAL INITIAL 1. 
DEFINE VARIABLE child1                  AS INTEGER              NO-UNDO. 
DEFINE VARIABLE fix-rate                AS LOGICAL INITIAL NO   NO-UNDO. 
DEFINE VARIABLE post-date               AS DATE                 NO-UNDO. 
DEFINE VARIABLE curr-zikatnr            AS INTEGER              NO-UNDO. 
DEFINE VARIABLE w-day                   AS INTEGER              NO-UNDO. 
DEFINE VARIABLE ebdisc-flag             AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag             AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found              AS LOGICAL              NO-UNDO.
DEFINE VARIABLE early-flag              AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag              AS LOGICAL              NO-UNDO.

DEFINE VARIABLE wd-array                AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

DEFINE BUFFER w1                FOR waehrung. 
  
    qty2 = res-line.zimmeranz.

    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK. 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
    FIND FIRST arrangement WHERE arrangement.arrangement 
        = res-line.arrangement NO-LOCK. 
   
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        AND bill-date GE reslin-queasy.date1 
        AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN /* fixed rate */
    DO: 
        roomrate = reslin-queasy.deci1. 
        RUN cal-lodging(bill-date, INPUT-OUTPUT roomrate).
    END. 
 
    FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest-pr THEN 
    DO: 
        contcode = guest-pr.CODE.
        ct = res-line.zimmer-wunsch.
        IF ct MATCHES("*$CODE$*") THEN
        DO:
            ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
            contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
        END.
        
        post-date = bill-date. 
        FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = 
            res-line.reserve-int NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy AND queasy.logi3 THEN post-date = res-line.ankunft. 
        
        ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*").
        kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").
        IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
        ELSE curr-zikatnr = res-line.zikatnr. 
        
        RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
            res-line.reslinnr, contcode, ?, post-date, res-line.ankunft,
            res-line.abreise, res-line.reserve-int, arrangement.argtnr,
            curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
            res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
            OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
        roomrate = rm-rate. 
        RUN cal-lodging(bill-date, INPUT-OUTPUT roomrate).
        RETURN. 
    END. /* IF AVAILABLE guest-pr */ 

    ELSE /* publish rate */ 
    DO: 
        DEFINE VARIABLE publish-rate AS DECIMAL INITIAL 0 NO-UNDO. 
        w-day = wd-array[WEEKDAY(bill-date - 1)]. 
        FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
            AND katpreis.argtnr = arrangement.argtnr 
            AND katpreis.startperiode LE (bill-date - 1) 
            AND katpreis.endperiode GE (bill-date - 1) 
            AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE katpreis THEN 
            FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                AND katpreis.argtnr = arrangement.argtnr 
                AND katpreis.startperiode LE (bill-date - 1) 
                AND katpreis.endperiode GE (bill-date - 1) 
                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE katpreis THEN RETURN. 
        IF res-line.zipreis NE get-rackrate(res-line.erwachs, 
            res-line.kind1, res-line.kind2) THEN RETURN. 
        
        w-day = wd-array[WEEKDAY(bill-date)]. 
        FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
            AND katpreis.argtnr = arrangement.argtnr 
            AND katpreis.startperiode LE bill-date 
            AND katpreis.endperiode GE bill-date 
            AND katpreis.betriebsnr = w-day NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE katpreis THEN 
            FIND FIRST katpreis WHERE katpreis.zikat = curr-zikatnr 
                AND katpreis.argtnr = arrangement.argtnr 
                AND katpreis.startperiode LE bill-date 
                AND katpreis.endperiode GE bill-date 
                AND katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE katpreis THEN 
        DO: 
            publish-rate = get-rackrate(res-line.erwachs, res-line.kind1, 
              res-line.kind2). 
            IF publish-rate = 0 THEN RETURN. 
            roomrate = publish-rate.                          
            RUN cal-lodging(bill-date, INPUT-OUTPUT roomrate).
        END. 
        RUN cal-lodging(bill-date, INPUT-OUTPUT roomrate).
    END. 
END.  

PROCEDURE cal-lodging:
DEFINE INPUT PARAMETER bill-date      AS DATE.
DEFINE INPUT-OUTPUT PARAMETER zipreis AS DECIMAL.
DEFINE VARIABLE rate                  AS DECIMAL NO-UNDO.
DEFINE VARIABLE lodg-betrag           AS DECIMAL NO-UNDO.
DEFINE VARIABLE service               AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE vat                   AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE vat2                  AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE fact                  AS DECIMAL INITIAL 1 NO-UNDO.
DEFINE VARIABLE frate                 AS DECIMAL           NO-UNDO.
DEFINE VARIABLE argt-betrag           AS DECIMAL           NO-UNDO.
DEFINE VARIABLE ex-rate               AS DECIMAL           NO-UNDO INIT 1.
DEFINE VARIABLE qty2                  AS INT NO-UNDO.

    IF zipreis = 0 THEN RETURN.
    rate = zipreis. 
    qty2 = res-line.zimmeranz.

    IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
    ELSE 
    DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN frate = waehrung.ankauf / waehrung.einheit. 
    END. 
  
    FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
        AND artikel.departement = 0 NO-LOCK. 
/*
/*    IF rm-serv THEN  */ 
  FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN service = htparam.fdecimal / 100. 

/*    IF rm-vat THEN   */ 
  FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK NO-ERROR. 
  IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN vat = htparam.fdecimal / 100. 
  
  FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
  IF htparam.flogical THEN vat = vat + vat * service. 
  vat = ROUND(vat, 2). 
  
  fact = 1 + service + vat.
*/

/* SY AUG 13 2017 */
    RUN calc-servtaxesbl.p(1, artikel.artnr, artikel.departement,
        bill-date, OUTPUT service, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
    ASSIGN vat = vat + vat2.
    
    lodg-betrag = rate * frate. 
    FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
        AND NOT argt-line.kind2 NO-LOCK: 
        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
            AND artikel.departement = argt-line.departement NO-LOCK. 
        RUN argt-betrag(bill-date, OUTPUT argt-betrag, OUTPUT ex-rate). 
        lodg-betrag = lodg-betrag - argt-betrag * ex-rate. 
    END. 
    
    IF NOT rm-serv THEN  /* rate includes tax AND service */ 
        lodg-betrag = lodg-betrag / fact. 
    
    zipreis = lodg-betrag.
END.

PROCEDURE argt-betrag:
DEFINE INPUT  PARAMETER bill-date AS DATE.
DEFINE OUTPUT PARAMETER betrag    AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER ex-rate   AS DECIMAL INITIAL 1. 
                                  
DEFINE VARIABLE add-it            AS LOGICAL INITIAL NO. 
DEFINE VARIABLE marknr            AS INTEGER. 
DEFINE VARIABLE argt-defined      AS LOGICAL INITIAL NO. 
DEFINE VARIABLE qty               AS INTEGER. 
DEFINE VARIABLE exrate1           AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2               AS DECIMAL INITIAL 1. 
DEFINE BUFFER w1                  FOR waehrung. 
  
    IF argt-line.vt-percnt = 0 THEN 
    DO: 
        IF argt-line.betriebsnr = 0 THEN qty = res-line.erwachs. 
        ELSE qty = argt-line.betriebsnr. 
    END. 
    ELSE IF argt-line.vt-percnt = 1 THEN qty = res-line.kind1. 
    ELSE IF argt-line.vt-percnt = 2 THEN qty = res-line.kind2. 
    IF qty = 0 THEN RETURN. 
    
    IF argt-line.fakt-modus = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 2 THEN 
    DO: 
        IF res-line.ankunft EQ bill-date THEN add-it = YES. 
    END. 
    ELSE IF argt-line.fakt-modus = 3 THEN 
    DO: 
        IF (res-line.ankunft + 1) EQ bill-date THEN add-it = YES. 
    END. 
    ELSE IF argt-line.fakt-modus = 4 AND day(bill-date) = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 5 AND day(bill-date + 1) = 1 THEN add-it = YES. 
    ELSE IF argt-line.fakt-modus = 6 THEN 
    DO: 
        IF (res-line.ankunft + (argt-line.intervall - 1)) GE bill-date 
        THEN add-it = YES. 
    END. 
    
    IF NOT add-it THEN RETURN. 
    
    marknr = res-line.reserve-int. 
 
/* AdHoc Reservation */ 
    FIND FIRST reslin-queasy WHERE key = "fargt-line" 
        AND reslin-queasy.char1    = "" 
        AND reslin-queasy.resnr    = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr 
        AND reslin-queasy.number1  = argt-line.departement 
        AND reslin-queasy.number2  = argt-line.argtnr 
        AND reslin-queasy.number3  = argt-line.argt-artnr 
        AND bill-date GE reslin-queasy.date1 
        AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN   /* AdHoc Ventillation */ 
    DO: 
        argt-defined = YES. 
        betrag = reslin-queasy.deci1 * qty. 
        RUN get-exrate1(OUTPUT ex-rate). 
        RETURN. 
    END. 
 
/*  reservation under contract rates */ 

    IF AVAILABLE guest-pr AND marknr NE 0 AND NOT argt-defined THEN 
    DO: 
        FIND FIRST reslin-queasy WHERE key = "argt-line" 
            AND reslin-queasy.char1    = contcode 
            AND reslin-queasy.number1  = marknr 
            AND reslin-queasy.number2  =  argt-line.argtnr 
            AND reslin-queasy.reslinnr = res-line.zikatnr 
            AND reslin-queasy.number3  = argt-line.argt-artnr 
            AND reslin-queasy.resnr    = argt-line.departement 
            AND bill-date GE reslin-queasy.date1 
            AND bill-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        
        IF AVAILABLE reslin-queasy THEN 
        DO: 
            betrag = reslin-queasy.deci1 * qty. 
            RUN get-exrate2(marknr, OUTPUT ex-rate). 
            RETURN. 
        END. 
    END. 

/* other reservations */ 
    betrag = argt-line.betrag * qty. 
    RUN get-exrate3(OUTPUT ex-rate). 
END.

PROCEDURE get-exrate1: 
DEF OUTPUT PARAM ex-rate AS DECIMAL INITIAL 1.
    IF reservation.insurance AND res-line.reserve-dec NE 0 THEN 
        ex-rate = res-line.reserve-dec. 
    ELSE IF res-line.betriebsnr NE 0 THEN 
    DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
    END. 
    ELSE IF res-line.adrflag OR NOT foreign-rate THEN 
    DO: 
        FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
        FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
    END. 
    ELSE 
    DO: 
        FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
        FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
    END. 
END. 
 
PROCEDURE get-exrate2: 
DEF INPUT  PARAM marknr  AS INTEGER.
DEF OUTPUT PARAM ex-rate AS DECIMAL INITIAL 1.
    IF reservation.insurance AND res-line.reserve-dec NE 0 THEN 
    DO: 
        ex-rate = res-line.reserve-dec. 
        RETURN. 
    END. 
    FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = marknr 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") THEN 
    FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = contcode 
        NO-LOCK. 
    IF queasy.KEY = 18 THEN FIND FIRST waehrung WHERE 
        waehrung.wabkurz = queasy.char3 NO-LOCK NO-ERROR. 
    ELSE
    DO:
        IF queasy.number1 NE 0 THEN FIND FIRST waehrung WHERE 
            waehrung.waehrungsnr = queasy.number1 NO-LOCK NO-ERROR. 
        ELSE IF queasy.logi1 /* local rate */ OR NOT foreign-rate THEN 
        DO: 
            FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
            FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK 
                NO-ERROR. 
        END. 
        ELSE 
        DO: 
            FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
            FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK 
                NO-ERROR. 
        END.
    END.
    IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
END. 
 
PROCEDURE get-exrate3: 
DEFINE OUTPUT PARAM ex-rate AS DECIMAL INITIAL 1.
DEFINE VARIABLE local-nr    AS INTEGER. 
DEFINE VARIABLE foreign-nr  AS INTEGER. 
    IF arrangement.betriebsnr NE 0 THEN 
    DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN 
        DO: 
            ex-rate = waehrung.ankauf / waehrung.einheit. 
            RETURN. 
        END. 
    END. 
    IF foreign-rate THEN 
    DO: 
        FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
        FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
    END. 
    ELSE 
    DO: 
        FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
        FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN ex-rate = waehrung.ankauf / waehrung.einheit. 
    END. 
END. 

PROCEDURE create-rev:
    /*
    mm = INTEGER(SUBSTR(from-month,1,2)). 
  yy = INTEGER(SUBSTR(from-month,3,4)). 
 
  dlist = "               ". 
 
  DO i = 1 TO 12: 
    curr-day = mm. 
    datum = DATE(mm, 1, yy). 
    datum1 = SUBSTR(STRING(datum),1,5). 
    */
    DEFINE VARIABLE i       AS INTEGER NO-UNDO.
    DEFINE VARIABLE mm      AS INTEGER NO-UNDO.
    DEFINE VARIABLE yy      AS INTEGER NO-UNDO.
    DEFINE VARIABLE datum   AS DATE.
    DEFINE VARIABLE datum1  AS CHAR FORMAT "x(5)".

    mm = INTEGER(SUBSTR(from-month,1,2)). 
    yy = INTEGER(SUBSTR(from-month,3,4)). 

    FOR EACH rev-list:
        DELETE rev-list.
    END.

    curr-day = mm - 1.
    CREATE rev-list.
    bezeich = "Period".
    DO i = 1 TO 6:
        curr-day = curr-day + 1.
        IF curr-day = 13 THEN curr-day = 1.
        rev-list.str1[i] = "         " + STRING(week-list[curr-day], "x(5)").
        /*rev-list.str = rev-list.str + /*STRING(datum1) + "!" + */
             "         " + STRING(week-list[curr-day], "x(5)").*/
    END.

    CREATE rev-list.
    bezeich = "Room Revenue".
    DO i = 1 TO 6:
        ASSIGN 
        /* rev-list.str[i] = STRING(rev-array[i], "->,>>>,>>>,>>9"). */  
        rev-list.str1[i] = STRING(rev-array[i], "->,>>>,>>>,>>9").               /* Rulita 131224 | Fixing serverless issue git 135 */
    END.

    CREATE rev-list.
    bezeich = "Period".
    DO i = 1 TO 6:
        curr-day = curr-day + 1.
        IF curr-day = 13 THEN
            curr-day = 1.
        rev-list.str1[i] = "         " + STRING(week-list[curr-day], "x(5)").
    END.

    CREATE rev-list.
    bezeich = "Room Revenue".
    DO i = 1 TO 6:
        ASSIGN 
        rev-list.str1[i] = STRING(rev-array[i + 6], "->,>>>,>>>,>>9").
    END.
END.

PROCEDURE sum-rooms: 
    ASSIGN
        tot-room = 0
        inactive = 0.
    FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES NO-LOCK: 
        FOR EACH zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr NO-LOCK: 
            IF sleeping THEN tot-room = tot-room + 1. 
            ELSE inactive = inactive + 1. 
        END. 
    END.
END. 

/*MT
PROCEDURE print-txt:
    DEFINE VARIABLE t-occ AS INTEGER INITIAL 0. 
    DEFINE VARIABLE t-vac AS INTEGER INITIAL 0. 
    DEFINE buffer rm-list FOR room-list. 

    DEFINE VARIABLE str1 AS CHAR FORMAT "x(28)". 
    DEFINE VARIABLE str2 AS CHAR FORMAT "x(28)". 
    DEFINE VARIABLE str3 AS CHAR FORMAT "x(48)". 
 
    DEFINE VARIABLE st1 AS CHAR FORMAT "x(80)" NO-UNDO. 
    st1 = translateExtended( "Segments    :",lvCAREA,"") + " ". 
    DEFINE VARIABLE st2 AS CHAR FORMAT "x(80)" NO-UNDO. 
    st2 = translateExtended( "Arrangements:",lvCAREA,"") + " ". 
    DEFINE VARIABLE st3 AS CHAR FORMAT "x(80)" NO-UNDO. 
    st3 = translateExtended( "Room Types  :",lvCAREA,"") + " ". 

    IF all-segm THEN st1 = st1 + translateExtended( "ALL",lvCAREA,""). 
    ELSE 
    FOR EACH segm1-list WHERE segm1-list.selected: 
      st1 = st1 + SUBSTR(segm1-list.bezeich, 5, length(segm1-list.bezeich)) 
        + "; ". 
    END. 
 
    IF all-argt THEN st2 = st2 + translateExtended( "ALL",lvCAREA,""). 
    ELSE 
    FOR EACH argt-list WHERE argt-list.selected: 
        
      st2 = st2 + argt-list.argt + "; ". 
    END. 
 
    IF all-zikat THEN st3 = st3 + translateExtended( "ALL",lvCAREA,""). 
    ELSE 
    FOR EACH zikat-list WHERE zikat-list.selected: 
      st3 = st3 + zikat-list.kurzbez + "; ". 
    END. 
 
    mm = INTEGER(SUBSTR(from-month,1,2)). 
    yy = INTEGER(SUBSTR(from-month,3,4)). 

    curr-date = DATE(mm,1, yy).
    date1 = DATE(month(curr-date), 1, year(curr-date) + 1) - 1. 
    str1 = " " + STRING(curr-date) + " - " + STRING(date1). 
    str2 = "Date   : " + STRING(today) + "   " + STRING(time, "HH:MM:SS"). 
    IF roompaxselect = 0 THEN 
      str3 = translateExtended( "Annual Forecast of Room Occupancy",lvCAREA,""). 
    ELSE 
      str3 = translateExtended( "Annual Forecast of Persons Occupancy",lvCAREA,""). 
    CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait"). 
    PROCESS EVENTS. 
    FIND FIRST PRINTER WHERE printer.nr = printer-nr NO-LOCK. 
 
    datum = curr-date. 
    wlist = "               ". 
    DO i = 1 TO 12: 
      curr-day = month(datum). 
      DO j = 1 TO (8 - length(TRIM(week-list[curr-day]))): 
        wlist = wlist + " ". 
      END. 
      wlist= wlist + TRIM(week-list[curr-day]). 
      IF month(datum) LT 12 THEN 
        datum = DATE(month(datum) + 1, day(datum), year(datum)). 
      ELSE datum = DATE(1, day(datum), year(datum) + 1). 
    END. 
    
    IF txt-file NE "" THEN
        OUTPUT STREAM s1 TO VALUE(txt-file) page-size value(printer.pglen). 
    ELSE 
        OUTPUT STREAM s1 TO value(printer.path) page-size value(printer.pglen). 
    FIND FIRST printcod WHERE 
      printcod.emu = printer.emu AND printcod.code="17cpi" NO-LOCK NO-ERROR. 
 
    form header TRIM(Contcode) 
         SKIP htl-name "Page   :" AT 83 " " 
              STRING(page-number(s1)) SKIP 
              htl-adr "Period :" AT 83 str1 SKIP 
              "Tel " htl-tel 
              str2 AT 83 SKIP(1) 
              str3 AT 1 SKIP(1) 
              st1 AT 1 SKIP 
              st2 AT 1 SKIP 
              st3 AT 1 SKIP(1) 
              dlist SKIP 
              wlist SKIP 
          "---------------------------------------------------------------------------------------------------------------" 
         WITH FRAME hdr PAGE-TOP NO-BOX NO-ATTR-SPACE COLUMN 1 WIDTH 145. 
    VIEW STREAM s1 FRAME hdr . 
 
    IF monthdayselect = 1 THEN 
    FOR EACH room-list: 
      IF room-list.rstat = 0 THEN PUT STREAM s1 room-list.bezeich " ". 
      ELSE 
      DO: 
          IF incl-tent AND NOT incl-wait THEN 
          PUT STREAM s1 
          ("     " + translateExtended ("Tent",lvCAREA,"")) FORMAT "x(15) ". 
          ELSE IF incl-tent AND incl-wait THEN 
          PUT STREAM s1 
          ("     " + translateExtended ("Tent+WL",lvCAREA,"")) FORMAT "x(15) ". 
          ELSE IF NOT incl-tent AND 
             incl-wait THEN 
          PUT STREAM s1 
          ("     " + translateExtended ("WList",lvCAREA,"")) FORMAT "x(15) ". 
      END. 
      DO i = 1 TO 12: 
        PUT STREAM s1 room-list.coom[i] " ". 
        IF room-list.tag = 33 THEN t-occ = t-occ + room-list.room[i]. 
        IF room-list.tag = 34 THEN t-vac = t-vac + room-list.room[i]. 
      END. 
      IF room-list.tag = 33 THEN PUT STREAM s1 STRING(t-occ, ">>>,>>9"). 
      ELSE IF room-list.tag = 34 THEN PUT STREAM s1 STRING(t-vac, ">>>,>>9"). 
      ELSE IF room-list.tag = 35 THEN 
         PUT STREAM s1 STRING((t-occ / (t-occ + t-vac) * 100), "->>9,99"). 
      PUT STREAM s1 "" SKIP. 
    END. 
 
    ELSE IF monthdayselect = 0 THEN 
    DO: 
      FOR EACH rm-list BY rm-list.nr: 
        PUT STREAM s1 rm-list.bezeich " ". 
        DO i = 1 TO 12: 
          PUT STREAM s1 rm-list.room[i] " ". 
        END. 
        PUT STREAM s1 "" SKIP. 
      END. 
 
      PUT STREAM s1 "" SKIP. 
      FOR EACH sum-list: 
        PUT STREAM s1 sum-list.bezeich " ". 
        DO i = 1 TO 12: 
          PUT STREAM s1 sum-list.summe[i] " ". 
        END. 
        PUT STREAM s1 "" SKIP. 
      END. 
 
      PUT STREAM s1 "" SKIP. 
      FOR EACH segm-list: 
        PUT STREAM s1 segm-list.bezeich " ". 
        DO i = 1 TO 12: 
          PUT STREAM s1 segm-list.segm[i] " ". 
        END. 
        PUT STREAM s1 "" SKIP. 
      END. 
    END. 

    IF show-rmrev THEN
    DO:
        PUT STREAM s1 "" SKIP.
        FOR EACH rev-list:
            PUT STREAM s1 rev-list.bezeich " ".
            DO i = 1 TO 6:
                PUT STREAM s1 rev-list.str[i] " ".
            END.
            PUT STREAM s1 "" SKIP.
        END.
    END.
 
    FIND FIRST printcod WHERE 
      printcod.emu = printer.emu AND printcod.code="rs" NO-LOCK NO-ERROR. 
    IF AVAILABLE printcod THEN PUT STREAM s1 TRIM(Contcode). 
    OUTPUT STREAM s1 CLOSE. 
    CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow"). 
END.
*/

PROCEDURE create-label11: 
DEFINE VARIABLE datum1 AS CHAR FORMAT "x(5)". 
DEFINE VARIABLE mm AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE i AS INTEGER NO-UNDO.

    mm = INTEGER(SUBSTR(from-month,1,2)). 
    yy = INTEGER(SUBSTR(from-month,3,4)). 
    
    dlist = "               ". 
    
    DO i = 1 TO 12: 
        curr-day = mm. 
        datum  = DATE(mm, 1, yy). 
        datum1 = SUBSTR(STRING(datum),1,5). 
    
        dlist = dlist + "   " + datum1. 
    
        month-str[i] = datum1 + "                  "
            + translateExtended(week-list[curr-day],lvCAREA,""). 
        mm = mm + 1. 
        IF mm = 13 THEN 
        DO: 
            mm = 1. 
            yy = yy + 1. 
        END.
 
    /*IF i = 1 THEN DO: 
      /*ASSIGN room-list.coom[1]:LABEL IN BROWSE b11 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[1]:label-fgcolor = 0. 
      ASSIGN room-list.coom[1]:label-bgcolor = 8. */
      month-str1 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 2 THEN DO: 
      /*ASSIGN room-list.coom[2]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[2]:label-fgcolor = 0. 
      ASSIGN room-list.coom[2]:label-bgcolor = 8. */
      month-str2 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 3 THEN DO: 
      /*ASSIGN room-list.coom[3]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[3]:label-fgcolor = 0. 
      ASSIGN room-list.coom[3]:label-bgcolor = 8. */
      month-str3 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 4 THEN DO: 
      ASSIGN room-list.coom[4]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[4]:label-fgcolor = 0. 
      ASSIGN room-list.coom[4]:label-bgcolor = 8. 
      month-str4 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 5 THEN DO: 
      ASSIGN room-list.coom[5]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[5]:label-fgcolor = 0. 
      ASSIGN room-list.coom[5]:label-bgcolor = 8. 
      month-str5 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 6 THEN DO: 
      ASSIGN room-list.coom[6]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[6]:label-fgcolor = 0. 
      ASSIGN room-list.coom[6]:label-bgcolor = 8. 
      month-str6 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 7 THEN DO: 
      ASSIGN room-list.coom[7]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[7]:label-fgcolor = 0. 
      ASSIGN room-list.coom[7]:label-bgcolor = 8. 
      month-str7 = datum1 + "                  " 
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 8 THEN DO: 
      ASSIGN room-list.coom[8]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[8]:label-fgcolor = 0. 
      ASSIGN room-list.coom[8]:label-bgcolor = 8. 
      month-str8 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 9 THEN DO: 
      ASSIGN room-list.coom[9]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[9]:label-fgcolor = 0. 
      ASSIGN room-list.coom[9]:label-bgcolor = 8. 
      month-str9 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 10 THEN DO: 
      ASSIGN room-list.coom[10]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[10]:label-fgcolor = 0. 
      ASSIGN room-list.coom[10]:label-bgcolor = 8. 
      month-str10 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 11 THEN DO: 
      ASSIGN room-list.coom[11]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[11]:label-fgcolor = 0. 
      ASSIGN room-list.coom[11]:label-bgcolor = 8. 
      month-str11 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    ELSE IF i = 12 THEN DO: 
      ASSIGN room-list.coom[12]:LABEL 
        = datum1 + "!" + week-list[curr-day]. 
      ASSIGN room-list.coom[12]:label-fgcolor = 0. 
      ASSIGN room-list.coom[12]:label-bgcolor = 8. 
      month-str12 = datum1 + "                  "
          + translateExtended(week-list[curr-day],lvCAREA,""). 
    END. 
    mm = mm + 1. 
    IF mm = 13 THEN 
    DO: 
      mm = 1. 
      yy = yy + 1. 
    END.*/ 
    END. 
END. 

PROCEDURE clear-shared:
    FOR EACH room-list:
        DELETE room-list.
    END.
    FOR EACH segm-list:
        DELETE segm-list.
    END.
    FOR EACH rev-list:
        DELETE rev-list.
    END.
    
    FOR EACH sum-list:
        DELETE sum-list.
    END.
    /*
    FOR EACH SEGM1-LIST:
        DELETE segm1-list.
    END.
    FOR EACH zikat-list:
        DELETE zikat-list.
    END.
    FOR EACH argt-list:
        DELETE argt-list.
    END.
    */
END.

PROCEDURE clear-shared1:
    FOR EACH room-list:
        DELETE room-list.
    END.
    FOR EACH segm-list:
        DELETE segm-list.
    END.
    FOR EACH rev-list:
        DELETE rev-list.
    END.
    
    FOR EACH sum-list:
        DELETE sum-list.
    END.
    
    FOR EACH SEGM1-LIST:
        DELETE segm1-list.
    END.
    FOR EACH zikat-list:
        DELETE zikat-list.
    END.
    FOR EACH argt-list:
        DELETE argt-list.
    END.
END.

/*MT
PROCEDURE design-lnl:
    DEFINE VARIABLE record-exist AS LOGICAL INITIAL YES NO-UNDO.
    DEFINE VARIABLE str1 AS CHAR.
    DEFINE VARIABLE str3 AS CHAR.
    DEFINE VARIABLE str2 AS CHAR.

    RUN MasterLnL.p("","","","","clear").

/* DEFINE variables AND FIELDS WITH sample-data FOR Designer */ 
    FIND FIRST room-list NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE room-list THEN 
    DO: 
        record-exist = NO. 
        CREATE room-list. 
        ASSIGN 
            room-list.bezeich = "ABC". 
            room-list.coom = "999". 
    END. 

    str1 = "$TI" + translateExtended("Annual Forecast of Room Occupancy",lvCAREA, "") + LnLDelimeter + "$Pr" + translateextended("From Month :  ",lvCAREA, "") +
           STRING(from-month, "99/9999").
    
    str2 = translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter 
           + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter 
           + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter + 
            translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter + translateExtended("01/04                  Jan", lvCAREA, "") 
           + LnLDelimeter + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter
           + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter + translateExtended("01/04                  Jan", lvCAREA, "") + LnLDelimeter
           + translateExtended(avl-rm, lvCAREA, "") + LnLDelimeter + translateExtended(pax-occ, lvCAREA, "") + LnLDelimeter
           + translateExtended(occ-proz, lvCAREA, "") + LnLDelimeter + translateExtended(rm-occ, lvCAREA, "") + LnLDelimeter
           + translateExtended(dis-type, lvCAREA, "") + LnLDelimeter + translateExtended(out-type, lvCAREA, "") + LnLDelimeter. 
   
    str3= room-list.bezeich + LnLDelimeter + "" + LnLDelimeter + ""
          + LnLDelimeter + STRING(999,">>>")+ LnLDelimeter + STRING(999,">>>")
          + LnLDelimeter + STRING(999,">>>") + LnLDelimeter + STRING(999,">>>") + LnLDelimeter + STRING(999,">>>")
          + LnLDelimeter + STRING(999,">>>") + LnLDelimeter + STRING(999,">>>") + LnLDelimeter + 
          STRING(999,">>>") + LnLDelimeter + STRING(999,">>>") + LnLDelimeter + 
          STRING(999,">>>") + LnLDelimeter + STRING(999,">>>") + LnLDelimeter + STRING(999,">>>").

   record-exist = YES.
   RUN MasterLnL.p("annual-fcast.lst",str1,str2,str3,"Design").
   IF NOT record-exist THEN DELETE room-list.                  
END.


PROCEDURE print-lnl:
DEFINE VARIABLE str1 AS CHAR FORMAT "X(40)".
   DEFINE VARIABLE str2 AS CHAR.
   DEFINE VARIABLE str3 AS CHAR.
   DEF BUFFER r-list FOR room-list. 
   DEFINE VARIABLE i AS INTEGER.
   DEFINE VARIABLE nRecno AS INTEGER.
 
   RUN MasterLnL.p("","","","","clear").
   
   FIND FIRST r-list NO-LOCK NO-ERROR. 
   IF NOT AVAILABLE r-list THEN 
    DO:
        RETURN.
    END. 
    
    /* DEFINE variables AND FIELDS WITH sample-data FOR Designer */ 
    FIND FIRST r-list NO-LOCK. 
    
    str1 = "$TI" + translateExtended("Annual Forecast of Room Occupancy",lvCAREA, "") + LnLDelimeter + "$Pr" + translateextended("From Month :  ",lvCAREA, "") +
           STRING(from-month, "99/9999").
   
    IF monthdayselect = 0 THEN dis-type = translateExtended("Display : Monthly Basis", lvCAREA,""). 
    IF roompaxselect = 1 THEN out-type = translateExtended("Output by : Person", lvCAREA,"") . 

    DO i = 1 TO 12:
        str2 = str2 + translateExtended(month-str[i], lvCAREA, "")  + 
            LnLDelimeter .
    END.
   str2 = str2 + translateExtended(avl-rm, lvCAREA, "") + LnLDelimeter + translateExtended(pax-occ, lvCAREA, "") + LnLDelimeter
          + translateExtended(occ-proz, lvCAREA, "") + LnLDelimeter + translateExtended(rm-occ, lvCAREA, "") + LnLDelimeter
          + translateExtended(dis-type, lvCAREA, "") + LnLDelimeter + translateExtended(out-type, lvCAREA, "") + LnLDelimeter. 

    /*
    str2 = translateExtended(month-str1, lvCAREA, "") + LnLDelimeter + translateExtended(month-str2, lvCAREA, "") + LnLDelimeter 
           + translateExtended(month-str3, lvCAREA, "") + LnLDelimeter + translateExtended(month-str4, lvCAREA, "") + LnLDelimeter 
           + translateExtended(month-str5, lvCAREA, "") + LnLDelimeter + translateExtended(month-str6, lvCAREA, "") + LnLDelimeter + 
            translateExtended(month-str7, lvCAREA, "") + LnLDelimeter + translateExtended(month-str8, lvCAREA, "") 
           + LnLDelimeter + translateExtended(month-str9, lvCAREA, "") + LnLDelimeter + translateExtended(month-str10, lvCAREA, "") + LnLDelimeter
           + translateExtended(month-str11, lvCAREA, "") + LnLDelimeter + translateExtended(month-str12, lvCAREA, "") + LnLDelimeter
           + translateExtended(avl-rm, lvCAREA, "") + LnLDelimeter + translateExtended(pax-occ, lvCAREA, "") + LnLDelimeter
           + translateExtended(occ-proz, lvCAREA, "") + LnLDelimeter + translateExtended(rm-occ, lvCAREA, "") + LnLDelimeter
           + translateExtended(dis-type, lvCAREA, "") + LnLDelimeter + translateExtended(out-type, lvCAREA, "") + LnLDelimeter. 
    */

    /*for DISPLAY type monthly*/ 
    IF monthdayselect = 0 THEN 
    DO: 
       /* Iterate over all records OF the Customer table */ 
        FOR EACH r-list WHERE SUBSTR(r-list.bezeich,1,5) NE "=====": 
    /* UPDATE meterbar */
         str3= r-list.bezeich + LnLDelimeter + "" + LnLDelimeter + ""
                + LnLDelimeter + STRING(r-list.room[1],">,>>9" ) + LnLDelimeter + STRING(r-list.room[2],">,>>9" )
                + LnLDelimeter + STRING(r-list.room[3],">,>>9" ) + LnLDelimeter + STRING(r-list.room[4],">,>>9" ) + LnLDelimeter 
                + STRING(r-list.room[5],">,>>9" ) + LnLDelimeter + STRING(r-list.room[6],">,>>9" ) + LnLDelimeter + 
                STRING(r-list.room[7],">,>>9" ) + LnLDelimeter + STRING(r-list.room[8],">,>>9" ) + LnLDelimeter + 
                STRING(r-list.room[9],">,>>9" ) + LnLDelimeter + STRING(r-list.room[10],">,>>9" ) + LnLDelimeter + 
                STRING(r-list.room[11],">,>>9" ) + LnLDelimeter + STRING(r-list.room[12],">,>>9" ).

           RUN MasterLnL.p("","","",str3,"add"). 

        END. 
 
        nRecno = 0. 

        FOR EACH sum-list WHERE SUBSTR(sum-list.bezeich,1,5) NE "=====": 
     /* UPDATE meterbar */
          nRecno = nRecno + 1. 
          str3= sum-list.bezeich + LnLDelimeter + "" + LnLDelimeter + STRING(nRecno)
                + LnLDelimeter + STRING(sum-list.summe[1], ">,>>9") + LnLDelimeter + STRING(sum-list.summe[2], ">,>>9")
                + LnLDelimeter + STRING(sum-list.summe[3], ">,>>9") + LnLDelimeter + STRING(sum-list.summe[4], ">,>>9") + LnLDelimeter 
                + STRING(sum-list.summe[5], ">,>>9") + LnLDelimeter + STRING(sum-list.summe[6], ">,>>9") + LnLDelimeter + 
                STRING(sum-list.summe[7], ">,>>9") + LnLDelimeter + STRING(sum-list.summe[8], ">,>>9") + LnLDelimeter + 
                STRING(sum-list.summe[9], ">,>>9") + LnLDelimeter + STRING(sum-list.summe[10], ">,>>9") + LnLDelimeter + 
                STRING(sum-list.summe[11], ">,>>9") + LnLDelimeter + STRING(sum-list.summe[12], ">,>>9").

          RUN MasterLnL.p("","","",str3,"add"). 
        END. 

        nRecno = 0. 
        FOR EACH segm-list WHERE SUBSTR(segm-list.bezeich,1,5) NE "=====": 
    /* UPDATE meterbar */ 
            nRecno = nRecno + 1. 
            str3= segm-list.bezeich + LnLDelimeter + STRING(nRecno) + LnLDelimeter + ""
                + LnLDelimeter + STRING(segm-list.segm[1], ">,>>9") + LnLDelimeter + STRING(segm-list.segm[2], ">,>>9")
                + LnLDelimeter + STRING(segm-list.segm[3], ">,>>9") + LnLDelimeter + STRING(segm-list.segm[4], ">,>>9") + LnLDelimeter 
                + STRING(segm-list.segm[5], ">,>>9") + LnLDelimeter + STRING(segm-list.segm[6], ">,>>9") + LnLDelimeter + 
                STRING(segm-list.segm[7], ">,>>9") + LnLDelimeter + STRING(segm-list.segm[8], ">,>>9") + LnLDelimeter + 
                STRING(segm-list.segm[9], ">,>>9") + LnLDelimeter + STRING(segm-list.segm[10], ">,>>9") + LnLDelimeter + 
                STRING(segm-list.segm[11], ">,>>9") + LnLDelimeter + STRING(segm-list.segm[12], ">,>>9").

          RUN MasterLnL.p("","","",str3,"add").   
        END.                                      
    END.
    ELSE IF monthdayselect = 1 THEN 
    DO: 
       
       FOR EACH room-list WHERE SUBSTR(room-list.bezeich,1,5) NE "=====": 
           str3 = TRIM(room-list.bezeich)  + LnLDelimeter + "" + LnLDelimeter + "" + LnLDelimeter + room-list.coom[1]
                + LnLDelimeter + room-list.coom[2] + LnLDelimeter + room-list.coom[3] + LnLDelimeter + room-list.coom[4]
                + LnLDelimeter + room-list.coom[5] + LnLDelimeter + room-list.coom[6] + LnLDelimeter 
                + room-list.coom[7] + LnLDelimeter + room-list.coom[8] + LnLDelimeter + 
                room-list.coom[9] + LnLDelimeter + room-list.coom[10] + LnLDelimeter + 
                room-list.coom[11] + LnLDelimeter + room-list.coom[12] + LnLDelimeter.  
            RUN MasterLnL.p("","","",str3,"add"). 
        END. 
    END.
    IF call-from = 0 THEN
        RUN MasterLnL.p("annual-fcast.lst",str1,str2,str3,"Print").
    ELSE RUN MasterLnL.p("annual-fcast.lst",str1,str2,str3,"pdf").
END.
*/
