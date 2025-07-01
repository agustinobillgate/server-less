DEFINE INPUT PARAMETER res-number        AS INT.
DEFINE INPUT PARAMETER resline-number    AS INT.
DEFINE INPUT PARAMETER est-AT            AS INT.
DEFINE INPUT PARAMETER pickrequest       AS LOGICAL INIT NO.
DEFINE INPUT PARAMETER pickdetail        AS CHAR.
DEFINE INPUT PARAMETER room-preferences  AS CHAR.
DEFINE INPUT PARAMETER spesial-req       AS CHAR.
DEFINE INPUT PARAMETER guest-phnumber    AS CHAR.
DEFINE INPUT PARAMETER guest-nationality AS CHAR.
DEFINE INPUT PARAMETER guest-country     AS CHAR.
DEFINE INPUT PARAMETER guest-region      AS CHAR.
DEFINE INPUT PARAMETER agreed-term       AS LOGICAL INIT NO.
DEFINE INPUT PARAMETER purpose-of-stay   AS CHAR.

DEFINE OUTPUT PARAMETER mess-result      AS CHAR.

DEF VAR segm_purcode AS INT.

IF res-number EQ 0 OR res-number EQ ? OR resline-number EQ 0 OR resline-number EQ ? THEN
DO:
    mess-result = "1 - Reservation Number and Line can't be null!".
    RETURN.
END.

IF purpose-of-stay EQ "" OR purpose-of-stay EQ ? THEN
DO:
    mess-result = "2 - Purpose Of Stay can't be null!".
    RETURN.
END.

IF pickdetail        EQ ? THEN pickdetail        = "".
IF room-preferences  EQ ? THEN room-preferences  = "".
IF spesial-req       EQ ? THEN spesial-req       = "".
IF guest-phnumber    EQ ? THEN guest-phnumber    = "".
IF guest-nationality EQ ? THEN guest-nationality = "".
IF guest-country     EQ ? THEN guest-country     = "".
IF guest-region      EQ ? THEN guest-region      = "".

FIND FIRST res-line WHERE res-line.resnr EQ res-number 
AND res-line.reslinnr EQ resline-number EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.char3 EQ purpose-of-stay NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN ASSIGN segm_purcode = queasy.number1.

    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        ASSIGN 
            guest.mobil-telefon = guest-phnumber                       
            guest.nation1       = guest-nationality
            guest.land          = guest-country    
            guest.geburt-ort2   = guest-region.    
    END.
    ASSIGN 
        res-line.abreisezeit   = est-AT
        res-line.zimmer-wunsch = res-line.zimmer-wunsch 
                                 + "PCIFLAG=YES|PICKUP=" + STRING(pickrequest) 
                                 + "|PICKDETAIL=" + pickdetail 
                                 + "|ROOMREF=" + room-preferences 
                                 + "|TERM=" + STRING(agreed-term) 
                                 + ";SEGM_PUR" + STRING(segm_purcode) 
                                 + ";".



                                   
    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
    AND reslin-queasy.resnr EQ res-line.resnr 
    AND reslin-queasy.reslinnr EQ res-line.reslinnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN
        ASSIGN reslin-queasy.char3 = reslin-queasy.char3 + "," + spesial-req. 
    ELSE
    DO:
        CREATE reslin-queasy.
        ASSIGN 
            reslin-queasy.KEY      = "specialRequest" 
            reslin-queasy.resnr    = res-line.resnr
            reslin-queasy.reslinnr = res-line.reslinnr
            .
    END.
    mess-result = "0 - update data success".
END.
