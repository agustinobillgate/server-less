DEFINE TEMP-TABLE tmp-resline LIKE res-line.

DEFINE TEMP-TABLE tmp-extra 
    FIELD reihe     AS INTEGER INITIAL 0
    FIELD typ-pos   AS CHAR
    FIELD pos-from  AS CHAR
    FIELD cdate     AS DATE
    FIELD room      AS CHAR
    FIELD qty       AS INTEGER
    FIELD rsvno     AS INTEGER.

DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER art-nr          AS INTEGER.
DEF INPUT PARAMETER fdate           AS DATE.
DEF INPUT PARAMETER tdate           AS DATE.

DEF OUTPUT PARAMETER TABLE FOR tmp-extra.

DEF VAR bdate    AS DATE.
DEF VAR edate    AS DATE.
DEF VAR eposdate AS DATE.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "hk-availextra". 

RUN create-data.

PROCEDURE create-data :
    
    DEF VAR do-it  AS LOGICAL.
    DEF VAR argtnr   AS INTEGER.

    
    FOR EACH tmp-resline :
        DELETE tmp-resline.
    END.
    FOR EACH tmp-extra :
        DELETE tmp-extra.
    END.

    FOR EACH res-line WHERE NOT (res-line.abreise LT fdate) AND NOT (res-line.ankunft GT tdate) 
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK BY res-line.resnr :
        CREATE tmp-resline.
        BUFFER-COPY res-line TO tmp-resline.
    END.    

    FOR EACH tmp-resline BY tmp-resline.resnr :
        FOR EACH fixleist WHERE fixleist.resnr = tmp-resline.resnr 
            AND fixleist.reslinnr = tmp-resline.reslinnr
            AND fixleist.artnr = art-nr 
            AND fixleist.departement = 0 NO-LOCK :
           
            IF tmp-resline.ankunft = tmp-resline.abreise THEN
            DO:
                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 6 THEN
                    RUN create-tmpExtra (0, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).   
                ELSE IF fixleist.sequenz = 4 THEN
                    IF DAY(tmp-resline.ankunft) = 1 THEN 
                        RUN create-tmpExtra ("Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
                ELSE IF fixleist.sequenz = 5 THEN
                    IF DAY(tmp-resline.ankunft + 1) = 1 THEN 
                        RUN create-tmpExtra (0, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
            END.
            ELSE
            DO:
                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 4 OR fixleist.sequenz = 5 THEN
                DO:
                    IF tmp-resline.ankunft < fdate THEN
                        bdate = fdate.
                    ELSE
                        bdate = tmp-resline.ankunft.
    
                    IF tmp-resline.abreise GT tdate THEN /* IF tmp-resline.abreise > tdate THEN */
                        edate = tdate.
                    ELSE 
                        edate = tmp-resline.abreise.
                END.

                IF fixleist.sequenz = 1 THEN
                DO:
                    DO WHILE bdate LE edate :
                        IF tmp-resline.abreise GT bdate THEN
                          RUN create-tmpExtra (0, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).    
                        ELSE IF tmp-resline.abreise = bdate AND tmp-resline.abreisezeit GE (18 * 3600) THEN
                        DO:
                          RUN create-tmpExtra (1, "Dayuse", "1", bdate, tmp-resline.zinr 
                              + " " + translateExtended ("DayUse till",lvCAREA,"") 
                              + " " + STRING(tmp-resline.abreisezeit, "HH:MM"), 0).
                        END.
                        bdate = bdate + 1.
                    END.
                END.
                ELSE IF fixleist.sequenz = 2 THEN
                DO:
                    RUN create-tmpExtra (0, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).
                END.
                ELSE IF fixleist.sequenz = 4 THEN
                DO:
                     DO WHILE bdate LE edate :
                        IF DAY(bdate) = 1 AND tmp-resline.abreise GT bdate THEN 
                             RUN create-tmpExtra (0, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).    
                        ELSE IF DAY(bdate) = 1 AND tmp-resline.abreise = bdate AND tmp-resline.abreisezeit GE (18 * 3600) THEN
                            RUN create-tmpExtra (1, "Dayuse", "1", bdate, tmp-resline.zinr 
                                + " " + translateExtended ("DayUse till",lvCAREA,"") + " " + STRING(tmp-resline.abreisezeit, "HH:MM"), 0).    
                        bdate = bdate + 1.
                    END.
                END.
                ELSE IF fixleist.sequenz = 5 THEN
                DO:
                    DO WHILE bdate LE edate :
                        IF DAY(bdate + 1) = 1 AND tmp-resline.abreise LT bdate THEN 
                            RUN create-tmpExtra (0, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number). 
                        ELSE IF DAY(bdate + 1) = 1 AND tmp-resline.abreise = bdate AND tmp-resline.abreisezeit GE (18 * 3600) THEN
                            RUN create-tmpExtra (1, "Dayuse", "1", bdate, tmp-resline.zinr 
                                + " " + translateExtended ("DayUse till",lvCAREA,"") + " " + STRING(tmp-resline.abreisezeit, "HH:MM"), 0).    
                        bdate = bdate + 1.
                    END.
                END.
                ELSE IF fixleist.sequenz = 6 THEN
                DO:
                    eposdate = (fixleist.lfakt + fixleist.dekade - 1).

                    IF fixleist.lfakt LE fdate THEN
                        bdate = fdate.
                    ELSE
                        bdate = fixleist.lfakt.

                    IF eposdate > tdate THEN
                        edate = tdate.
                    ELSE IF eposdate <= tdate THEN
                    DO:
                        IF eposdate GE tmp-resline.abreise THEN
                            edate = tmp-resline.abreise.
                        ELSE 
                            edate = eposdate.
                    END.    
                        

                    DO WHILE bdate LE edate :
                        IF tmp-resline.abreise GT bdate THEN
                            RUN create-tmpExtra (0, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).
                        ELSE IF tmp-resline.abreise = bdate AND tmp-resline.abreisezeit GE (18 * 3600) THEN
                            RUN create-tmpExtra (1, "Dayuse", "1", bdate, tmp-resline.zinr 
                                + " " + translateExtended ("DayUse till",lvCAREA,"") + " " + STRING(tmp-resline.abreisezeit, "HH:MM"), 0).    
                        bdate = bdate + 1.
                    END.

                END.
            END.
        END.
    
        FIND FIRST arrangement WHERE arrangement.arrangement = tmp-resline.arrangement NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN ASSIGN argtnr = arrangement.argtnr.    

        FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
            AND reslin-queasy.resnr = tmp-resline.resnr 
            /*MT 28052012 */
            AND reslin-queasy.reslinnr = tmp-resline.reslinnr 
            AND reslin-queasy.number1 = 0 
            AND reslin-queasy.number3 = art-nr
            AND reslin-queasy.number2 = argtnr NO-LOCK :
    
            IF reslin-queasy.date1 < fdate THEN
                bdate = fdate.
            ELSE
                bdate = reslin-queasy.date1.
    
            IF reslin-queasy.date2 > tdate THEN
                edate = tdate.
            ELSE
                edate = reslin-queasy.date2.
           
            DO WHILE bdate LE edate :
                IF tmp-resline.abreise GT bdate THEN
                    RUN create-tmpExtra (0, "argt line", "0", bdate, tmp-resline.zinr, 1).
                ELSE IF tmp-resline.abreise = bdate AND tmp-resline.abreisezeit GE (18 * 3600) THEN
                    RUN create-tmpExtra (1, "Dayuse", "1", bdate, tmp-resline.zinr 
                        + " " + translateExtended ("DayUse till",lvCAREA,"") + " " + STRING(tmp-resline.abreisezeit, "HH:MM"), 0).    
                bdate = bdate + 1.
            END.
        END.
    END.
END.

PROCEDURE create-tmpExtra:
DEFINE INPUT PARAMETER reihe    AS INTEGER.
DEFINE INPUT PARAMETER typ-pos  AS CHAR.
DEFINE INPUT PARAMETER pos-from AS CHAR.
DEFINE INPUT PARAMETER cdate    AS DATE.
DEFINE INPUT PARAMETER room     AS  CHAR.
DEFINE INPUT PARAMETER qty      AS INTEGER.

CREATE tmp-extra. 
ASSIGN tmp-extra.typ-pos    = typ-pos
       tmp-extra.pos-from   = pos-from
       tmp-extra.cdate      = cdate
       tmp-extra.room       = room
       tmp-extra.qty        = qty
       tmp-extra.reihe      = reihe
       tmp-extra.rsvno      = tmp-resline.resnr.
END.
