DEF TEMP-TABLE s-list
    FIELD gastnr            AS INT
    FIELD datum             AS CHAR
    FIELD NAME              AS CHAR
    FIELD address           AS CHAR
    FIELD city              AS CHAR
    FIELD zimmeranz         AS INT INITIAL 0
    FIELD lodging           AS DEC FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0
   .

DEF TEMP-TABLE t-list LIKE guest
    FIELD cp1 AS CHAR
    FIELD cp2 AS CHAR
    FIELD cp3 AS CHAR
    FIELD guest-name AS CHAR
    FIELD guest-adr  AS CHAR.

/* */
DEF TEMP-TABLE u-list
    FIELD rmSegmt            AS INTEGER
    FIELD rmRev              AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0
   .

DEF BUFFER segTmp            FOR segment.

DEFINE TEMP-TABLE occupancy-forecast
    FIELD datum                     AS CHAR
    FIELD days                      AS CHAR
    FIELD group-onhand-definite     AS INT
    FIELD group-onhand-tentative    AS INT
    FIELD booking-onhand-fit        AS INT
    FIELD total-otb-group-fit       AS INT
    FIELD total-room-avail          AS INT
    FIELD arr-otb                   AS INT
    FIELD total-otb-percent         AS CHAR
    FIELD leadtime-booking          AS INT
    FIELD samedate-lastyear         AS INT
    FIELD samedate-lastyear-percent AS CHAR
    FIELD arr-last-year             AS INT.


DEFINE INPUT PARAMETER curr-date  AS DATE.
DEFINE INPUT PARAMETER occRpt     AS LOGICAL. 
DEFINE INPUT PARAMETER occ-month  AS INT.    
DEFINE INPUT PARAMETER occ-year   AS INT. 
DEFINE INPUT PARAMETER linkgsheet AS CHAR.
DEFINE INPUT PARAMETER filenm     AS CHAR.
DEFINE INPUT PARAMETER guestRpt   AS LOGICAL.
DEFINE INPUT PARAMETER fDate      AS DATE.   
DEFINE INPUT PARAMETER tDate      AS DATE.   
DEFINE INPUT PARAMETER revRpt     AS LOGICAL.
DEFINE INPUT PARAMETER fDate1     AS DATE.   
DEFINE INPUT PARAMETER tDate1     AS DATE.   
DEFINE INPUT PARAMETER otbMseg    AS LOGICAL.
DEFINE INPUT PARAMETER otbMonth   AS INT.    
DEFINE INPUT PARAMETER otbYear    AS INT.  
DEFINE OUTPUT PARAMETER TABLE FOR occupancy-forecast.
DEFINE OUTPUT PARAMETER TABLE FOR t-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR u-list.

DEFINE VARIABLE week-list                   AS CHAR EXTENT 14 FORMAT "x(5)" 
    INITIAL ["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ]. 
DEFINE VARIABLE month-list                  AS CHAR EXTENT 14 FORMAT "x(9)" 
    INITIAL ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"].

IF occRpt   THEN RUN generate-occupancyForecast.
IF guestRpt THEN RUN generate-clientdata.
IF revRpt   THEN RUN generate-revenuedata.
IF otbMseg  THEN RUN generate-otbMseg.


PROCEDURE generate-occupancyForecast :
    DEFINE VARIABLE currDate        AS DATE NO-UNDO.
    DEFINE VARIABLE lyDate          AS DATE NO-UNDO.
    DEFINE VARIABLE i               AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE j               AS INT  NO-UNDO INITIAL 1.
    DEFINE VARIABLE LastDay         AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE lyLastDay       AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE qtyFIT          AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE qtyGroupD       AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE qtyGroupT       AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE LYqtyFIT        AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE LYqtyGroupD     AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE LYqtyGroupT     AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE avrgRate        AS DEC  NO-UNDO INITIAL 0.
    DEFINE VARIABLE LyavrgRate      AS DEC  NO-UNDO INITIAL 0.
    DEFINE VARIABLE qtyTotal        AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE LyqtyTotal      AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE lyTotal         AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE totRoom         AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE LYtotRoom       AS INT  NO-UNDO INITIAL 0.
    
    DEFINE VARIABLE GrandTot-FIT    AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE GrandTot-GroupD AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE GrandTotQty     AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE GrandLyTotQty   AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE GrandTotRoom    AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE GrandTotLYRoom  AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE str-AvFIT       AS CHAR NO-UNDO INITIAL "".
    DEFINE VARIABLE str-AvGroupD    AS CHAR NO-UNDO INITIAL "".
    DEFINE VARIABLE str-qtyTotal    AS CHAR NO-UNDO INITIAL "".
    DEFINE VARIABLE str-qtyTotalLy  AS CHAR NO-UNDO INITIAL "".
    DEFINE VARIABLE str-GTqty       AS CHAR NO-UNDO INITIAL "".
    DEFINE VARIABLE str-GTroom      AS CHAR NO-UNDO INITIAL "".
    DEFINE VARIABLE str-GTroomly    AS CHAR NO-UNDO INITIAL "".

    DEFINE VARIABLE lead-time       AS DEC NO-UNDO INITIAL 0.
    
    DEFINE VARIABLE pay             AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE Lypay           AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE casetype        AS INT  NO-UNDO INITIAL 0.

    IF linkgsheet EQ ? THEN linkgsheet = "".

    IF linkgsheet NE "" THEN 
    DO:
        RUN nt-tauziarpt-gen-occfcast-gsheetbl.p(curr-date, occ-month, occ-year, filenm, linkgsheet).
    END.
    ELSE 
    DO:       
        DO i = 0 TO 2 :
            ASSIGN GrandTot-FIT     = 0
                   GrandTot-GroupD  = 0
                   GrandTotQty      = 0
                   GrandLyTotQty    = 0
                   GrandTotRoom     = 0
                   GrandTotLYRoom   = 0
                   .
            
            RUN lastDayInMonth (occ-month + i, occ-year, OUTPUT LastDay).
            RUN lastDayInMonth (occ-month + i, occ-year - 1, OUTPUT lyLastDay).
            /*MT 08/11/12 */
            IF occ-month GT 10 THEN
            DO:
                IF occ-month + i = 13 THEN
                DO:
                    RUN lastDayInMonth (1, occ-year + 1, OUTPUT LastDay).
                    RUN lastDayInMonth (1, occ-year, OUTPUT lyLastDay).
                END.
                    
                ELSE IF occ-month + i = 14 THEN
                DO:
                    RUN lastDayInMonth (2, occ-year + 1, OUTPUT LastDay).
                    RUN lastDayInMonth (2, occ-year, OUTPUT lyLastDay).
                END.
                    
            END.
    
            DO j = 1 TO LastDay :
                IF occ-month + i = 13 THEN
                    ASSIGN 
                    currDate    = DATE(1, j, occ-year + 1)
                    lyDate      = DATE (1, j ,occ-year).
                ELSE IF occ-month + i = 14 THEN
                DO:
                    currDate    = DATE(2, j, occ-year + 1).
                    IF MONTH(currDate) = 2 AND DAY(currDate) = 29 AND
                        YEAR(currDate) MOD 4 = 0 THEN
                        lyDate      = DATE (2, 28 ,occ-year).
                    ELSE        
                        lyDate      = DATE (2, j ,occ-year).
                END.                                             
                ELSE 
                DO:
                    currDate   = DATE(occ-month + i, j, occ-year).
                    IF MONTH(currDate) = 2 AND DAY(currDate) = 29 AND
                        YEAR(currDate) MOD 4 = 0 THEN
                        lyDate = DATE(occ-month + i, 28 ,occ-year - 1).
                    ELSE
                        lyDate = DATE(occ-month + i, j ,occ-year - 1).
                END.
                
                IF currDate LT curr-date THEN casetype = 1.
                ELSE casetype = 2.

                RUN nt-tauziarpt-gen-occfcastbl.p(lyDate, casetype, currDate, curr-date,
                               OUTPUT avrgRate,OUTPUT LyavrgRate, OUTPUT qtyGroupD, OUTPUT LyqtyGroupD, OUTPUT qtyGroupT,
                               OUTPUT qtyFIT, OUTPUT LyqtyFIT, OUTPUT totRoom,OUTPUT LYtotRoom, OUTPUT Lead-time,
                               OUTPUT pay, OUTPUT Lypay).
                
                ASSIGN qtyTotal          = qtyFIT + qtyGroupD
                       LyQtyTotal        = LyqtyFIT + LyqtyGroupD
                       GrandTot-FIT      = GrandTot-FIT + qtyFIT
                       GrandTot-GroupD   = GrandTot-GroupD + qtyGroupD
                       GrandTotQty       = GrandTotQty + qtyTotal
                       GrandLyTotQty     = GrandLyTotQty + LyqtyTotal
                       GrandTotRoom      = GrandTotRoom + totRoom
                       GrandTotLYRoom    = GrandTotLYRoom + LYtotRoom.
    
                RUN create-decimal(STRING((pay / totRoom) * 100), 8, 
                                   OUTPUT str-qtyTotal).
                RUN create-decimal(STRING((Lypay / LYtotRoom) * 100), 8, 
                                   OUTPUT str-qtyTotalLy).
                CREATE occupancy-forecast.
                ASSIGN 
                    datum                     = STRING(currDate)
                    days                      = week-list[WEEKDAY(currDate)]
                    group-onhand-definite     = qtyGroupD      
                    group-onhand-tentative    = qtyGroupT     
                    booking-onhand-fit        = qtyFIT    
                    total-otb-group-fit       = qtyTotal     
                    total-room-avail          = totRoom      
                    arr-otb                   = avrgRate
                    total-otb-percent         = str-qtyTotal
                    leadtime-booking          = lead-time
                    samedate-lastyear         = LyQtyTotal
                    samedate-lastyear-percent = str-qtyTotalLy
                    arr-last-year             = LyavrgRate.
            END.
            CREATE occupancy-forecast.
            ASSIGN 
                datum                     = "Total"
                days                      = ""
                group-onhand-definite     = GrandTot-GroupD      
                group-onhand-tentative    = 0     
                booking-onhand-fit        = GrandTot-FIT 
                total-otb-group-fit       = GrandTotQty   
                total-room-avail          = GrandTotRoom   
                arr-otb                   = 0
                total-otb-percent         = ""
                leadtime-booking          = 0
                samedate-lastyear         = GrandLyTotQty
                samedate-lastyear-percent = ""
                arr-last-year             = 0.
    
            RUN create-decimal(STRING(GrandTot-FIT / (LastDay - 1)), 6, OUTPUT str-AvFIT).
            RUN create-decimal(STRING(GrandTot-GroupD / (LastDay - 1)), 6, OUTPUT str-AvGroupD).
            RUN create-decimal(STRING(GrandTotQty / (LastDay - 1)), 6, OUTPUT str-GTqty).
            RUN create-decimal(STRING(GrandTotRoom / (LastDay - 1)), 6, OUTPUT str-GTroom).
            RUN create-decimal(STRING(GrandLyTotQty / (lyLastDay - 1)), 6, OUTPUT str-GTroomly).
            CREATE occupancy-forecast.
            ASSIGN 
                datum                     = "Average"
                days                      = ""
                group-onhand-definite     = INT(str-AvGroupD)     
                group-onhand-tentative    = 0     
                booking-onhand-fit        = INT(str-AvFIT) 
                total-otb-group-fit       = INT(str-GTqty)   
                total-room-avail          = INT(str-GTroom)   
                arr-otb                   = 0
                total-otb-percent         = ""
                leadtime-booking          = 0
                samedate-lastyear         = INT(str-GTroomly)
                samedate-lastyear-percent = ""
                arr-last-year             = 0.
        END.
    END.
END PROCEDURE.

PROCEDURE generate-ClientData:
    RUN nt-tauziarpt-gen-clientdatabl.p (2,curr-date,fDate, tDate, OUTPUT TABLE t-list).
END PROCEDURE. 

PROCEDURE generate-RevenueData:
    RUN nt-tauziarpt-gen-revdatabl.p (fDate1, tDate1, OUTPUT TABLE s-list).
END PROCEDURE. 

PROCEDURE lastDayInMonth :
    DEFINE INPUT PARAMETER intMont  AS INT NO-UNDO.
    DEFINE INPUT PARAMETER intYear  AS INT NO-UNDO.
    DEFINE OUTPUT PARAMETER lastDay AS INT NO-UNDO.
    
    CASE intMont:
        WHEN 1 OR WHEN 3 OR WHEN 5 OR WHEN 7 OR WHEN 8 OR WHEN 10 OR WHEN 12 THEN
            lastDay =  31.
        WHEN 4 OR WHEN 6 OR WHEN 9 OR WHEN 11 THEN lastDay =  30.
        WHEN 2 THEN
        DO:
            IF ( intYear MOD 4 )= 0 THEN lastDay =  29.
            ELSE lastDay =  28.       
        END.
    END CASE.
END PROCEDURE.

PROCEDURE create-decimal:
    DEFINE INPUT PARAMETER strPrice     AS CHAR NO-UNDO.
    DEFINE INPUT PARAMETER digit        AS INT  NO-UNDO.
    DEFINE OUTPUT PARAMETER strAmount   AS CHAR NO-UNDO INIT "".
    
    DEFINE VARIABLE sInt        AS CHAR NO-UNDO.
    DEFINE VARIABLE sDec        AS CHAR NO-UNDO.
    DEFINE VARIABLE i           AS INT  NO-UNDO.
    DEFINE VARIABLE nDec        AS CHAR NO-UNDO.
    
    IF strPrice EQ "" THEN RETURN.
    
    IF NUM-ENTRIES (strPrice, ".") GT 1 THEN
    DO:
        sInt = ENTRY(1, strPrice, ".").
        sDec = ENTRY(2, strPrice, ".").       
    
        IF LENGTH(sDec) GT 2 THEN nDec = SUBSTRING(sDec, 1, 2).
        ELSE nDec = sDec.

        IF digit GT (LENGTH(sInt) + LENGTH(nDec) + 1) THEN
        DO i = 1 TO ( digit - (LENGTH(sInt) + LENGTH(nDec) + 1) ):
            strAmount = strAmount + " ".
        END.
        
        IF INT(sint) = 0 THEN strAmount = strAmount + "0." + nDec.
        ELSE strAmount = strAmount + sInt + "." + nDec.
    END.
    ELSE
    DO:
        IF LENGTH(strPrice) LT digit THEN
        DO:
            DO i = 1 TO ( digit - LENGTH(strPrice)):
                strAmount = strAmount + " ".
            END.
            strAmount = strAmount + strPrice.
        END.
        ELSE strAmount = strPrice.
    END.
END PROCEDURE.

PROCEDURE generate-otbMseg:
    DEFINE VARIABLE currDate  AS DATE NO-UNDO.
    DEFINE VARIABLE lyDate    AS DATE NO-UNDO FORMAT "99/99/99".
    DEFINE VARIABLE LastDay   AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE j         AS INT  NO-UNDO INITIAL 1.
    DEFINE VARIABLE h         AS INT  NO-UNDO.
    DEFINE VARIABLE iColSeg   AS INT NO-UNDO.
    DEFINE VARIABLE iRowSeg   AS INT NO-UNDO.

    DEFINE VARIABLE iColumn   AS INT  NO-UNDO INITIAL 0. 
    DEFINE VARIABLE cColumn   AS CHARACTER. 
    DEFINE VARIABLE cRange    AS CHARACTER.
    DEFINE VARIABLE curr-row  AS INTEGER NO-UNDO INIT 7.
    DEFINE VARIABLE week-row  AS INTEGER NO-UNDO EXTENT 2.
    DEFINE VARIABLE curr-col  AS INTEGER NO-UNDO INIT 1.
    DEFINE VARIABLE totRoom   AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE rSold     AS INT  NO-UNDO INITIAL 0.
    DEFINE VARIABLE rRev      AS DECIMAL NO-UNDO FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0.
    DEFINE VARIABLE rSeg      AS CHARACTER NO-UNDO.
    DEFINE VARIABLE colSeg    AS CHARACTER NO-UNDO FORMAT "X(2)" EXTENT.
    DEFINE VARIABLE tmpSeg    AS CHARACTER NO-UNDO FORMAT "X(5)" EXTENT.

    DEFINE VARIABLE week-list AS CHAR EXTENT 14 FORMAT "x(5)" 
      INITIAL ["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ]. 

    RUN nt-tauziarpt-gen-otbmseg-gsheetbl.p (?, OUTPUT totRoom, OUTPUT TABLE u-list).
 
END PROCEDURE.

