DEFINE TEMP-TABLE om-list 
  FIELD zinr AS CHAR 
  FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID" 
  FIELD ind AS INTEGER INITIAL 0
  FIELD reason      AS CHAR 
  FIELD gespstart   AS DATE 
  FIELD gespende    AS DATE.

DEFINE TEMP-TABLE ooo-list
    FIELD zinr      LIKE outorder.zinr 
    FIELD gespgrund LIKE outorder.gespgrund
    FIELD gespstart LIKE outorder.gespstart
    FIELD gespende  LIKE outorder.gespende
    FIELD userinit  LIKE om-list.userinit
    FIELD etage     LIKE zimmer.etage
    FIELD ind       LIKE om-list.ind
    FIELD bezeich   LIKE zimmer.bezeich
    FIELD betriebsnr LIKE outorder.betriebsnr
    FIELD selected-om AS LOGICAL INITIAL NO
    FIELD rec-id      AS INTEGER
    .

DEFINE INPUT PARAMETER TABLE FOR om-list.
DEFINE INPUT PARAMETER fdate     AS DATE NO-UNDO.
DEFINE INPUT PARAMETER tdate     AS DATE NO-UNDO.
DEFINE INPUT PARAMETER disptype  AS INT  NO-UNDO.
DEFINE INPUT PARAMETER sorttype  AS INT  NO-UNDO.
DEFINE INPUT PARAMETER user-init AS CHAR NO-UNDO.

DEFINE OUTPUT PARAMETER ci-date  AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR ooo-list.

FOR EACH ooo-list:
    DELETE ooo-list.
END.

/* FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. */ /* malik serverless */

RUN htpdate.p (87, OUTPUT ci-date).

IF fdate = ? AND tdate = ? THEN
  RUN disp-it. 
ELSE IF fdate NE ? AND tdate NE ? THEN
  RUN disp-it1.


PROCEDURE disp-it: 
  IF disptype = 0 THEN 
  DO: 
    IF sorttype = 0 THEN 
    FOR EACH outorder NO-LOCK, 
      FIRST om-list WHERE om-list.zinr = outorder.zinr 
        AND om-list.gespstart = outorder.gespstart
        AND om-list.gespende = outorder.gespende
        NO-LOCK,
      FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
      BY (outorder.zinr):
        RUN assign-it.
    END.
    ELSE 
    FOR EACH outorder NO-LOCK, 
      FIRST om-list WHERE om-list.zinr = outorder.zinr 
        AND om-list.gespstart = outorder.gespstart
        AND om-list.gespende = outorder.gespende
        NO-LOCK,
      FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
      BY outorder.betriebsnr BY (outorder.zinr):
        RUN assign-it.
    END.
  END. 
  ELSE IF disptype = 1 THEN 
  DO: 
    IF sorttype = 0 THEN 
    FOR EACH outorder NO-LOCK, 
      FIRST om-list WHERE om-list.zinr = outorder.zinr 
        AND om-list.ind NE 3 
        AND om-list.gespstart = outorder.gespstart
        AND om-list.gespende = outorder.gespende NO-LOCK, 
      FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
        BY (outorder.zinr):
      RUN assign-it.
    END.
    ELSE 
    FOR EACH outorder NO-LOCK, 
      FIRST om-list WHERE om-list.zinr = outorder.zinr 
        AND om-list.ind NE 3
        AND om-list.gespstart = outorder.gespstart
        AND om-list.gespende = outorder.gespende NO-LOCK, 
      FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
        BY outorder.betriebsnr BY (outorder.zinr):
      RUN assign-it.
    END.
  END. 
  ELSE IF disptype = 2 THEN 
  DO: 
    IF sorttype = 0 THEN 
    FOR EACH outorder NO-LOCK, 
      FIRST om-list WHERE om-list.zinr = outorder.zinr 
        AND om-list.ind EQ 3
        AND om-list.gespstart = outorder.gespstart
        AND om-list.gespende = outorder.gespende NO-LOCK, 
      FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
        BY (outorder.zinr):
      RUN assign-it.
    END.
    ELSE
    FOR EACH outorder NO-LOCK, 
      FIRST om-list WHERE om-list.zinr = outorder.zinr 
        AND om-list.ind EQ 3
        AND om-list.gespstart = outorder.gespstart
        AND om-list.gespende = outorder.gespende NO-LOCK, 
      FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
        BY outorder.betriebsnr BY (outorder.zinr):
      RUN assign-it.
    END.
  END.
END.

PROCEDURE disp-it1: 
  IF disptype = 0 THEN 
  DO: 
    IF sorttype = 0 THEN
      FOR EACH outorder NO-LOCK,
        FIRST om-list WHERE om-list.zinr = outorder.zinr 
          AND om-list.gespstart = outorder.gespstart
          AND om-list.gespende = outorder.gespende
          NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
        BY (outorder.zinr):
        RUN assign-it.
      END.
    ELSE 
      FOR EACH outorder NO-LOCK,
        FIRST om-list WHERE om-list.zinr = outorder.zinr 
          AND om-list.gespstart = outorder.gespstart
          AND om-list.gespende = outorder.gespende
          NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
          BY outorder.betriebsnr BY (outorder.zinr):
        RUN assign-it.
      END.
  END. 
  ELSE IF disptype = 1 THEN 
  DO: 
    IF sorttype = 0 THEN 
      FOR EACH outorder NO-LOCK,
        FIRST om-list WHERE om-list.zinr = outorder.zinr 
          AND om-list.ind NE 3 
          AND om-list.gespstart = outorder.gespstart
          AND om-list.gespende = outorder.gespende
          NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
          BY (outorder.zinr):
        RUN assign-it.
      END.
    ELSE 
      FOR EACH outorder NO-LOCK,
        FIRST om-list WHERE om-list.zinr = outorder.zinr 
          AND om-list.ind NE 3 
          AND om-list.gespstart = outorder.gespstart
          AND om-list.gespende = outorder.gespende
          NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
          BY outorder.betriebsnr BY (outorder.zinr):
         RUN assign-it.
      END.
  END. 
  ELSE IF disptype = 2 THEN 
  DO: 
    IF sorttype = 0 THEN 
      FOR EACH outorder NO-LOCK,
        FIRST om-list WHERE om-list.zinr = outorder.zinr 
          AND om-list.ind EQ 3 
          AND om-list.gespstart = outorder.gespstart
          AND om-list.gespende = outorder.gespende
          NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
          BY (outorder.zinr):
        RUN assign-it.
      END.
    ELSE
      FOR EACH outorder NO-LOCK,
        FIRST om-list WHERE om-list.zinr = outorder.zinr 
          AND om-list.ind EQ 3 
          AND om-list.gespstart = outorder.gespstart
          AND om-list.gespende = outorder.gespende
          NO-LOCK, 
        FIRST zimmer WHERE zimmer.zinr = outorder.zinr NO-LOCK 
          BY outorder.betriebsnr BY (outorder.zinr):
        RUN assign-it.
      END.
  END. 
END.


PROCEDURE assign-it:
    CREATE ooo-list.
    ASSIGN  
      ooo-list.zinr       = outorder.zinr 
      ooo-list.gespstart  = outorder.gespstart
      ooo-list.gespende   = outorder.gespende
      ooo-list.userinit   = om-list.userinit
      ooo-list.etage      = zimmer.etage
      ooo-list.bezeich    = zimmer.bezeich
      ooo-list.ind        = om-list.ind
      ooo-list.betriebsnr = outorder.betriebsnr
      ooo-list.rec-id     = RECID(outorder).

    IF om-list.reason MATCHES "*$*" THEN
        ooo-list.gespgrund = ENTRY(2,om-list.reason,"$").
    ELSE ooo-list.gespgrund  = om-list.reason.
END.

