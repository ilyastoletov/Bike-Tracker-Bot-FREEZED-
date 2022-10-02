from aiogram.fsm.state import StatesGroup, State

class BikeStates(StatesGroup):
    choose_sport = State()
    location_start = State()
    ready = State()
    ride = State()
    registration = State()