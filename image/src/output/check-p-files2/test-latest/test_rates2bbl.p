DEFINE TEMP-TABLE rate-list1
        FIELD origcode  AS CHAR
        FIELD rcode     AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" EXTENT 31 COLUMN-LABEL "Rcode"
        FIELD BERates   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" EXTENT 31 COLUMN-LABEL "BERates".
        
DEFINE TEMP-TABLE rate-list2 like rate-list1.    

/**/
define input parameter gastnr       as integer.
define input parameter frDate       as date.
define input parameter toDate       as date.
define input parameter rateCode     as character.
define output parameter table for rate-list1.
/**/

/*
define variable frDate      as date         initial 8/3/18     no-undo.
define variable toDate      as date         initial 8/5/18    no-undo.
define variable ratecode    as character    initial ""          no-undo.
*/

define variable x           as integer                  no-undo.
define variable i           as integer                  no-undo.
define variable byPax       as logical                  no-undo.
define variable x1          as integer                  no-undo.
define variable currRate    as character                no-undo.    
define variable rm          as character                no-undo.
define variable currDate    as date                     no-undo.


x = toDate - frDate + 1.

currDate = frDate - 1.

find first queasy where queasy.key eq 160 no-lock no-error.
if available queasy then byPax = LOGICAL(STRING(entry(3,entry(15,queasy.char1,"$"),"="))).

/*
frDate toDate ratecode.startperiod ratecode.endperiode
*/

if rateCode eq "" then
do:
    for each guest-pr where guest-pr.gastnr eq gastnr no-lock:
        for each ratecode where ratecode.code eq guest-pr.code
            and ((ratecode.startperiod ge frDate and ratecode.startperiod le toDate) or
                 (ratecode.endperiod ge frDate and ratecode.endperiod le toDate) or 
                 (ratecode.startperiod lt frDate and ratecode.endperiod gt toDate)) no-lock by ratecode.zikatnr by ratecode.zipreis:
        
            run create-list.
        end.       
    end.
end.
else
do:
    for each guest-pr where guest-pr.gastnr eq gastnr
        and guest-pr.code eq rateCode no-lock:
        for each ratecode where ratecode.code eq guest-pr.code
            and ((ratecode.startperiod ge frDate and ratecode.startperiod le toDate) or
                 (ratecode.endperiod ge frDate and ratecode.endperiod le toDate) or 
                 (ratecode.startperiod lt frDate and ratecode.endperiod gt toDate)) no-lock by ratecode.zikatnr by ratecode.zipreis:
        
            run create-list. 
        end.      
    end.
end.


for each rate-list1:
    create rate-list2.
    buffer-copy rate-list1 to rate-list2.
end.    

if byPax eq no then
do:
    for each rate-list1 by rate-list1.origcode:
        if currRate ne rate-list1.origcode then
        do:
            x1 = 1.
        end.       
        else
        do:
            x1 = x1 + 1.
        end. 
        
        currRate = rate-list1.origcode.
        
        if x1 eq 2 then
        do:
            find first rate-list2 where rate-list2.origcode eq currRate no-error.
            if available rate-list2 then
            do:
                delete rate-list2.
            end.
        end.
    end.
end.

for each rate-list1:
    delete rate-list1.
    release rate-list1.
end.

for each rate-list2:
    create rate-list1.
    buffer-copy rate-list2 to rate-list1.
end.            

/*
for each rate-list1:
    /*
    do i = 1 to x:
        find first ratecode where ratecode.code eq rate-list1.origcode no-lock no-error.
        rate-list1.rcode[i] = string(ratecode.zipreis).
    end.
    */
    display rate-list1.origcode format "x(5)" rate-list1.rcode rate-list1.BERates.
end.
*/

/*Untuk ambil value yang udah pernah dilakukan update Rates
IF 060818*/
do i = 1 to x:
    currDate = currDate + 1.
    find last queasy where queasy.key eq 201
        and queasy.number1 eq 5
        and queasy.date1 eq currDate no-lock no-error.
    if available queasy then
    do:
        find first rate-list1 where rate-list1.origcode eq queasy.char1 exclusive-lock no-error.
        if available rate-list1 then
        do:
            if queasy.deci2 ne 0 then
            do:
                assign
                    rate-list1.BERates[i]       = queasy.deci2.
            end.
            else
            do:
                assign
                    rate-list1.BERates[i]       = queasy.deci3.
            end.
        end.
    end.    
end.

/*
for each rate-list1:
    display rate-list1.
end.
*/

procedure create-list:
    find first arrangement where arrangement.argtnr eq ratecode.argtnr no-lock no-error.
    find first queasy where queasy.key eq 152 and queasy.number1 eq ratecode.zikatnr no-lock no-error.
    if available queasy then
    do:
/*        if zimkateg.zikatnr ne 0 then*/
        do:
            rm = queasy.char1.
        end.
    end.
    else if not available queasy then
    do:
        find first zimkateg where zimkateg.typ eq queasy.number1 no-lock no-error.
        if available zimkateg then
        do:
            rm = zimkateg.kurzbez.
        end.
        
    end.
    
        
    create rate-list1.                
    assign
        rate-list1.origcode     = ratecode.code + ":" + rm.          
    
    do i = 1 to x:  
        if (frDate + i - 1) ge ratecode.startperiode and
           (frDate + i - 1) le ratecode.endperiod and 
           i le 31 then
           do:
                assign
                rate-list1.rcode[i]     = ratecode.zipreis
                rate-list1.BERates[i]   = ratecode.zipreis.
            
           end.    
    end.       
end.
