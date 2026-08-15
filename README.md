# TestUZ — Online Test Platformasi (Django)

## O'rnatish
```bash
pip install django pillow
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Sayt: http://127.0.0.1:8000/
Admin panel: http://127.0.0.1:8000/admin-panel/

## Yangi imkoniyatlar
- **Javoblar aralashtiriladi** — har bir urinishda savol javob variantlari tasodifiy tartibda ko'rsatiladi.
- **Darhol natija** — javobni bosgan zahoti to'g'ri (yashil) yoki noto'g'ri (qizil, to'g'ri javob ko'rsatiladi) ekani ko'rinadi, keyin "Keyingi savol" tugmasi chiqadi.
- **Yakuniy hisobot** — barcha savollarga javob berilgach, pastda "X ta savoldan Y tasiga to'g'ri javob berdingiz" ko'rinadi, so'ng natija saqlanadi.
- **Reyting** — foydalanuvchilarning umumiy to'g'ri javoblar soni (ball) bo'yicha reytingi (`/rating/`), eng ko'p to'plagan birinchi o'rinda.
- **Login / Ro'yxatdan o'tish / Chiqish** — Django auth asosida.
- **Vaqt nazorati (soatlarda)** — admin panelda har bir test uchun "Vaqt (soat)" maydonini to'ldirasiz (masalan 1 soat uchun `1`, 30 daqiqa uchun `0.5`). Foydalanuvchi testni boshlagach, sahifada orqaga sanoqli taymer ko'rinadi; belgilangan vaqt tugashi bilan test **avtomatik yakunlanadi va yopiladi** — hozirgacha berilgan javoblar bilan natija saqlanadi. Bu server tomonida ham nazorat qilinadi: sahifa yangilansa yoki vaqtidan keyin qayta ochilsa, eski urinish 0/berilgan ball bilan yopib qo'yiladi va yangi urinish boshlanadi.

## Admin panel (`/admin-panel/`)
- **Fanlar** (Subject) qo'shiladi.
- **Testlar** (Test) yaratiladi — sarlavha, fan, **vaqt (soat)**, faolligi. Test ichida to'g'ridan-to'g'ri **Savollar** qo'shiladi (inline forma).
- Har bir savolni ochib, **Javob variantlari**ni (4 tadan) va qaysi biri to'g'riligini belgilaysiz.
  - **Validatsiya**: har bir savolda aynan bitta to'g'ri javob bo'lishi shart — 0 ta yoki 2+ ta to'g'ri javob belgilansa, admin panel xatolik ko'rsatib saqlamaydi.
- Bu yerda to'ldirilgan har qanday forma bevosita bazaga (`db.sqlite3`) saqlanadi — sayt darhol yangi test/savollarni ko'rsata boshlaydi.
- Faqat xodim (`is_staff=True`) foydalanuvchilarga navbardagi "⚙️ Admin panel" tugmasi ko'rinadi.
- Admin formalari `core/forms.py` faylidagi `TestAdminForm`, `QuestionAdminForm`, `ChoiceAdminForm` orqali ishlaydi (`core/admin.py` shu formalarni ishlatadi).

## Loyiha tuzilishi
- `testuz/` — sozlamalar va asosiy URL'lar
- `core/` — ilova:
  - `models.py` — Subject, Test (`duration_hours`), Question, Choice, Attempt (`deadline`, `is_expired`), Profile
  - `forms.py` — RegisterForm + admin panel uchun TestAdminForm / QuestionAdminForm / ChoiceAdminForm
  - `admin.py` — admin panel sozlamalari, bitta-to'g'ri-javob validatsiyasi
  - `views.py` — login/register, test ro'yxati, testni ishlash (aralashtirish, taymer, avtomatik yopilish), natija, reyting
  - `templates/core/` — barcha shablonlar (take_test.html — JS asosidagi interaktiv test interfeysi)
