from aiogram.types import Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.context import FSMContext
from aiogram_dialog.widgets.kbd import Button, Row

from bot.states import FSMAddNote


async def get_note(event_update: Update, state: FSMContext, dialog_manager: DialogManager, **kwargs):
    print(dialog_manager.start_data)
    dialog_manager.dialog_data.update(note=event_update.message.text)
    await state.update_data(note=event_update.message.text)

    return {"note": event_update.message.text}


async def get_date(event_update: Update, state: FSMContext, **kwargs):
    await state.update_data(date=event_update.message.text)
    data_note = await state.get_data()

    return {
        "note": data_note["note"],
        "date": data_note["date"]
    }


async def save_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    # data_note = await state.get_data()
    # await message.answer(text="DONE")
    # await state.clear()
    await callback.message.answer(text="Save")
    print(dialog_manager.start_data)
    print(dialog_manager.dialog_data)
    await dialog_manager.done()


async def close_second_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.done()


note_dialog = Dialog(
    Window(
        Format(
            "Вы находитесь в режиме добавления заметок.\n"
            "Для добавления заметки напиши текс заметки и нажми кнопку отправить."),
        TextInput(
            id="start_input",
            type_factory=str,
            on_success=Next(),
        ),
        state=FSMAddNote.start,
    ),
    Window(
        Format(
            'Отлично!\n'
            'Твоя заметка: {note}\n'
            'Теперь укажи время и дату или можешь просто написать '
            '"Сегодя", "Завтра" или "Всегда :)"'),
        TextInput(
            id="note_input",
            on_success=Next(),
        ),
        getter=get_note,
        state=FSMAddNote.text_note,
    ),
    Window(
        Format(
            "Давате проверим содержание, перед сохранением\n"
            "Дата: {date}"
            "Содержание {note}"
        ),
        Row(
            Button(
                text=Const('Save!'),
                id='button_1',
                on_click=save_dialog),
            Button(
                text=Const('Edit'),
                id='button_2',
                on_click=save_dialog),
            Button(
                text=Const('Cancel'),
                id='button_3',
                on_click=close_second_dialog),
        ),
        getter=get_date,
        state=FSMAddNote.date,
    ),
)
