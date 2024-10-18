
DEFINE INPUT PARAMETER froom        AS CHAR.
DEFINE INPUT PARAMETER troom        AS CHAR.
DEFINE INPUT PARAMETER curr-zinr    AS CHAR.
DEFINE INPUT PARAMETER gname        AS CHAR.
DEFINE INPUT PARAMETER ci-date      AS DATE.

FOR EACH zimmer WHERE zimmer.zinr GE froom AND zimmer.zinr LE troom 
    NO-LOCK BY (zimmer.zinr): 
    FIND FIRST interface WHERE interface.key = 2 
      AND interface.zinr = zimmer.zinr 
      AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE interface: 
      FIND CURRENT interface EXCLUSIVE-LOCK. 
      delete interface. 
      FIND NEXT interface WHERE interface.key = 2 
        AND interface.zinr = zimmer.zinr 
        AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
    END. 
    curr-zinr = zimmer.zinr. 
    FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
      AND res-line.resstatus = 6 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line THEN
    FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr 
      AND res-line.resstatus = 13 NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN 
    DO: 
      gname = res-line.name. 
      RUN intevent-1.p( 1, res-line.zinr, "Manual Checkin!", 
        res-line.resnr, res-line.reslinnr). 
    END. 
    ELSE 
    DO: 
      gname = "Vacant". 
      FIND FIRST res-line WHERE res-line.resstatus = 8 
          AND res-line.abreise = ci-date
          AND NOT res-line.zimmerfix NO-LOCK NO-ERROR.
      IF NOT AVAILABLE res-line THEN
      FIND FIRST res-line WHERE res-line.resstatus = 8 
          AND res-line.abreise = ci-date NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
        RUN intevent-1.p( 2, zimmer.zinr, "Manual Checkout!", res-line.resnr,
                          res-line.reslinnr). 
      ELSE RUN intevent-1.p( 2, zimmer.zinr, "Manual Checkout!", 0, 0). 
    END. 
END. 
