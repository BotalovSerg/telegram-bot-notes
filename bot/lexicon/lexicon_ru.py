from typing import TypedDict, Dict


class LexiconRuDTO(TypedDict):
    command: Dict[str, str]


class LexiconRuMenuDTO(TypedDict):
    main_menu: Dict[str, str]


LEXICON: LexiconRuDTO = LexiconRuDTO(command={
    '/start': '<b>Привет!</b>\nЯ бот, который '
              'поможет тебе управлять своими заметками.'
              '\nЧтобы посмотреть список доступных '
              'команд - набери /help или нажми кнопку Menu',
    '/help': '/addnote - Добавить закладку\n'
             '/showallnotes - Список все заметок',
    '/addnote': 'Давай добавим заметку.\nНапиши текс заметки и нажми кнопку отправить.',
    '/showallnotes': '<b>Список заметок: </b>',
    '/contact': 'Предложения и замечания просьба отправлять на email: 89090168690@mail.ru',
    'edit_notes_button': '❌ РЕДАКТИРОВАТЬ',
    'edit_notes': '<b>Редактировать заметки</b>',
    'cancel': 'ОТМЕНИТЬ',
    'cancel_text': 'Что бы добавить заметку, отправь команду /addnote',
    'no_notes': 'У вас еще нет заметок, что бы добавить заметку, отправь команду /addnote',
    'end_state_add_note': 'Спасибо! Ваша заметка сохранена.\n'
                          'Что бы посмотреть все Ваши заметки \nотправь команду /showallnotes'
                          '\nили отправть команду /addnote для добавления новой заметки'
})

LEXICON_MENU: LexiconRuMenuDTO = LexiconRuMenuDTO(main_menu={
    '/help': 'Список доступных команд',
    '/addnote': 'Добавить закладку',
    '/showallnotes': 'Посмотреть список заметок',
    '/contact': 'Информация для связи😀'
})
