
DEF TEMP-TABLE in-list
    FIELD lscheinr AS CHAR.

DEF TEMP-TABLE s-list
    FIELD datum      AS DATE
    FIELD lief-nr    AS INTEGER 
    FIELD lager      AS INTEGER
    FIELD docu-nr    AS CHAR
    FIELD lscheinnr  AS CHAR
    FIELD userNo     AS INTEGER
    FIELD zeit       AS INTEGER
    FIELD amount     AS DECIMAL INITIAL 0
    FIELD storno     AS CHAR
    FIELD loeschflag AS INT
    FIELD artnr      AS INT
    FIELD inv-dept   AS LOGICAL 
    FIELD user-init  AS CHAR
.

DEF TEMP-TABLE rcv-list
    FIELD datum      AS DATE
    FIELD lief-nr    AS INTEGER 
    FIELD lager      AS INTEGER
    FIELD docu-nr    AS CHAR
    FIELD lscheinnr  AS CHAR
    FIELD userNo     AS INTEGER
    FIELD zeit       AS INTEGER
    FIELD amount     AS DECIMAL INITIAL 0
    FIELD storno     AS CHAR
    FIELD loeschflag AS INT
    FIELD artnr      AS INT
    FIELD inv-dept   AS LOGICAL 
    FIELD user-init  AS CHAR
.

DEFINE TEMP-TABLE out-list
    FIELD msg-str    AS CHAR.

DEFINE BUFFER b-kredit FOR l-kredit.
DEFINE BUFFER buff-kredit FOR l-kredit.
DEFINE BUFFER b-journal FOR ap-journal.

DEFINE INPUT PARAMETER TABLE FOR in-list.
DEFINE INPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR out-list.

DEFINE VARIABLE amount AS DECIMAL NO-UNDO.
DEFINE VARIABLE ct AS INTEGER NO-UNDO.


FIND FIRST in-list NO-LOCK NO-ERROR.
IF AVAILABLE in-list THEN DO:   
    FOR EACH s-list WHERE s-list.lscheinnr EQ in-list.lscheinr:
        ASSIGN amount = 0.
    
        FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = s-list.lscheinnr 
           AND queasy.number1 = s-list.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN ASSIGN amount = s-list.amount + (s-list.amount * (queasy.deci1 / 100)).
        ELSE amount = s-list.amount. /**/
    
        amount = ROUND(amount,2).
    
        FIND FIRST rcv-list WHERE rcv-list.docu-nr = s-list.docu-nr
           AND rcv-list.lschein = s-list.lscheinnr NO-ERROR.
        IF NOT AVAILABLE rcv-list THEN DO:
             CREATE rcv-list.
             ASSIGN
                 rcv-list.datum      = s-list.datum
                 rcv-list.lief-nr    = s-list.lief-nr
                 rcv-list.docu-nr    = s-list.docu-nr
                 rcv-list.lschein    = s-list.lscheinnr
                 rcv-list.lager      = s-list.lager
                 rcv-list.zeit       = s-list.zeit
                 rcv-list.userNo     = s-list.userNo
                 rcv-list.storno     = s-list.storno 
                 rcv-list.loeschflag = s-list.loeschflag
                 rcv-list.user-init  = s-list.user-init
                 rcv-list.amount     = amount
                 rcv-list.inv-dept   = YES.
        END.
        ELSE ASSIGN  rcv-list.amount  = rcv-list.amount + amount.
    
    END.
    
    
    FIND FIRST rcv-list NO-LOCK NO-ERROR.
    IF AVAILABLE rcv-list THEN DO:
        FIND FIRST b-kredit WHERE b-kredit.lscheinnr = rcv-list.lschein
         AND b-kredit.lief-nr   = rcv-list.lief-nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE b-kredit THEN /*create AP jika tidak ditemukan*/
        DO:            
            
            
            CREATE b-kredit.
            ASSIGN
               b-kredit.NAME        = rcv-list.docu-nr
               b-kredit.lief-nr     = rcv-list.lief-nr
               b-kredit.lscheinnr   = rcv-list.lscheinnr
               b-kredit.rgdatum     = rcv-list.datum
               b-kredit.datum       = ?
               b-kredit.ziel        = 30
               b-kredit.saldo       = rcv-list.amount
               b-kredit.netto       = rcv-list.amount
            .

            CREATE b-journal.
            ASSIGN
               b-journal.docu-nr   = rcv-list.docu-nr
               b-journal.lscheinnr = rcv-list.lscheinnr 
               b-journal.lief-nr   = rcv-list.lief-nr
               b-journal.rgdatum   = rcv-list.datum
               b-journal.zeit      = rcv-list.zeit
               b-journal.saldo     = rcv-list.amount
               b-journal.netto     = rcv-list.amount
            .
            
            FIND FIRST bediener WHERE bediener.userinit = rcv-list.user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN DO: 
                ASSIGN
                    b-kredit.bediener-nr = bediener.nr
                    b-journal.userinit = bediener.userinit.
            END.
    
        END.
        ELSE DO:
            /*delete ap double and cek partial amount*/
            FOR EACH l-kredit WHERE l-kredit.lscheinnr EQ s-list.lschein NO-LOCK:
               FIND FIRST b-kredit WHERE RECID(b-kredit) EQ RECID(l-kredit) EXCLUSIVE-LOCK.
               DELETE b-kredit.
               RELEASE b-kredit.
            END. 
            
            FOR EACH ap-journal WHERE ap-journal.lscheinnr EQ s-list.lschein NO-LOCK:
               FIND FIRST b-journal WHERE RECID(b-journal) EQ RECID(ap-journal) EXCLUSIVE-LOCK.
               DELETE b-journal.
               RELEASE b-journal.
            END.
            
            CREATE b-kredit.
            ASSIGN
               b-kredit.NAME        = rcv-list.docu-nr
               b-kredit.lief-nr     = rcv-list.lief-nr
               b-kredit.lscheinnr   = rcv-list.lscheinnr
               b-kredit.rgdatum     = rcv-list.datum
               b-kredit.datum       = ?
               b-kredit.ziel        = 30
               b-kredit.saldo       = rcv-list.amount
               b-kredit.netto       = rcv-list.amount
               b-kredit.bediener-nr = rcv-list.userNo
            .
        
            CREATE b-journal.
            ASSIGN
               b-journal.docu-nr   = rcv-list.docu-nr
               b-journal.lscheinnr = rcv-list.lscheinnr 
               b-journal.lief-nr   = rcv-list.lief-nr
               b-journal.rgdatum   = rcv-list.datum
               b-journal.zeit      = rcv-list.zeit
               b-journal.saldo     = rcv-list.amount
               b-journal.netto     = rcv-list.amount
            .

            FIND FIRST bediener WHERE bediener.userinit = rcv-list.user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN DO: 
                ASSIGN
                    b-kredit.bediener-nr = bediener.nr
                    b-journal.userinit = bediener.userinit.
            END.
        END.
    END.
END.
