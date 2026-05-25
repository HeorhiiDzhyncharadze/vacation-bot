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
        'ask_hu_confirm': '📋 Використати *{hours:.0f} год* для розрахунку або ввести своє число?',
        'btn_huc_use': '✅ Використати {hours:.0f} год',
        'btn_huc_change': '✏️ Ввести своє число',
        'ask_hours_type': '📋 Твій контракт *{start}–{end}* ({dur} міс.). Скільки годин відпустки маєш?',
        'btn_ht_period': '📅 За контракт ({start}–{end}, {dur} міс.)',
        'btn_ht_annual': '📆 За повний рік (12 міс.)',
        'btn_ht_period_chosen': '📅 Введу за контракт',
        'ask_total_period': '📋 Скільки *годин відпустки* маєш за цей контракт (*{start}–{end}*, {dur} міс.)?',
        'ask_total': (
            '📋 *Скільки годин відпустки* ти маєш за *повний рік* (12 місяців)?\n'
            '_(Ця цифра в трудовому договорі або у HR — у кожного своя)_'
        ),
        'ask_start_default': (
            '📅 *З якого місяця* нараховується твоя відпустка цього року?\n'
            'Зазвичай — з *Січня*. Якщо не впевнений — залишай Січень.'
        ),
        'btn_yes': 'Так', 'btn_no': 'Ні',
        'btn_cs_keep': '✅ З Січня', 'btn_cs_change': '📅 Інший місяць',
        'ask_end_year_yn': '📅 Твій контракт *до кінця цього року* (до Грудня)?',
        'btn_ey_yes': '✅ Так, до Грудня', 'btn_ey_no': '📅 Ні, обрати місяць',
        'ask_end': '📅 У якому місяці *закінчується* твій контракт?',
        'ask_used': (
            '🏖️ Скільки *днів відпустки* ти вже взяв цього року?\n'
            '_(Введи 0 якщо ще не брав)_'
        ),
        'ask_balance_yn': (
            '💼 Чи є в тебе *залишок із минулого року*?\n'
            '_(Невикористані дні або взяв більше ніж мав право.\n'
            'Якщо не знаєш — тисни "Ні")_'
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
        'timeout': '⏱️ Сесія завершилась через бездіяльність. Натисни /calc щоб почати знову.',
        'help': (
            'ℹ️ *Vacation Calculator Bot*\n\n'
            'Рахує скільки днів відпустки можна взяти зараз і до кінця контракту.\n\n'
            '*Команди:*\n'
            '/calc — розрахувати\n'
            '/reset — ввести дані заново\n'
            '/cancel — скасувати\n'
            '/help — ця довідка'
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
        'ask_hu_confirm': '📋 Use *{hours:.0f} h* for the calculation or enter your own number?',
        'btn_huc_use': '✅ Use {hours:.0f} h',
        'btn_huc_change': '✏️ Enter my own',
        'ask_hours_type': '📋 Your contract: *{start}–{end}* ({dur} months). How many vacation hours do you have?',
        'btn_ht_period': '📅 For this period ({start}–{end}, {dur} mo)',
        'btn_ht_annual': '📆 Full year (12 months)',
        'btn_ht_period_chosen': '📅 Entering for contract period',
        'ask_total_period': '📋 How many *vacation hours* do you have for this period (*{start}–{end}*, {dur} months)?',
        'ask_total': (
            '📋 How many *vacation hours* do you have per *full year* (12 months)?\n'
            '_(Check your employment contract or ask HR — it differs for everyone)_'
        ),
        'ask_start_default': (
            '📅 *Which month* does your vacation year start?\n'
            'Usually *January*. If unsure — keep January.'
        ),
        'btn_yes': 'Yes', 'btn_no': 'No',
        'btn_cs_keep': '✅ From January', 'btn_cs_change': '📅 Different month',
        'ask_end_year_yn': '📅 Does your contract run *until end of this year* (December)?',
        'btn_ey_yes': '✅ Yes, until December', 'btn_ey_no': '📅 No, choose month',
        'ask_end': '📅 In which month does your contract *end*?',
        'ask_used': (
            '🏖️ How many *vacation days* have you already taken this year?\n'
            '_(Enter 0 if none)_'
        ),
        'ask_balance_yn': (
            '💼 Do you have a *carry-over balance from last year*?\n'
            '_(Unused days left over, or you took more than allowed.\n'
            'If unsure — tap "No")_'
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
        'timeout': '⏱️ Session timed out. Press /calc to start again.',
        'help': (
            'ℹ️ *Vacation Calculator Bot*\n\n'
            'Calculates how many vacation days you can take now and by contract end.\n\n'
            '*Commands:*\n'
            '/calc — calculate\n'
            '/reset — re-enter contract data\n'
            '/cancel — cancel\n'
            '/help — this help'
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
        'ask_hu_confirm': '📋 Használd a *{hours:.0f} óra* értéket a számításhoz, vagy add meg a sajátodat?',
        'btn_huc_use': '✅ {hours:.0f} óra használata',
        'btn_huc_change': '✏️ Saját szám megadása',
        'ask_hours_type': '📋 A szerződésed: *{start}–{end}* ({dur} hó). Hány szabadságórád van?',
        'btn_ht_period': '📅 Erre az időszakra ({start}–{end}, {dur} hó)',
        'btn_ht_annual': '📆 Teljes évre (12 hónap)',
        'btn_ht_period_chosen': '📅 Időszakra adom meg',
        'ask_total_period': '📋 Hány *szabadságórád* van erre az időszakra (*{start}–{end}*, {dur} hó)?',
        'ask_total': (
            '📋 Hány *szabadságórád* van *teljes évre* (12 hónapra)?\n'
            '_(Ez a munkaszerződésedben szerepel vagy kérdezd meg a HR-t — mindenkinél más)_'
        ),
        'ask_start_default': (
            '📅 *Melyik hónaptól* gyűlik a szabadságod az idén?\n'
            'Általában *januártól*. Ha nem tudod — hagyd Januárt.'
        ),
        'btn_yes': 'Igen', 'btn_no': 'Nem',
        'btn_cs_keep': '✅ Januártól', 'btn_cs_change': '📅 Más hónap',
        'ask_end_year_yn': '📅 A szerződésed *az év végéig* tart (December)?',
        'btn_ey_yes': '✅ Igen, decemberig', 'btn_ey_no': '📅 Nem, hónap választás',
        'ask_end': '📅 Melyik hónapban *ér véget* a szerződésed?',
        'ask_used': (
            '🏖️ Hány *szabadnapot* vettél már ki ebben az évben?\n'
            '_(Írd be 0-t, ha még nem vettél ki)_'
        ),
        'ask_balance_yn': (
            '💼 Van *átvitt egyenleged a tavalyi évből*?\n'
            '_(Ki nem vett napok, vagy többet vettél ki, mint amennyi járt.\n'
            'Ha nem tudod — nyomd a "Nem"-et)_'
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
        'timeout': '⏱️ A munkamenet lejárt. Nyomd meg a /calc gombot az újrakezdéshez.',
        'help': (
            'ℹ️ *Vacation Calculator Bot*\n\n'
            'Kiszámítja hány szabadnapot vehetsz ki most és a szerződés végéig.\n\n'
            '*Parancsok:*\n'
            '/calc — számítás\n'
            '/reset — adatok újbóli megadása\n'
            '/cancel — megszakítás\n'
            '/help — ez a súgó'
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
