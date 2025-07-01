
DEFINE TEMP-TABLE bfast-data
    FIELD tDate         AS DATE
    FIELD roomNr        AS CHARACTER
    FIELD resNr         AS INTEGER
    FIELD guestNr       AS INTEGER
    FIELD vip           AS LOGICAL
    FIELD nation        AS CHARACTER
    FIELD guestName     AS CHARACTER
    FIELD totalAdult    AS INTEGER
    FIELD totalCompli   AS INTEGER
    FIELD totalChild    AS INTEGER
    FIELD totalUse      AS INTEGER
    FIELD dummyChr      AS CHARACTER
        .

DEFINE INPUT PARAMETER room         AS CHARACTER.
DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER mealTime     AS CHARACTER.
DEFINE INPUT PARAMETER dummyInput   AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR bfast-data.

DEFINE VARIABLE getDataNr       AS INTEGER.
DEFINE VARIABLE i               AS INTEGER.
DEFINE VARIABLE ii              AS INTEGER.
DEFINE VARIABLE sumAdult        AS INTEGER.
DEFINE VARIABLE sumCompl        AS INTEGER.
DEFINE VARIABLE sumChild        AS INTEGER.
DEFINE VARIABLE sumTotUse       AS INTEGER.

DEFINE VARIABLE dateval         AS INTEGER INIT 0.

DEFINE VARIABLE artGrp-abf     AS INTEGER.
DEFINE VARIABLE artGrp-lunch   AS INTEGER.
DEFINE VARIABLE artGrp-dinner  AS INTEGER.

DEFINE VARIABLE tempresnr  AS INTEGER INIT 0.
DEFINE VARIABLE strdayuse  AS CHAR INIT "".
DEFINE VARIABLE strday     AS CHAR INIT "".

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK NO-ERROR. /*Breakfast*/
IF AVAILABLE htparam THEN artGrp-abf = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 227 NO-LOCK NO-ERROR. /*Lunch*/
IF AVAILABLE htparam THEN artGrp-lunch = htparam.finteger.

FIND FIRST htparam WHERE paramnr = 228 NO-LOCK NO-ERROR. /*Dinner*/
IF AVAILABLE htparam THEN artGrp-dinner = htparam.finteger.
/*
IF fdate EQ ? THEN
DO:
    FOR EACH mealcoup WHERE mealcoup.NAME = mealTime
        AND mealcoup.zinr MATCHES("*" + room + "*") NO-LOCK:
        FIND FIRST res-line WHERE res-line.resnr = mealcoup.resnr 
            AND res-line.zinr = mealcoup.zinr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest THEN FIND FIRST guest WHERE guest.gastnr = res-line.gastnr.

            /*getDataNr = mealcoup.abreise - mealcoup.ankunft.*/
            getDataNr = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                      + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                      + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                      + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                      + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                      + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                      + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
            
                strdayuse = "".
                IF mealcoup.verbrauch[1] NE 0 THEN strdayuse = "1;".
                IF mealcoup.verbrauch[2] NE 0 THEN strdayuse = strdayuse + "2;".  
                IF mealcoup.verbrauch[3] NE 0 THEN strdayuse = strdayuse + "3;".                                 
                IF mealcoup.verbrauch[4] NE 0 THEN strdayuse = strdayuse + "4;".
                IF mealcoup.verbrauch[5] NE 0 THEN strdayuse = strdayuse + "5;".
                IF mealcoup.verbrauch[6] NE 0 THEN strdayuse = strdayuse + "6;".
                IF mealcoup.verbrauch[7] NE 0 THEN strdayuse = strdayuse + "7;".
                IF mealcoup.verbrauch[8] NE 0 THEN strdayuse = strdayuse + "8;".
                IF mealcoup.verbrauch[9] NE 0 THEN strdayuse = strdayuse + "9;".
                IF mealcoup.verbrauch[10] NE 0 THEN strdayuse = strdayuse + "10;".
                IF mealcoup.verbrauch[11] NE 0 THEN strdayuse = strdayuse + "11;".
                IF mealcoup.verbrauch[12] NE 0 THEN strdayuse = strdayuse + "12;".
                IF mealcoup.verbrauch[13] NE 0 THEN strdayuse = strdayuse + "13;".
                IF mealcoup.verbrauch[14] NE 0 THEN strdayuse = strdayuse + "14;".
                IF mealcoup.verbrauch[15] NE 0 THEN strdayuse = strdayuse + "15;".
                IF mealcoup.verbrauch[16] NE 0 THEN strdayuse = strdayuse + "16;".
                IF mealcoup.verbrauch[17] NE 0 THEN strdayuse = strdayuse + "17;".
                IF mealcoup.verbrauch[18] NE 0 THEN strdayuse = strdayuse + "18;".
                IF mealcoup.verbrauch[19] NE 0 THEN strdayuse = strdayuse + "19;".
                IF mealcoup.verbrauch[20] NE 0 THEN strdayuse = strdayuse + "20;".
                IF mealcoup.verbrauch[21] NE 0 THEN strdayuse = strdayuse + "21;".
                IF mealcoup.verbrauch[22] NE 0 THEN strdayuse = strdayuse + "22;".
                IF mealcoup.verbrauch[23] NE 0 THEN strdayuse = strdayuse + "23;".
                IF mealcoup.verbrauch[24] NE 0 THEN strdayuse = strdayuse + "24;".
                IF mealcoup.verbrauch[25] NE 0 THEN strdayuse = strdayuse + "25;".
                IF mealcoup.verbrauch[26] NE 0 THEN strdayuse = strdayuse + "26;".
                IF mealcoup.verbrauch[27] NE 0 THEN strdayuse = strdayuse + "27;".
                IF mealcoup.verbrauch[28] NE 0 THEN strdayuse = strdayuse + "28;".
                IF mealcoup.verbrauch[29] NE 0 THEN strdayuse = strdayuse + "29;".
                IF mealcoup.verbrauch[30] NE 0 THEN strdayuse = strdayuse + "30;".
                IF mealcoup.verbrauch[31] NE 0 THEN strdayuse = strdayuse + "31;".
                IF mealcoup.verbrauch[32] NE 0 THEN strdayuse = strdayuse + "32".

                IF mealcoup.resnr = 7 THEN 
                    MESSAGE strdayuse
                        VIEW-AS ALERT-BOX INFO BUTTONS OK.

            DO i =  1 TO getDatanr:
               dateval = INT(ENTRY(i, strdayuse, ";")).
               RUN fill-data(i, dateval). 
            END.
            
        END.
    END.
END.
ELSE 
DO:
    FOR EACH mealcoup WHERE mealcoup.NAME = mealTime 
        AND fdate GT mealcoup.ankunft AND fdate LE mealcoup.abreise 
        AND mealcoup.zinr MATCHES("*" + room + "*") NO-LOCK:

        /*getDataNr = fdate - mealcoup.ankunft.*/
        getDataNr = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                  + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                  + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                  + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                  + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                  + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                  + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].

        FIND FIRST res-line WHERE res-line.resnr = mealcoup.resnr 
            AND res-line.zinr = mealcoup.zinr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest THEN FIND FIRST guest WHERE guest.gastnr = res-line.gastnr.
            RUN fill-data(getDataNr).
        END.
    END.
END.
*/

IF fdate EQ ? THEN
DO:
    FOR EACH mealcoup WHERE mealcoup.NAME = mealTime
        AND mealcoup.zinr MATCHES("*" + room + "*") NO-LOCK:
        FIND FIRST res-line WHERE res-line.resnr = mealcoup.resnr AND res-line.zinr = mealcoup.zinr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN 
        DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest THEN FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-ERROR.
            getDataNr = 0.
            /*
            getDataNr = mealcoup.abreise - mealcoup.ankunft.
            getDataNr = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                      + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                      + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                      + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                      + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                      + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                      + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
            */
            DO ii = 1 TO 32:
                IF mealcoup.verbrauch[ii] NE 0 THEN
                getDataNr = getDataNr + 1.
            END.
            
            strdayuse = "".
            IF mealcoup.verbrauch[1]  NE 0 THEN strdayuse = "1;".
            IF mealcoup.verbrauch[2]  NE 0 THEN strdayuse = strdayuse + "2;".  
            IF mealcoup.verbrauch[3]  NE 0 THEN strdayuse = strdayuse + "3;".                                 
            IF mealcoup.verbrauch[4]  NE 0 THEN strdayuse = strdayuse + "4;".
            IF mealcoup.verbrauch[5]  NE 0 THEN strdayuse = strdayuse + "5;".
            IF mealcoup.verbrauch[6]  NE 0 THEN strdayuse = strdayuse + "6;".
            IF mealcoup.verbrauch[7]  NE 0 THEN strdayuse = strdayuse + "7;".
            IF mealcoup.verbrauch[8]  NE 0 THEN strdayuse = strdayuse + "8;".
            IF mealcoup.verbrauch[9]  NE 0 THEN strdayuse = strdayuse + "9;".
            IF mealcoup.verbrauch[10] NE 0 THEN strdayuse = strdayuse + "10;".
            IF mealcoup.verbrauch[11] NE 0 THEN strdayuse = strdayuse + "11;".
            IF mealcoup.verbrauch[12] NE 0 THEN strdayuse = strdayuse + "12;".
            IF mealcoup.verbrauch[13] NE 0 THEN strdayuse = strdayuse + "13;".
            IF mealcoup.verbrauch[14] NE 0 THEN strdayuse = strdayuse + "14;".
            IF mealcoup.verbrauch[15] NE 0 THEN strdayuse = strdayuse + "15;".
            IF mealcoup.verbrauch[16] NE 0 THEN strdayuse = strdayuse + "16;".
            IF mealcoup.verbrauch[17] NE 0 THEN strdayuse = strdayuse + "17;".
            IF mealcoup.verbrauch[18] NE 0 THEN strdayuse = strdayuse + "18;".
            IF mealcoup.verbrauch[19] NE 0 THEN strdayuse = strdayuse + "19;".
            IF mealcoup.verbrauch[20] NE 0 THEN strdayuse = strdayuse + "20;".
            IF mealcoup.verbrauch[21] NE 0 THEN strdayuse = strdayuse + "21;".
            IF mealcoup.verbrauch[22] NE 0 THEN strdayuse = strdayuse + "22;".
            IF mealcoup.verbrauch[23] NE 0 THEN strdayuse = strdayuse + "23;".
            IF mealcoup.verbrauch[24] NE 0 THEN strdayuse = strdayuse + "24;".
            IF mealcoup.verbrauch[25] NE 0 THEN strdayuse = strdayuse + "25;".
            IF mealcoup.verbrauch[26] NE 0 THEN strdayuse = strdayuse + "26;".
            IF mealcoup.verbrauch[27] NE 0 THEN strdayuse = strdayuse + "27;".
            IF mealcoup.verbrauch[28] NE 0 THEN strdayuse = strdayuse + "28;".
            IF mealcoup.verbrauch[29] NE 0 THEN strdayuse = strdayuse + "29;".
            IF mealcoup.verbrauch[30] NE 0 THEN strdayuse = strdayuse + "30;".
            IF mealcoup.verbrauch[31] NE 0 THEN strdayuse = strdayuse + "31;".
            IF mealcoup.verbrauch[32] NE 0 THEN strdayuse = strdayuse + "32".
        
            DO i =  1 TO getDatanr:
                dateval = INT(ENTRY(i, strdayuse, ";")).
                RUN fill-data(i, dateval). 
            END.      
        END.
    END.
END.
ELSE DO:
    FOR EACH mealcoup WHERE mealcoup.NAME = mealTime
        AND fdate GT mealcoup.ankunft AND fdate LE mealcoup.abreise
        AND mealcoup.zinr MATCHES("*" + room + "*") NO-LOCK:
        FIND FIRST res-line WHERE res-line.resnr = mealcoup.resnr AND res-line.zinr = mealcoup.zinr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN 
        DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest THEN FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-ERROR.
            getDataNr = 0.
            /*
            getDataNr = mealcoup.abreise - mealcoup.ankunft.
            getDataNr = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                      + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                      + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                      + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                      + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                      + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                      + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
            */
            DO ii = 1 TO 32:
                IF mealcoup.verbrauch[ii] NE 0 THEN
                getDataNr = getDataNr + 1.
            END.
            
            strdayuse = "".
            IF mealcoup.verbrauch[1]  NE 0 THEN strdayuse = "1;".
            IF mealcoup.verbrauch[2]  NE 0 THEN strdayuse = strdayuse + "2;".  
            IF mealcoup.verbrauch[3]  NE 0 THEN strdayuse = strdayuse + "3;".                                 
            IF mealcoup.verbrauch[4]  NE 0 THEN strdayuse = strdayuse + "4;".
            IF mealcoup.verbrauch[5]  NE 0 THEN strdayuse = strdayuse + "5;".
            IF mealcoup.verbrauch[6]  NE 0 THEN strdayuse = strdayuse + "6;".
            IF mealcoup.verbrauch[7]  NE 0 THEN strdayuse = strdayuse + "7;".
            IF mealcoup.verbrauch[8]  NE 0 THEN strdayuse = strdayuse + "8;".
            IF mealcoup.verbrauch[9]  NE 0 THEN strdayuse = strdayuse + "9;".
            IF mealcoup.verbrauch[10] NE 0 THEN strdayuse = strdayuse + "10;".
            IF mealcoup.verbrauch[11] NE 0 THEN strdayuse = strdayuse + "11;".
            IF mealcoup.verbrauch[12] NE 0 THEN strdayuse = strdayuse + "12;".
            IF mealcoup.verbrauch[13] NE 0 THEN strdayuse = strdayuse + "13;".
            IF mealcoup.verbrauch[14] NE 0 THEN strdayuse = strdayuse + "14;".
            IF mealcoup.verbrauch[15] NE 0 THEN strdayuse = strdayuse + "15;".
            IF mealcoup.verbrauch[16] NE 0 THEN strdayuse = strdayuse + "16;".
            IF mealcoup.verbrauch[17] NE 0 THEN strdayuse = strdayuse + "17;".
            IF mealcoup.verbrauch[18] NE 0 THEN strdayuse = strdayuse + "18;".
            IF mealcoup.verbrauch[19] NE 0 THEN strdayuse = strdayuse + "19;".
            IF mealcoup.verbrauch[20] NE 0 THEN strdayuse = strdayuse + "20;".
            IF mealcoup.verbrauch[21] NE 0 THEN strdayuse = strdayuse + "21;".
            IF mealcoup.verbrauch[22] NE 0 THEN strdayuse = strdayuse + "22;".
            IF mealcoup.verbrauch[23] NE 0 THEN strdayuse = strdayuse + "23;".
            IF mealcoup.verbrauch[24] NE 0 THEN strdayuse = strdayuse + "24;".
            IF mealcoup.verbrauch[25] NE 0 THEN strdayuse = strdayuse + "25;".
            IF mealcoup.verbrauch[26] NE 0 THEN strdayuse = strdayuse + "26;".
            IF mealcoup.verbrauch[27] NE 0 THEN strdayuse = strdayuse + "27;".
            IF mealcoup.verbrauch[28] NE 0 THEN strdayuse = strdayuse + "28;".
            IF mealcoup.verbrauch[29] NE 0 THEN strdayuse = strdayuse + "29;".
            IF mealcoup.verbrauch[30] NE 0 THEN strdayuse = strdayuse + "30;".
            IF mealcoup.verbrauch[31] NE 0 THEN strdayuse = strdayuse + "31;".
            IF mealcoup.verbrauch[32] NE 0 THEN strdayuse = strdayuse + "32".
        
            DO i =  1 TO getDatanr:
                dateval = INT(ENTRY(i, strdayuse, ";")).
                RUN fill-data(i, dateval). 
            END.      
        END.
    END.
END.

/*Create Total Records*/
CREATE bfast-data.
ASSIGN
    bfast-data.roomNr        = "T O T A L"
    bfast-data.totalAdult    = sumAdult
    bfast-data.totalCompli   = sumCompl
    bfast-data.totalChild    = sumChild
    bfast-data.totalUse      = sumTotUse
    .

PROCEDURE fill-data:
    DEFINE INPUT PARAMETER used     AS INTEGER.
    DEFINE INPUT PARAMETER daycount AS INTEGER.

    DEFINE VARIABLE tDate       AS DATE.
    DEFINE VARIABLE totAdult    AS INTEGER.
    DEFINE VARIABLE totCompli   AS INTEGER.
    DEFINE VARIABLE totChild    AS INTEGER.
    DEFINE VARIABLE j           AS INTEGER.
    DEFINE VARIABLE tmpStr      AS CHARACTER.
    DEFINE VARIABLE tmpint      AS INTEGER.
    DEFINE VARIABLE day-use     AS DATE.

    tDate = mealcoup.ankunft + used.
    day-use = mealcoup.ankunft + daycount.

    IF day-use EQ fdate THEN
    DO:
        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
        FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr:
            IF argt-line.argt-artnr = artGrp-abf AND MealTime = "Breakfast" THEN 
            DO:
                IF argt-line.fakt-modus = 3 AND (tDate - res-line.ankunft EQ 1) THEN DO: /*Second day of stay*/
                    totAdult = res-line.erwachs. 
                    totCompli = res-line.gratis.
                END.
                ELSE IF argt-line.fakt-modus = 6 AND (tDate - res-line.ankunft LE argt-line.intervall) THEN DO: /*Special*/
                    totAdult = res-line.erwachs.
                    totCompli = res-line.gratis.
                END.
                ELSE IF argt-line.fakt-modus NE 3 AND argt-line.fakt-modus NE 6 THEN DO: /*Daily or others*/
                    totAdult = res-line.erwachs.
                    totCompli = res-line.gratis.
                END.
        
                /*Mencari list umur anak, jika lebih dari 12 tahun di anggap adult*/
                DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                    IF ENTRY(j, res-line.zimmer-wunsch, ";") MATCHES "*ChAge*" THEN
                        tmpStr = SUBSTR(ENTRY(j, res-line.zimmer-wunsch, ";"),6).
                END.
        
                DO j = 1 TO res-line.kind1:
                    IF j > NUM-ENTRIES(tmpStr, ",") THEN LEAVE.
                    IF INT(ENTRY(j, tmpStr, ",")) GT 12 THEN tmpInt = tmpInt + 1.
                END.
        
                totAdult = totAdult + tmpInt.
                totChild = res-line.kind1 - tmpInt.
        
                sumAdult = sumAdult + totAdult.
                sumChild = sumChild + totChild.
                sumCompl = sumCompl + totCompli.
                /*
                IF argt-line.betriebsnr = 1 THEN  do: /*Quantity always 1*/
                    IF argt-line.fakt-modus = 3 AND (tDate - res-line.ankunft EQ 1) THEN 
                    DO: /*Second day of stay*/
                        totAdult = 1.
                        totCompli = 1.
                    END.
                    ELSE IF argt-line.fakt-modus = 6 AND (tDate - res-line.ankunft LE argt-line.intervall) THEN 
                    DO: /*Special*/
                        totAdult = 1.
                        totCompli = 1.
                    END.
                    ELSE IF argt-line.fakt-modus NE 3 AND argt-line.fakt-modus NE 6 THEN 
                    DO: /*Daily or others*/
                        totAdult = 1.
                        totCompli = 1.
                    END.
        
                    IF res-line.erwachs = 0 THEN totAdult = 0.
                    IF res-line.gratis  = 0 THEN totCompli = 0.
        
                    /*Mencari list umur anak*/
                    DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                        IF ENTRY(j, res-line.zimmer-wunsch, ";") EQ "ChAge" THEN
                            tmpStr = ENTRY(j, res-line.zimmer-wunsch, ";").
                    END.
                    
                    DO j = 1 TO res-line.kind1:
                        IF j > NUM-ENTRIES(tmpStr, ",") THEN LEAVE.
                        IF INT(ENTRY(j, tmpStr, ",")) GT 12 THEN tmpInt = tmpInt + 1.
                    END.
                    IF tmpInt GT 0 THEN totAdult = 1.
                    totChild = res-line.kind1 - tmpInt.
                    sumAdult = sumAdult + totAdult.
                    sumChild = sumChild + totChild.
                    sumCompl = sumCompl + totCompli.
                END.
                ELSE 
                DO: /*Not Quantity always one*/
                    IF argt-line.fakt-modus = 3 AND (tDate - res-line.ankunft EQ 1) THEN DO: /*Second day of stay*/
                        totAdult = res-line.erwachs. 
                        totCompli = res-line.gratis.
                    END.
                    ELSE IF argt-line.fakt-modus = 6 AND (tDate - res-line.ankunft LE argt-line.intervall) THEN DO: /*Special*/
                        totAdult = res-line.erwachs.
                        totCompli = res-line.gratis.
                    END.
                    ELSE IF argt-line.fakt-modus NE 3 AND argt-line.fakt-modus NE 6 THEN DO: /*Daily or others*/
                        totAdult = res-line.erwachs.
                        totCompli = res-line.gratis.
                    END.
        
                    /*Mencari list umur anak, jika lebih dari 12 tahun di anggap adult*/
                    DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                        IF ENTRY(j, res-line.zimmer-wunsch, ";") MATCHES "*ChAge*" THEN
                            tmpStr = SUBSTR(ENTRY(j, res-line.zimmer-wunsch, ";"),6).
                    END.
        
                    DO j = 1 TO res-line.kind1:
                        IF j > NUM-ENTRIES(tmpStr, ",") THEN LEAVE.
                        IF INT(ENTRY(j, tmpStr, ",")) GT 12 THEN tmpInt = tmpInt + 1.
                    END.
        
                    totAdult = totAdult + tmpInt.
                    totChild = res-line.kind1 - tmpInt.
        
                    sumAdult = sumAdult + totAdult.
                    sumChild = sumChild + totChild.
                    sumCompl = sumCompl + totCompli.
                END.*/
        
            END.
        END.
        
        /* FIND FIRST mealcoup WHERE meal-coup. NO-ERROR.*/
        CREATE bfast-data.
        ASSIGN
            bfast-data.tDate         = day-use
            bfast-data.roomNr        = mealcoup.zinr
            bfast-data.resNr         = mealcoup.resnr
            bfast-data.guestNr       = guest.gastnr
            bfast-data.guestName     = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
            bfast-data.totalAdult    = totAdult
            bfast-data.totalCompli   = totCompli
            bfast-data.totalChild    = totChild
            bfast-data.totalUse      = mealcoup.verbrauch[daycount]
            sumTotUse                = sumTotUse + mealcoup.verbrauch[daycount].
        END.
END PROCEDURE.
