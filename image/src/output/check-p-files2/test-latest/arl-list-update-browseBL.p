DEFINE WORKFILE setup-list   
  FIELD nr AS INTEGER   
  FIELD CHAR AS CHAR FORMAT "x(1)".   
  
CREATE setup-list.   
setup-list.nr = 1.   
setup-list.char = " ".   
   
FOR EACH paramtext WHERE paramtext.txtnr GE 9201   
    AND paramtext.txtnr LE 9299 NO-LOCK:   
    CREATE setup-list.   
    setup-list.nr = paramtext.txtnr - 9199.   
    setup-list.char = SUBSTR(paramtext.notes,1,1).  
END.   
  
DEFINE BUFFER gbuff FOR guest.  
  
DEFINE TEMP-TABLE arl-list  
    FIELD resnr             LIKE res-line.resnr  
    FIELD reslinnr          LIKE res-line.reslinnr  
    FIELD resline-wabkurz   LIKE res-line.wabkurz  
    FIELD voucher-nr        LIKE res-line.voucher-nr  
    FIELD grpflag           LIKE reservation.grpflag  
    FIELD verstat           LIKE reservation.verstat  
    FIELD l-zuordnung2      LIKE res-line.l-zuordnung[2]  
    FIELD kontignr          LIKE res-line.kontignr  
    FIELD firmen-nr         LIKE gbuff.firmen-nr  
    FIELD steuernr          LIKE gbuff.steuernr  
    FIELD rsv-name          LIKE reservation.name  
    FIELD zinr              LIKE res-line.zinr  
    FIELD setup-list-char   LIKE setup-list.CHAR  
    FIELD resline-name      LIKE res-line.name  
    FIELD waehrung-wabkurz  LIKE waehrung.wabkurz  
    FIELD segmentcode       LIKE reservation.segmentcode  
    FIELD ankunft           LIKE res-line.ankunft  
    FIELD abreise           LIKE res-line.abreise  
    FIELD zimmeranz         LIKE res-line.zimmeranz  
    FIELD kurzbez           LIKE zimkateg.kurzbez  
    FIELD arrangement       LIKE res-line.arrangement  
    FIELD zipreis           LIKE res-line.zipreis  
    FIELD anztage           LIKE res-line.anztage  
    FIELD erwachs           LIKE res-line.erwachs  
    FIELD kind1             LIKE res-line.kind1  
    FIELD kind2             LIKE res-line.kind2  
    FIELD gratis            LIKE res-line.gratis  
    FIELD l-zuordnung4      LIKE res-line.l-zuordnung[4]  
    FIELD resstatus         LIKE res-line.resstatus  
    FIELD l-zuordnung3      LIKE res-line.l-zuordnung[3]  
    FIELD flight-nr         LIKE res-line.flight-nr  
    FIELD ankzeit           LIKE res-line.ankzeit  
    FIELD abreisezeit       LIKE res-line.abreisezeit  
    FIELD betrieb-gast      LIKE res-line.betrieb-gast  
    FIELD resdat            LIKE reservation.resdat  
    FIELD useridanlage      LIKE reservation.useridanlage  
    FIELD reserve-dec       LIKE res-line.reserve-dec  
    FIELD cancelled-id      LIKE res-line.cancelled-id  
    FIELD changed-id        LIKE res-line.changed-id  
    FIELD groupname         LIKE reservation.groupname  
  
    FIELD active-flag       LIKE res-line.active-flag  
    FIELD gastnr            LIKE res-line.gastnr  

    FIELD gastnrmember      LIKE res-line.gastnrmember  
    FIELD karteityp         LIKE guest.karteityp
    
    FIELD reserve-int       LIKE res-line.reserve-int  
    FIELD zikatnr           LIKE res-line.zikatnr  
    FIELD betrieb-gastmem   LIKE res-line.betrieb-gastmem  
    FIELD pseudofix         LIKE res-line.pseudofix  
    FIELD reserve-char      LIKE res-line.reserve-char  
    FIELD bemerk            LIKE res-line.bemerk  
  
    FIELD depositbez        LIKE reservation.depositbez  
    FIELD depositbez2       LIKE reservation.depositbez2  
    FIELD bestat-dat        LIKE reservation.bestat-dat  
    FIELD briefnr           LIKE reservation.briefnr  
    FIELD rsv-gastnr        LIKE reservation.gastnr  
    FIELD rsv-resnr         LIKE reservation.resnr  
    FIELD rsv-bemerk        LIKE reservation.bemerk  
    FIELD rsv-grpflag       LIKE reservation.grpflag  
    FIELD recid-resline     AS INT  
    FIELD address           LIKE guest.adresse1  
    FIELD city              AS CHAR  
    FIELD comments          AS CHAR  
      
    FIELD resnr-fgcol       AS INT INIT -1  
    FIELD mc-str-fgcol      AS INT INIT -1  
    FIELD mc-str-bgcol      AS INT INIT -1  
    FIELD rsv-name-fgcol    AS INT INIT -1  
    FIELD rsv-name-bgcol    AS INT INIT -1  
    FIELD zinr-fgcol        AS INT INIT -1  
    FIELD reslin-name-fgcol AS INT INIT -1  
    FIELD ankunft-fgcol     AS INT INIT -1  
    FIELD anztage-fgcol     AS INT INIT -1  
    FIELD abreise-fgcol     AS INT INIT -1  
    FIELD segmentcode-fgcol AS INT INIT -1  
    FIELD reslin-name-bgcol AS INT INIT -1  
    FIELD segmentcode-bgcol AS INT INIT -1  
    FIELD zinr-bgcol        AS INT INIT -1
    FIELD webci             AS CHAR
    FIELD webci-flag        AS CHAR
    FIELD voucher-flag      AS CHAR
    FIELD kontignr-flag     AS CHAR
    FIELD ratecode          AS CHAR. /*willi add ratecode 02CBF8*/
  
DEF INPUT PARAMETER show-rate AS LOGICAL.  
DEF INPUT PARAMETER recid-resline AS INT.  
DEF INPUT  PARAMETER long-stay    AS INT.  
DEF INPUT  PARAMETER ci-date      AS DATE.  
DEF OUTPUT PARAMETER TABLE FOR arl-list.  
  
DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE all-inclusive AS CHAR.  
DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
DEFINE VARIABLE loopj   AS INTEGER NO-UNDO.
DEFINE VARIABLE loopk   AS INTEGER NO-UNDO.
DEFINE VARIABLE loopl   AS INTEGER NO-UNDO.
DEFINE VARIABLE ratecodestr AS CHAR NO-UNDO.

DEFINE VARIABLE str1    AS CHAR    NO-UNDO.
DEFINE VARIABLE str2    AS CHAR    NO-UNDO.
DEFINE VARIABLE web-com AS CHAR    NO-UNDO.
  
RUN get-vipnrbl.p  
    (OUTPUT vipnr1, OUTPUT vipnr2, OUTPUT vipnr3, OUTPUT vipnr4,  
     OUTPUT vipnr5, OUTPUT vipnr6, OUTPUT vipnr7, OUTPUT vipnr8,  
     OUTPUT vipnr9).  
  
FIND FIRST res-line WHERE RECID(res-line) = recid-resline NO-LOCK NO-ERROR.  
FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK NO-ERROR.  
FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.  
FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.  
FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.  
FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1 NO-LOCK NO-ERROR.  

    IF res-line.zimmer-wunsch MATCHES "*$CODE$*" THEN
    DO:
        ratecodestr = ENTRY(1, substring(res-line.zimmer-wunsch, INDEX(res-line.zimmer-wunsch,"$CODE$") + 6) ,";"). /*willi add ratecode 02CBF8*/ 
    END.
    ELSE 
        ratecodestr = "".

    CREATE arl-list.  
    ASSIGN  
    arl-list.resnr             = res-line.resnr  
    arl-list.reslinnr          = res-line.reslinnr  
    arl-list.resline-wabkurz   = res-line.wabkurz  
    arl-list.voucher-nr        = res-line.voucher-nr  
    arl-list.grpflag           = reservation.grpflag  
    arl-list.verstat           = reservation.verstat  
    arl-list.l-zuordnung2      = res-line.l-zuordnung[2]  
    arl-list.kontignr          = res-line.kontignr  
    arl-list.firmen-nr         = gbuff.firmen-nr  
    arl-list.steuernr          = gbuff.steuernr  
    arl-list.rsv-name          = reservation.name  
    arl-list.zinr              = res-line.zinr  
    arl-list.setup-list-char   = setup-list.CHAR  
    arl-list.resline-name      = res-line.name  
    arl-list.waehrung-wabkurz  = waehrung.wabkurz  
    arl-list.segmentcode       = reservation.segmentcode  
    arl-list.ankunft           = res-line.ankunft  
    arl-list.abreise           = res-line.abreise  
    arl-list.zimmeranz         = res-line.zimmeranz  
    arl-list.kurzbez           = zimkateg.kurzbez  
    arl-list.arrangement       = res-line.arrangement  
    arl-list.zipreis           = res-line.zipreis  
    arl-list.anztage           = res-line.anztage  
    arl-list.erwachs           = res-line.erwachs  
    arl-list.kind1             = res-line.kind1  
    arl-list.kind2             = res-line.kind2  
    arl-list.gratis            = res-line.gratis  
    arl-list.l-zuordnung4      = res-line.l-zuordnung[4]  
    arl-list.resstatus         = res-line.resstatus  
    arl-list.l-zuordnung3      = res-line.l-zuordnung[3]  
    arl-list.flight-nr         = res-line.flight-nr  
    arl-list.ankzeit           = res-line.ankzeit  
    arl-list.abreisezeit       = res-line.abreisezeit  
    arl-list.betrieb-gast      = res-line.betrieb-gast  
    arl-list.resdat            = reservation.resdat  
    arl-list.useridanlage      = reservation.useridanlage  
    arl-list.reserve-dec       = res-line.reserve-dec  
    arl-list.cancelled-id      = res-line.cancelled-id  
    arl-list.changed-id        = res-line.changed-id  
    arl-list.groupname         = reservation.groupname  
  
    arl-list.active-flag       = res-line.active-flag  
    arl-list.gastnr            = res-line.gastnr  
    arl-list.gastnrmember      = res-line.gastnrmember  
    arl-list.reserve-int       = res-line.reserve-int  
    arl-list.zikatnr           = res-line.zikatnr  
    arl-list.betrieb-gastmem   = res-line.betrieb-gastmem  
    arl-list.pseudofix         = res-line.pseudofix  
    arl-list.reserve-char      = res-line.reserve-char  
    arl-list.bemerk            = res-line.bemerk  
  
    arl-list.depositbez        = reservation.depositbez  
    arl-list.depositbez2       = reservation.depositbez2  
    arl-list.bestat-dat        = reservation.bestat-dat  
    arl-list.briefnr           = reservation.briefnr  
    arl-list.rsv-gastnr        = reservation.gastnr  
    arl-list.rsv-resnr         = reservation.resnr  
    arl-list.rsv-bemerk        = reservation.bemerk  
    arl-list.rsv-grpflag       = reservation.grpflag  
    arl-list.recid-resline     = RECID(res-line)
    arl-list.ratecode          = ratecodestr.

    IF AVAILABLE res-line THEN   
    DO:  
        FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR.   
        arl-list.address = guest.adresse1.   
        arl-list.city = guest.wohnort + " " + guest.plz.  
    END.  
    IF res-line.kontignr GT 0 THEN   
    DO:   
      FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr   
        AND kontline.betriebsnr = 0   
        AND kontline.kontstat = 1 NO-LOCK NO-ERROR.   
      IF AVAILABLE kontline THEN   
      arl-list.comments = "ALLOTMENT: " + kontline.kontcode + chr(10).   
    END.   
    ELSE IF res-line.kontignr LT 0 THEN   
    DO:   
      FIND FIRST kontline WHERE kontline.kontignr = res-line.kontignr   
        AND kontline.betriebsnr = 1   
        AND kontline.kontstat = 1 NO-LOCK NO-ERROR.   
      IF AVAILABLE kontline THEN   
      arl-list.comments = "GLOBAL RES: " + kontline.kontcode + chr(10).   
    END.   
    IF reservation.bemerk NE "" THEN comments = reservation.bemerk + chr(10).   
      IF res-line.bemerk NE "" THEN   
      arl-list.comments = arl-list.comments + res-line.bemerk.   
  
  
  
      IF AVAILABLE res-line THEN  
      DO:  
        FIND FIRST gentable WHERE gentable.KEY = "reservation"  
            AND gentable.number1 = res-line.resnr  
            AND gentable.number2 = res-line.reslinnr NO-LOCK NO-ERROR.  
        IF AVAILABLE gentable THEN ASSIGN arl-list.resnr-fgcol = 12.  
      END.  
  
      IF AVAILABLE res-line AND show-rate THEN   
      DO:   
          FIND FIRST mc-guest WHERE mc-guest.gastnr = res-line.gastnrmember  
              AND mc-guest.activeflag = YES NO-LOCK NO-ERROR.  
          IF AVAILABLE mc-guest THEN  
          DO:  
            ASSIGN arl-list.mc-str-fgcol = 15.   
            ASSIGN arl-list.mc-str-bgcol  = 6.   
          END.  
      END.  
  
      IF AVAILABLE res-line AND res-line.resstatus GE 11 THEN   
      DO:   
        IF res-line.l-zuordnung[3] = 0 THEN  
          ASSIGN arl-list.rsv-name-fgcol = 9.   
        ELSE  
        ASSIGN   
            arl-list.rsv-name-bgcol = 9  
            arl-list.rsv-name-fgcol = 15  
        .  
      END.   
  
      IF AVAILABLE res-line AND   
        (res-line.betrieb-gastmem = vipnr1 OR   
         res-line.betrieb-gastmem = vipnr2 OR   
         res-line.betrieb-gastmem = vipnr3 OR   
         res-line.betrieb-gastmem = vipnr4 OR   
         res-line.betrieb-gastmem = vipnr5 OR   
         res-line.betrieb-gastmem = vipnr6 OR   
         res-line.betrieb-gastmem = vipnr7 OR   
         res-line.betrieb-gastmem = vipnr8 OR   
         res-line.betrieb-gastmem = vipnr9) THEN   
      ASSIGN   
          arl-list.zinr-fgcol            = 12  
          arl-list.reslin-name-fgcol     = 12   
          arl-list.ankunft-fgcol         = 12   
          arl-list.anztage-fgcol         = 12   
          arl-list.abreise-fgcol         = 12   
          arl-list.segmentcode-fgcol     = 12  
      .  
  
      FIND FIRST htparam WHERE htparam.paramnr = 496 NO-LOCK.  
      all-inclusive = ";" + htparam.fchar + ";".  
      IF AVAILABLE res-line AND   
        all-inclusive MATCHES ("*;" + res-line.arrangement + ";*") THEN  
      ASSIGN   
          arl-list.reslin-name-bgcol    = 2  
          arl-list.reslin-name-fgcol    = 15  
          arl-list.segmentcode-bgcol    = 2  
          arl-list.segmentcode-fgcol    = 15  
      .  
  
      IF AVAILABLE res-line AND res-line.active-flag = 1 AND long-stay GT 0   
        AND (res-line.abreise - res-line.ankunft) GE long-stay   
        AND res-line.erwachs GT 0 THEN   
      ASSIGN   
          arl-list.reslin-name-fgcol = 15  
          arl-list.reslin-name-bgcol = 9.   
  
      IF AVAILABLE res-line AND res-line.active-flag LE 1 AND   
         res-line.abreise = res-line.ankunft THEN   
      ASSIGN   
          arl-list.reslin-name-fgcol = 0  
          arl-list.reslin-name-bgcol = 14.   
  
      IF AVAILABLE res-line AND res-line.pseudofix THEN   
      ASSIGN   
          arl-list.reslin-name-bgcol = 12  
          arl-list.reslin-name-fgcol = 15.   
  
      IF AVAILABLE res-line THEN   
      DO:   
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag"   
          AND reslin-queasy.resnr = res-line.resnr   
          AND reslin-queasy.reslinnr = res-line.reslinnr   
          AND reslin-queasy.betriebsnr = 0 NO-LOCK NO-ERROR.   
        IF AVAILABLE reslin-queasy THEN   
        DO:   
          IF (reslin-queasy.char1 NE "" AND reslin-queasy.deci1 = 0)   
              OR (reslin-queasy.char2 NE "" AND reslin-queasy.deci2 = 0)   
              OR (reslin-queasy.char3 NE "" AND reslin-queasy.deci3 = 0) THEN  
          ASSIGN   
              arl-list.zinr-bgcol = 1  
              arl-list.zinr-fgcol = 15.   
          ELSE  
          ASSIGN   
              arl-list.zinr-bgcol = 9  
              arl-list.zinr-fgcol = 15.   
        END.   
  
        IF res-line.active-flag = 0 AND res-line.zinr NE ""   
           AND res-line.ankunft = ci-date THEN   
        DO:   
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK.   
          IF zimmer.zistatus = 1 THEN   
          DO:   
            ASSIGN arl-list.zinr-fgcol = 0.   
            ASSIGN arl-list.zinr-bgcol = 11.   
          END.   
          ELSE IF zimmer.zistatus = 2 THEN   
          DO:   
            ASSIGN arl-list.zinr-fgcol = 0.   
            ASSIGN arl-list.zinr-bgcol = 10.   
          END.   
          ELSE IF zimmer.zistatus = 3 THEN   
          DO:   
            ASSIGN arl-list.zinr-fgcol = 12.   
            ASSIGN arl-list.zinr-bgcol = 14.   
          END.   
        END.   
      END.   

    /*ITA 090715*/
    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        IF ENTRY(loopi,res-line.zimmer-wunsch, ";") = "WCI-flag" THEN DO:
            ASSIGN arl-list.webci = ENTRY(loopi,res-line.zimmer-wunsch, ";").
            LEAVE.
        END.
    END.
    
    IF arl-list.voucher-nr NE "" THEN ASSIGN arl-list.voucher-flag = "L".
    IF arl-list.kontignr GT 0 THEN ASSIGN arl-list.kontignr-flag = "A ".
    IF arl-list.webci NE "" THEN DO:
        DO loopj = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str1 = ENTRY(loopj,res-line.zimmer-wunsch, ";").
            IF str1 MATCHES "*WCI-req*" THEN DO:
               str2 = ENTRY(2, str1, "=").
               DO loopk = 1 TO NUM-ENTRIES(str2, ","):
                   FIND FIRST queasy WHERE queasy.KEY = 160
                       AND queasy.number1 = INT(ENTRY(loopk, str2, ",")) NO-LOCK NO-ERROR.
                   IF AVAILABLE queasy THEN DO:
                        DO loopl = 1 TO NUM-ENTRIES(queasy.char1, ";") :
                            IF ENTRY(loopl, queasy.char1, ";") MATCHES "*en*" THEN
                            DO:
                                ASSIGN web-com = ENTRY(2, ENTRY(loopl, queasy.char1, ";"), "=") + ", " + web-com.
                                LEAVE.
                            END.
                        END.
                   END.
               END.
               ASSIGN arl-list.comments = "-WEB C/I PREFERENCE-" + CHR(10) + web-com + CHR(10) + arl-list.comments .
            END.
        END.
        ASSIGN arl-list.webci-flag = "W".
    END.
