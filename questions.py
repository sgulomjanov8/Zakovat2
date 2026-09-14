# questions.py
import re
from difflib import SequenceMatcher

LOGICAL_QUESTIONS = [
    {
        "id": 1,
        "q": "1. Bir kishi yomg'irda soyabonsiz va kalta shlyapasiz yurgan bo'lsa ham, birorta sochi ho'l bo'lmadi. Bu qanday bo'lishi mumkin?",
        "image": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800",
        "hint": "💡 Maslahat: Insonning boshida sochi bo'lmasligi ham mumkin.",
        "a": ["kal", "u kal", "sochi yo'q", "sochi yoq", "kal edi", "sochi yo'qligi uchun"]
    },
    {
        "id": 2,
        "q": "2. Qaysi oyda odamlar eng kam uxlashadi?",
        "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
        "hint": "💡 Maslahat: Bu oyda kunlar soni boshqalariga qaraganda kamroq.",
        "a": ["fevral", "fevral oyida", "fevralda"]
    },
    {
        "id": 3,
        "q": "3. Tunda qorong'i xonada qora mushuk o'tiribdi. Qora ko'zoynak taqqan haydovchi uni qanday qilib darrov ko'rib qoldi?",
        "image": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800",
        "hint": "💡 Maslahat: Xona qorong'i bo'lsa ham, ko'chada vaqt boshqacha bo'lishi mumkin.",
        "a": ["kunduzi", "kun duzi", "kun edi", "kunduzi edi", "kunduz kuni", "kun vakti"]
    },
    {
        "id": 4,
        "q": "4. Uni qanchalik ko'p olsangiz, uning hajmi shunchalik kattalashib boraveradi. U nima?",
        "image": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=800",
        "hint": "💡 Maslahat: Yer ostidagi yoki devordagi bo'shliq.",
        "a": ["chuqur", "chuqurcha", "o'ra", "ora", "chuqurini"]
    },
    {
        "id": 5,
        "q": "5. Siz uni ushlay olmaysiz, lekin u doim siz bilan birga yuradi va faqat qorong'ida yo'qoladi. U nima?",
        "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=800",
        "hint": "💡 Maslahat: Yorug'lik tushganda yerda hosil bo'ladi.",
        "a": ["soya", "soyasi", "o'z soyasi", "soyamiz"]
    },
    {
        "id": 6,
        "q": "6. Suv ostida qaysi ko'zoynak bilan ham biror narsa ko'rib bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
        "hint": "💡 Maslahat: Suv ostida hamma joy qorong'i yoki ko'z yumuq bo'lishi mumkin.",
        "a": ["qorong'ida", "qorongida", "ko'z yumilganda", "yumuq ko'z", "ko'z yumik bo'lsa", "yumilgan koz"]
    },
    {
        "id": 7,
        "q": "7. Qaysi idishdan biror narsa yeb bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800",
        "hint": "💡 Maslahat: Bu idish bo'sh yoki teshik bo'lishi mumkin.",
        "a": ["bo'sh idish", "bosh idish", "bo'sh", "bosh", "teshik idish"]
    },
    {
        "id": 8,
        "q": "8. Stol ustida 3 ta olma bor edi. Siz 2 tasini oldingiz. Sizda nechta olma bor?",
        "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
        "hint": "💡 Maslahat: Siz olgan olmalarni hisoblang.",
        "a": ["2 ta", "2", "ikkita", "2ta"]
    },
    {
        "id": 9,
        "q": "9. Bir xonada 5 ta sham yonib turibdi. 2 tasi o'chirildi. Xonada nechta sham qoldi?",
        "image": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=800",
        "hint": "💡 Maslahat: O'chirilgan shamlar ham xonada qoladi.",
        "a": ["5 ta", "5", "beshta", "5ta"]
    },
    {
        "id": 10,
        "q": "10. Daraxtda 10 ta qush o'tirgan edi. Ovchi bittasini otdi. Daraxtda nechta qush qoldi?",
        "image": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=800",
        "hint": "💡 Maslahat: O'q ovozidan keyin qolgan qushlar nima qiladi?",
        "a": ["0 ta", "0", "hech biri", "bironta ham", "qolmaydi", "hech qancha", "0ta"]
    },
    {
        "id": 11,
        "q": "11. Elektr poyezdi shimolga qarab ketmoqda. Uning tutuni qaysi tomonga ketadi?",
        "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800",
        "hint": "💡 Maslahat: Elektr poyezdiga e'tibor bering.",
        "a": ["tutuni yo'q", "tutun chiqmaydi", "hech qaysi tomonga", "tutuni yoq", "elektr poyezdida tutun bo'lmaydi"]
    },
    {
        "id": 12,
        "q": "12. Siz poygada ikkinchi o'rindagi odamni quvib o'tdingiz. Endi nechanchi o'rindasiz?",
        "image": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800",
        "hint": "💡 Maslahat: Siz kimning o'rnini egalladingiz?",
        "a": ["2", "ikkinchi", "2-o'rin", "ikkinchi o'rin", "2 o'rin", "2-orin"]
    },
    {
        "id": 13,
        "q": "13. Poygada oxirgi odamni quvib o'tdingiz. Endi nechanchi o'rindasiz?",
        "image": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800",
        "hint": "💡 Maslahat: Oxirgi odamni quvib o'tish mumkinmi?",
        "a": ["mumkin emas", "bo'lmaydi", "imkonsiz", "oxirgisini quvib bo'lmaydi", "bolmaydi"]
    },
    {
        "id": 14,
        "q": "14. Bir odam 10 qavatli binodan sakradi, ammo hech qanday jarohat olmadi. Qanday qilib?",
        "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800",
        "hint": "💡 Maslahat: U qayerdan sakraganiga e'tibor bering.",
        "a": ["birinchi qavatdan", "1-qavatdan", "pastdan", "1 qavatdan", "paski qavatdan"]
    },
    {
        "id": 15,
        "q": "15. Qaysi narsa qurigani sari ho'l bo'lib boradi?",
        "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800",
        "hint": "💡 Maslahat: U bilan suvni artamiz.",
        "a": ["sochiq", "sochiqni", "lappa"]
    },
    {
        "id": 16,
        "q": "16. Qaysi narsa qancha ko'p ishlatilsa, shuncha qisqaradi?",
        "image": "https://images.unsplash.com/photo-1603899122634-f086ca5f5ddd?w=800",
        "hint": "💡 Maslahat: U yorug'lik beradi.",
        "a": ["sham", "shamni", "sovun", "qalam"]
    },
    {
        "id": 17,
        "q": "17. Qaysi narsa og'zi bor, lekin gapirmaydi?",
        "image": "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=800",
        "hint": "💡 Maslahat: U suv bilan bog'liq.",
        "a": ["daryo", "daryoning og'zi", "qop", "ko'za"]
    },
    {
        "id": 18,
        "q": "18. Qaysi narsa oyog'i bor, lekin yura olmaydi?",
        "image": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
        "hint": "💡 Maslahat: Uyda undan ko'p uchraydi.",
        "a": ["stol", "stul", "mebel", "karavot", "krovat"]
    },
    {
        "id": 19,
        "q": "19. Qaysi narsa qo'li bor, lekin hech narsani ushlay olmaydi?",
        "image": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?w=800",
        "hint": "💡 Maslahat: U vaqtni ko'rsatadi.",
        "a": ["soat", "soatning qo'li", "soat strelkasi", "strelka"]
    },
    {
        "id": 20,
        "q": "20. Qaysi narsa ko'zi bor, lekin ko'ra olmaydi?",
        "image": "https://images.unsplash.com/photo-1512758017271-d7b84c2113f1?w=800",
        "hint": "💡 Maslahat: Tikishda undan foydalaniladi.",
        "a": ["igna", "ignaning ko'zi", "igna ko'zi"]
    },
    {
        "id": 21,
        "q": "21. Qaysi narsa tishi bor, lekin tishlay olmaydi?",
        "image": "https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800",
        "hint": "💡 Maslahat: Soch bilan ishlatiladi.",
        "a": ["taroq", "soch taroq", "taroqning tishi", "arra"]
    },
    {
        "id": 22,
        "q": "22. Qaysi narsa qanotsiz uchadi?",
        "image": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=800",
        "hint": "💡 Maslahat: Uni osmonda ko'rish mumkin.",
        "a": ["bulut", "bulutlar", "vaqt", "shamol"]
    },
    {
        "id": 23,
        "q": "23. Qaysi narsa qancha ko'paysa, shuncha kam ko'rasiz?",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "hint": "💡 Maslahat: Yorug'likning teskarisini o'ylang.",
        "a": ["qorong'ulik", "qorong'i", "zulmat", "qorong'ulik ko'payganda", "tuman"]
    },
    {
        "id": 24,
        "q": "24. Qaysi narsa sizniki, lekin uni boshqalar sizdan ko'proq ishlatadi?",
        "image": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=800",
        "hint": "💡 Maslahat: Odamlar sizga murojaat qilganda aytadi.",
        "a": ["ism", "ismingiz", "mening ismim", "otim"]
    },
    {
        "id": 25,
        "q": "25. Qaysi savolga hech qachon 'ha' deb javob bera olmaysiz?",
        "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
        "hint": "💡 Maslahat: Oddiy holat haqida o'ylang.",
        "a": ["uxlayapsanmi", "uxlayapsizmi", "uxlayotganmisan", "o'ldingmi", "uxlayapsanmi?"]
    },
    {
        "id": 26,
        "q": "26. Ertalab 4 oyoqda, tushda 2 oyoqda, kechqurun 3 oyoqda yuradigan narsa nima?",
        "image": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=800",
        "hint": "💡 Maslahat: Bu mashhur qadimiy topishmoq.",
        "a": ["inson", "odam", "odamzod"]
    },
    {
        "id": 27,
        "q": "27. Bir kilogramm temir og'irmi yoki bir kilogramm paxta?",
        "image": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800",
        "hint": "💡 Maslahat: Ikkalasining massasini solishtiring.",
        "a": ["teng", "bir xil", "ikkalasi teng", "teng keladi"]
    },
    {
        "id": 28,
        "q": "28. Xonada 4 burchak bor. Har burchakda bittadan mushuk o'tiribdi. Har mushuk qarshisida 3 ta mushukni ko'rmoqda. Jami nechta mushuk bor?",
        "image": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=800",
        "hint": "💡 Maslahat: Har burchakda bittadan mushuk bor.",
        "a": ["4 ta", "4", "to'rtta", "4ta"]
    },
    {
        "id": 29,
        "q": "29. 2 ta ota va 2 ta o'g'il baliq oviga bordi. Ular jami 3 ta baliq tutishdi va har biriga bittadan tegdi. Qanday qilib?",
        "image": "https://images.unsplash.com/photo-1516707352573-1b1e2e8e1d4a?w=800",
        "hint": "💡 Maslahat: Ular uch kishi bo'lishi mumkin.",
        "a": ["bobo ota o'g'il", "bobo, ota va o'g'il", "3 kishi", "bobo ota o'g'il edi"]
    },
    {
        "id": 30,
        "q": "30. Bir odam dushanba kuni shaharga keldi. U uch kun turib, dushanba kuni qaytib ketdi. Bu qanday mumkin?",
        "image": "https://images.unsplash.com/photo-1494526585095-c41746248156?w=800",
        "hint": "💡 Maslahat: 'Dushanba' faqat hafta kuni emas.",
        "a": ["otining nomi dushanba", "otining nomi", "oti dushanba", "otining ismi dushanba"]
    },
    {
        "id": 31,
        "q": "31. 5 ta aka-uka bir xonada. Har birining o'z mashg'uloti bor: biri kitob o'qiydi, biri rasm chizadi, biri shaxmat o'ynaydi, biri ovqat pishiradi. Beshinchisi nima qiladi?",
        "image": "https://images.unsplash.com/photo-1529068755536-a5ade0dcb4e8?w=800",
        "hint": "💡 Maslahat: Shaxmatni odam yolg'iz o'ynamaydi.",
        "a": ["shaxmat o'ynaydi", "shaxmat", "ukasi bilan shaxmat o'ynaydi", "shaxmat oynaydi"]
    },
    {
        "id": 32,
        "q": "32. Bir oilada 6 ta qiz bor. Har bir qizning bittadan akasi bor. Oilada nechta farzand bor?",
        "image": "https://images.unsplash.com/photo-1504159506876-f8338247a14a?w=800",
        "hint": "💡 Maslahat: Barcha qizlarning akasi bitta odam bo'lishi mumkin.",
        "a": ["7 ta", "7", "yetti", "7ta"]
    },
    {
        "id": 33,
        "q": "33. Sizda 10 ta qo'y bor edi. Barchasidan tashqari 3 tasi qochib ketdi. Nechta qo'y qoldi?",
        "image": "https://images.unsplash.com/photo-1484557985045-edf25e08da73?w=800",
        "hint": "💡 Maslahat: 'Barchasidan tashqari 3 tasi' nimani anglatadi?",
        "a": ["3 ta", "3", "uchta", "3ta"]
    },
    {
        "id": 34,
        "q": "34. 10 ta baliqdan 2 tasi cho'kib ketdi. Akvariumda nechta baliq qoldi?",
        "image": "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=800",
        "hint": "💡 Maslahat: Baliqlar suvda yashaydi.",
        "a": ["10 ta", "10", "o'nta", "10ta", "baliq chokmaydi"]
    },
    {
        "id": 35,
        "q": "35. Bir qo'lingizda 5 ta olma, ikkinchi qo'lingizda 5 ta olma bor. Sizda nima bor?",
        "image": "https://images.unsplash.com/photo-1570913149827-d2ac84ab3f9a?w=800",
        "hint": "💡 Maslahat: Savol olmalardan ko'ra boshqa narsani so'rayapti.",
        "a": ["katta qo'llar", "ikkita qo'l", "qo'llar", "katta qol"]
    },
    {
        "id": 36,
        "q": "36. Qaysi xona eshigi yoki derazasi bo'lmasa ham xona hisoblanadi?",
        "image": "https://images.unsplash.com/photo-1511497584788-876760111969?w=800",
        "hint": "💡 Maslahat: Tabiatda ham 'xona'ga o'xshash joy bor.",
        "a": ["qo'ziqorin", "qo'ziqorin xonasi", "qozasiz xona"]
    },
    {
        "id": 37,
        "q": "37. Qaysi daraxtning bargi yo'q, lekin u daraxt deb ataladi?",
        "image": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800",
        "hint": "💡 Maslahat: Kitob bilan bog'liq bo'lishi mumkin.",
        "a": ["nasab daraxti", "genealogik daraxt", "daraxt rasmi", "shajara"]
    },
    {
        "id": 38,
        "q": "38. Qaysi kalit hech qanday qulfni ochmaydi?",
        "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=800",
        "hint": "💡 Maslahat: U musiqa bilan bog'liq.",
        "a": ["musiqa kaliti", "skripka kaliti", "sol kaliti", "buloq"]
    },
    {
        "id": 39,
        "q": "39. Qaysi stol ustida ovqat yeyib bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800",
        "hint": "💡 Maslahat: Bu stol o'yin bilan bog'liq.",
        "a": ["kompyuter stoli", "ping pong stoli", "o'yin stoli", "shaxmat stoli"]
    },
    {
        "id": 40,
        "q": "40. Qaysi ko'z bilan hech narsani ko'rib bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1516321165247-4aa89a48be28?w=800",
        "hint": "💡 Maslahat: U ignada ham bo'ladi.",
        "a": ["igna ko'zi", "ignaning ko'zi", "ko'z teshigi", "buloq ko'zi"]
    },
    {
        "id": 41,
        "q": "41. Qaysi til bilan gapirib bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=800",
        "hint": "💡 Maslahat: Poyabzal bilan bog'liq.",
        "a": ["poyabzal tili", "etik tili", "poyabzalning tili", "oyoq kiyim tili"]
    },
    {
        "id": 42,
        "q": "42. Qaysi quloq eshitmaydi?",
        "image": "https://images.unsplash.com/photo-1587778082149-bd5b1e4a7a4e?w=800",
        "hint": "💡 Maslahat: U idishda bo'lishi mumkin.",
        "a": ["qozon qulog'i", "qozonning qulog'i", "idish qulog'i", "qozon qulogi"]
    },
    {
        "id": 43,
        "q": "43. Qaysi boshda miya bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800",
        "hint": "💡 Maslahat: Bu bosh kiyim bilan bog'liq.",
        "a": ["mix boshi", "mixning boshi", "mix", "piyoz boshi", "sarimsoq boshi"]
    },
    {
        "id": 44,
        "q": "44. Bir uyda 4 ta xona bor. Har xonada bittadan chiroq, tashqarida esa 4 ta kalit bor. Qaysi kalit qaysi chiroqqa tegishli ekanini qanday aniqlash mumkin?",
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800",
        "hint": "💡 Maslahat: Chiroqning issiqligidan ham foydalanish mumkin.",
        "a": ["birini yoqib kutish", "chiroqni yoqib issiqligini tekshirish", "issiqlik bilan", "yoqib kutish"]
    },
    {
        "id": 45,
        "q": "45. Uchta lampochka bor. Siz xonaga faqat bir marta kirishingiz mumkin. Tashqaridagi uchta kalitdan qaysi biri qaysi lampochkaniki ekanini qanday topasiz?",
        "image": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800",
        "hint": "💡 Maslahat: Bir lampochkani yoqing, keyin o'chiring va issiqligini tekshiring.",
        "a": ["bittasini yoqib, bittasini yoqib-o'chirib, issiqligini tekshirish", "issiqlik orqali", "issiqlik bilan"]
    },
    {
        "id": 46,
        "q": "46. Sizda 2 ta arqon bor. Har biri aynan 1 soatda yonib tugaydi, ammo notekis yonadi. 45 daqiqani qanday o'lchaysiz?",
        "image": "https://images.unsplash.com/photo-1501426026826-31c667bdf23d?w=800",
        "hint": "💡 Maslahat: Arqonning ikki uchini bir vaqtda yoqishdan foydalaning.",
        "a": ["birinchi arqonning ikki uchini, ikkinchisining bir uchini yoqish", "ikki uchidan yoqish", "har ikkala uchini yoqish"]
    },
    {
        "id": 47,
        "q": "47. Bir odam yomg'irda ko'chada yurdi, lekin oyoqlari ham, kiyimlari ham ho'l bo'lmadi. U qanday qilib?",
        "image": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=800",
        "hint": "💡 Maslahat: Yomg'ir qayerda yog'ayotganiga qarang.",
        "a": ["yomg'ir yog'mayotgan joyda", "yomg'ir to'xtagan edi", "yopiq joyda", "soyabon bilan", "ustida yopinchiq bor edi"]
    },
    {
        "id": 48,
        "q": "48. Bir odam har kuni lift bilan 10-qavatga chiqadi, lekin pastga tushishda faqat 5-qavatgacha lift bilan tushib, qolganini piyoda yuradi. Nega?",
        "image": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b0?w=800",
        "hint": "💡 Maslahat: Odamning bo'yi haqida o'ylang.",
        "a": ["bo'yi kalta", "liftning tugmasiga yetmaydi", "5-qavatdan yuqoridagi tugmaga qo'li yetmaydi", "boyi kalta", "bo'yi yetmaydi"]
    },
    {
        "id": 49,
        "q": "49. Bir odam yakshanba kuni otiga minib yo'lga chiqdi. Uch kun o'tib yakshanba kuni qaytdi. Qanday qilib?",
        "image": "https://images.unsplash.com/photo-1551884831-bbf3cdc6469e?w=800",
        "hint": "💡 Maslahat: Otining nomi haqida o'ylang.",
        "a": ["otining nomi yakshanba", "oti yakshanba", "otining ismi yakshanba"]
    },
    {
        "id": 50,
        "q": "50. Bir xona ichida 10 kishi bor. Har biri boshqa odam bilan qo'l berib ko'rishdi. Jami nechta qo'l siqish bo'ladi?",
        "image": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800",
        "hint": "💡 Maslahat: Har bir juftlik faqat bir marta qo'l berishadi.",
        "a": ["45", "45 ta", "45ta"]
    },
    {
        "id": 51,
        "q": "51. 5 ta odam bir-biri bilan qo'l berishdi. Har bir juftlik bir marta qo'l bergan bo'lsa, jami nechta qo'l siqish bo'ldi?",
        "image": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800",
        "hint": "💡 Maslahat: Juftliklarni sanang.",
        "a": ["10", "10 ta", "10ta"]
    },
    {
        "id": 52,
        "q": "52. Bir sonni 2 ga ko'paytirib, 2 qo'shib, 2 ga bo'lsangiz 6 chiqadi. Bu son nechchi?",
        "image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800",
        "hint": "💡 Maslahat: Amallarni teskari tartibda bajaring.",
        "a": ["5", "besh"]
    },
    {
        "id": 53,
        "q": "53. 3 ta mushuk 3 daqiqada 3 ta sichqon tutsa, 100 ta mushuk 100 ta sichqonni necha daqiqada tutadi?",
        "image": "https://images.unsplash.com/photo-1519052537078-e6302a4968d4?w=800",
        "hint": "💡 Maslahat: Har bir mushuk bir xil tezlikda ishlayapti.",
        "a": ["3 daqiqa", "3", "uch daqiqa", "3 daqiqada"]
    },
    {
        "id": 54,
        "q": "54. 1 ta g'isht 1 kilogramm va yarim g'isht og'irligiga teng. To'liq g'isht necha kilogramm?",
        "image": "https://images.unsplash.com/photo-1590077213355-cf9f2e5e5d72?w=800",
        "hint": "💡 Maslahat: Tenglamani tuzing.",
        "a": ["2 kg", "2 kilogramm", "2", "2kg"]
    },
    {
        "id": 55,
        "q": "55. Daraxtda 20 ta olma bor edi. 5 tasi tushib ketdi. Daraxtda nechta olma qoldi?",
        "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
        "hint": "💡 Maslahat: Oddiy hisob.",
        "a": ["15", "15 ta", "15 dona", "15ta"]
    },
    {
        "id": 56,
        "q": "56. 10 dan 1 ni necha marta ayirish mumkin?",
        "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800",
        "hint": "💡 Maslahat: Birinchi marta ayirgandan keyin son o'zgaradi.",
        "a": ["1 marta", "bir marta", "1"]
    },
    {
        "id": 57,
        "q": "57. 30 ni uchdan biriga bo'lib, 10 qo'shsangiz nechchi chiqadi?",
        "image": "https://images.unsplash.com/photo-1596495578066-9a8e5e2c6f7d?w=800",
        "hint": "💡 Maslahat: 30 ning uchdan biri 10.",
        "a": ["100", "100 ta", "yuz", "100ta"]
    },
    {
        "id": 58,
        "q": "58. Bir oyda 28 kun bor. Nechta oyda 28 kun bor?",
        "image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800",
        "hint": "💡 Maslahat: Faqat fevral haqida o'ylamang.",
        "a": ["12 ta", "12", "barcha oyda", "12 oyda", "hammasida", "hamma oyda"]
    },
    {
        "id": 59,
        "q": "59. Bir yilda nechta oy 30 kundan iborat?",
        "image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800",
        "hint": "💡 Maslahat: Aynan 30 kunlik oylarni sanang.",
        "a": ["4 ta", "4", "to'rtta", "4ta", "11 ta"]
    },
    {
        "id": 60,
        "q": "60. Qaysi oyda 28 kun bo'lishi aniq?",
        "image": "https://images.unsplash.com/photo-1455849318743-b2233052fcff?w=800",
        "hint": "💡 Maslahat: Barcha oylarni o'ylab ko'ring.",
        "a": ["har oyda", "barcha oyda", "12 oyda", "hamma oyda", "fevral"]
    },
    {
        "id": 61,
        "q": "61. Soat 3:00 bo'lsa, soat strelkasi va minut strelkasi orasidagi burchak nechchi daraja?",
        "image": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?w=800",
        "hint": "💡 Maslahat: Strelkalar to'g'ri burchak hosil qiladi.",
        "a": ["90", "90 daraja", "90 gradus"]
    },
    {
        "id": 62,
        "q": "62. Soat 6:00 bo'lsa, ikki strelka orasidagi burchak nechchi daraja?",
        "image": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?w=800",
        "hint": "💡 Maslahat: Strelkalar qarama-qarshi turadi.",
        "a": ["180", "180 daraja", "180 gradus"]
    },
    {
        "id": 63,
        "q": "63. Bir odamning 4 ta qizi bor. Har bir qizning bittadan ukasi bor. Jami nechta farzand?",
        "image": "https://images.unsplash.com/photo-1504159506876-f8338247a14a?w=800",
        "hint": "💡 Maslahat: Uka hamma qizlar uchun bitta bo'lishi mumkin.",
        "a": ["5 ta", "5", "beshta", "5ta"]
    },
    {
        "id": 64,
        "q": "64. Bir xonada 7 ta sham bor. 3 tasi o'chib qoldi. Nechta sham bor?",
        "image": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=800",
        "hint": "💡 Maslahat: Savol yonib turgan shamlar haqida emas.",
        "a": ["7 ta", "7", "yettita", "7ta"]
    },
    {
        "id": 65,
        "q": "65. Sizda gugurt bor. Qorong'i xonada sham, kerosin chiroq va pechka turibdi. Avval nimani yoqasiz?",
        "image": "https://images.unsplash.com/photo-1509565840034-3c2f1f4f5f75?w=800",
        "hint": "💡 Maslahat: Olov kerak bo'ladi.",
        "a": ["gugurtni", "gugurt", "avval gugurtni"]
    },
    {
        "id": 66,
        "q": "66. Qaysi narsa sindirilsa, undan keyin ishlatiladi?",
        "image": "https://images.unsplash.com/photo-1589927986089-35812388d1f4?w=800",
        "hint": "💡 Maslahat: Nonushtada ko'p uchraydi.",
        "a": ["tuxum", "tuxumni", "koks va tuxum"]
    },
    {
        "id": 67,
        "q": "67. Qaysi narsa ochilmasdan turib ichiladi?",
        "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=800",
        "hint": "💡 Maslahat: Ustiga qopqoq qo'yilgan idishni o'ylang.",
        "a": ["somoncha bilan ichimlik", "trubka orqali ichimlik", "naycha orqali", "trubkada"]
    },
    {
        "id": 68,
        "q": "68. Qaysi narsa yuradi, lekin oyog'i yo'q?",
        "image": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=800",
        "hint": "💡 Maslahat: Vaqt ham 'yuradi'.",
        "a": ["soat", "vaqt", "soat yuradi", "daryo", "suv"]
    },
    {
        "id": 69,
        "q": "69. Qaysi narsa gapiradi, lekin og'zi yo'q?",
        "image": "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=800",
        "hint": "💡 Maslahat: U tovushni qaytarishi mumkin.",
        "a": ["aks-sado", "echo", "sado", "aks sado"]
    },
    {
        "id": 70,
        "q": "70. Qaysi narsa sizga javob beradi, lekin o'zi savol bermaydi?",
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800",
        "hint": "💡 Maslahat: Ovoz bilan bog'liq.",
        "a": ["aks-sado", "echo", "sado", "telefon", "aks sado"]
    },
    {
        "id": 71,
        "q": "71. Qaysi narsa bir joyda turib butun dunyoni aylanib chiqadi?",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
        "hint": "💡 Maslahat: U xat yoki posilkada bo'lishi mumkin.",
        "a": ["marka", "pochta markasi", "pochta"]
    },
    {
        "id": 72,
        "q": "72. Qaysi narsa devordan o'ta oladi, lekin devorni buzmaydi?",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "hint": "💡 Maslahat: Yorug'lik haqida o'ylang.",
        "a": ["nur", "yorug'lik", "soya", "ovoz"]
    },
    {
        "id": 73,
        "q": "73. Qaysi narsa derazadan kiradi, lekin eshikdan kirmaydi?",
        "image": "https://images.unsplash.com/photo-1497250681960-ef046c08a56e?w=800",
        "hint": "💡 Maslahat: Uni ko'ra olasiz, lekin ushlay olmaysiz.",
        "a": ["quyosh nuri", "nur", "yorug'lik"]
    },
    {
        "id": 74,
        "q": "74. Qaysi narsa qancha ko'p olinsa, shuncha ko'p ortida qoladi?",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "hint": "💡 Maslahat: Yurish bilan bog'liq.",
        "a": ["qadam", "qadamlar", "iz"]
    },
    {
        "id": 75,
        "q": "75. Qaysi narsa yuradi-yuradi, lekin joyidan qimirlamaydi?",
        "image": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?w=800",
        "hint": "💡 Maslahat: Vaqtni ko'rsatadigan narsani o'ylang.",
        "a": ["soat", "soat strelkasi"]
    },
    {
        "id": 76,
        "q": "76. Qaysi narsa boshiga tegsa ham og'riq sezmaydi?",
        "image": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800",
        "hint": "💡 Maslahat: Mixning boshi bor.",
        "a": ["mix", "mixning boshi"]
    },
    {
        "id": 77,
        "q": "77. Qaysi narsa ko'tarilgan sari pastga tushadi?",
        "image": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=800",
        "hint": "💡 Maslahat: Harorat bilan bog'liq.",
        "a": ["termometr", "termometrdagi simob"]
    },
    {
        "id": 78,
        "q": "78. Qaysi narsa yozda ham, qishda ham bir xil rangda qoladi?",
        "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
        "hint": "💡 Maslahat: Doim yashil daraxtni o'ylang.",
        "a": ["archa", "doim yashil daraxt", "qarag'ay"]
    },
    {
        "id": 79,
        "q": "79. Bir odamning oldida ikki kishi, orqasida ikki kishi va o'rtasida bir kishi turibdi. Jami nechta odam bor?",
        "image": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800",
        "hint": "💡 Maslahat: Odamlar bir qatorda turishi mumkin.",
        "a": ["5 ta", "5", "beshta", "3 ta", "3", "3 kishi"]
    },
    {
        "id": 80,
        "q": "80. Uchta odam bir soyabon ostida turibdi, lekin hech biri ho'l bo'lmadi. Nega?",
        "image": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800",
        "hint": "💡 Maslahat: Yomg'ir yog'ayotgan bo'lishi shart emas.",
        "a": ["yomg'ir yog'mayotgan edi", "yomg'ir yo'q edi", "yomg'ir yog'mayapti"]
    },
    {
        "id": 81,
        "q": "81. Bir odamning 10 ta barmog'i bor. 10 odamning nechta barmog'i bor?",
        "image": "https://images.unsplash.com/photo-1504159506876-f8338247a14a?w=800",
        "hint": "💡 Maslahat: Har bir odamda 10 ta barmoq bor deb hisoblang.",
        "a": ["100 ta", "100", "yuzta", "100ta"]
    },
    {
        "id": 82,
        "q": "82. Bir kishi 20 yoshda, ammo tug'ilgan kunini atigi 5 marta nishonlagan. Qanday qilib?",
        "image": "https://images.unsplash.com/photo-1464349153735-7db50ed83c84?w=800",
        "hint": "💡 Maslahat: Tug'ilgan sanasi oddiy sana emas.",
        "a": ["29 fevralda tug'ilgan", "29-fevral", "kabisa kuni", "29 fevral", "29 fevralda tugilgan", "29 fevralda"]
    },
    {
        "id": 83,
        "q": "83. Bir odam 2020-yilda 20 yoshda edi, 2025-yilda esa 15 yoshda bo'ldi. Bu qanday mumkin?",
        "image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800",
        "hint": "💡 Maslahat: Yillar oddiy tartibda o'tmayapti.",
        "a": ["miloddan avval", "miloddan avvalgi", "bc", "miloddan ilgari"]
    },
    {
        "id": 84,
        "q": "84. Qaysi raqamni teskari aylantirsangiz ham o'sha raqam bo'lib qoladi?",
        "image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800",
        "hint": "💡 Maslahat: Raqamning shakliga qarang.",
        "a": ["0", "8", "nol", "sakkiz"]
    },
    {
        "id": 85,
        "q": "85. 2 + 2 × 2 nechchi bo'ladi?",
        "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800",
        "hint": "💡 Maslahat: Amal bajarish tartibiga rioya qiling.",
        "a": ["6", "olti"]
    },
    {
        "id": 86,
        "q": "86. 100 dan 10 ni necha marta ayirsangiz 50 qoladi?",
        "image": "https://images.unsplash.com/photo-1596495578066-9a8e5e2c6f7d?w=800",
        "hint": "💡 Maslahat: Oddiy hisob emas, savolning qanday berilganiga e'tibor bering.",
        "a": ["1 marta", "bir marta", "5 marta", "1"]
    },
    {
        "id": 87,
        "q": "87. Bir daraxtda 6 ta qush bor. Siz 2 tasini qo'rqitdingiz. Nechta qush daraxtda qoladi?",
        "image": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=800",
        "hint": "💡 Maslahat: Qo'rqqan qushlar uchib ketishi mumkin.",
        "a": ["4 ta", "4", "to'rtta", "0", "hech qancha"]
    },
    {
        "id": 88,
        "q": "88. 4 ta tuxumning har birini 5 daqiqadan qaynatish kerak. Barchasini bir vaqtda qaynatsangiz qancha vaqt ketadi?",
        "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800",
        "hint": "💡 Maslahat: Tuxumlarni bir vaqtda qozonga solish mumkin.",
        "a": ["5 daqiqa", "5", "besh daqiqa", "5 daqiqada"]
    },
    {
        "id": 89,
        "q": "89. 3 ta tuxum 3 daqiqada pishadi. 9 ta tuxum bir qozonda necha daqiqada pishadi?",
        "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800",
        "hint": "💡 Maslahat: Ular bir vaqtda pishishi mumkin.",
        "a": ["3 daqiqa", "3", "uch daqiqa", "3 daqiqada"]
    },
    {
        "id": 90,
        "q": "90. Bir xonada 4 ta burchak bor. Har burchakda bittadan sham turibdi. Har shamning yonida 2 ta sham bor. Jami nechta sham bor?",
        "image": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=800",
        "hint": "💡 Maslahat: Shamlar bir-birining yonida bo'lishi mumkin.",
        "a": ["4 ta", "4", "to'rtta", "4ta"]
    },
    {
        "id": 91,
        "q": "91. Bir savatda 5 ta olma bor. 5 bola bittadan olma oldi, lekin savatda bitta olma qoldi. Qanday qilib?",
        "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
        "hint": "💡 Maslahat: Oxirgi bola olmani savati bilan olishi mumkin.",
        "a": ["oxirgi bola savatdagi olmani oldi", "savat bilan oldi", "olmani savati bilan oldi", "savatda oldi"]
    },
    {
        "id": 92,
        "q": "92. Bir odam do'konga kirib 10 000 so'mlik mahsulot oldi va 20 000 so'm berdi. Sotuvchi 10 000 qaytim berdi. Keyin u mahsulotni qaytarib berdi. Sotuvchi qancha pulni qaytarishi kerak?",
        "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800",
        "hint": "💡 Maslahat: Xaridor avval mahsulot uchun qancha to'lagan?",
        "a": ["10000", "10 000", "10000 so'm", "10 ming", "10000 som"]
    },
    {
        "id": 93,
        "q": "93. Bir xonada 3 ta it bor. Har bir itning qarshisida 2 ta it bor. Jami nechta it bor?",
        "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=800",
        "hint": "💡 Maslahat: Itlar bir-biriga qarab turishi mumkin.",
        "a": ["3 ta", "3", "uchta", "3ta"]
    },
    {
        "id": 94,
        "q": "94. Qaysi narsa suvga tushsa ham ho'l bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
        "hint": "💡 Maslahat: U yorug'lik bilan bog'liq.",
        "a": ["soya", "aks", "soyasi", "nur"]
    },
    {
        "id": 95,
        "q": "95. Qaysi narsa sizdan oldin keladi, lekin uni ko'ra olmaysiz?",
        "image": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=800",
        "hint": "💡 Maslahat: Kelajak haqida o'ylang.",
        "a": ["kelajak", "ertangi kun", "kelajakdagi vaqt", "ertaga"]
    },
    {
        "id": 96,
        "q": "96. Qaysi narsa doim oldinda bo'ladi, lekin unga hech qachon yetib bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=800",
        "hint": "💡 Maslahat: Vaqt bilan bog'liq.",
        "a": ["kelajak", "ertangi kun", "ertaga", "ufq"]
    },
    {
        "id": 97,
        "q": "97. Qaysi narsa bir marta aytilsa, uni qaytarib bo'lmaydi?",
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800",
        "hint": "💡 Maslahat: So'z bilan bog'liq.",
        "a": ["so'z", "aytilgan so'z", "gap", "soz"]
    },
    {
        "id": 98,
        "q": "98. Qaysi narsa qancha ko'p bo'lsa, shuncha kam og'irlik qiladi?",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "hint": "💡 Maslahat: Juda yengil narsalarni o'ylang.",
        "a": ["havo", "havo pufakchalari", "sharlar", "teshiklar"]
    },
    {
        "id": 99,
        "q": "99. Qaysi narsa ko'tarilganda tushadi, tushirilganda ko'tariladi?",
        "image": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?w=800",
        "hint": "💡 Maslahat: Tarozi bilan bog'liq.",
        "a": ["tarozi", "tarozi pallasi", "anchar"]
    },
    {
        "id": 100,
        "q": "100. Qaysi narsa har doim siz bilan, ammo siz uni ko'ra olmaysiz?",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "hint": "💡 Maslahat: U tanangizga tegishli emas.",
        "a": ["soya", "nafas", "havo", "aql"]
    },
    {
        "id": 101,
        "q": "101. Bir odam oynaga qaradi va o'zini ko'rmadi. Nega?",
        "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800",
        "hint": "💡 Maslahat: Oyna haqida emas, atrofdagi sharoit haqida o'ylang.",
        "a": ["qorong'i edi", "xona qorong'i edi", "yorug'lik yo'q edi", "qorongida"]
    },
    {
        "id": 102,
        "q": "102. Bir uyda barcha derazalar janubga qaragan. Uy yonidan ayiq o'tdi. Ayiq qanday rangda?",
        "image": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=800",
        "hint": "💡 Maslahat: Barcha derazalar janubga qarashi mumkin bo'lgan joyni o'ylang.",
        "a": ["oq", "oq rangda", "oq ayiq"]
    },
    {
        "id": 103,
        "q": "103. Bir odam 5 kun uxlamasdan yashadi, lekin sog'-salomat qoldi. Qanday qilib?",
        "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
        "hint": "💡 Maslahat: U faqat kechasi uxlamagan bo'lishi shart emas.",
        "a": ["kechasi uxlagan", "kunduzi uxlagan", "u kechasi uxlagan", "kechqurun uxlagan", "kechasi uxladi"]
    },
    {
        "id": 104,
        "q": "104. Bir odam yomg'irda boshiga hech narsa kiymadi, lekin sochlari ho'l bo'lmadi. Nega?",
        "image": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800",
        "hint": "💡 Maslahat: Uning sochiga e'tibor bering.",
        "a": ["u kal edi", "sochi yo'q edi", "kal", "kal edi", "sochi yoq"]
    },
    {
        "id": 105,
        "q": "105. Bir odamning qo'lida 5 ta barmog'i bor, lekin ularning hech biri uning qo'li emas. Bu qanday mumkin?",
        "image": "https://images.unsplash.com/photo-1504159506876-f8338247a14a?w=800",
        "hint": "💡 Maslahat: 'Qo'lida' so'zining boshqa ma'nosini o'ylang.",
        "a": ["qo'lqopda", "qo'lqop", "qo'lqopning barmoqlari", "qolqop"]
    },
    {
        "id": 106,
        "q": "106. Bir kishi xonaga kirib, chiroqni yoqdi. Chiroq yoqilgach xona kichrayib qoldi. Qanday qilib?",
        "image": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800",
        "hint": "💡 Maslahat: Xonaning o'zi emas, ko'rinishi o'zgargan.",
        "a": ["soya yo'qoldi", "yorug'lik sababli ko'rinishi o'zgardi", "soya yoqoldi"]
    },
    {
        "id": 107,
        "q": "107. Siz qorong'i xonaga kirdingiz. Xonada gugurt, sham, chiroq va pechka bor. Sizda faqat bitta gugurt bor. Birinchi bo'lib nimani yoqasiz?",
        "image": "https://images.unsplash.com/photo-1509565840034-3c2f1f4f5f75?w=800",
        "hint": "💡 Maslahat: Avval olov manbasini yoqish kerak.",
        "a": ["gugurtni", "gugurt", "avval gugurtni"]
    }
]

# --- KODGA QO'SHILADIGAN JAVOBNI TEKSHIRISH FUNKSIYASI ---

def normalize_text(text: str) -> str:
    """Matndagi tuturuq belgilari, apostroflar va ortiqcha bo'shliqlarni olib tashlaydi."""
    if not text:
        return ""
    text = str(text).lower().strip()
    text = re.sub(r"[‘`ʼ'ʹʻ]", "", text)
    text = text.replace("oʻ", "o").replace("gʻ", "g").replace("o'", "o").replace("g'", "g")
    return text.strip()

def check_answer(user_answer: str, correct_answers: list) -> bool:
    """
    Foydalanuvchi javobini qabul qilingan javoblar ro'yxati bilan solishtiradi.
    1. Aniq yoki qism-matn mosligi.
    2. Fuzzy/SequenceMatcher orqali 75% o'xshashlik bo'lsa ham to'g'ri deb oladi.
    """
    user_clean = normalize_text(user_answer)
    
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
        
    for ans in correct_answers:
        ans_clean = normalize_text(ans)
        
        # Exact match yoki kalit so'z qismi bo'lsa
        if user_clean == ans_clean or user_clean in ans_clean or ans_clean in user_clean:
            return True
            
        # O'xshashlik foizini tekshirish (75% dan yuqori bo'lsa)
        ratio = SequenceMatcher(None, user_clean, ans_clean).ratio()
        if ratio >= 0.75:
            return True
            
    return False
