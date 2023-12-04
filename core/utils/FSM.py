from aiogram.fsm.state import StatesGroup, State


class FSM(StatesGroup):
    main_menu = State()
    types = State()
    offers = State()
    geo = State()
    languages = State()
    sizes = State()
    TB = State()  # Test or Buy
    feedback = State()
    statistics = State()
    report = State()
