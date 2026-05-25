MONTHS = {
    'uk': ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
           "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"],
    'en': ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"],
    'hu': ["Január", "Február", "Március", "Április", "Május", "Június",
           "Július", "Augusztus", "Szeptember", "Október", "November", "December"],
}

STRINGS = {
    'uk': {
        'choose_lang': '🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:',
        'welcome': (
            '👋 Привіт!\n'
            'Я рахую *скільки днів відпустки* ти можеш взяти прямо зараз '
            'і до кінця контракту.\n\n'
            '🔢 /calc — зробити розрахунок\n'
            '♻️ Після першого разу /calc запитає тільки скільки днів вже взяв\n'
            '🗑️ /reset — ввести дані заново\n'
            '⛔ /cancel — скасувати будь-коли'
        ),
        'ask_know_hours': '📋 Ти знаєш скільки *годин відпустки* тобі надано цього року?',
        'btn_kh_yes': '✅ Так, знаю',
        'btn_kh_calc': '🔢 Порахувати за законом',
        'ask_age': (
            '🎂 Скільки тобі *повних* років?\n'
            '_(Для розрахунку за законодавством Угорщини)_'
        ),
        'err_age': '⚠️ Введи вік — ціле число (напр. *35*). Спробуй ще раз:',
        'ask_children': (
            '👶 Скільки у тебе *дітей до 16 років*?\n'
            '_(Введи 0 якщо немає)_'
        ),
        'err_children': '⚠️ Введи 0 або більше (ціле число). Спробуй ще раз:',
        'calc_hu_result': (
            '✅ Розраховано за законодавством Угорщини:\n'
            'Вік: *{age} р.*, дітей до 16: *{children}*\n'
            '➡️ *{days} дн = {hours:.0f} год*\n'
            '_(Орієнтовно — уточни у HR)_'
        ),
        'ask_total': (
            '📋 *Скільки годин відпустки* ти маєш за рік?\n'
            '_(Ця цифра є у твоєму трудовому договорі або запитай у HR. Найчастіше 168)_'
        ),
        'ask_start_default': '📅 Відпустковий рік починається *1 Січня*.\nПотрібно змінити?',
        'btn_yes': 'Так', 'btn_no': 'Ні',
        'ask_end': '📅 У якому місяці *закінчується* твій контракт?',
        'ask_used': (
            '🏖️ Скільки *днів відпустки* ти вже взяв цього року?\n'
            '_(Введи 0 якщо ще не брав)_'
        ),
        'ask_balance_yn': (
            '💼 Чи є в тебе *перенесені години* з попереднього контракту?\n'
            '_(Наприклад, якщо у тебе лишились невикористані дні або навпаки '
            'ти взяв більше ніж мав право)_'
        ),
        'btn_bal_yes': '✅ Так, є',
        'btn_bal_no': '❌ Ні',
        'ask_balance_val': (
            '💼 Введи баланс у *годинах*:\n'
            '• Лишились дні → позитивне число (напр. `24`)\n'
            '• Взяв більше ніж мав → від\'ємне (напр. `-12`)'
        ),
        'err_balance': '⚠️ Потрібно число — позитивне або від\'ємне (напр. *24* або *\\-12*). Спробуй ще раз:',
        'report_balance_line': 'Баланс-початок: {bal:+.1f} год ({bal_d:+.1f} дн)',
        'now_available_pos': '✅ *Зараз ({month}): {days:.1f} дн* можна взяти',
        'now_available_neg': '⏳ *Зараз ({month}): {days:.1f} дн* ще не вистачає',
        'saved_prompt': (
            '👋 З поверненням! Збережено: *{total}* год, {start}–{end}, баланс: {bal:+.1f} год.\n'
            '🏖️ Скільки *днів* відпустки ти вже взяв?'
        ),
        'reset_done': '🗑️ Дані видалено. Наступний /calc запитає все заново.',
        'reset_none': 'Немає збережених даних.',
        'cancelled': '⛔ Скасовано. Обери мову або /calc щоб почати знову:',
        'err_positive': '⚠️ Потрібно число більше 0 (напр. *168*). Спробуй ще раз:',
        'err_nonneg': '⚠️ Потрібно 0 або більше (напр. *0* або *6*). Спробуй ще раз:',
        'report_header': '📊 *Розрахунок відпустки*',
        'contract_line': 'Контракт: {start} – {end} ({dur} міс.)',
        'total_line': 'До кінця контракту: *{rem_d:.1f} дн*',
        'col_month': 'Місяць', 'col_accrued': 'Накоп', 'col_avail': 'Дост.',
        'disclaimer': '_Орієнтовно, не юридична консультація._',
        'calc_again': '🔄 Порахувати ще раз — /calc',
    },
    'en': {
        'choose_lang': '🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:',
        'welcome': (
            '👋 Hi!\n'
            'I calculate *how many vacation days* you can take right now '
            'and by the end of your contract.\n\n'
            '🔢 /calc — run the calculation\n'
            '♻️ After the first time, /calc only asks how many days you\'ve used\n'
            '🗑️ /reset — enter new contract data\n'
            '⛔ /cancel — cancel at any time'
        ),
        'ask_know_hours': '📋 Do you know how many *vacation hours* you have this year?',
        'btn_kh_yes': '✅ Yes, I know',
        'btn_kh_calc': '🔢 Calculate by law',
        'ask_age': (
            '🎂 How old are you (full years)?\n'
            '_(For calculation under Hungarian labour law)_'
        ),
        'err_age': '⚠️ Enter age as a whole number (e.g. *35*). Try again:',
        'ask_children': (
            '👶 How many *children under 16* do you have?\n'
            '_(Enter 0 if none)_'
        ),
        'err_children': '⚠️ Enter 0 or more (whole number). Try again:',
        'calc_hu_result': (
            '✅ Calculated under Hungarian labour law:\n'
            'Age: *{age}*, children under 16: *{children}*\n'
            '➡️ *{days} d = {hours:.0f} h*\n'
            '_(Approximate — confirm with HR)_'
        ),
        'ask_total': (
            '📋 How many *vacation hours* do you have per year?\n'
            '_(This is written in your employment contract or ask HR. Usually 168)_'
        ),
        'ask_start_default': '📅 Vacation year starts *January 1st*.\nDo you need to change this?',
        'btn_yes': 'Yes', 'btn_no': 'No',
        'ask_end': '📅 In which month does your contract *end*?',
        'ask_used': (
            '🏖️ How many *vacation days* have you already taken this year?\n'
            '_(Enter 0 if none)_'
        ),
        'ask_balance_yn': (
            '💼 Do you have *carried-over hours* from a previous contract?\n'
            '_(For example, if you had unused days left over or took more than you were entitled to)_'
        ),
        'btn_bal_yes': '✅ Yes',
        'btn_bal_no': '❌ No',
        'ask_balance_val': (
            '💼 Enter balance in *hours*:\n'
            '• Days remaining → positive number (e.g. `24`)\n'
            '• Took more than entitled → negative (e.g. `-12`)'
        ),
        'err_balance': '⚠️ Enter a number — positive or negative (e.g. *24* or *\\-12*). Try again:',
        'report_balance_line': 'Opening balance: {bal:+.1f} h ({bal_d:+.1f} d)',
        'now_available_pos': '✅ *Right now ({month}): {days:.1f} d* available to take',
        'now_available_neg': '⏳ *Right now ({month}): {days:.1f} d* short (accruing each month)',
        'saved_prompt': (
            '👋 Welcome back! Saved: *{total}* h, {start}–{end}, balance: {bal:+.1f} h.\n'
            '🏖️ How many *vacation days* have you already taken?'
        ),
        'reset_done': '🗑️ Data cleared. The next /calc will ask everything again.',
        'reset_none': 'No saved data.',
        'cancelled': '⛔ Cancelled. Choose a language or /calc to start again:',
        'err_positive': '⚠️ Enter a number greater than 0 (e.g. *168*). Try again:',
        'err_nonneg': '⚠️ Enter 0 or more (e.g. *0* or *6*). Try again:',
        'report_header': '📊 *Vacation Report*',
        'contract_line': 'Contract: {start} – {end} ({dur} months)',
        'total_line': 'Remaining by end of contract: *{rem_d:.1f} d*',
        'col_month': 'Month', 'col_accrued': 'Accr.', 'col_avail': 'Avail.',
        'disclaimer': '_Approximate, not legal advice._',
        'calc_again': '🔄 Calculate again — /calc',
    },
    'hu': {
        'choose_lang': '🇺🇦 Оберіть мову / 🇬🇧 Choose language / 🇭🇺 Válasszon nyelvet:',
        'welcome': (
            '👋 Szia!\n'
            'Kiszámolom, hogy *hány szabadnapot* vehetsz ki most azonnal '
            'és a szerződés végéig összesen.\n\n'
            '🔢 /calc — számítás indítása\n'
            '♻️ Első alkalom után a /calc csak azt kérdezi, hány napot vettél ki\n'
            '🗑️ /reset — adatok újbóli megadása\n'
            '⛔ /cancel — megszakítás bármikor'
        ),
        'ask_know_hours': '📋 Tudod, hány *szabadságórád* van ebben az évben?',
        'btn_kh_yes': '✅ Igen, tudom',
        'btn_kh_calc': '🔢 Törvény alapján számítsd ki',
        'ask_age': (
            '🎂 Hány éves vagy (betöltött évek)?\n'
            '_(Magyar munkatörvény alapján számítjuk ki)_'
        ),
        'err_age': '⚠️ Add meg koredat egész számként (pl. *35*). Próbáld újra:',
        'ask_children': (
            '👶 Hány *16 éven aluli gyermeked* van?\n'
            '_(Írj be 0-t, ha nincs)_'
        ),
        'err_children': '⚠️ Adj meg 0-t vagy annál nagyobb számot. Próbáld újra:',
        'calc_hu_result': (
            '✅ Magyar munkatörvény alapján kiszámítva:\n'
            'Kor: *{age} év*, 16 alatti gyerek: *{children}*\n'
            '➡️ *{days} nap = {hours:.0f} óra*\n'
            '_(Tájékoztató — kérjük ellenőrizd HR-rel)_'
        ),
        'ask_total': (
            '📋 Hány *szabadságórád* van évente?\n'
            '_(Ez a munkaszerződésedben van írva, vagy kérdezd meg a HR-t. Általában 168)_'
        ),
        'ask_start_default': '📅 A szabadságév *január 1-jén* kezdődik.\nMeg kell változtatni?',
        'btn_yes': 'Igen', 'btn_no': 'Nem',
        'ask_end': '📅 Melyik hónapban *ér véget* a szerződésed?',
        'ask_used': (
            '🏖️ Hány *szabadnapot* vettél már ki ebben az évben?\n'
            '_(Írd be 0-t, ha még nem vettél ki)_'
        ),
        'ask_balance_yn': (
            '💼 Van *átvitt egyenleged* az előző szerződésből?\n'
            '_(Például ha maradt ki nem vett szabadnapod, vagy többet vettél ki, mint amennyi járt)_'
        ),
        'btn_bal_yes': '✅ Igen',
        'btn_bal_no': '❌ Nem',
        'ask_balance_val': (
            '💼 Add meg az egyenleget *órában*:\n'
            '• Maradt napok → pozitív szám (pl. `24`)\n'
            '• Többet vettél ki → negatív (pl. `-12`)'
        ),
        'err_balance': '⚠️ Adj meg egy számot — pozitívat vagy negatívat (pl. *24* vagy *\\-12*). Próbáld újra:',
        'report_balance_line': 'Nyitó egyenleg: {bal:+.1f} óra ({bal_d:+.1f} nap)',
        'now_available_pos': '✅ *Most ({month}): {days:.1f} nap* kivehető',
        'now_available_neg': '⏳ *Most ({month}): {days:.1f} nappal* kevesebb (havonta gyűlik)',
        'saved_prompt': (
            '👋 Üdv újra! Mentve: *{total}* óra, {start}–{end}, egyenleg: {bal:+.1f} óra.\n'
            '🏖️ Hány *szabadnapot* vettél már ki?'
        ),
        'reset_done': '🗑️ Adatok törölve. A következő /calc mindent újra kérdez.',
        'reset_none': 'Nincs mentett adat.',
        'cancelled': '⛔ Megszakítva. Válassz nyelvet vagy /calc az újrakezdéshez:',
        'err_positive': '⚠️ Adj meg 0-nál nagyobb számot (pl. *168*). Próbáld újra:',
        'err_nonneg': '⚠️ Adj meg 0-t vagy annál nagyobb számot (pl. *0* vagy *6*). Próbáld újra:',
        'report_header': '📊 *Szabadság kalkulátor*',
        'contract_line': 'Szerződés: {start} – {end} ({dur} hó)',
        'total_line': 'A szerződés végéig marad: *{rem_d:.1f} nap*',
        'col_month': 'Hónap', 'col_accrued': 'Felhalm.', 'col_avail': 'Elérh.',
        'disclaimer': '_Tájékoztató jellegű, nem jogi tanácsadás._',
        'calc_again': '🔄 Újra számolni — /calc',
    },
}
