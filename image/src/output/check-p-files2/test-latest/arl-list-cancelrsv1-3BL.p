  
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.  
DEF INPUT  PARAMETER arl-list-resnr AS INT.  
DEF INPUT  PARAMETER cancel-str     AS CHAR.  
DEF INPUT  PARAMETER user-init      AS CHAR.  
DEF OUTPUT PARAMETER done           AS LOGICAL INITIAL NO.  
DEF OUTPUT PARAMETER msg-str        AS CHAR.  
  
DEF BUFFER mainres FOR reservation. 
DEF BUFFER r-line FOR res-line.
  
FIND FIRST mainres WHERE mainres.resnr = arl-list-resnr NO-LOCK NO-ERROR.   
DO TRANSACTION:   
    FIND CURRENT mainres EXCLUSIVE-LOCK.   
    IF cancel-str NE "" THEN mainres.vesrdepot2 = cancel-str.   
    FIND CURRENT mainres NO-LOCK. 

    /*FD Oct 13, 2022 => Ticket B1B3A0 - Create Reservation Log*/
    FIND FIRST r-line WHERE r-line.resnr EQ arl-list-resnr   
        AND r-line.active-flag EQ 0   
        AND r-line.l-zuordnung[3] EQ 0 NO-LOCK NO-ERROR.   
    DO WHILE AVAILABLE r-line:   
      
        CREATE reslin-queasy.
        ASSIGN
            reslin-queasy.key       = "ResChanges"
            reslin-queasy.resnr     = r-line.resnr 
            reslin-queasy.reslinnr  = r-line.reslinnr 
            reslin-queasy.date2     = TODAY 
            reslin-queasy.number2   = TIME
        .
    
        reslin-queasy.char3 = STRING(r-line.ankunft) + ";" 
                            + STRING(r-line.ankunft) + ";" 
                            + STRING(r-line.abreise) + ";" 
                            + STRING(r-line.abreise) + ";" 
                            + STRING(r-line.zimmeranz) + ";" 
                            + STRING(r-line.zimmeranz) + ";" 
                            + STRING(r-line.erwachs) + ";" 
                            + STRING(r-line.erwachs) + ";" 
                            + STRING(r-line.kind1) + ";" 
                            + STRING(r-line.kind1) + ";" 
                            + STRING(r-line.gratis) + ";" 
                            + STRING(r-line.gratis) + ";" 
                            + STRING(r-line.zikatnr) + ";" 
                            + STRING(r-line.zikatnr) + ";" 
                            + STRING(r-line.zinr) + ";" 
                            + STRING(r-line.zinr) + ";" 
                            + STRING(r-line.arrangement) + ";" 
                            + STRING(r-line.arrangement) + ";"
                            + STRING(r-line.zipreis) + ";" 
                            + STRING(r-line.zipreis) + ";"
                            + STRING(user-init) + ";" 
                            + STRING(user-init) + ";" 
                            + STRING(TODAY) + ";" 
                            + STRING(TODAY) + ";" 
                            + STRING(r-line.name) + ";" 
                            + STRING("CANCEL RSV") + ";"
                            + STRING(" ") + ";" 
                            + STRING(" ") + ";"
                            .         
    
        FIND NEXT r-line WHERE r-line.resnr EQ arl-list-resnr   
            AND r-line.active-flag EQ 0  
            AND r-line.l-zuordnung[3] EQ 0 NO-LOCK NO-ERROR.   
    END.  

    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 
END.  
RUN del-reservebl.p(pvILanguage, "cancel", arl-list-resnr, user-init, cancel-str,  
                    OUTPUT msg-str).  
done = YES.  
