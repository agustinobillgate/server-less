DEFINE INPUT PARAMETER resno     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER reslino   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER gastno    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER gdpr-flag AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER mark-flag AS LOGICAL.
DEFINE INPUT PARAMETER news-flag AS LOGICAL.
DEFINE VARIABLE tempzwunsch1 AS CHAR.
DEFINE VARIABLE tempzwunsch2 AS CHAR.
IF gdpr-flag EQ ? THEN gdpr-flag = NO.
IF mark-flag EQ ? THEN mark-flag = NO.
IF news-flag EQ ? THEN news-flag = NO.
    


MESSAGE 
    "resno     : " + string(resno    ) skip
    "reslino   : " + string(reslino  ) skip
    "gastno    : " + string(gastno   ) skip
    "gdpr-flag : " + string(gdpr-flag) skip
    "mark-flag : " + string(mark-flag) skip
    "news-flag : " + string(news-flag) skip
    VIEW-AS ALERT-BOX INFO BUTTONS OK.


FIND FIRST res-line WHERE res-line.resnr EQ resno 
    AND res-line.reslinnr EQ reslino 
    AND res-line.gastnrmember EQ gastno EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    IF NOT res-line.zimmer-wunsch MATCHES "*GDPR*" THEN 
        res-line.zimmer-wunsch = res-line.zimmer-wunsch + "GDPRyes;".
    ELSE IF res-line.zimmer-wunsch MATCHES "*GDPR*" THEN
    DO:
        tempzwunsch1 = res-line.zimmer-wunsch.
        IF tempzwunsch1 MATCHES "*GDPRyes*" THEN 
            tempzwunsch2 = REPLACE(tempzwunsch1,"GDPRyes","").
        ELSE IF tempzwunsch1 MATCHES "*GDPRno*" THEN 
            tempzwunsch2 = REPLACE(tempzwunsch1,"GDPRno","").
        ASSIGN 
            res-line.zimmer-wunsch = tempzwunsch2 + "GDPR" + STRING(gdpr-flag) + ";".
    END.
    IF mark-flag EQ YES THEN
    DO:
        IF NOT res-line.zimmer-wunsch MATCHES "*MARKETING*" THEN 
            res-line.zimmer-wunsch = res-line.zimmer-wunsch + "MARKETINGyes;".
        ELSE IF res-line.zimmer-wunsch MATCHES "*MARKETING*" THEN
        DO:
            tempzwunsch1 = res-line.zimmer-wunsch.
            IF tempzwunsch1 MATCHES "*MARKETINGyes*" THEN 
                tempzwunsch2 = REPLACE(tempzwunsch1,"MARKETINGyes","").
            ELSE IF tempzwunsch1 MATCHES "*MARKETINGno*" THEN 
                tempzwunsch2 = REPLACE(tempzwunsch1,"MARKETINGno","").
            ASSIGN 
                res-line.zimmer-wunsch = tempzwunsch2 + "MARKETING" + STRING(mark-flag) + ";".
        END.
    END.
    ELSE res-line.zimmer-wunsch = res-line.zimmer-wunsch + "MARKETINGno;".
    IF news-flag EQ YES THEN
    DO:
        IF NOT res-line.zimmer-wunsch MATCHES "*NEWSLETTER*" THEN 
            res-line.zimmer-wunsch = res-line.zimmer-wunsch + "NEWSLETTERyes;".
        ELSE IF res-line.zimmer-wunsch MATCHES "*NEWSLETTER*" THEN
        DO:
            tempzwunsch1 = res-line.zimmer-wunsch.
            IF tempzwunsch1 MATCHES "*NEWSLETTERyes*" THEN 
                tempzwunsch2 = REPLACE(tempzwunsch1,"NEWSLETTERyes","").
            ELSE IF tempzwunsch1 MATCHES "*NEWSLETTERno*" THEN 
                tempzwunsch2 = REPLACE(tempzwunsch1,"NEWSLETTERno","").
            ASSIGN 
                res-line.zimmer-wunsch = tempzwunsch2 + "NEWSLETTER" + STRING(news-flag) + ";".
        END.
    END.
    ELSE res-line.zimmer-wunsch = res-line.zimmer-wunsch + "NEWSLETTERno;".
END.
