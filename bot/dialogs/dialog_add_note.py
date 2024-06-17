from aiogram.types import Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row

from bot.states import FSMAddNote
from bot.db.requests import add_note


async def get_note(
        event_update: Update,
        dialog_manager: DialogManager,
        **kwargs,
) -> dict[str, str]:
    dialog_manager.dialog_data.update(note=event_update.message.text)

    return {"note": event_update.message.text}


async def get_date(
        event_update: Update,
        dialog_manager: DialogManager,
        **kwargs,
) -> dict[str, str]:
    dialog_manager.dialog_data.update(date=event_update.message.text)

    return {
        "note": dialog_manager.dialog_data["note"],
        "date": dialog_manager.dialog_data["date"]
    }


async def save_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:

    await callback.message.answer(
        text=f"Заметка сохранена\nДля того чтобы посмотреть Ваши земетки\nотправь команду /showallnotes")
    print(callback.from_user.id)
    await add_note(
        session=dialog_manager.start_data["session"],
        data_note=dialog_manager.dialog_data,
        user_id=callback.from_user.id,
    )
    await dialog_manager.done()


async def close_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    await callback.message.answer(text="Отмена")
    await dialog_manager.done()


async def edit_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.switch_to(state=FSMAddNote.start)


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
            'Текс заметки: {note}\n'
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
            "Дата: {date}\n"
            "Содержание: {note}"
        ),
        Row(
            Button(
                text=Const('Save'),
                id='button_1',
                on_click=save_dialog),
            Button(
                text=Const('Edit'),
                id='button_2',
                on_click=edit_dialog),
            Button(
                text=Const('Cancel'),
                id='button_3',
                on_click=close_dialog),
        ),
        getter=get_date,
        state=FSMAddNote.date,
    ),
)
