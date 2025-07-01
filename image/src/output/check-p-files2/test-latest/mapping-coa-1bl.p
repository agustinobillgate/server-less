DEF TEMP-TABLE coa-list
    FIELD old-fibu AS CHAR FORMAT "x(12)"
    FIELD new-fibu AS CHAR FORMAT "x(12)"
    FIELD bezeich AS CHAR FORMAT "x(48)"  /**/
    FIELD coaStat  AS INTEGER INITIAL -1
    FIELD old-main AS INTEGER
    FIELD new-main AS INTEGER
    FIELD bezeichM AS CHAR
    FIELD old-dept AS INTEGER
    FIELD new-dept AS INTEGER
    FIELD bezeichD AS CHAR
    FIELD catno    AS INTEGER
    FIELD acct     AS INTEGER
    FIELD old-acct AS INTEGER
    INDEX coa-ix old-fibu
.

DEFINE INPUT PARAMETER TABLE FOR coa-list.

DEFINE BUFFER l-ophdrBuff   FOR l-ophdr.
DEFINE BUFFER l-opBuff      FOR l-op.
DEFINE BUFFER l-ophisbuff   FOR l-ophis.
DEFINE BUFFER l-ophhisBuff  FOR l-ophhis.
DEFINE BUFFER l-hhisBuff  FOR l-ophhis.
DEFINE BUFFER artBuff     FOR artikel.
DEFINE BUFFER lartBuff    FOR l-artikel.
DEFINE BUFFER lodBuff     FOR l-order.
DEFINE BUFFER htpBuff     FOR htparam.
DEFINE BUFFER suppBuff    FOR l-lieferant.
DEFINE BUFFER faopBuff    FOR fa-op.

DEFINE BUFFER paramBuff  FOR parameters.
DEFINE BUFFER zwkumBuff  FOR zwkum.
DEFINE BUFFER lzwkumBuff FOR l-untergrup.
DEFINE BUFFER fa-artBuff FOR fa-artikel.
DEFINE BUFFER fa-zwBuff  FOR fa-grup.

MESSAGE "start mapping COA" VIEW-AS ALERT-BOX.

RUN update-lop.
RUN update-order.
RUN update-supplier.
RUN update-parameters.
RUN update-htparam.
RUN update-artikel.
RUN update-l-artikel.
RUN update-fa-artikel.

PROCEDURE update-lop:
    FIND FIRST l-op WHERE l-op.op-art = 3 AND l-op.stornogrund NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-op:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-op.stornogrund AND coa-list.new-fibu NE ?
        NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST l-opbuff WHERE RECID(l-opbuff) = RECID(l-op) EXCLUSIVE-LOCK.
        ASSIGN l-opbuff.stornogrund = coa-list.new-fibu.
        FIND CURRENT l-opbuff NO-LOCK.
        RELEASE l-opbuff.
      END.
      FIND NEXT l-op WHERE l-op.op-art = 3 AND l-op.stornogrund NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update l-op" VIEW-AS ALERT-BOX.
    
    FIND FIRST l-ophis WHERE l-ophis.op-art = 3 AND l-ophis.fibukonto NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-ophis:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-ophis.fibukonto AND coa-list.new-fibu NE ?
        NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST l-ophisbuff WHERE RECID(l-ophisbuff) = RECID(l-ophis) EXCLUSIVE-LOCK.
        ASSIGN l-ophisbuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT l-ophisbuff NO-LOCK.
        RELEASE l-ophisbuff.
      END.
      FIND NEXT l-ophis WHERE l-ophis.op-art = 3 AND l-ophis.fibukonto NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update l-ophis" VIEW-AS ALERT-BOX.
  
    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-ophdr:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-ophdr.fibukonto AND coa-list.new-fibu NE ?
        NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST l-ophdrbuff WHERE RECID(l-ophdrbuff) = RECID(l-ophdr) EXCLUSIVE-LOCK.
        ASSIGN l-ophdrbuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT l-ophdrbuff NO-LOCK.
        RELEASE l-ophdrbuff.
      END.  
      FIND NEXT l-ophdr WHERE l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update l-ophdr" VIEW-AS ALERT-BOX.
 
    FIND FIRST l-ophhis WHERE l-ophhis.op-typ = "STT" AND l-ophhis.fibukonto NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-ophhis:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-ophhis.fibukonto AND coa-list.new-fibu NE ?
        NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST l-ophhisbuff WHERE RECID(l-ophhisbuff) = RECID(l-ophhis) EXCLUSIVE-LOCK.
        ASSIGN l-ophhisbuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT l-ophhisbuff NO-LOCK.
        RELEASE l-ophhisbuff.
      END.
      FIND NEXT l-ophhis WHERE l-ophhis.op-typ = "STT" AND l-ophhis.fibukonto NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update l-ophhis" VIEW-AS ALERT-BOX.
END.

PROCEDURE update-order:
    FIND FIRST l-order WHERE l-order.stornogrund NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-order:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-order.stornogrund AND coa-list.new-fibu NE ?
        NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST lodBuff WHERE RECID(lodBuff) = RECID(l-order) EXCLUSIVE-LOCK.
        ASSIGN lodBuff.stornogrund = coa-list.new-fibu.
        FIND CURRENT lodBuff NO-LOCK.
        RELEASE lodBuff.
      END. 
      FIND NEXT l-order WHERE l-order.stornogrund NE "" NO-LOCK NO-ERROR.
    END.
    MESSAGE "done update l-order" VIEW-AS ALERT-BOX.
END.

PROCEDURE update-supplier:
    FIND FIRST l-lieferant WHERE l-lieferant.z-code NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-lieferant:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-lieferant.z-code AND coa-list.new-fibu NE ?
        NO-LOCK NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST suppBuff WHERE RECID(suppBuff) = RECID(l-lieferant) EXCLUSIVE-LOCK. 
        ASSIGN suppBuff.z-code = coa-list.new-fibu.
        FIND CURRENT suppBuff NO-LOCK.
        RELEASE suppBuff.
      END.
      FIND NEXT l-lieferant WHERE l-lieferant.z-code NE "" NO-LOCK NO-ERROR.
    END.
    MESSAGE "done update l-lieferant" VIEW-AS ALERT-BOX.
END.

PROCEDURE update-parameters:
    FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
        AND parameters.SECTION = "Alloc" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE parameters:
        FIND FIRST coa-list WHERE coa-list.old-fibu = parameters.vstring AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
        DO TRANSACTION:
            FIND FIRST paramBuff WHERE RECID(paramBuff) = RECID(parameters) EXCLUSIVE-LOCK.
            ASSIGN paramBuff.vstring = coa-list.new-fibu.
            FIND CURRENT paramBuff NO-LOCK.
            RELEASE paramBuff.
        END. 
        FIND NEXT parameters WHERE parameters.progname = "CostCenter"
            AND parameters.SECTION = "Alloc" NO-LOCK NO-ERROR.
    END.
    MESSAGE "done update parameters" VIEW-AS ALERT-BOX.
END.

PROCEDURE update-htparam:
    FIND FIRST htparam WHERE htparam.fchar NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE htparam:
        FIND FIRST coa-list WHERE coa-list.old-fibu = htparam.fchar AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR. 
        IF AVAILABLE coa-list THEN
        DO TRANSACTION:
            FIND FIRST htpBuff WHERE RECID(htpBuff) = RECID(htparam) EXCLUSIVE-LOCK.
            ASSIGN htpBuff.fchar = coa-list.new-fibu.
            FIND CURRENT htpBuff NO-LOCK.
            RELEASE htpBuff.
        END.
        FIND NEXT htparam WHERE htparam.fchar NE "" NO-LOCK NO-ERROR.
    END.
    MESSAGE "done update htparam" VIEW-AS ALERT-BOX.
END.

PROCEDURE update-artikel:
    FIND FIRST artikel NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE artikel:
      DO TRANSACTION:
        FIND FIRST artBuff WHERE RECID(artBuff) = RECID(artikel)EXCLUSIVE-LOCK.
        FIND FIRST coa-list WHERE coa-list.old-fibu = artikel.bezeich1 AND coa-list.new-fibu NE ?
          NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
          ASSIGN artBuff.bezeich1 = coa-list.new-fibu.
        FIND FIRST coa-list WHERE coa-list.old-fibu = artikel.fibukonto AND coa-list.new-fibu NE ?
          NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
          ASSIGN artBuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT artBuff NO-LOCK.
        RELEASE artBuff.
      END.
      FIND NEXT artikel NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update artikel" VIEW-AS ALERT-BOX.
    
    FIND FIRST zwkum WHERE zwkum.fibukonto NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE zwkum:
      FIND FIRST coa-list WHERE coa-list.old-fibu = zwkum.fibukonto AND coa-list.new-fibu NE ?
        NO-LOCK NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST zwkumBuff WHERE RECID(zwkumBuff) = RECID(zwkum) EXCLUSIVE-LOCK.
        ASSIGN zwkumBuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT zwkumBuff NO-LOCK.
        RELEASE zwkumBuff.
      END.
      FIND NEXT zwkum WHERE zwkum.fibukonto NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update zwkum" VIEW-AS ALERT-BOX.
END.

PROCEDURE update-l-artikel:
    FIND FIRST l-artikel WHERE l-artikel.fibukonto NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-artikel:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-artikel.fibukonto AND coa-list.new-fibu NE ?
        NO-LOCK NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST lartBuff WHERE RECID(lartBuff) = RECID(l-artikel)
            EXCLUSIVE-LOCK.
        ASSIGN lartBuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT lartBuff NO-LOCK.
        RELEASE lartBuff.
      END.
      FIND NEXT l-artikel WHERE l-artikel.fibukonto NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update l-artikel" VIEW-AS ALERT-BOX.

    FIND FIRST l-untergrup WHERE l-untergrup.fibukonto NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE l-untergrup:
      FIND FIRST coa-list WHERE coa-list.old-fibu = l-untergrup.fibukonto AND coa-list.new-fibu NE ?
        NO-LOCK NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST lzwkumBuff WHERE RECID(lzwkumBuff) = RECID(l-untergrup)
            EXCLUSIVE-LOCK.
        ASSIGN lzwkumBuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT lzwkumBuff NO-LOCK.
        RELEASE lzwkumBuff.
      END.
      FIND NEXT l-untergrup WHERE l-untergrup.fibukonto NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update l-untergrup" VIEW-AS ALERT-BOX.
END.

PROCEDURE update-fa-artikel:
    FIND FIRST fa-artikel NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE fa-artikel:
      DO TRANSACTION:
        FIND FIRST fa-artBuff WHERE RECID(fa-artBuff) = RECID(fa-artikel) EXCLUSIVE-LOCK.
        FIND FIRST coa-list WHERE coa-list.old-fibu = fa-artikel.fibukonto AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN ASSIGN fa-artBuff.fibukonto = coa-list.new-fibu.
        FIND FIRST coa-list WHERE coa-list.old-fibu = fa-artikel.credit-fibu AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN ASSIGN fa-artBuff.credit-fibu = coa-list.new-fibu.
        FIND FIRST coa-list WHERE coa-list.old-fibu = fa-artikel.debit-fibu AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN ASSIGN fa-artBuff.debit-fibu = coa-list.new-fibu.
        FIND CURRENT fa-artBuff NO-LOCK.
        RELEASE fa-artBuff.
      END.
      FIND NEXT fa-artikel NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update fa-artikel" VIEW-AS ALERT-BOX.

    FIND FIRST fa-grup NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE fa-grup:
      DO TRANSACTION:
        FIND FIRST fa-zwBuff WHERE RECID(fa-zwBuff) = RECID(fa-grup) EXCLUSIVE-LOCK.
        FIND FIRST coa-list WHERE coa-list.old-fibu = fa-grup.fibukonto AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
          ASSIGN fa-zwBuff.fibukonto = coa-list.new-fibu.
        FIND FIRST coa-list WHERE coa-list.old-fibu = fa-grup.credit-fibu AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
            ASSIGN fa-zwBuff.credit-fibu = coa-list.new-fibu.
        FIND FIRST coa-list WHERE coa-list.old-fibu = fa-grup.debit-fibu AND coa-list.new-fibu NE ?
            NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
            ASSIGN fa-zwBuff.debit-fibu = coa-list.new-fibu.
        FIND CURRENT fa-zwBuff NO-LOCK.
        RELEASE fa-zwBuff.
      END.
      FIND NEXT fa-grup NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update fa-group" VIEW-AS ALERT-BOX.

    FIND FIRST fa-op WHERE fa-op.fibukonto NE "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE fa-op:
      FIND FIRST coa-list WHERE coa-list.old-fibu = fa-op.fibukonto AND coa-list.new-fibu NE ?
        NO-LOCK NO-ERROR.
      IF AVAILABLE coa-list THEN
      DO TRANSACTION:
        FIND FIRST faopBuff WHERE RECID(faopBuff) = RECID(fa-op) EXCLUSIVE-LOCK.
        ASSIGN faopBuff.fibukonto = coa-list.new-fibu.
        FIND CURRENT faopBuff NO-LOCK.
        RELEASE faopBuff.
      END.
      FIND NEXT fa-op WHERE fa-op.fibukonto NE "" NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update fa-op" VIEW-AS ALERT-BOX.
END.

