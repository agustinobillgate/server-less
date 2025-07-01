DEF TEMP-TABLE s-list   
    FIELD grpname  AS CHAR FORMAT "x(24)"    LABEL "Group Name" INITIAL ""   
    FIELD ankunft  AS DATE LABEL "Arrival"   INITIAL ?   
    FIELD abreise  AS DATE LABEL "Departure" INITIAL ?   
    FIELD anzahl   AS INTEGER FORMAT ">>9"   LABEL "QTY" INITIAL 0.   
  
DEF INPUT  PARAM pvILanguage    AS INTEGER         NO-UNDO.  
DEF INPUT  PARAM resNo          AS INTEGER         NO-UNDO.  
DEF INPUT  PARAM user-init      AS CHAR            NO-UNDO.  
DEF INPUT  PARAM TABLE          FOR s-list.  
DEF OUTPUT PARAM created        AS LOGICAL INIT NO NO-UNDO.  
DEF OUTPUT PARAM msg-str        AS CHAR INIT ""    NO-UNDO.  
  
DEF VARIABLE new-resnr          AS INTEGER         NO-UNDO.  
  
DEF BUFFER bguest FOR guest.
DEF BUFFER rline1 FOR res-line.   
DEF BUFFER rline2 FOR res-line.   
DEF BUFFER reser1 FOR reservation.   
DEF BUFFER reser2 FOR reservation.   
  
{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "reservation".

FOR EACH rline1 WHERE rline1.resnr = resNo NO-LOCK,
    FIRST bguest WHERE bguest.gastnr = rLine1.gastnr
    AND bguest.karteityp = 0 NO-LOCK:
    msg-str = translateExtended ("One of this line has been modified to individual guest!
                                 Changed not possible!",lvCAREA,"").
    RETURN.
END.
IF msg-str NE "" THEN RETURN.
  
FIND FIRST reser1 WHERE reser1.resnr = resNo NO-LOCK.   
FOR EACH s-list:   
  RUN get-NewResNo(OUTPUT new-resnr).  
  CREATE reser2.   
  BUFFER-COPY reser1 EXCEPT resnr useridmutat mutdat depositbez   
    zahldatum zahlkonto depositbez2 zahldatum2 zahlkonto2 TO reser2.   
  ASSIGN   
    reser2.resnr        = new-resnr   
    reser2.groupname    = s-list.grpname   
    reser2.useridanlage = user-init  
    created             = YES  
  .   
  FIND CURRENT reser2 NO-LOCK.   
  RELEASE reser2.   
  FOR EACH rline1 WHERE rline1.resnr = resNo   
    AND rline1.active-flag LE 1 AND rline1.resstatus NE 12 NO-LOCK:   
    CREATE rline2.   
    BUFFER-COPY rline1 EXCEPT resnr betrieb-gast zinr flight-nr kontignr   
      TO rline2.   
    ASSIGN   
      rline2.resnr          = new-resnr   
      rline2.active-flag    = 0   
      rline2.resstatus      = 3   
      rline2.ankunft        = s-list.ankunft   
      rline2.abreise        = s-list.abreise   
      rline2.anztage        = s-list.abreise - s-list.ankunft   
      rline2.zimmeranz      = s-list.anzahl   
      rline2.reserve-char   = STRING(TODAY) + STRING(TIME,"HH:MM") + user-init  
    .   
    FIND CURRENT rline2 NO-LOCK.   
    RELEASE rline2.   
    RUN add-resplan(new-resnr, rline1.reslinnr).   
    RUN check-fixedrate(rline1.resnr, rline1.reslinnr, new-resnr).   
    RUN create-logfile(new-resnr, rline1.reslinnr).   
  END.   
END.  
  
PROCEDURE get-NewResNo:  
DEF OUTPUT PARAMETER resNo AS INTEGER.  
  RUN get-newresnobl.p (OUTPUT resNo).  
END.  
  
PROCEDURE add-resplan:   
DEF INPUT PARAMETER resnr    AS INTEGER NO-UNDO.   
DEF INPUT PARAMETER reslinnr AS INTEGER NO-UNDO.   
  
DEF VAR curr-date            AS DATE    NO-UNDO.   
DEF VAR beg-datum            AS DATE    NO-UNDO.   
DEF VAR end-datum            AS DATE    NO-UNDO.   
DEF VAR i                    AS INTEGER NO-UNDO.   
  
DEF BUFFER rline             FOR res-line.
DEF BUFFER rbuff             FOR resplan.
   
  FIND FIRST rline WHERE rline.resnr = resnr   
    AND rline.reslinnr = reslinnr NO-LOCK.   
  i = rline.resstatus.   
  FIND FIRST zimkateg WHERE zimkateg.zikatnr = rline.zikatnr NO-LOCK.   
  ASSIGN  
    beg-datum = rline.ankunft  
    end-datum = rline.abreise - 1  
    curr-date = beg-datum  
  .   
  DO curr-date = beg-datum TO end-datum:   
    FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr   
      AND resplan.datum = curr-date EXCLUSIVE-LOCK NO-ERROR.   
    IF NOT AVAILABLE resplan THEN   
    DO:   
      CREATE resplan.   
      ASSIGN   
        resplan.datum     = curr-date   
        resplan.zikatnr   = zimkateg.zikatnr
        resplan.anzzim[i] = resplan.anzzim[i] + rline.zimmeranz.   
    END.   
    ELSE DO:
        FIND FIRST rbuff WHERE RECID(rbuff) = RECID(resplan) EXCLUSIVE-LOCK.
        rbuff.anzzim[i] = rbuff.anzzim[i] + rline.zimmeranz.   
        FIND CURRENT rbuff NO-LOCK.   
        RELEASE rbuff. 

    END.  
  END.   
END.   
  
PROCEDURE check-fixedrate:   
DEFINE INPUT PARAMETER resnr        AS INTEGER          NO-UNDO.   
DEFINE INPUT PARAMETER reslinnr     AS INTEGER          NO-UNDO.   
DEFINE INPUT PARAMETER new-resnr    AS INTEGER          NO-UNDO.   
DEFINE VARIABLE found               AS LOGICAL INIT NO  NO-UNDO.   
  
DEF BUFFER rqsy   FOR reslin-queasy.   
DEF BUFFER rline1 FOR res-line.   
DEF BUFFER rline2 FOR res-line.   
   
  FIND FIRST rline1 WHERE rline1.resnr = resnr   
    AND rline1.reslinnr = reslinnr NO-LOCK.   
  FIND FIRST rline2 WHERE rline2.resnr = new-resnr   
    AND rline2.reslinnr = reslinnr NO-LOCK.   
  FOR EACH reslin-queasy WHERE reslin-queasy.key = "arrangement"   
    AND reslin-queasy.resnr = resnr   
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK:   
    CREATE rqsy.   
    BUFFER-COPY reslin-queasy EXCEPT resnr TO rqsy.   
    ASSIGN rqsy.resnr = new-resnr.   
    IF reslin-queasy.date1 = rline1.ankunft THEN rqsy.date1 = rline2.ankunft.   
    ELSE found = YES.   
    IF reslin-queasy.date2 = rline1.abreise THEN rqsy.date2 = rline2.abreise.   
    ELSE found = YES.   
  END.   
    
  IF found AND msg-str EQ "" THEN msg-str = "&W" +   
    translateExtended ("Wrong date in fixed-rate setup. Re-check it.",lvCAREA,"").  
  
END.   
   
PROCEDURE create-logfile:   
DEFINE INPUT PARAMETER resnr    AS INTEGER NO-UNDO.   
DEFINE INPUT PARAMETER reslinnr AS INTEGER NO-UNDO.  
  
DEFINE VARIABLE fixed-rate      AS LOGICAL NO-UNDO.   
  
DEFINE BUFFER rline  FOR res-line.   
DEFINE BUFFER guest1 FOR guest.   
   
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement"   
    AND reslin-queasy.resnr = resnr   
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK NO-ERROR.   
  fixed-rate = AVAILABLE reslin-queasy.   
   
  FIND FIRST rline WHERE rline.resnr = resnr AND rline.reslinnr = reslinnr   
    NO-LOCK.   
    
  CREATE reslin-queasy.   
  ASSIGN  
    reslin-queasy.key      = "ResChanges"   
    reslin-queasy.resnr    = rline.resnr   
    reslin-queasy.reslinnr = rline.reslinnr   
    reslin-queasy.date2    = TODAY  
    reslin-queasy.number2  = TIME  
  .   
  reslin-queasy.char3 = STRING(rline.ankunft) + ";"   
                      + STRING(rline.ankunft) + ";"   
                      + STRING(rline.abreise) + ";"   
                      + STRING(rline.abreise) + ";"   
                      + STRING(rline.zimmeranz) + ";"   
                      + STRING(rline.zimmeranz) + ";"   
                      + STRING(rline.erwachs) + ";"   
                      + STRING(rline.erwachs) + ";"   
                      + STRING(rline.kind1) + ";"   
                      + STRING(rline.kind1) + ";"   
                      + STRING(rline.gratis) + ";"   
                      + STRING(rline.gratis) + ";"   
                      + STRING(rline.zikatnr) + ";"   
                      + STRING(rline.zikatnr) + ";"   
                      + STRING(rline.zinr) + ";"   
                      + STRING(rline.zinr) + ";"   
                      + STRING(rline.arrangement) + ";"   
                      + STRING(rline.arrangement) + ";"   
                      + STRING(rline.zipreis) + ";"   
                      + STRING(rline.zipreis) + ";"   
                      + STRING(user-init) + ";"   
                      + STRING(user-init) + ";"   
                      + STRING(TODAY) + ";"   
                      + STRING(TODAY) + ";"   
                      + STRING(rline.NAME) + ";"   
                      + STRING("New Reservation") + ";".   
  IF rline.was-status = 0 THEN   
    reslin-queasy.char3 = reslin-queasy.char3 + STRING(" NO") + ";".   
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";".   
   
  IF NOT fixed-rate THEN   
    reslin-queasy.char3 = reslin-queasy.char3 + STRING(" NO") + ";".   
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";".   
   
  FIND CURRENT reslin-queasy NO-LOCK.   
  RELEASE reslin-queasy.   
   
END.   
