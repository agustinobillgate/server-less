

DEF TEMP-TABLE orges-list
    FIELD region-nr                 AS INT
    FIELD nationnr                  AS INT
    FIELD nationality               AS CHAR
    FIELD B-totRmNights             AS INT
    FIELD B-groupRmNights           AS INT
    FIELD B-individualRmNights      AS INT
    FIELD L-totRmNights             AS INT
    FIELD L-groupRmNights           AS INT
    FIELD L-individualRmNights      AS INT
    FIELD YTD-BtotRmNights          AS INT
    FIELD YTD-BgroupRmNights        AS INT
    FIELD YTD-BindividualRmNights   AS INT
    FIELD YTD-LtotRmNights          AS INT
    FIELD YTD-LgroupRmNights        AS INT
    FIELD YTD-LindividualRmNights   AS INT
    FIELD MTD-BtotRmNights          AS INT
    FIELD MTD-BgroupRmNights        AS INT
    FIELD MTD-BindividualRmNights   AS INT
    FIELD MTD-LtotRmNights          AS INT
    FIELD MTD-LgroupRmNights        AS INT
    FIELD MTD-LindividualRmNights   AS INT
    FIELD pMTD-BtotRmNights         AS DEC
    FIELD pMTD-BgroupRmNights       AS DEC
    FIELD pMTD-BindividualRmNights  AS DEC
    FIELD pMTD-LtotRmNights         AS DEC
    FIELD pMTD-LgroupRmNights       AS DEC
    FIELD pMTD-LindividualRmNights  AS DEC
    FIELD pYTD-BtotRmNights         AS DEC
    FIELD pYTD-BgroupRmNights       AS DEC
    FIELD pYTD-BindividualRmNights  AS DEC
    FIELD pYTD-LtotRmNights         AS DEC
    FIELD pYTD-LgroupRmNights       AS DEC
    FIELD pYTD-LindividualRmNights  AS DEC
    FIELD subtotal-date             AS INT
    FIELD subtotal-MTD              AS INT
    FIELD subtotal-YTD              AS INT
    FIELD psubtotal-date            AS DEC
    FIELD psubtotal-MTD             AS DEC
    FIELD psubtotal-YTD             AS DEC
.



DEF TEMP-TABLE out-list
    FIELD str       AS CHAR
    FIELD num       AS INT
    FIELD nationnr  AS INT
    FIELD region-nr AS INT.

DEF TEMP-TABLE out-list1
    FIELD str       AS CHAR
    FIELD num       AS INT
    FIELD nationnr  AS INT
    FIELD region-nr AS INT.

DEFINE INPUT PARAMETER fdate       AS DATE .
DEFINE INPUT PARAMETER to-date     AS DATE .
DEFINE INPUT PARAMETER show-ytd    AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR out-list.
DEFINE OUTPUT PARAMETER TABLE FOR out-list1.

/*
DEFINE VARIABLE fdate       AS DATE INIT 05/01/13.
DEFINE VARIABLE to-date     AS DATE INIT 06/09/13.
DEFINE VARIABLE show-ytd    AS LOGICAL NO-UNDO INIT YES.
*/

DEFINE VARIABLE tot-b-individual            AS INTEGER.
DEFINE VARIABLE tot-b-grup                  AS INTEGER.
DEFINE VARIABLE tot-l-individual            AS INTEGER.
DEFINE VARIABLE tot-l-grup                  AS INTEGER.
DEFINE VARIABLE MTDtot-b-individual         AS INTEGER.
DEFINE VARIABLE MTDtot-b-grup               AS INTEGER.
DEFINE VARIABLE MTDtot-l-individual         AS INTEGER.
DEFINE VARIABLE MTDtot-l-grup               AS INTEGER.
DEFINE VARIABLE YTDtot-b-individual         AS INTEGER.
DEFINE VARIABLE YTDtot-b-grup               AS INTEGER.
DEFINE VARIABLE YTDtot-l-individual         AS INTEGER.
DEFINE VARIABLE YTDtot-l-grup               AS INTEGER.
DEFINE VARIABLE subtot-b                    AS INTEGER.
DEFINE VARIABLE subtot-l                    AS INTEGER.
DEFINE VARIABLE YTDsubtot-b                 AS INTEGER.
DEFINE VARIABLE YTDsubtot-l                 AS INTEGER.
DEFINE VARIABLE MTDsubtot-b                 AS INTEGER.
DEFINE VARIABLE MTDsubtot-l                 AS INTEGER.
DEFINE VARIABLE subtot-date                 AS INTEGER.
DEFINE VARIABLE subtot-MTD                  AS INTEGER.
DEFINE VARIABLE subtot-YTD                  AS INTEGER.
DEFINE VARIABLE pMTD-BtotRmNights           AS DEC.
DEFINE VARIABLE pMTD-BgroupRmNights         AS DEC.
DEFINE VARIABLE pMTD-BindividualRmNights    AS DEC.
DEFINE VARIABLE pMTD-LtotRmNights           AS DEC.
DEFINE VARIABLE pMTD-LgroupRmNights         AS DEC.
DEFINE VARIABLE pMTD-LindividualRmNights    AS DEC.
DEFINE VARIABLE pYTD-BtotRmNights           AS DEC.
DEFINE VARIABLE pYTD-BgroupRmNights         AS DEC.
DEFINE VARIABLE pYTD-BindividualRmNights    AS DEC.
DEFINE VARIABLE pYTD-LtotRmNights           AS DEC.
DEFINE VARIABLE pYTD-LgroupRmNights         AS DEC.
DEFINE VARIABLE pYTD-LindividualRmNights    AS DEC.
DEFINE VARIABLE psubtotal-date              AS DEC.
DEFINE VARIABLE psubtotal-MTD               AS DEC.
DEFINE VARIABLE psubtotal-YTD               AS DEC.
DEFINE VARIABLE segm_purcode                AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE i                           AS INTEGER.
DEFINE VARIABLE str                         AS CHAR.
DEFINE VARIABLE from-date                   AS DATE.
DEFINE VARIABLE jan1                        AS DATE.
DEFINE VARIABLE mtd1                        AS DATE.

jan1 = DATE(1,1, YEAR(to-date)).
mtd1 = DATE(MONTH(to-date),1,YEAR(to-date)).

IF show-ytd THEN DO:
    from-date = jan1.
    RUN create-list1.
END. 
ELSE DO: 
    from-date = fdate.
    RUN create-list.
END.



PROCEDURE create-list:
    FOR EACH out-list:
      DELETE out-list.
    END.
    FOR EACH out-list1:
        DELETE out-list1.
    END.
    
    FOR EACH orges-list:
      DELETE orges-list.
    END.
    
    ASSIGN
        tot-b-individual            = 0
        tot-b-grup                  = 0
        tot-l-individual            = 0
        tot-l-grup                  = 0
        MTDtot-b-individual         = 0
        MTDtot-b-grup               = 0
        MTDtot-l-individual         = 0
        MTDtot-l-grup               = 0
        YTDtot-b-individual         = 0
        YTDtot-b-grup               = 0
        YTDtot-l-individual         = 0
        YTDtot-l-grup               = 0
        subtot-b                    = 0
        subtot-l                    = 0
        MTDsubtot-b                 = 0
        MTDsubtot-l                 = 0
        YTDsubtot-b                 = 0
        YTDsubtot-l                 = 0
        subtot-date                 = 0
        subtot-MTD                  = 0
        subtot-YTD                  = 0
        pMTD-BtotRmNights           = 0  
        pMTD-BgroupRmNights         = 0  
        pMTD-BindividualRmNights    = 0  
        pMTD-LtotRmNights           = 0  
        pMTD-LgroupRmNights         = 0  
        pMTD-LindividualRmNights    = 0  
        pYTD-BtotRmNights           = 0 
        pYTD-BgroupRmNights         = 0
        pYTD-BindividualRmNights    = 0 
        pYTD-LtotRmNights           = 0 
        pYTD-LgroupRmNights         = 0 
        pYTD-LindividualRmNights    = 0
        psubtotal-date              = 0 
        psubtotal-MTD               = 0 
        psubtotal-YTD               = 0
   .
    
    FOR EACH genstat WHERE genstat.datum GE from-date
        AND genstat.datum LE to-date
        AND genstat.resstatus NE 13
        AND genstat.segmentcode NE 0
        AND genstat.domestic NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES
        AND genstat.res-char[2] MATCHES ("*SEGM_PUR*")
        USE-INDEX gastnrmember_ix NO-LOCK, 
        FIRST nation WHERE nation.nationnr = genstat.domestic :
        
        FIND FIRST orges-list WHERE orges-list.nationnr = nation.nationnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE orges-list THEN
        DO:
            CREATE orges-list.
            ASSIGN orges-list.nationnr    = nation.nationnr
                   orges-list.nationality = nation.bezeich.
        END.
    
        DO i = 1 TO NUM-ENTRIES(genstat.res-char[2],";") - 1:
            str = ENTRY(i, genstat.res-char[2], ";").
            IF SUBSTR(str,1,8) = "SEGM_PUR" THEN 
                segm_purcode = INTEGER(SUBSTR(str,9)).
        END.
        FIND FIRST queasy WHERE queasy.KEY = 143 
            AND queasy.number1 = segm_purcode NO-LOCK NO-ERROR.
        IF queasy.char1 MATCHES "BS" THEN   /* bussiness */
        DO:

            IF genstat.datum GE fdate AND genstat.datum LE to-date THEN DO:

                orges-list.B-totRmNights = orges-list.B-totRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    
                    orges-list.B-groupRmNights = orges-list.B-groupRmNights + 1.
                    tot-b-grup = tot-b-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    
                    orges-list.B-individualRmNights = orges-list.B-individualRmNights + 1.
                    tot-b-individual = tot-b-individual + 1.
                END.
            END.
            
            IF MONTH(genstat.datum) = MONTH(to-date) THEN DO: /*MTD*/
                orges-list.MTD-BtotRmNights = orges-list.MTD-BtotRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.

                IF AVAILABLE reservation AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                   
                    orges-list.MTD-BgroupRmNights = orges-list.MTD-BgroupRmNights + 1.
                    MTDtot-b-grup = MTDtot-b-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    
                    orges-list.MTD-BindividualRmNights = orges-list.MTD-BindividualRmNights + 1.
                    MTDtot-b-individual = MTDtot-b-individual + 1.
                END.
            END.
        END.
        ELSE IF queasy.char1 MATCHES "LS" THEN   /* leissure */
        DO:
            IF genstat.datum GE fdate AND genstat.datum LE to-date THEN DO:
               
                orges-list.L-totRmNights = orges-list.L-totRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    
                    orges-list.L-groupRmNights = orges-list.L-groupRmNights + 1.
                    tot-l-grup = tot-l-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    
                    orges-list.L-individualRmNights = orges-list.L-individualRmNights + 1.
                    tot-l-individual = tot-l-individual + 1.
                END.
            END.

            IF MONTH(genstat.datum) = MONTH(to-date) THEN DO: /*MTD*/
                
                orges-list.MTD-LtotRmNights = orges-list.MTD-LtotRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    
                    orges-list.MTD-LgroupRmNights = orges-list.MTD-LgroupRmNights + 1.
                    MTDtot-l-grup = MTDtot-l-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    
                    orges-list.MTD-LindividualRmNights = orges-list.MTD-LindividualRmNights + 1.
                    MTDtot-l-individual = MTDtot-l-individual + 1.
                END.
            END.
        END.
    END.
    
    
    subtot-b    = tot-b-grup + tot-b-individual.
    subtot-l    = tot-l-grup + tot-l-individual.
    MTDsubtot-b = MTDtot-b-grup + MTDtot-b-individual.
    MTDsubtot-l = MTDtot-l-grup + MTDtot-l-individual.
    subtot-date = subtot-b + subtot-l.
    subtot-MTD  = MTDsubtot-b + MTDsubtot-l.

    
    FOR EACH orges-list NO-LOCK BY orges-list.nationnr:
         
       ASSIGN
            
            orges-list.subtotal-date              = orges-list.B-totRmNights + orges-list.L-totRmNights
            orges-list.subtotal-MTD               = orges-list.MTD-BtotRmNights + orges-list.MTD-LtotRmNights
            orges-list.pMTD-BtotRmNights          = (orges-list.MTD-BtotRmNights / MTDsubtot-b) * 100.00
            orges-list.pMTD-BgroupRmNights        = (orges-list.MTD-BgroupRmNights / MTDtot-b-grup) * 100.00
            orges-list.pMTD-BindividualRmNights   = (orges-list.MTD-BindividualRmNights / MTDtot-b-individual) * 100.00
            orges-list.pMTD-LtotRmNights          = (orges-list.MTD-LtotRmNights / MTDsubtot-l) * 100.00
            orges-list.pMTD-LgroupRmNights        = (orges-list.MTD-LgroupRmNights / MTDtot-l-grup) * 100.00
            orges-list.pMTD-LindividualRmNights   = (orges-list.MTD-LindividualRmNights / MTDtot-l-individual) * 100.00
            orges-list.psubtotal-date             = (orges-list.subtotal-date / subtot-date) * 100.00
            orges-list.psubtotal-MTD              = (orges-list.subtotal-MTD / subtot-MTD) * 100.00

         .
         
         
         IF orges-list.pMTD-BtotRmNights            = ? THEN orges-list.pMTD-BtotRmNights           = 0.00.
         IF orges-list.pMTD-BgroupRmNights          = ? THEN orges-list.pMTD-BgroupRmNights         = 0.00.
         IF orges-list.pMTD-BindividualRmNights     = ? THEN orges-list.pMTD-BindividualRmNights    = 0.00.
         IF orges-list.pMTD-LtotRmNights            = ? THEN orges-list.pMTD-LtotRmNights           = 0.00.
         IF orges-list.pMTD-LgroupRmNights          = ? THEN orges-list.pMTD-LgroupRmNights         = 0.00.
         IF orges-list.pMTD-LindividualRmNights     = ? THEN orges-list.pMTD-LindividualRmNights    = 0.00.
         IF orges-list.psubtotal-date               = ? THEN orges-list.psubtotal-date              = 0.00.
         IF orges-list.psubtotal-MTD                = ? THEN orges-list.psubtotal-MTD               = 0.00.
            

        ASSIGN
            pMTD-BtotRmNights           = pMTD-BtotRmNights         +   orges-list.pMTD-BtotRmNights
            pMTD-BgroupRmNights         = pMTD-BgroupRmNights       +   orges-list.pMTD-BgroupRmNights
            pMTD-BindividualRmNights    = pMTD-BindividualRmNights  +   orges-list.pMTD-BindividualRmNights
            pMTD-LtotRmNights           = pMTD-LtotRmNights         +   orges-list.pMTD-LtotRmNights
            pMTD-LgroupRmNights         = pMTD-LgroupRmNights       +   orges-list.pMTD-LgroupRmNights
            pMTD-LindividualRmNights    = pMTD-LindividualRmNights  +   orges-list.pMTD-LindividualRmNights
            psubtotal-date              = psubtotal-date            +   orges-list.psubtotal-date
            psubtotal-MTD               = psubtotal-MTD             +   orges-list.psubtotal-MTD
         .
        

        CREATE out-list.
        ASSIGN out-list.num = 1
               /*out-list.region-nr = orges-list.region-nr*/
               out-list.str = out-list.str + STRING(orges-list.nationality, "x(30)")
                            + STRING(orges-list.B-totRmNights,          "               >>>>9")
                            + STRING(orges-list.B-groupRmNights,        "               >>>>9")
                            + STRING(orges-list.B-individualRmNights,   "               >>>>9")
                            + STRING(orges-list.L-totRmNights,          "               >>>>9")
                            + STRING(orges-list.L-groupRmNights,        "               >>>>9")
                            + STRING(orges-list.L-individualRmNights,   "               >>>>9")
                            + STRING(orges-list.MTD-BtotRmNights,     "               >>>>9")
                            + STRING(orges-list.MTD-BgroupRmNights,   "               >>>>9")
                            + STRING(orges-list.MTD-BindividualRmNights, "               >>>>9")
                            + STRING(orges-list.MTD-LtotRmNights,     "               >>>>9")
                            + STRING(orges-list.MTD-LgroupRmNights,   "               >>>>9")
                            + STRING(orges-list.MTD-LindividualRmNights, "               >>>>9")
                            + STRING(orges-list.pMTD-BtotRmNights,     "              >>9.99")
                            + STRING(orges-list.pMTD-BgroupRmNights,   "              >>9.99")
                            + STRING(orges-list.pMTD-BindividualRmNights, "              >>9.99")
                            + STRING(orges-list.pMTD-LtotRmNights,     "              >>9.99")
                            + STRING(orges-list.pMTD-LgroupRmNights,   "              >>9.99")
                            + STRING(orges-list.pMTD-LindividualRmNights, "              >>9.99")
                            + STRING(orges-list.subtotal-date,         "               >>>>9")
                            + STRING(orges-list.subtotal-MTD,          "               >>>>9")
                            + STRING(orges-list.psubtotal-date,        "              >>9.99")
                            + STRING(orges-list.psubtotal-MTD,         "              >>9.99")

       .  
    END.
        
        CREATE out-list.
        ASSIGN out-list.num = 9999
           /*out-list.region-nr = 999*/
           out-list.str = out-list.str + STRING("SUB TOTAL", "x(30)")
                        + STRING(subtot-b,         "               >>>>9")
                        + STRING(tot-b-grup,       "               >>>>9")
                        + STRING(tot-b-individual, "               >>>>9")
                        + STRING(subtot-l,         "               >>>>9")
                        + STRING(tot-l-grup,       "               >>>>9")
                        + STRING(tot-l-individual, "               >>>>9")
                        + STRING(MTDsubtot-b,      "               >>>>9")
                        + STRING(MTDtot-b-grup,    "               >>>>9")
                        + STRING(MTDtot-b-individual, "               >>>>9")
                        + STRING(MTDsubtot-l,      "               >>>>9")
                        + STRING(MTDtot-l-grup,       "               >>>>9")
                        + STRING(MTDtot-l-individual, "               >>>>9")
                        + STRING(pMTD-BtotRmNights, "              >>9.99")
                        + STRING(pMTD-BgroupRmNights, "              >>9.99")
                        + STRING(pMTD-BindividualRmNights, "              >>9.99")
                        + STRING(pMTD-LtotRmNights, "              >>9.99")
                        + STRING(pMTD-LgroupRmNights, "              >>9.99")
                        + STRING(pMTD-LindividualRmNights, "              >>9.99")
                        + STRING(subtot-date, "               >>>>9")
                        + STRING(subtot-MTD,  "               >>>>9")
                        + STRING(psubtotal-date, "              >>9.99")
                        + STRING(psubtotal-MTD, "              >>9.99")
                        
           .
        
        
        CREATE out-list.
        ASSIGN out-list.num = 9999
           /*out-list.region-nr = 9999*/
           out-list.str = out-list.str + STRING("G. TOTAL of ROOM NIGHTS : " + STRING(INT(subtot-b + subtot-l)), "x(30)").

END.


PROCEDURE create-list1:
    FOR EACH out-list:
        DELETE out-list.
    END.
    FOR EACH out-list1:
      DELETE out-list1.
    END.
    FOR EACH orges-list:
      DELETE orges-list.
    END.
    
    
    ASSIGN
        tot-b-individual            = 0
        tot-b-grup                  = 0
        tot-l-individual            = 0
        tot-l-grup                  = 0
        MTDtot-b-individual         = 0
        MTDtot-b-grup               = 0
        MTDtot-l-individual         = 0
        MTDtot-l-grup               = 0
        YTDtot-b-individual         = 0
        YTDtot-b-grup               = 0
        YTDtot-l-individual         = 0
        YTDtot-l-grup               = 0
        subtot-b                    = 0
        subtot-l                    = 0
        MTDsubtot-b                 = 0
        MTDsubtot-l                 = 0
        YTDsubtot-b                 = 0
        YTDsubtot-l                 = 0
        subtot-date                 = 0
        subtot-MTD                  = 0
        subtot-YTD                  = 0
        pMTD-BtotRmNights           = 0  
        pMTD-BgroupRmNights         = 0  
        pMTD-BindividualRmNights    = 0  
        pMTD-LtotRmNights           = 0  
        pMTD-LgroupRmNights         = 0  
        pMTD-LindividualRmNights    = 0  
        pYTD-BtotRmNights           = 0 
        pYTD-BgroupRmNights         = 0
        pYTD-BindividualRmNights    = 0 
        pYTD-LtotRmNights           = 0 
        pYTD-LgroupRmNights         = 0 
        pYTD-LindividualRmNights    = 0
        psubtotal-date              = 0 
        psubtotal-MTD               = 0 
        psubtotal-YTD               = 0
   .
    
    FOR EACH genstat WHERE genstat.datum GE from-date
        AND genstat.datum LE to-date
        AND genstat.resstatus NE 13
        AND genstat.segmentcode NE 0
        AND genstat.domestic NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] EQ YES
        AND genstat.res-char[2] MATCHES ("*SEGM_PUR*")
        USE-INDEX gastnrmember_ix NO-LOCK,
        FIRST nation WHERE nation.nationnr = genstat.domestic :
    
        FIND FIRST orges-list WHERE orges-list.nationnr = nation.nationnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE orges-list THEN
        DO:
            CREATE orges-list.
            ASSIGN orges-list.nationnr    = nation.nationnr
                   orges-list.nationality = nation.bezeich.
        END.
    
        DO i = 1 TO NUM-ENTRIES(genstat.res-char[2],";") - 1:
            str = ENTRY(i, genstat.res-char[2], ";").
            IF SUBSTR(str,1,8) = "SEGM_PUR" THEN 
                segm_purcode = INTEGER(SUBSTR(str,9)).
        END.
        FIND FIRST queasy WHERE queasy.KEY = 143 
            AND queasy.number1 = segm_purcode NO-LOCK NO-ERROR.
        IF queasy.char1 MATCHES "BS" THEN   /* bussiness */
        DO:

            IF genstat.datum GE fdate AND genstat.datum LE to-date THEN DO:
                orges-list.B-totRmNights = orges-list.B-totRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation 
                    AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    orges-list.B-groupRmNights = orges-list.B-groupRmNights + 1.
                    tot-b-grup = tot-b-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    orges-list.B-individualRmNights = orges-list.B-individualRmNights + 1.
                    tot-b-individual = tot-b-individual + 1.
                END.
            END.

            IF MONTH(genstat.datum) = MONTH(to-date) THEN DO: /*mtd*/
                orges-list.MTD-BtotRmNights = orges-list.MTD-BtotRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation 
                    AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    orges-list.MTD-BgroupRmNights = orges-list.MTD-BgroupRmNights + 1.
                    MTDtot-b-grup = MTDtot-b-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    orges-list.MTD-BindividualRmNights = orges-list.MTD-BindividualRmNights + 1.
                    MTDtot-b-individual = MTDtot-b-individual + 1.
                END.
            END.
            

            IF genstat.datum GE jan1 AND genstat.datum LE to-date THEN DO:
                orges-list.YTD-BtotRmNights = orges-list.YTD-BtotRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation 
                    AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    orges-list.YTD-BgroupRmNights = orges-list.YTD-BgroupRmNights + 1.
                    YTDtot-b-grup = YTDtot-b-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    orges-list.YTD-BindividualRmNights = orges-list.YTD-BindividualRmNights + 1.
                    YTDtot-b-individual = YTDtot-b-individual + 1.
                END.
            END. 
        END.
        ELSE IF queasy.char1 MATCHES "LS" THEN   /* leissure */
        DO:
           IF genstat.datum GE fdate AND genstat.datum LE to-date THEN DO:
                orges-list.L-totRmNights = orges-list.L-totRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation 
                    AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    orges-list.L-groupRmNights = orges-list.L-groupRmNights + 1.
                    tot-l-grup = tot-l-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    orges-list.L-individualRmNights = orges-list.L-individualRmNights + 1.
                    tot-l-individual = tot-l-individual + 1.
                END.
           END.
           
           IF MONTH(genstat.datum) = MONTH(to-date) THEN DO: /*mtd*/
                orges-list.MTD-LtotRmNights = orges-list.MTD-LtotRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation 
                    AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    orges-list.MTD-LgroupRmNights = orges-list.MTD-LgroupRmNights + 1.
                    MTDtot-l-grup = MTDtot-l-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    orges-list.MTD-LindividualRmNights = orges-list.MTD-LindividualRmNights + 1.
                    MTDtot-l-individual = MTDtot-l-individual + 1.
                END.

           END.

           IF genstat.datum GE jan1 AND genstat.datum LE to-date THEN DO:
                orges-list.YTD-LtotRmNights = orges-list.YTD-LtotRmNights + 1.
                FIND FIRST reservation WHERE reservation.resnr = genstat.resnr
                    NO-LOCK NO-ERROR.
                IF AVAILABLE reservation 
                    AND (INTEGER(reservation.grpflag) + 1) = 2 THEN     /* grup rsv */
                DO:
                    orges-list.YTD-LgroupRmNights = orges-list.YTD-LgroupRmNights + 1.
                    YTDtot-l-grup = YTDtot-l-grup + 1.
                END.
                ELSE    /* individual */
                DO:
                    orges-list.YTD-LindividualRmNights = orges-list.YTD-LindividualRmNights + 1.
                    YTDtot-l-individual = YTDtot-l-individual + 1.
                END.
           END.
        END.
    END.
    
    subtot-b    = tot-b-grup + tot-b-individual.
    subtot-l    = tot-l-grup + tot-l-individual.
    MTDsubtot-b = MTDtot-b-grup + MTDtot-b-individual.
    MTDsubtot-l = MTDtot-l-grup + MTDtot-l-individual.
    YTDsubtot-b = YTDtot-b-grup + YTDtot-b-individual.
    YTDsubtot-l = YTDtot-l-grup + YTDtot-l-individual.
    subtot-date = subtot-b + subtot-l.
    subtot-MTD  = MTDsubtot-b + MTDsubtot-l.
    subtot-YTD  = YTDsubtot-b + YTDsubtot-l.
    
    
    FOR EACH orges-list NO-LOCK BY orges-list.nationnr:
         
         ASSIGN
             orges-list.subtotal-date              = orges-list.B-totRmNights + orges-list.L-totRmNights
             orges-list.subtotal-MTD               = orges-list.MTD-BtotRmNights + orges-list.MTD-LtotRmNights
             orges-list.subtotal-YTD               = orges-list.YTD-BtotRmNights + orges-list.YTD-LtotRmNights
             orges-list.pMTD-BtotRmNights          = (orges-list.MTD-BtotRmNights / MTDsubtot-b) * 100.00
             orges-list.pMTD-BgroupRmNights        = (orges-list.MTD-BgroupRmNights / MTDtot-b-grup) * 100.00
             orges-list.pMTD-BindividualRmNights   = (orges-list.MTD-BindividualRmNights / MTDtot-b-individual) * 100.00
             orges-list.pMTD-LtotRmNights          = (orges-list.MTD-LtotRmNights / MTDsubtot-l) * 100.00
             orges-list.pMTD-LgroupRmNights        = (orges-list.MTD-LgroupRmNights / MTDtot-l-grup) * 100.00
             orges-list.pMTD-LindividualRmNights   = (orges-list.MTD-LindividualRmNights / MTDtot-l-individual) * 100.00
             orges-list.psubtotal-date             = (orges-list.subtotal-date / subtot-date) * 100.00
             orges-list.psubtotal-MTD              = (orges-list.subtotal-MTD / subtot-MTD) * 100.00
             orges-list.pYTD-BtotRmNights          = (orges-list.YTD-BtotRmNights / YTDsubtot-b) * 100.00
             orges-list.pYTD-BgroupRmNights        = (orges-list.YTD-BgroupRmNights / YTDtot-b-grup) * 100.00
             orges-list.pYTD-BindividualRmNights   = (orges-list.YTD-BindividualRmNights / YTDtot-b-individual) * 100.00
             orges-list.pYTD-LtotRmNights          = (orges-list.YTD-LtotRmNights / YTDsubtot-l) * 100.00
             orges-list.pYTD-LgroupRmNights        = (orges-list.YTD-LgroupRmNights / YTDtot-l-grup) * 100.00
             orges-list.pYTD-LindividualRmNights   = (orges-list.YTD-LindividualRmNights / YTDtot-l-individual) * 100.00
             orges-list.psubtotal-YTD              = (orges-list.subtotal-YTD / subtot-YTD) * 100.00
         .
         
         
         IF orges-list.pMTD-BtotRmNights            = ? THEN orges-list.pMTD-BtotRmNights           = 0.00.
         IF orges-list.pMTD-BgroupRmNights          = ? THEN orges-list.pMTD-BgroupRmNights         = 0.00.
         IF orges-list.pMTD-BindividualRmNights     = ? THEN orges-list.pMTD-BindividualRmNights    = 0.00.
         IF orges-list.pMTD-LtotRmNights            = ? THEN orges-list.pMTD-LtotRmNights           = 0.00.
         IF orges-list.pMTD-LgroupRmNights          = ? THEN orges-list.pMTD-LgroupRmNights         = 0.00.
         IF orges-list.pMTD-LindividualRmNights     = ? THEN orges-list.pMTD-LindividualRmNights    = 0.00.
         IF orges-list.psubtotal-date               = ? THEN orges-list.psubtotal-date              = 0.00.
         IF orges-list.psubtotal-MTD                = ? THEN orges-list.psubtotal-MTD               = 0.00.

         
         IF orges-list.pYTD-BtotRmNights            = ? THEN orges-list.pYTD-BtotRmNights           = 0.00.
         IF orges-list.pYTD-BgroupRmNights          = ? THEN orges-list.pYTD-BgroupRmNights         = 0.00.
         IF orges-list.pYTD-BindividualRmNights     = ? THEN orges-list.pYTD-BindividualRmNights    = 0.00.
         IF orges-list.pYTD-LtotRmNights            = ? THEN orges-list.pYTD-LtotRmNights           = 0.00.
         IF orges-list.pYTD-LgroupRmNights          = ? THEN orges-list.pYTD-LgroupRmNights         = 0.00.
         IF orges-list.pYTD-LindividualRmNights     = ? THEN orges-list.pYTD-LindividualRmNights    = 0.00.
         IF orges-list.psubtotal-YTD                = ? THEN orges-list.psubtotal-YTD               = 0.00.

         
         ASSIGN
            pMTD-BtotRmNights           = pMTD-BtotRmNights         +   orges-list.pMTD-BtotRmNights
            pMTD-BgroupRmNights         = pMTD-BgroupRmNights       +   orges-list.pMTD-BgroupRmNights
            pMTD-BindividualRmNights    = pMTD-BindividualRmNights  +   orges-list.pMTD-BindividualRmNights
            pMTD-LtotRmNights           = pMTD-LtotRmNights         +   orges-list.pMTD-LtotRmNights
            pMTD-LgroupRmNights         = pMTD-LgroupRmNights       +   orges-list.pMTD-LgroupRmNights
            pMTD-LindividualRmNights    = pMTD-LindividualRmNights  +   orges-list.pMTD-LindividualRmNights
            pYTD-BtotRmNights           = pYTD-BtotRmNights         +   orges-list.pYTD-BtotRmNights
            pYTD-BgroupRmNights         = pYTD-BgroupRmNights       +   orges-list.pYTD-BgroupRmNights
            pYTD-BindividualRmNights    = pYTD-BindividualRmNights  +   orges-list.pYTD-BindividualRmNights
            pYTD-LtotRmNights           = pYTD-LtotRmNights         +   orges-list.pYTD-LtotRmNights
            pYTD-LgroupRmNights         = pYTD-LgroupRmNights       +   orges-list.pYTD-LgroupRmNights
            pYTD-LindividualRmNights    = pYTD-LindividualRmNights  +   orges-list.pYTD-LindividualRmNights
            psubtotal-date              = psubtotal-date            +   orges-list.psubtotal-date
            psubtotal-MTD               = psubtotal-MTD             +   orges-list.psubtotal-MTD
            psubtotal-YTD               = psubtotal-YTD             +   orges-list.psubtotal-YTD
         .
        
        CREATE out-list1.
        ASSIGN out-list1.num = 1
               /*out-list1.region-nr = orges-list.region-nr*/
               out-list1.str = out-list1.str + STRING(orges-list.nationality, "x(30)")
                            + STRING(orges-list.B-totRmNights,          "               >>>>9")
                            + STRING(orges-list.B-groupRmNights,        "               >>>>9")
                            + STRING(orges-list.B-individualRmNights,   "               >>>>9")
                            + STRING(orges-list.L-totRmNights,          "               >>>>9")
                            + STRING(orges-list.L-groupRmNights,        "               >>>>9")
                            + STRING(orges-list.L-individualRmNights,   "               >>>>9")
                            + STRING(orges-list.MTD-BtotRmNights,     "               >>>>9")
                            + STRING(orges-list.MTD-BgroupRmNights,   "               >>>>9")
                            + STRING(orges-list.MTD-BindividualRmNights, "               >>>>9")
                            + STRING(orges-list.MTD-LtotRmNights,     "               >>>>9")
                            + STRING(orges-list.MTD-LgroupRmNights,   "               >>>>9")
                            + STRING(orges-list.MTD-LindividualRmNights, "               >>>>9")
                            + STRING(orges-list.pMTD-BtotRmNights,     "              >>9.99")
                            + STRING(orges-list.pMTD-BgroupRmNights,   "              >>9.99")
                            + STRING(orges-list.pMTD-BindividualRmNights, "              >>9.99")
                            + STRING(orges-list.pMTD-LtotRmNights,     "              >>9.99")
                            + STRING(orges-list.pMTD-LgroupRmNights,   "              >>9.99")
                            + STRING(orges-list.pMTD-LindividualRmNights, "              >>9.99")
                            + STRING(orges-list.subtotal-date,         "               >>>>9")
                            + STRING(orges-list.subtotal-MTD,          "               >>>>9")
                            + STRING(orges-list.psubtotal-date,        "              >>9.99")
                            + STRING(orges-list.psubtotal-MTD,         "              >>9.99")
                            + STRING(orges-list.YTD-BtotRmNights,       "               >>>>9")
                            + STRING(orges-list.YTD-BgroupRmNights,     "               >>>>9")
                            + STRING(orges-list.YTD-BindividualRmNights,"               >>>>9")
                            + STRING(orges-list.YTD-LtotRmNights,       "               >>>>9")
                            + STRING(orges-list.YTD-LgroupRmNights,     "               >>>>9")
                            + STRING(orges-list.YTD-LindividualRmNights,"               >>>>9")
                            + STRING(orges-list.pYTD-BtotRmNights,     "              >>9.99")
                            + STRING(orges-list.pYTD-BgroupRmNights,   "              >>9.99")
                            + STRING(orges-list.pYTD-BindividualRmNights, "              >>9.99")
                            + STRING(orges-list.pYTD-LtotRmNights,     "              >>9.99")
                            + STRING(orges-list.pYTD-LgroupRmNights,   "              >>9.99")
                            + STRING(orges-list.pYTD-LindividualRmNights, "              >>9.99")
                            + STRING(orges-list.subtotal-YTD,          "               >>>>9")
                            + STRING(orges-list.psubtotal-YTD,         "              >>9.99")
            .
    END.

        CREATE out-list1.
        ASSIGN out-list1.num = 9999
           /*out-list1.region-nr = 999*/
           out-list1.str = out-list1.str + STRING("SUB TOTAL", "x(30)")
                        + STRING(subtot-b,         "               >>>>9")
                        + STRING(tot-b-grup,       "               >>>>9")
                        + STRING(tot-b-individual, "               >>>>9")
                        + STRING(subtot-l,         "               >>>>9")
                        + STRING(tot-l-grup,       "               >>>>9")
                        + STRING(tot-l-individual, "               >>>>9")
                        + STRING(MTDsubtot-b,      "               >>>>9")
                        + STRING(MTDtot-b-grup,    "               >>>>9")
                        + STRING(MTDtot-b-individual, "               >>>>9")
                        + STRING(MTDsubtot-l,      "               >>>>9")
                        + STRING(MTDtot-l-grup,       "               >>>>9")
                        + STRING(MTDtot-l-individual, "               >>>>9")
                        + STRING(pMTD-BtotRmNights, "              >>9.99")
                        + STRING(pMTD-BgroupRmNights, "              >>9.99")
                        + STRING(pMTD-BindividualRmNights, "              >>9.99")
                        + STRING(pMTD-LtotRmNights, "              >>9.99")
                        + STRING(pMTD-LgroupRmNights, "              >>9.99")
                        + STRING(pMTD-LindividualRmNights, "              >>9.99")
                        + STRING(subtot-date, "               >>>>9")
                        + STRING(subtot-MTD,  "               >>>>9")
                        + STRING(psubtotal-date, "              >>9.99")
                        + STRING(psubtotal-MTD, "              >>9.99")
                        + STRING(YTDsubtot-b,      "               >>>>9")
                        + STRING(YTDtot-b-grup,    "               >>>>9")
                        + STRING(YTDtot-b-individual, "               >>>>9")
                        + STRING(YTDsubtot-l,      "               >>>>9")
                        + STRING(YTDtot-l-grup,       "               >>>>9")
                        + STRING(YTDtot-l-individual, "               >>>>9")
                        + STRING(pYTD-BtotRmNights, "              >>9.99")
                        + STRING(pYTD-BgroupRmNights, "              >>9.99")
                        + STRING(pYTD-BindividualRmNights, "              >>9.99")
                        + STRING(pYTD-LtotRmNights , "              >>9.99")
                        + STRING(pYTD-LgroupRmNights, "              >>9.99")
                        + STRING(pYTD-LindividualRmNights, "              >>9.99")
                        + STRING(subtot-YTD,  "               >>>>9")
                        + STRING(psubtotal-YTD, "              >>9.99")
           .
        
        
        CREATE out-list1.
        ASSIGN out-list1.num = 9999
           /*out-list1.region-nr = 9999*/
           out-list1.str = out-list1.str + STRING("G. TOTAL of ROOM NIGHTS : " + STRING(INT(subtot-b + subtot-l)), "x(30)").
    
END.    


