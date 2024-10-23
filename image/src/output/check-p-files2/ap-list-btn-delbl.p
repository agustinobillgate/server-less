

DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER ap-recid    AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER msg-str    AS CHAR     NO-UNDO INIT "".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ap-list".

DEFINE VARIABLE saldo AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE netto AS DECIMAL NO-UNDO INIT 0.
DEF BUFFER apbuff FOR l-kredit. 

FIND FIRST l-kredit WHERE RECID(l-kredit) = ap-recid NO-LOCK. 
IF l-kredit.counter GT 0 THEN 
DO: 
    FIND FIRST apbuff WHERE apbuff.counter = l-kredit.counter 
        AND apbuff.zahlkonto > 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE apbuff THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("A/P Payment exists, deleting not possible.",lvCAREA,"").
      /*APPLY "entry" TO from-date. */
      RETURN NO-APPLY. 
    END. 
END. 
 
FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = l-kredit.NAME 
    AND gl-jouhdr.datum = l-kredit.rgdatum NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr AND gl-jouhdr.activeflag = 1 THEN 
DO: 
     msg-str = msg-str + CHR(2)
             + translateExtended ("The related journals are no longer active.",lvCAREA,"").
     /*APPLY "entry" TO from-date. */
     RETURN NO-APPLY. 
END. 
 
 
DO TRANSACTION: 
    IF AVAILABLE gl-jouhdr THEN 
    DO: 
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr EXCLUSIVE-LOCK: 
            DELETE gl-journal. 
        END. 
        RELEASE gl-journal.

        FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
        DELETE gl-jouhdr. 
        RELEASE gl-jouhdr.
    END. 
    
    /*ITA 030815*/
    ASSIGN saldo = saldo - l-kredit.saldo
           netto = netto - l-kredit.netto.

    CREATE ap-journal. 
    ASSIGN 
      ap-journal.lief-nr    = l-kredit.lief-nr 
      ap-journal.docu-nr    = l-kredit.name 
      ap-journal.lscheinnr  = l-kredit.lscheinnr 
      ap-journal.rgdatum    = l-kredit.rgdatum 
      ap-journal.saldo      = saldo
      ap-journal.netto      = netto 
      ap-journal.userinit   = user-init
      ap-journal.zeit       = TIME 
      ap-journal.betriebsnr = l-kredit.betriebsnr. 

    FIND CURRENT l-kredit EXCLUSIVE-LOCK. 
    DELETE l-kredit. 
    /*MTAPPLY "choose" TO btn-go. 
    RETURN NO-APPLY. */
END. 
