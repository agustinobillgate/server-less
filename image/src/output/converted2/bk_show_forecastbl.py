from functions.additional_functions import *
import decimal

def bk_show_forecastbl(blockid:str):
    t_bk_event_list = []
    t_bk_room_list = []
    grandtotal:decimal = to_decimal("0.0")
    totamount:decimal = to_decimal("0.0")
    i:int = 0
    blockcode:str = ""
    revenue:decimal = to_decimal("0.0")
    roomrates:decimal = to_decimal("0.0")

    t_bk_event = t_bk_room = None

    t_bk_event_list, T_bk_event = create_model("T_bk_event", {"bezeich":str, "amount":decimal})
    t_bk_room_list, T_bk_room = create_model("T_bk_room", {"bezeich":str, "amount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_event_list, t_bk_room_list, grandtotal, totamount, i, blockcode, revenue, roomrates
        nonlocal blockid


        nonlocal t_bk_event, t_bk_room
        nonlocal t_bk_event_list, t_bk_room_list
        return {"t-bk-event": t_bk_event_list, "t-bk-room": t_bk_room_list}

    grandtotal =  to_decimal("0")
    totamount =  to_decimal("0")

    for bk_event in query(bk_event_list, filters=(lambda bk_event: bk_event.block_id == blockid and bk_event.flag.lower()  == ("**").lower())):

        bk_event_detail = db_session.query(Bk_event_detail).filter(
                 (Bk_event_detail.block_id == bk_event.block_id) & (Bk_event_detail.nr == bk_event.nr)).first()

        if bk_event_detail:
            grandtotal =  to_decimal(bk_event.amount) * to_decimal(bk_event_detail.atendees)
            totamount =  to_decimal(totamount) + to_decimal(grandtotal)
    t_bk_event = T_bk_event()
    t_bk_event_list.append(t_bk_event)

    t_bk_event.bezeich = "Catering revenue"
    t_bk_event.amount =  to_decimal(totamount)

    bk_master = db_session.query(Bk_master).filter(
             (Bk_master.block_id == blockid)).first()

    if bk_master:
        blockcode = bk_master.block_code
        roomrates =  to_decimal("0")
        revenue =  to_decimal("0")


        t_bk_room = T_bk_room()
        t_bk_room_list.append(t_bk_room)

        t_bk_room.bezeich = "Room revenue"
        t_bk_room.amount =  to_decimal(revenue)

        for bk_grid in query(bk_grid_list, filters=(lambda bk_grid: bk_grid.block_code == blockcode)):
            roomrates =  to_decimal(bk_grid.original_qty) * to_decimal(room_rates)
            revenue =  to_decimal(revenue) + to_decimal(roomrates)

            t_bk_room = query(t_bk_room_list, first=True)

            if t_bk_room:
                t_bk_room.amount =  to_decimal(revenue)


            roomrates =  to_decimal("0")

    return generate_output()