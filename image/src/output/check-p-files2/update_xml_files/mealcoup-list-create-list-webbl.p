 
DEFINE TEMP-TABLE mlist LIKE mealcoup.

DEFINE INPUT  PARAMETER curr-month  AS INTEGER.
DEFINE INPUT  PARAMETER curr-year   AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR mlist.

DEFINE VARIABLE total-used AS INTEGER.
DEFINE VARIABLE total-coupday AS INTEGER EXTENT 31.
DEFINE VARIABLE count-i AS INTEGER.

RUN create-list.

PROCEDURE create-list:
    DEFINE VARIABLE rmNo LIKE zimmer.zinr.    

    FOR EACH mlist:
        DELETE mlist.
    END.
    
    FOR EACH h-journal WHERE MONTH(h-journal.bill-datum) EQ curr-month
        AND YEAR(h-journal.bill-datum) EQ curr-year NO-LOCK,
        FIRST h-bill WHERE h-bill.rechnr EQ h-journal.rechnr 
        AND h-bill.departement EQ h-journal.departement NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr 
        AND h-artikel.departement EQ h-journal.departement 
        AND h-artikel.artart EQ 12 NO-LOCK BY h-journal.bill-datum:
        
        FIND FIRST res-line WHERE res-line.resnr EQ h-bill.resnr
            AND res-line.reslinnr EQ h-bill.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN rmNo = res-line.zinr.
        ELSE rmNo = "".

        FIND FIRST mlist WHERE mlist.resnr EQ h-bill.resnr 
            AND mlist.zinr EQ rmNo NO-ERROR.
        IF NOT AVAILABLE mlist THEN
        DO:
            CREATE mlist.
            ASSIGN 
                mlist.resnr = h-bill.resnr
                mlist.zinr  = rmNo
                mlist.name  = h-bill.bilname.
            .
            IF AVAILABLE res-line THEN
            DO:
                ASSIGN
                    mlist.ankunft = res-line.ankunft
                    mlist.abreise = res-line.abreise.
            END.     

            /*FDL Sept 12, 2024: 033C2C*/
            IF rmNo EQ "" THEN
            DO:
                ASSIGN
                    mlist.NAME  = "[OUTSIDER]"
                    mlist.ankunft = ?
                    mlist.abreise = ?.
            END.
        END.
        ASSIGN 
            /*mlist.verbrauch[DAY(h-journal.bill-datum)] = h-journal.anzahl*/
            mlist.verbrauch[DAY(h-journal.bill-datum)] = mlist.verbrauch[DAY(h-journal.bill-datum)] + h-journal.anzahl
            mlist.verbrauch[32] = mlist.verbrauch[32] + h-journal.anzahl.                      
    END.

    /*FDL Sept 12, 2024: 033C2C*/
    FOR EACH mlist:
        total-used = total-used + mlist.verbrauch[32].

        ASSIGN
            total-coupday[1] = total-coupday[1] + mlist.verbrauch[1]
            total-coupday[2] = total-coupday[2] + mlist.verbrauch[2]
            total-coupday[3] = total-coupday[3] + mlist.verbrauch[3]
            total-coupday[4] = total-coupday[4] + mlist.verbrauch[4]
            total-coupday[5] = total-coupday[5] + mlist.verbrauch[5]
            total-coupday[6] = total-coupday[6] + mlist.verbrauch[6]
            total-coupday[7] = total-coupday[7] + mlist.verbrauch[7]
            total-coupday[8] = total-coupday[8] + mlist.verbrauch[8]
            total-coupday[9] = total-coupday[9] + mlist.verbrauch[9]
            total-coupday[10] = total-coupday[10] + mlist.verbrauch[10]
            total-coupday[11] = total-coupday[11] + mlist.verbrauch[11]
            total-coupday[12] = total-coupday[12] + mlist.verbrauch[12]
            total-coupday[13] = total-coupday[13] + mlist.verbrauch[13]
            total-coupday[14] = total-coupday[14] + mlist.verbrauch[14]
            total-coupday[15] = total-coupday[15] + mlist.verbrauch[15]
            total-coupday[16] = total-coupday[16] + mlist.verbrauch[16]
            total-coupday[17] = total-coupday[17] + mlist.verbrauch[17]
            total-coupday[18] = total-coupday[18] + mlist.verbrauch[18]
            total-coupday[19] = total-coupday[19] + mlist.verbrauch[19]
            total-coupday[20] = total-coupday[20] + mlist.verbrauch[20]
            total-coupday[21] = total-coupday[21] + mlist.verbrauch[21]
            total-coupday[22] = total-coupday[22] + mlist.verbrauch[22]
            total-coupday[23] = total-coupday[23] + mlist.verbrauch[23]
            total-coupday[24] = total-coupday[24] + mlist.verbrauch[24]
            total-coupday[25] = total-coupday[25] + mlist.verbrauch[25]
            total-coupday[26] = total-coupday[26] + mlist.verbrauch[26]
            total-coupday[27] = total-coupday[27] + mlist.verbrauch[27]
            total-coupday[28] = total-coupday[28] + mlist.verbrauch[28]
            total-coupday[29] = total-coupday[29] + mlist.verbrauch[29]
            total-coupday[30] = total-coupday[30] + mlist.verbrauch[30]
            total-coupday[31] = total-coupday[31] + mlist.verbrauch[31]
            .
    END.

    FIND FIRST mlist NO-LOCK NO-ERROR.
    IF AVAILABLE mlist THEN
    DO:
        CREATE mlist.
        ASSIGN
            mlist.zinr          = "ALL"
            mlist.name          = "TOTAL USED:"
            mlist.ankunft       = ?
            mlist.abreise       = ?
            mlist.verbrauch[32] = total-used
            .

        DO count-i = 1 TO 31:
            mlist.verbrauch[count-i] = total-coupday[count-i]. 
        END.
    END.
    /*END FDL*/
END.
