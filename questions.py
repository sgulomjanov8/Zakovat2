# questions.py
import re
from difflib import SequenceMatcher

LOGICAL_QUESTIONS= [ 
  {
    "id": 1,
    "q": "1. Qaysi narsa ko'tarilganda tushadi, tushirilganda ko'tariladi?",
    "image": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?w=800",
    "hint": "💡 Maslahat: Tarozi yoki kema bilan bog'liq.",
    "a": ["kema yakori", "yakor", "anker", "tarozi", "tarozi pallasi"]
  },
  {
    "id": 2,
    "q": "2. O'zi yemaydi, lekin hammani ovqatlantiradi. U nima?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Oshxonada ishlatiladigan idish-tovoq.",
    "a": ["qoshiq", "qoshiq"]
  },
  {
    "id": 3,
    "q": "3. U qanchalik ko'p bo'lsa, shunchalik kam ko'rasiz. U nima?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Tunda paydo bo'ladi.",
    "a": ["qorong'ilik", "qorongilik", "qorong'u"]
  },
  {
    "id": 4,
    "q": "4. U doim sizning qarshingizda, lekin uni hech qachon ko'ra olmaysiz. U nima?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Hali yetib kelmagan vaqt.",
    "a": ["kelajak", "kelajak vaqt"]
  },
  {
    "id": 5,
    "q": "5. Nimaning boshi bor, dumi bor, lekin oyog'i va tanasi yo'q?",
    "image": "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?w=800",
    "hint": "💡 Maslahat: Hamyoningizdagi metal pul.",
    "a": ["tanga", "som", "so'm", "tanga pul"]
  },
  {
    "id": 6,
    "q": "6. Qaysi idishdan hech qachon ovqat yeb bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800",
    "hint": "💡 Maslahat: Ichida hech narsa yo'q idish.",
    "a": ["bo'sh idishdan", "bosh idishdan", "bo'sh idish", "bosh idish"]
  },
  {
    "id": 7,
    "q": "7. Uni ushlab turish uchun qo'l kerak emas, lekin u ushlanmasa yo'qoladi. U nima?",
    "image": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=800",
    "hint": "💡 Maslahat: Ichingizga yutasiz yoki kimgadir berasiz.",
    "a": ["nafas", "va'da", "vada"]
  },
  {
    "id": 8,
    "q": "8. Dunyodagi barcha insonlar bir vaqtning o'zida nima qilishadi?",
    "image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800",
    "hint": "💡 Maslahat: Yoshi ulg'ayish jarayoni.",
    "a": ["qarishadi", "yoshi kattalashadi", "qarish"]
  },
  {
    "id": 9,
    "q": "9. Qancha ko'p olsangiz, shuncha kattalashadigan narsa nima?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Yerda kavlanadigan narsa.",
    "a": ["chuqur", "o'ra", "ora"]
  },
  {
    "id": 10,
    "q": "10. U sizga tegishli, lekin undan boshqalar ko'proq foydalanishadi. U nima?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Sizni chaqirishganda aytishadi.",
    "a": ["ismingiz", "ism", "ot"]
  },
  {
    "id": 11,
    "q": "11. Barcha tillarda gapira oladigan, lekin tili yo'q narsa nima?",
    "image": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800",
    "hint": "💡 Maslahat: Tog'da baqirsangiz qaytib keladigan ovoz.",
    "a": ["aks-sado", "aks sado", "sado"]
  },
  {
    "id": 12,
    "q": "12. Qaysi savolga hech qachon 'Ha' deb javob berib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
    "hint": "💡 Maslahat: Inson uxlab yotganida beriladigan savol.",
    "a": ["uxlayapsizmi", "uxlayapsizmi?", "uxlayapsanmi"]
  },
  {
    "id": 13,
    "q": "13. Suvda cho'kmaydi, olovda yonmaydi. U nima?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Suvning muzlagan holati.",
    "a": ["muz"]
  },
  {
    "id": 14,
    "q": "14. Bir odam yomg'irda soyabonsiz yurgan bo'lsa ham sochi ho'l bo'lmadi. Nega?",
    "image": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800",
    "hint": "💡 Maslahat: Uning boshida nima yo'q?",
    "a": ["kachal", "sochi yo'q", "sochi yoq", "boshi kal"]
  },
  {
    "id": 15,
    "q": "15. Xonada 10 ta sham yonayotgandi. Ulardan 3 tasi o'chirildi. Qancha sham qoldi?",
    "image": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=800",
    "hint": "💡 Maslahat: O'chirilmaganlari erib yo'q bo'lib ketadi.",
    "a": ["3 ta", "3", "3 ta sham"]
  },
  {
    "id": 16,
    "q": "16. Nimani yeb bo'lmaydi, lekin tayyorlash mumkin?",
    "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800",
    "hint": "💡 Maslahat: Maktabda beriladigan topshiriq.",
    "a": ["dars", "topshiriq", "darslik"]
  },
  {
    "id": 17,
    "q": "17. U har doim keladi, lekin hech qachon bugun bo'lmaydi. U nima?",
    "image": "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?w=800",
    "hint": "💡 Maslahat: Bugundan keyin keladigan kun.",
    "a": ["ertangi kun", "erta", "ertagacha"]
  },
  {
    "id": 18,
    "q": "18. Qatorda 5 ta olma bor. Siz ulardan 3 tasini oldingiz. Sizda nechta olma bor?",
    "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    "hint": "💡 Maslahat: Qo'lingizga nechta olma oldingiz?",
    "a": ["3 ta", "3", "3 ta olma"]
  },
  {
    "id": 19,
    "q": "19. Nima chaqilganda yoki singanda ishlay boshlaydi?",
    "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800",
    "hint": "💡 Maslahat: Qobiqli oziq-ovqat mahsuloti.",
    "a": ["tuxum", "yong'oq", "yongoq"]
  },
  {
    "id": 20,
    "q": "20. U yugurishi mumkin, lekin yurolmaydi. U nima?",
    "image": "https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?w=800",
    "hint": "💡 Maslahat: Oqib yotgan suv havzasi.",
    "a": ["daryo", "soy", "irmoq"]
  },
  {
    "id": 21,
    "q": "21. Bir kishi qorong'i xonada o'tiribdi, chiroq yo'q. U kitob o'qiyapti. Bu qanday mumkin?",
    "image": "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=800",
    "hint": "💡 Maslahat: Ko'zi ojizlar alifbosi.",
    "a": ["brayl alifbosi", "brayl", "ko'zi ojiz", "kozi ojiz"]
  },
  {
    "id": 22,
    "q": "22. Nechta oyda 28 kun bor?",
    "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800",
    "hint": "💡 Maslahat: Barcha oylarda kamida 28 kun bor-yo'qligini o'ylang.",
    "a": ["12 ta", "hamma oyda", "barcha oylarda", "12"]
  },
  {
    "id": 23,
    "q": "23. Qaysi toshni daryodan topib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Suvga tushmagan tosh.",
    "a": ["quruq tosh", "quruq toshni", "quruq"]
  },
  {
    "id": 24,
    "q": "24. Qaysi qo'l bilan choyni aralashtirgan ma'qul?",
    "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=800",
    "hint": "💡 Maslahat: Qo'l bilan emas, boshqa narsa bilan aralashtiriladi.",
    "a": ["qoshiq bilan", "qoshiq bilan", "qoshiq"]
  },
  {
    "id": 25,
    "q": "25. Nima har doim tushadi, lekin hech qachon ko'tarilmaydi?",
    "image": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=800",
    "hint": "💡 Maslahat: Osmondan yog'adigan yog'in.",
    "a": ["yomg'ir", "yomgir", "qor"]
  },
  {
    "id": 26,
    "q": "26. Nimani chap qo'l bilan ushlash mumkin, lekin o'ng qo'l bilan ushlab bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800",
    "hint": "💡 Maslahat: O'ng qo'lingizdagi bo'g'im.",
    "a": ["o'ng tirsakni", "ong tirsakni", "o'ng tirsak"]
  },
  {
    "id": 27,
    "q": "27. O'z og'irligi yo'q, lekin uni idishga solsangiz idish yengillashadi. U nima?",
    "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800",
    "hint": "💡 Maslahat: Narsada paydo bo'ladigan o'ra/bo'shliq.",
    "a": ["teshik"]
  },
  {
    "id": 28,
    "q": "28. Qaysi so'z lug'atda xato yozilgan bo'ladi?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: So'zning o'zi xato deb ataladi.",
    "a": ["xato", "xato so'zi"]
  },
  {
    "id": 29,
    "q": "29. Qaysi oy eng qisqa oy hisoblanadi?",
    "image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800",
    "hint": "💡 Maslahat: Nomi bor-yo'g'i 3 ta harfdan iborat.",
    "a": ["may", "may oyi"]
  },
  {
    "id": 30,
    "q": "30. Otasining o'g'li, lekin u insonning ukasi ham, akasi ham emas. U kim?",
    "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=800",
    "hint": "💡 Maslahat: O'sha insonning shaxsan o'zi.",
    "a": ["o'zi", "ozi", "u insonning o'zi"]
  },
  {
    "id": 31,
    "q": "31. Nima bir joyda turib ham butun dunyoni aylanib chiqa oladi?",
    "image": "https://images.unsplash.com/photo-1579273166152-d725a4e2b755?w=800",
    "hint": "💡 Maslahat: Xat yoki konvertga yopishtiriladi.",
    "a": ["pochta markasi", "marka"]
  },
  {
    "id": 32,
    "q": "32. Qaysi daraxt shoxida qush yomg'ir yog'ayotganda o'tirishi mumkin?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Yomg'irda qolgan shox qanday bo'ladi?",
    "a": ["ho'l shoxda", "hol shoxda", "ho'l"]
  },
  {
    "id": 33,
    "q": "33. Qanday samolyotdan sakrasangiz soyabon (parashyut) kerak emas?",
    "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
    "hint": "💡 Maslahat: Yerdan ko'tarilmagan samolyot.",
    "a": ["yerdagi samolyotdan", "yerdagi", "uchmayotgan samolyotdan"]
  },
  {
    "id": 34,
    "q": "34. Bitta uyda 4 ta burchak bor, har bir burchakda bittadan mushuk o'tiribdi. Nechta mushuk bor?",
    "image": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800",
    "hint": "💡 Maslahat: Burchaklarni sanang.",
    "a": ["4 ta", "4", "to'rtta"]
  },
  {
    "id": 35,
    "q": "35. Fil va chumoli uchrashdi. Nega fil qochib ketdi?",
    "image": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=800",
    "hint": "💡 Maslahat: Hazil mantiqiy savol.",
    "a": ["oyog'ini bosib oldi", "oyogini bosib oldi"]
  },
  {
    "id": 36,
    "q": "36. Qaysi joyda yakshanba shanbadan oldin keladi?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: Alifbo tartibi bo'yicha kitob.",
    "a": ["lug'atda", "lugatda", "lug'at"]
  },
  {
    "id": 37,
    "q": "37. Ikki ota va ikki o'g'il o'rmondan 3 ta quyonni olib kelishdi. Ularga 1 tadan tegdi. Bu qanday bo'ldi?",
    "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800",
    "hint": "💡 Maslahat: Oila a'zolarining avlodi (3 kishi).",
    "a": ["bobo ota va o'g'il", "bobo ota ogil", "3 kishi edi"]
  },
  {
    "id": 38,
    "q": "38. Qaysi kalit bilan eshikni ochib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=800",
    "hint": "💡 Maslahat: Musiqiy kalit yoki yer ostidan chiqadigan suv.",
    "a": ["buloq kaliti", "musiqa kaliti", "musiqiy kalit", "buloq"]
  },
  {
    "id": 39,
    "q": "39. Suv ostida o'tirib guvohnoma topshirsa bo'ladimi?",
    "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
    "hint": "💡 Maslahat: G'avvoshlik kurslari.",
    "a": ["bo'ladi", "boladi", "g'avvoshlik"]
  },
  {
    "id": 40,
    "q": "40. Suv sathi ko'tarilganda kema va unga osilgan zina nima bo'ladi?",
    "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
    "hint": "💡 Maslahat: Kema suvda suzib yuradi.",
    "a": ["kema ham ko'tariladi", "zina ham ko'tariladi", "suv yetmaydi"]
  },
  {
    "id": 41,
    "q": "41. Ko'zi bor, lekin ko'rmaydi. U nima?",
    "image": "https://images.unsplash.com/photo-1512290900673-0498b368a52e?w=800",
    "hint": "💡 Maslahat: Tikuvchilik quroli yoki kartoshka.",
    "a": ["igna", "kartoshka", "igna ko'zi"]
  },
  {
    "id": 42,
    "q": "42. Nima qancha ko'p qurisa, shuncha ho'l bo'ladi?",
    "image": "https://images.unsplash.com/photo-1616627547584-bf28cee262db?w=800",
    "hint": "💡 Maslahat: Cho'milgandan keyin ishlatiladi.",
    "a": ["sochiq"]
  },
  {
    "id": 43,
    "q": "43. Odam qachon xonada boshsiz bo'ladi?",
    "image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
    "hint": "💡 Maslahat: Boshini derazadan chiqarib turganda.",
    "a": ["derazadan boshini chiqarganda", "boshini chiqarganda"]
  },
  {
    "id": 44,
    "q": "44. Yerda yotgan qaysi narsaning ustidan sakrab o'tib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Yorug'likda paydo bo'ladigan aksi.",
    "a": ["o'z soyasi", "soya", "devor yonidagi narsa"]
  },
  {
    "id": 45,
    "q": "45. Nima to'xtovsiz harakat qiladi, lekin joyidan jilmaydi?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: Devorga osib qo'yiladigan buyum.",
    "a": ["soat"]
  },
  {
    "id": 46,
    "q": "46. Oq it qora dengizga tushsa nima bo'ladi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Suvga tushgan har qanday narsa nima bo'ladi?",
    "a": ["ho'l bo'ladi", "hol boladi", "ho'llanadi"]
  },
  {
    "id": 47,
    "q": "47. Nimaning xotirasi zo'r, lekin o'zi fikrlay olmaydi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Axborot saqlaydigan texnika.",
    "a": ["kompyuter", "xotira kartasi", "fleshka"]
  },
  {
    "id": 48,
    "q": "48. Qanday savolga har doim har xil javob beriladi?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: Soatga qarab javob beriladigan savol.",
    "a": ["soat necha bo'ldi", "soat necha", "vaqt necha bo'ldi"]
  },
  {
    "id": 49,
    "q": "49. Mart oyida bor, lekin aprelda yo'q. Mayda bor, iyunda yo'q. U nima?",
    "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800",
    "hint": "💡 Maslahat: So'zlar tarkibidagi harf.",
    "a": ["m harfi", "m", "harf"]
  },
  {
    "id": 50,
    "q": "50. Bir odam 8 kun uxlab bilmadi. U buni qanday uddaladi?",
    "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
    "hint": "💡 Maslahat: U kechalari uxlagan.",
    "a": ["kechasi uxlagan", "kechalari uxlagan", "tunda uxlagan"]
  },
  {
    "id": 51,
    "q": "51. Mashina burilayotganda qaysi g'ildirak aylanmaydi?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Bagajda turadigan zaxira g'ildirak.",
    "a": ["zaxira g'ildirak", "zapaska", "zaxira", "zaxiradagi g'ildirak"]
  },
  {
    "id": 52,
    "q": "52. Poyezd 100 km/soat tezlikda ketyapti. Elektr poyezdi bo'lsa, tutuni qaysi tomonga uchadi?",
    "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800",
    "hint": "💡 Maslahat: Elektrda ishlaydigan transport vositasi.",
    "a": ["tutun chiqarmaydi", "tutuni yo'q", "tutuni yoq", "elektr poyezdda tutun bo'lmaydi"]
  },
  {
    "id": 53,
    "q": "53. Qaysi kasallik bilan faqat suvda/kemada og'rish mumkin?",
    "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
    "hint": "💡 Maslahat: Suv va kemaga bog'liq kasallik.",
    "a": ["dengiz kasalligi", "dengiz kasalligi bilan"]
  },
  {
    "id": 54,
    "q": "54. Qorong'i xonada kerosin lampasi, sham va gaz plitasi bor. Qo'lingizda 1 ta gugurt bo'lsa, birinchi nimani yoqasiz?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Qolganlarini yoqish uchun birinchi kerak bo'ladigan narsa.",
    "a": ["gugurt", "gugurtni", "chirishni"]
  },
  {
    "id": 55,
    "q": "55. Nimaga tez yugursangiz ham yetib ololmaysiz?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Yorug'likda ketningizdan qolmaydigan aksi.",
    "a": ["o'z soyangizga", "soya", "soyaga", "o'z soyasi"]
  },
  {
    "id": 56,
    "q": "56. Qaysi matodan ko'ylak tikib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800",
    "hint": "💡 Maslahat: Poyezd yuradigan temir yo'l.",
    "a": ["temir yo'l matosidan", "rels", "temir yol matosi"]
  },
  {
    "id": 57,
    "q": "57. Bitta tuxum 5 minutda pishsa, 4 ta tuxum necha minutda pishadi?",
    "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800",
    "hint": "💡 Maslahat: Hamma tuxumlar birga solinadi.",
    "a": ["5 minutda", "5 minut", "5 daqiqa", "5 daqiqada"]
  },
  {
    "id": 58,
    "q": "58. Uyning qaysi joyida stulni qo'yib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
    "hint": "💡 Maslahat: Uyning eng tepasi/tobi.",
    "a": ["shiftida", "potolokda", "shiftga"]
  },
  {
    "id": 59,
    "q": "59. Har bir insonning 2 tadan bor, lekin o'zi ko'zgusiz ko'ra olmaydi. U nima?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Eshitish organi.",
    "a": ["quloqlar", "quloq", "quloqlari"]
  },
  {
    "id": 60,
    "q": "60. Nima pastga qarab o'sadi?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Qishda tom ostida osilib turadigan muz.",
    "a": ["sumalak", "muz tili", "muz sumalak", "muz"]
  },
  {
    "id": 61,
    "q": "61. Nimani ushlab bo'lmaydi, lekin yo'qotish juda oson?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: To'xtovsiz o'tib boradigan narsa.",
    "a": ["vaqt", "vaqtni"]
  },
  {
    "id": 62,
    "q": "62. Toshkentda 1 ta, Samarqandda 2 ta, Buxoroda umuman yo'q. U nima?",
    "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800",
    "hint": "💡 Maslahat: Shahar nomlaridagi harf.",
    "a": ["a harfi", "a", "harf"]
  },
  {
    "id": 63,
    "q": "63. Bir odam uyining to'rtala devori ham janubga qaragan qilib uy qurdi. Ayiq keldi. Ayiqning rangi qanday?",
    "image": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=800",
    "hint": "💡 Maslahat: Shimoliy qutbdagi ayiq.",
    "a": ["oq", "oq ayiq", "oq rangda"]
  },
  {
    "id": 64,
    "q": "64. Qirol va malika o'rtasida nima bor?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: So'zlarni bog'lovchi harflar.",
    "a": ["va bog'lovchisi", "va", "va harfi"]
  },
  {
    "id": 65,
    "q": "65. O'z joyida turib ham butun dunyoni ko'rsatadi yoki sayr qildiradi. U nima?",
    "image": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800",
    "hint": "💡 Maslahat: Dumaloq yer modeli.",
    "a": ["globus", "xarita"]
  },
  {
    "id": 66,
    "q": "66. Toshni suvga tashlasangiz u nima bo'ladi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Suvga tushgan har qanday narsaning holati.",
    "a": ["ho'l bo'ladi", "ho'llanadi", "cho'kadi va ho'l bo'ladi"]
  },
  {
    "id": 67,
    "q": "67. Inson tanasining qaysi a'zosi hayajonlanganda ko'zda kattalashadi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Ko'zning ichidagi qismi.",
    "a": ["ko'z qorachig'i", "koz qorachigi", "qorachiq"]
  },
  {
    "id": 68,
    "q": "68. Qaysi so'z har doim noto'g'ri aytiladi?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: So'zning o'zi noto'g'ri.",
    "a": ["noto'g'ri", "notogri", "noto'g'ri so'zi"]
  },
  {
    "id": 69,
    "q": "69. Suv o'rtasida nima bor?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: So'z markazidagi harf.",
    "a": ["u harfi", "u", "harf"]
  },
  {
    "id": 70,
    "q": "70. Ot sportida ot nima uchun to'siqdan sakraydi?",
    "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800",
    "hint": "💡 Maslahat: To'siq ostidan nima qila olmaydi?",
    "a": ["ostidan o'ta olmaydi", "tagidan o'ta olmaydi", "ostidan ota olmaydi"]
  },
  {
    "id": 71,
    "q": "71. Qaysi oyda odamlar eng kam uxlashadi?",
    "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800",
    "hint": "💡 Maslahat: Kunlari eng kam bo'lgan oy.",
    "a": ["fevral", "fevral oyida", "fevralda"]
  },
  {
    "id": 72,
    "q": "72. Nimaning tishi bor, lekin tishlay olmaydi?",
    "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800",
    "hint": "💡 Maslahat: Sochni tartibga solish uchun ishlatiladi.",
    "a": ["taroq", "arra", "taroq tishlari"]
  },
  {
    "id": 73,
    "q": "73. Qaysi idishdan umuman suv ichib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800",
    "hint": "💡 Maslahat: Teshigi bor idish.",
    "a": ["teshik idishdan", "teshik idish", "bo'sh idish"]
  },
  {
    "id": 74,
    "q": "74. Nimaning oyog'i bor, lekin yurolmaydi?",
    "image": "https://images.unsplash.com/photo-1503602642458-232111445657?w=800",
    "hint": "💡 Maslahat: Xonadagi mebel.",
    "a": ["stul", "stol", "stul oyog'i", "stol oyog'i"]
  },
  {
    "id": 75,
    "q": "75. Qaysi qush tuxum qo'ymaydi, lekin tuxumdan chiqadi?",
    "image": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=800",
    "hint": "💡 Maslahat: Tovuqning erkak jufti.",
    "a": ["xo'roz", "xoroz"]
  },
  {
    "id": 76,
    "q": "76. Nima qanchalik toza bo'lsa, shunchalik qora bo'ladi?",
    "image": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800",
    "hint": "💡 Maslahat: Maktab xonasida bo'r bilan yoziladigan doska.",
    "a": ["doska", "maktab doskasi", "sinf doskasi"]
  },
  {
    "id": 77,
    "q": "77. Dengizning o'rtasida nima bor?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: So'z o'rtasidagi harf.",
    "a": ["n harfi", "n", "harf"]
  },
  {
    "id": 78,
    "q": "78. Nimaning qanoti bor, lekin ucholmaydi?",
    "image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
    "hint": "💡 Maslahat: Katta binolarning yon taraflari/qismlari.",
    "a": ["bino qanoti", "bino", "imorat qanoti"]
  },
  {
    "id": 79,
    "q": "79. Bir kishining 3 ta qizi bor. Har birining bittadan ukasi bor. Nechta farzand bor?",
    "image": "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=800",
    "hint": "💡 Maslahat: Barcha qizlar uchun bitta uka yetarli.",
    "a": ["4 ta", "4", "to'rtta"]
  },
  {
    "id": 80,
    "q": "80. Qaysi tugmani kiyimda bosib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800",
    "hint": "💡 Maslahat: Kiyimga tikilgan oddiy tugma.",
    "a": ["kiyim tugmasini", "tikilgan tugmani", "tugma"]
  },
  {
    "id": 81,
    "q": "81. Nima o'z egasiga va uni yasagan kishiga kerak emas, ishlatgan kishi ko'rmaydi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Mayit solinadigan yog'och buyum.",
    "a": ["tobut"]
  },
  {
    "id": 82,
    "q": "82. Yerdan ko'tarish oson, lekin uzoqqa otish qiyin bo'lgan narsa nima?",
    "image": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=800",
    "hint": "💡 Maslahat: Qushning yengil pati.",
    "a": ["par", "qush pati", "pat"]
  },
  {
    "id": 83,
    "q": "83. Har bir odamda bor, lekin barmoqlarda hech qachon bir xil bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Biometrik identifikatsiya vositasi.",
    "a": ["barmoq izi", "barmoq izlari"]
  },
  {
    "id": 84,
    "q": "84. Nima tun-u kun ishlaydi, lekin charchamaydi?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: Ko'krak qafasidagi muhim organ yoki soat.",
    "a": ["yurak", "soat"]
  },
  {
    "id": 85,
    "q": "85. Qaysi hayvon o'z nomini aytib baqiradi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Boshqa qushlar iniga tuxum qo'yadigan qush.",
    "a": ["kakku", "kakku qushi"]
  },
  {
    "id": 86,
    "q": "86. Nima uchun qarg'a shoxga qo'nadi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Uchishdan charchagani uchun.",
    "a": ["charchagani uchun", "uchishdan charchagani uchun"]
  },
  {
    "id": 87,
    "q": "87. Har kuni ovqat yeydi, suv ichsa o'ladi. U nima?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: O'tin bilan yonadigan narsa.",
    "a": ["olov", "olam"]
  },
  {
    "id": 88,
    "q": "88. Echki 6 yoshga kirsa nima bo'ladi?",
    "image": "https://images.unsplash.com/photo-1524024973431-2ad916746881?w=800",
    "hint": "💡 Maslahat: Keyingi yoshga o'tadi.",
    "a": ["7 yoshga o'tadi", "7 yoshga kiradi", "7-yosh bo'ladi"]
  },
  {
    "id": 89,
    "q": "89. Dunyoda eng tez narsa nima?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Inson miyasida zabil keladigan fikr yoki yorug'lik.",
    "a": ["xayol", "yorug'lik", "fikr"]
  },
  {
    "id": 90,
    "q": "90. Ko'zingizni yumganingizda nimani ko'rasiz?",
    "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
    "hint": "💡 Maslahat: Tunda uxlaganda ko'riladigan holat.",
    "a": ["tush", "qorong'ilik", "qorongilik"]
  },
  {
    "id": 91,
    "q": "91. Qo'lsiz va oyoqsiz eshikni ochadigan narsa nima?",
    "image": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=800",
    "hint": "💡 Maslahat: Kuchli esadigan havo oqimi.",
    "a": ["shamol"]
  },
  {
    "id": 92,
    "q": "92. Nimaning tomiri bor, lekin o'simlik emas?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Og'iz ichidagi a'zo yoki qon tomiri.",
    "a": ["tish", "qon tomiri", "tish tomiri"]
  },
  {
    "id": 93,
    "q": "93. Qaysi kemada dengizchilar bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Koinotga uchadigan transport.",
    "a": ["kosmik kemada", "kosmik kema", "koinot kemasida"]
  },
  {
    "id": 94,
    "q": "94. Cho'ntagingizda hech narsa yo'q, lekin unda nimadir bor. U nima?",
    "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800",
    "hint": "💡 Maslahat: Kiyim yirtilganda paydo bo'ladi.",
    "a": ["teshik"]
  },
  {
    "id": 95,
    "q": "95. Qaysi soat kuniga ikki marta to'g'ri vaqtni ko'rsatadi?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: Ishlamayotgan soat.",
    "a": ["buzilgan soat", "to'xtagan soat", "ishlamaydigan soat"]
  },
  {
    "id": 96,
    "q": "96. Nima ovqatni shirin qiladi, lekin o'zi yeyilmaydi?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Ovqat yeyish xohishi.",
    "a": ["ishtaha", "ishtaha!"]
  },
  {
    "id": 97,
    "q": "97. Nima har doim o'sadi, lekin hech qachon kichraymaydi?",
    "image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800",
    "hint": "💡 Maslahat: Insonning yosh ko'rsatkichi.",
    "a": ["inson yoshi", "yosh", "yoshi"]
  },
  {
    "id": 98,
    "q": "98. Nimani sotib olayotganda qora, ishlatganda qizil, tashlaganda kulrang bo'ladi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Yoqilg'i sifatida ishlatiladigan mineral.",
    "a": ["ko'mir", "komir"]
  },
  {
    "id": 99,
    "q": "99. Qaysi narsa ko'tarilganda tushadi, tushirilganda ko'tariladi?",
    "image": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?w=800",
    "hint": "💡 Maslahat: Tarozi yoki kema yakori bilan bog'liq.",
    "a": ["tarozi", "tarozi pallasi", "kema yakori"]
  },
  {
    "id": 100,
    "q": "100. Siz poyga o'yinida 2-o'rindagi ishtirokchini quvib o'tdingiz. Hozir nechanchi o'rindasiz?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Ikkinchi odamning o'rnini egallaysiz.",
    "a": ["2-o'rinda", "2", "ikkinchi o'rinda", "2-o'rin"]
  },
  {
    "id": 101,
    "q": "101. Poyga o'yinida oxirgi ishtirokchini quvib o'tsangiz, nechanchi o'ringa o'tasiz?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Oxirgi ishtirokchini quvib o'tib bo'ladimi?",
    "a": ["iloji yo'q", "oxirgi odamni quvib bo'lmaydi", "mumkin emas"]
  },
  {
    "id": 102,
    "q": "102. Uyda 5 ta sham yonib turibdi. Shamol tegib 2 tasi o'chdi. Nechta sham qoldi?",
    "image": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=800",
    "hint": "💡 Maslahat: O'chgan shamlargina erib ketmay saqlanib qoladi.",
    "a": ["2 ta", "2", "2 ta sham"]
  },
  {
    "id": 103,
    "q": "103. Dunyoda eng uzoq masofani ko'ra oladigan narsa nima?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Yuzingizdagi ko'rish organi.",
    "a": ["ko'z", "koz"]
  },
  {
    "id": 104,
    "q": "104. Qaysi oydan keyin aprel oyi keladi?",
    "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800",
    "hint": "💡 Maslahat: Bahorning birinchi oyi.",
    "a": ["mart", "mart oyidan"]
  },
  {
    "id": 105,
    "q": "105. Nimani chap qo'l bilan ushlab bo'ladi, lekin o'ng qo'l bilan ushlab bo meydi?",
    "image": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800",
    "hint": "💡 Maslahat: O'ng qo'lingiz tirsagi.",
    "a": ["o'ng tirsak", "o'ng tirsakni", "ong tirsak"]
  },
  {
    "id": 106,
    "q": "106. Qaysi hayvon suv ichmaydi, chunki suv ichsa o'lishi mumkin?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Avstraliyada yashaydigan kenga ko'rinishidagi kalamush simon hayvon.",
    "a": ["kenguru kalamushi", "kalamush"]
  },
  {
    "id": 107,
    "q": "107. Xonada chiroq yo'q, lekin stolda ochiq kitob turibdi. Qanday qilib uni o'qish mumkin?",
    "image": "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=800",
    "hint": "💡 Maslahat: Kunduzi derazadan tushayotgan nur yoki Brayl alifbosi.",
    "a": ["kunduzi", "brayl alifbosi", "kunduzyorug'ida"]
  },
  {
    "id": 108,
    "q": "108. Bir odam 3-qavatdan sakradi va oyog'ini sindirdi. U 9-qavatdan sakrasa nechta oyog'ini sindiradi?",
    "image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
    "hint": "💡 Maslahat: Inson tanasida nechta oyoq bor?",
    "a": ["2 ta", "2", "ikkkala oyog'ini"]
  },
  {
    "id": 109,
    "q": "109. Nima pishirilganda qattiqlashadi?",
    "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800",
    "hint": "💡 Maslahat: Qaynayotgan suvda pishadigan mahsulot.",
    "a": ["tuxum"]
  },
  {
    "id": 110,
    "q": "110. Barcha insonlar nima uchun ovqat yeyishadi?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Ovqat stolda yoki idishda turgan joyi.",
    "a": ["stolda turgani uchun", "idishda bo'lgani uchun", "och bo'lgani uchun"]
  },
  {
    "id": 111,
    "q": "111. Bitta chiziq tortib, uni kesmasdan yoki o'chirmasdan qanday qilib qisqartirish mumkin?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: Yoniga undan uzunroq chiziq chizish kerak.",
    "a": ["yoniga uzunroq chiziq chizib", "uzunroq chiziq chizib"]
  },
  {
    "id": 112,
    "q": "112. Qaysi savolga 'Yo'q' deb javob berib bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800",
    "hint": "💡 Maslahat: Siz tirikmisiz degan savol.",
    "a": ["tirikmisiz", "siz tirikmisiz?", "eshingiz yopiqmi"]
  },
  {
    "id": 113,
    "q": "113. Yer ostida yashaydi, lekin o'simlik emas. U nima?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Krot (ko'rchuqur).",
    "a": ["krot", "ko'rchuqur", "chuvalchang"]
  },
  {
    "id": 114,
    "q": "114. Qaysi daraxt barg chiqarmaydi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Qurigan yoki kaktus simon daraxt.",
    "a": ["qurigan daraxt", "quriydigan daraxt", "qurigan"]
  },
  {
    "id": 115,
    "q": "115. Nima har doim oldinga harakat qiladi, lekin orqaga qaytmaydi?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Vaqt oqimi.",
    "a": ["vaqt"]
  },
  {
    "id": 116,
    "q": "116. Nimani syndicate qilmay turib yeb bo'lmaydi?",
    "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800",
    "hint": "💡 Maslahat: Qobig'i barbod qilinishi kerak bo'lgan narsa.",
    "a": ["tuxum", "yong'oq"]
  },
  {
    "id": 117,
    "q": "117. Poyezdning qaysi qismida tezlik sezilmaydi?",
    "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800",
    "hint": "💡 Maslahat: Restoran yoki harakatlanmaydigan qismi.",
    "a": ["restoran vagonida", "ichida"]
  },
  {
    "id": 118,
    "q": "118. O'zbekiston bayrog'ida nechta yulduz bor?",
    "image": "https://images.unsplash.com/photo-1579273166152-d725a4e2b755?w=800",
    "hint": "💡 Maslahat: Oylar soni bilan teng.",
    "a": ["12 ta", "12", "o'n ikkita"]
  },
  {
    "id": 119,
    "q": "119. Qaysi hayvon o'z uyi bilan birga yuradi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Qoshi bor sekin yuradigan mavjudot.",
    "a": ["shilliq qurt", "tasbaha", "shilliqshurt"]
  },
  {
    "id": 120,
    "q": "120. Qaysi xonada eshik ham, deraza ham yo'q?",
    "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=800",
    "hint": "💡 Maslahat: Qazi yeyiladigan sabzavot/qo'ziqorin.",
    "a": ["qo'ziqorin", "qozimqorin"]
  },
  {
    "id": 121,
    "q": "121. Nima yozda kiyinadi, qishda yechinadi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Barg tashlaydigan o'simlik.",
    "a": ["daraxt", "daraxtlar"]
  },
  {
    "id": 122,
    "q": "122. Bitta o'rmonda nechta daraxt bor?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: O'rmon barglar va daraxtlardan iborat.",
    "a": ["juda ko'p", "sanoqsiz", "ko'p"]
  },
  {
    "id": 123,
    "q": "123. Suv qachon toshga aylanadi?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Muzlaganda.",
    "a": ["muzlaganda", "muz bo'lganda"]
  },
  {
    "id": 124,
    "q": "124. Bir xonada 3 kishi bor edi. Biri chiqib ketdi, necha kishi qoldi?",
    "image": "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=800",
    "hint": "💡 Maslahat: Oddiy ayirish amali.",
    "a": ["2 kishi", "2", "ikki kishi"]
  },
  {
    "id": 125,
    "q": "125. Nimaning quloqlari bor, lekin eshitmaydi?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Qozon ushlaydigan qismi.",
    "a": ["qozon", "qozon qulog'i", "yostiq"]
  },
  {
    "id": 126,
    "q": "126. Quyosh qayerdan chiqadi?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Dunyo tomonlaridan biri.",
    "a": ["sharqdan", "sharq"]
  },
  {
    "id": 127,
    "q": "127. Qaysi hayvon sudralib yuradi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Ilon yoki kiyikmas.",
    "a": ["ilon", "kaltakesak"]
  },
  {
    "id": 128,
    "q": "128. Inson tanasida nechta suyak bor?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Katta yoshli odamda 206 ta.",
    "a": ["206 ta", "206", "206-ta"]
  },
  {
    "id": 129,
    "q": "129. Qaysi sabzavot ko'zni yoshlantiradi?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: To'g'ralganda achishtiradigan o'simlik.",
    "a": ["piyoz"]
  },
  {
    "id": 130,
    "q": "130. Dunyodagi eng baland tog' qaysi?",
    "image": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800",
    "hint": "💡 Maslahat: Everest (Jomolungma).",
    "a": ["everest", "jomolungma"]
  },
  {
    "id": 131,
    "q": "131. Qaysi okean eng katta hisoblanadi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Tinch okeani.",
    "a": ["tinch okeani", "tinch"]
  },
  {
    "id": 132,
    "q": "132. Kompyuterning miyasi deb nimaga aytiladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Markaziy protsessor (CPU).",
    "a": ["protsessor", "cpu"]
  },
  {
    "id": 133,
    "q": "133. Futbol o'yinida maydonda nechta o'yinchi bo'ladi?",
    "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800",
    "hint": "💡 Maslahat: Har bir jamoada 11 tadan.",
    "a": ["22 ta", "22", "22 kishi"]
  },
  {
    "id": 134,
    "q": "134. Qaysi planetada biz yashaymiz?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Ko'k planeta.",
    "a": ["yer", "yer sayyorasi"]
  },
  {
    "id": 135,
    "q": "135. Yilning qaysi faslida qor yog'adi?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Eng sovuq fasl.",
    "a": ["qish", "qishda", "qish faslida"]
  },
  {
    "id": 136,
    "q": "136. Qaysi qush tunda ko'radi, kunduzi uxlaydi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Boyo'g'li.",
    "a": ["boyo'g'li", "boyogli"]
  },
  {
    "id": 137,
    "q": "137. Suvning kimyoviy formulasi qanday?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: H va O elementlari.",
    "a": ["h2o", "h2o"]
  },
  {
    "id": 138,
    "q": "138. Eng kichik musiqiy nota qaysi?",
    "image": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800",
    "hint": "💡 Maslahat: Do re mi fa sol la si.",
    "a": ["do", "si"]
  },
  {
    "id": 139,
    "q": "139. Qaysi hayvon 'sahro kemasi' deb ataladi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: O'rkachli hayvon.",
    "a": ["tuya", "tuya hayvoni"]
  },
  {
    "id": 140,
    "q": "140. Non tayyorlash uchun eng asosiy xomashyo nima?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Bug'doydan olinadigan kukunsimon mahsulot.",
    "a": ["un", "bug'doy uni"]
  },
  {
    "id": 141,
    "q": "141. Nima o'sadi, lekin joni yo'q?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Soch va tirnoqlar.",
    "a": ["soch", "tirnoq"]
  },
  {
    "id": 142,
    "q": "142. Bir yilda nechta kun bor?",
    "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800",
    "hint": "💡 Maslahat: Odatdagi yilda 365 kun.",
    "a": ["365", "365 kun", "366"]
  },
  {
    "id": 143,
    "q": "143. Kamalakda nechta rang bor?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: 7 ta asosiy rang.",
    "a": ["7 ta", "7", "yettita"]
  },
  {
    "id": 144,
    "q": "144. Qaysi faslda daraxtlar kurtak yoazdi?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Bahor fasli.",
    "a": ["bahor", "bahorda", "bahor faslida"]
  },
  {
    "id": 145,
    "q": "145. O'zbekiston Respublikasi mustaqillik kuni qachon?",
    "image": "https://images.unsplash.com/photo-1579273166152-d725a4e2b755?w=800",
    "hint": "💡 Maslahat: 1-sentyabr.",
    "a": ["1-sentyabr", "1 sentyabr", "1-sentyabrda"]
  },
  {
    "id": 146,
    "q": "146. Qaysi meva vitamin C ga eng boy hisoblanadi?",
    "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    "hint": "💡 Maslahat: Limon yoki apelsin.",
    "a": ["limon", "nartursh", "apelsin"]
  },
  {
    "id": 147,
    "q": "147. Qaysi soatda mil yo'q?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: Elektron yoki qum soat.",
    "a": ["elektron soat", "qum soat", "raqamli soat"]
  },
  {
    "id": 148,
    "q": "148. Nima doim pastga qaraydi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: O'simlik ildizi.",
    "a": ["ildiz", "o'simlik ildizi"]
  },
  {
    "id": 149,
    "q": "149. Telefonda kim bilan gaplashasiz?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Narigi tarafdagi suhbatdash.",
    "a": ["suhbatdosh", "odam bilan", "inson"]
  },
  {
    "id": 150,
    "q": "150. Quyosh tizimidagi eng katta planeta qaysi?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Yupiter.",
    "a": ["yupiter", "yupiter sayyorasi"]
  },
  {
    "id": 151,
    "q": "151. Dunyodagi eng mitti qush qaysi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Kolibri qushi.",
    "a": ["kolibri", "kolibri qushi"]
  },
  {
    "id": 152,
    "q": "152. Qaysi hayvon sudralib yurib, tishini har yili yangilaydi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Suvda va quruqlikda yashaydigan yirtqich emizikli.",
    "a": ["timsah", "krokodil"]
  },
  {
    "id": 153,
    "q": "153. Yer shari nechta qit'adan iborat?",
    "image": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800",
    "hint": "💡 Maslahat: 6 ta asosiy qit'a.",
    "a": ["6 ta", "6", "oltta"]
  },
  {
    "id": 154,
    "q": "154. Quyosh tizimida nechta planeta bor?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: 8 ta asosiy planeta.",
    "a": ["8 ta", "8", "sakkizta"]
  },
  {
    "id": 155,
    "q": "155. Qaysi metall xona haroratida suyuq holatda bo'ladi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Termometrlarda ishlatiladigan metall.",
    "a": ["simob"]
  },
  {
    "id": 156,
    "q": "156. Inson organizmida necha litr qon bor?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: O'rtacha 5 litr atrofida.",
    "a": ["5 litr", "5-6 litr", "5 litr atrofida"]
  },
  {
    "id": 157,
    "q": "157. Qaysi hayvon eng uzoq umr ko'radi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Suv toshbaqasi yoki Grenlandiya akulasi.",
    "a": ["toshbaqa", "akula", "grenlandiya akulasi"]
  },
  {
    "id": 158,
    "q": "158. Bitta haftada nechta soat bor?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: 7 kun x 24 soat.",
    "a": ["168", "168 soat"]
  },
  {
    "id": 159,
    "q": "159. Qaysi qit'ada muzliklar eng ko'p joylashgan?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Antarktida.",
    "a": ["antarktida", "antarktida qit'asi"]
  },
  {
    "id": 160,
    "q": "160. Shamolning yo'nalishini ko'rsatadigan asbob nima deb ataladi?",
    "image": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=800",
    "hint": "💡 Maslahat: Flyuger.",
    "a": ["flyuger", "flyugerk"]
  },
  {
    "id": 161,
    "q": "161. Qaysi mevaning urug'i tashqarisida bo'ladi?",
    "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    "hint": "💡 Maslahat: Qulupnay.",
    "a": ["qulupnay", "klubnika"]
  },
  {
    "id": 162,
    "q": "162. Shaharda yashaydi, lekin uyi yo'q. U nima?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Ko'cha yoki daydi hayvon.",
    "a": ["ko'cha", "daydi hayvon"]
  },
  {
    "id": 163,
    "q": "163. Yozda issiq, qishda sovuq bo'ladigan joy qayer?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Dala yoki ochiq havo.",
    "a": ["tashqari", "ko'cha", "ochiq havo"]
  },
  {
    "id": 164,
    "q": "164. Kompyuterda ma'lumotlarni saqlash qurilmasi nima deb ataladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Qattiq disk yoki SSD.",
    "a": ["qattiq disk", "ssd", "xotira", "xard disk"]
  },
  {
    "id": 165,
    "q": "165. Qaysi hayvon Tik-Tok yoki videolarda ko'p tarqalgan dangasa jonzot?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Leniveds (dangasa).",
    "a": ["dangasa", "leniveds"]
  },
  {
    "id": 166,
    "q": "166. Qaysi sport turida to'pni qo'l bilan ushlash mumkin emas (darvozabondan tashqari)?",
    "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800",
    "hint": "💡 Maslahat: Futbol.",
    "a": ["futbol", "futbol o'yinida"]
  },
  {
    "id": 167,
    "q": "167. Qaysi hayvon arining asalini o'g'irlab yeydi?",
    "image": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=800",
    "hint": "💡 Maslahat: O'rmon xo'jayini Ayiq.",
    "a": ["ayiq", "ayiqlar"]
  },
  {
    "id": 168,
    "q": "168. Alisher Navoiy qaysi asr buyuk shoiri?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: XV asr (15-asr).",
    "a": ["15-asr", "15 asr", "xv asr"]
  },
  {
    "id": 169,
    "q": "169. Dunyodagi eng chuqur ko'l qaysi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Baykal ko'li.",
    "a": ["baykal", "baykal ko'li"]
  },
  {
    "id": 170,
    "q": "170. Nima havoda uchadi, lekin qanoti yo'q?",
    "image": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=800",
    "hint": "💡 Maslahat: Bulut yoki chang.",
    "a": ["bulut", "chang", "tutun"]
  },
  {
    "id": 171,
    "q": "171. Harf va raqamlar bilan yoziladigan kod nima deb ataladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Parol yoki kod.",
    "a": ["parol", "kod"]
  },
  {
    "id": 172,
    "q": "172. Samolyotni boshqaradigan shaxs kim?",
    "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
    "hint": "💡 Maslahat: Uchuvchi (pilot).",
    "a": ["uchuvchi", "pilot"]
  },
  {
    "id": 173,
    "q": "173. Avtomobilga yoqilg'i quyiladigan joy nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Zapravka (AQS).",
    "a": ["zapravka", "aqs", "yoqilg'i quyish shoxobchasi"]
  },
  {
    "id": 174,
    "q": "174. Har doim oq, lekin iflos bo'lsa qorayadi. U nima?",
    "image": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800",
    "hint": "💡 Maslahat: Doska (yoki qor).",
    "a": ["qor", "doska"]
  },
  {
    "id": 175,
    "q": "175. Qaysi o'simlikdan eng ko meva va yog' olinadi?",
    "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    "hint": "💡 Maslahat: Zaytun yoki kungaboqar.",
    "a": ["zaytun", "kungaboqar"]
  },
  {
    "id": 176,
    "q": "176. Qaysi hayvon sut emizuvchi bo'lsada, tuxum qo'yadi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: O'rdakburun (Utkonos).",
    "a": ["o'rdakburun", "utkonos", "yexidna"]
  },
  {
    "id": 177,
    "q": "177. Bir sutkada nechta minut bor?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: 24 x 60 minut.",
    "a": ["1440", "1440 minut", "1440 daqiqa"]
  },
  {
    "id": 178,
    "q": "178. Elektr tokini o'tkazmaydigan material nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Izolyator (dielektrik).",
    "a": ["izolyator", "dielektrik"]
  },
  {
    "id": 179,
    "q": "179. Insonning qaysi organi hech qachon o'smaydi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Ko'z qorachig'i / ko meva.",
    "a": ["ko'z", "ko'z qorachig'i"]
  },
  {
    "id": 180,
    "q": "180. Qaysi harf O'zbek alifbosida unli hisoblanmaydi?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: Undosh harflar.",
    "a": ["b", "v", "g", "d", "undosh harflar"]
  },
  {
    "id": 181,
    "q": "181. Nima yerdan chiqadi, leking suvda eriydi?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Tuz yoki shakar.",
    "a": ["tuz", "shakar"]
  },
  {
    "id": 182,
    "q": "182. Dunyodagi eng tez yuguradigan quruqlik hayvoni qaysi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Gepard.",
    "a": ["gepard"]
  },
  {
    "id": 183,
    "q": "183. Qaysi xitoy devori dunyoning mo'jizalaridan biri?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Buyuk Xitoy devori.",
    "a": ["buyuk xitoy devori", "xitoy devori"]
  },
  {
    "id": 184,
    "q": "184. Inson tanasidagi eng katta organ qaysi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Teri.",
    "a": ["teri", "inson terisi"]
  },
  {
    "id": 185,
    "q": "185. Nechta shaxmat donasi (fiqurasi) bilan o'yin boshlanadi?",
    "image": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=800",
    "hint": "💡 Maslahat: Jami 32 ta dona.",
    "a": ["32 ta", "32", "32 dona"]
  },
  {
    "id": 186,
    "q": "186. Dunyodagi eng uzun daryo qaysi?",
    "image": "https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?w=800",
    "hint": "💡 Maslahat: Nil daryosi (yoki Amazonka).",
    "a": ["nil", "nil daryosi", "amazonka"]
  },
  {
    "id": 187,
    "q": "187. Kompyuter sichqonchasining nechta asosiy tugmasi bor?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Chap va o'ng tugmalar (2 ta).",
    "a": ["2 ta", "2", "ikkita"]
  },
  {
    "id": 188,
    "q": "188. Muz ko'p bo'lgan qutbda qanday ayiqlar yashaydi?",
    "image": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=800",
    "hint": "💡 Maslahat: Oq ayiqlar.",
    "a": ["oq ayiq", "oq ayiqlar"]
  },
  {
    "id": 189,
    "q": "189. Telefonga ilova yuklab olinadigan Android platformasidagi do'kon nima deb ataladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Google Play Store.",
    "a": ["play market", "google play", "play store"]
  },
  {
    "id": 190,
    "q": "190. Quyosh chiqishidan oldingi vaqt nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Saharlik yoki tong.",
    "a": ["tong", "sahar", "saharlik"]
  },
  {
    "id": 191,
    "q": "191. Internet brauzerlariga misol keltiring?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Google Chrome, Opera.",
    "a": ["chrome", "google chrome", "opera"]
  },
  {
    "id": 192,
    "q": "192. Suvning muzlash harorati necha daraja?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: 0 daraja Celsiy.",
    "a": ["0 daraja", "0", "0 gradus"]
  },
  {
    "id": 193,
    "q": "193. Suvning qaynash harorati necha daraja?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: 100 daraja Celsiy.",
    "a": ["100 daraja", "100", "100 gradus"]
  },
  {
    "id": 194,
    "q": "194. Oy Yer atrofida to'liq bir marta aylanishi uchun qancha vaqt ketadi?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Taxminan 27-28 kun (1 oy).",
    "a": ["1 oy", "27 kun", "28 kun", "bir oy"]
  },
  {
    "id": 195,
    "q": "195. Qaysi davlat piramidalar o'lkasi deb ataladi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Misr.",
    "a": ["misr", "egipet"]
  },
  {
    "id": 196,
    "q": "196. Qaysi meva suvda cho'kmaydi?",
    "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    "hint": "💡 Maslahat: Olma (tarkibida 25% havo bor).",
    "a": ["olma"]
  },
  {
    "id": 197,
    "q": "197. Qaysi organ tanamizdagi qonni haydab beradi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Yurak.",
    "a": ["yurak"]
  },
  {
    "id": 198,
    "q": "198. Dunyodagi eng baland bino qaysi?",
    "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800",
    "hint": "💡 Maslahat: Dubaydagi Burj Xalifa.",
    "a": ["burj xalifa", "burj khalifa"]
  },
  {
    "id": 199,
    "q": "199. Qaysi qush orqaga qarab ucha oladi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Mitti Kolibri qushi.",
    "a": ["kolibri", "kolibri qushi"]
  },
  {
    "id": 200,
    "q": "200. Bitta daqiqada nechta soniya bor?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: 60 soniya.",
    "a": ["60", "60 soniya", "60 sekund"]
  },
  {
    "id": 201,
    "q": "201. Qaysi hayvon eng baland bo'yli hisoblanadi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Bo'yni juda uzun jonivor.",
    "a": ["jirafa", "jiraf"]
  },
  {
    "id": 202,
    "q": "202. Dunyodagi eng katta sut emizuvchi hayvon qaysi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Ummon va okeanlarda yashaydi.",
    "a": ["ko'k kit", "kit", "kurt kit"]
  },
  {
    "id": 203,
    "q": "203. Qaysi davlat kunchiqar yurt deb ataladi?",
    "image": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800",
    "hint": "💡 Maslahat: Osiyodagi orol-davlat.",
    "a": ["yaponiya", "japonya"]
  },
  {
    "id": 204,
    "q": "204. Telefonga zaryad beradigan qurilma nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Zaryadnik.",
    "a": ["zaryadnik", "zaryadlovchi", "zaryad qurilmasi"]
  },
  {
    "id": 205,
    "q": "205. Inson tanasida kislorod tashuvchi qon hujayralari nima deb ataladi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Qizil qon tanachalari.",
    "a": ["eritrotsitlar", "eritrotsit", "qizil qon tanachalari"]
  },
  {
    "id": 206,
    "q": "206. Kompyuter ekranidagi tasvir aniqligi birligi nima?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Piksel.",
    "a": ["piksel", "pixel"]
  },
  {
    "id": 207,
    "q": "207. Qaysi sport turida 'shahmat toji' uchun bellashiladi?",
    "image": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=800",
    "hint": "💡 Maslahat: Taxta ustidagi mantiqiy o'yin.",
    "a": ["shahmat", "shaxmat"]
  },
  {
    "id": 208,
    "q": "208. Qaysi qit'a 'eng issiq qit'a' hisoblanadi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Sahara cho'li joylashgan qit'a.",
    "a": ["afrika", "afrika qit'asi"]
  },
  {
    "id": 209,
    "q": "209. Avtomobilning burilishini ko'rsatadigan chiroq nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Povorotnik.",
    "a": ["povorotnik", "burilish chirog'i"]
  },
  {
    "id": 210,
    "q": "210. Qaysi hayvon o'z tilini chiqara olmaydi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Suvda va quruqlikda yashaydigan yirtqich.",
    "a": ["timsah", "krokodil"]
  },
  {
    "id": 211,
    "q": "211. Yerning tabiiy yo'ldoshi nima?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Tunda osmonda porlaydi.",
    "a": ["oy", "oy sayyorasi"]
  },
  {
    "id": 212,
    "q": "212. O'zbekistonning poytaxti qaysi shahar?",
    "image": "https://images.unsplash.com/photo-1579273166152-d725a4e2b755?w=800",
    "hint": "💡 Maslahat: Markaziy Osiyodagi yirik megapolis.",
    "a": ["toshkent", "toshkent shahri"]
  },
  {
    "id": 213,
    "q": "213. Qaysi modda tabiatda 3 xil holatda (suyuq, qattiq, gaz) uchraydi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Hayot manbai.",
    "a": ["suv"]
  },
  {
    "id": 214,
    "q": "214. Kompyuter dasturlarini yozadigan mutaxassis kim?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Kod yozuvchi mutaxassis.",
    "a": ["dasturchi", "programmist"]
  },
  {
    "id": 215,
    "q": "215. Qaysi qush eng tez yuguradi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Ucha olmaydigan katta qush.",
    "a": ["tuyaqush", "tuya qush"]
  },
  {
    "id": 216,
    "q": "216. Nima doim keladi, lekin hech qachon yetib kelmaydi?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Ertangi kun.",
    "a": ["ertaga", "ertangi kun"]
  },
  {
    "id": 217,
    "q": "217. Qaysi geometrik shaklning burchaklari yo'q?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: Doira yoki aylana.",
    "a": ["doira", "aylana"]
  },
  {
    "id": 218,
    "q": "218. Inson miyasining asosiy vazifasi nima?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: O'ylash va boshqarish.",
    "a": ["fikrlash", "boshqarish", "o'ylash"]
  },
  {
    "id": 219,
    "q": "219. Qaysi hayvon suv tagida uxlay oladi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Delphin yoki kit.",
    "a": ["delfin", "kit"]
  },
  {
    "id": 220,
    "q": "220. Eng qattiq tabiat materiali nima?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Olmos.",
    "a": ["olmos", "almaz"]
  },
  {
    "id": 221,
    "q": "221. Dunyodagi eng katta orol qaysi?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Grenlandiya.",
    "a": ["grenlandiya", "grenlandiya oroli"]
  },
  {
    "id": 222,
    "q": "222. Avtomobilda xavfsizlikni ta'minlaydigan Tasma nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Xavfsizlik kamari.",
    "a": ["xavfsizlik kamari", "kamar"]
  },
  {
    "id": 223,
    "q": "223. Musiqada nechta asosiy nota bor?",
    "image": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800",
    "hint": "💡 Maslahat: Do, Re, Mi...",
    "a": ["7 ta", "7", "yettita"]
  },
  {
    "id": 224,
    "q": "224. Qaysi gaz inson nafas olishi uchun zarur?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Kislorod.",
    "a": ["kislorod", "o2"]
  },
  {
    "id": 225,
    "q": "225. O'simliklar quyosh nuridan foydalanib oziq modda hosil qilish jarayoni nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Fotosintez.",
    "a": ["fotosintez"]
  },
  {
    "id": 226,
    "q": "226. Dunyodagi eng ko'p aholiga ega davlat qaysi?",
    "image": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800",
    "hint": "💡 Maslahat: Hindiston (yoki Xitoy).",
    "a": ["hindiston", "xitoy"]
  },
  {
    "id": 227,
    "q": "227. Kompyuter xotirasi sig'imi birligi (eng kichigi) nima?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Bit yoki Bayt.",
    "a": ["bit", "bayt"]
  },
  {
    "id": 228,
    "q": "228. Qaysi hayvonning sutidan qimiz tayyorlanadi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Ot (biya).",
    "a": ["ot", "biya"]
  },
  {
    "id": 229,
    "q": "229. Yerdan eng yaqin yulduz qaysi?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Kunduzi charaglab turadi.",
    "a": ["quyosh"]
  },
  {
    "id": 230,
    "q": "230. Qaysi hayvonning dumi kesilsa, qayta o'sib chiqadi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Kaltakesak.",
    "a": ["kaltakesak"]
  },
  {
    "id": 231,
    "q": "231. Qaysi faslda kechalar eng uzun bo'ladi?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Qish fasli.",
    "a": ["qish", "qishda", "qish faslida"]
  },
  {
    "id": 232,
    "q": "232. Telefon tarmog'isiz muloqot qiladigan kichik radiostansiya nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Ratsiya.",
    "a": ["ratsiya", "rotiya"]
  },
  {
    "id": 233,
    "q": "233. O'zbekiston milliy valyutasi nima?",
    "image": "https://images.unsplash.com/photo-1579273166152-d725a4e2b755?w=800",
    "hint": "💡 Maslahat: So'm.",
    "a": ["so'm", "som"]
  },
  {
    "id": 234,
    "q": "234. Qaysi meva suvda 80% dan ortiq suvdan iborat?",
    "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    "hint": "💡 Maslahat: Tarvuz.",
    "a": ["tarvuz"]
  },
  {
    "id": 235,
    "q": "235. Yilning nechanchi oyida 28 yoki 29 kun bor?",
    "image": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800",
    "hint": "💡 Maslahat: Fevral.",
    "a": ["fevral", "fevral oyida"]
  },
  {
    "id": 236,
    "q": "236. Qaysi sport turida halqalar (ring) ustida kurashiladi?",
    "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800",
    "hint": "💡 Maslahat: Boks.",
    "a": ["boks"]
  },
  {
    "id": 237,
    "q": "237. Kompyuter klaviaturasidagi eng katta tugma qaysi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Probel (Spacebar).",
    "a": ["probel", "space", "spacebar"]
  },
  {
    "id": 238,
    "q": "238. Inson tanasida eng kuchli muskul (mushak) qayerda joylashgan?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Jag' yoki til mushagi.",
    "a": ["jag'", "til", "jag' mushagi"]
  },
  {
    "id": 239,
    "q": "239. Dunyodagi eng katta cho'l qaysi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Sahara (yoki Antarktida muz cho'li).",
    "a": ["sahara", "antarktida"]
  },
  {
    "id": 240,
    "q": "240. Samolyot havoga ko'tarilishi uchun nima kerak?",
    "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
    "hint": "💡 Maslahat: Tezlik va havo oqimi (qanot kuchi).",
    "a": ["tezlik", "havo oqimi", "yoqilg'i"]
  },
  {
    "id": 241,
    "q": "241. Qaysi jonivor o'z tanasining og'irligidan 50 baravar ko'p yuk ko'tara oladi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Chumoli.",
    "a": ["chumoli"]
  },
  {
    "id": 242,
    "q": "242. Qaysi davlat hududi bo'yicha dunyoda eng katta?",
    "image": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800",
    "hint": "💡 Maslahat: Rossiya.",
    "a": ["rossiya", "rossiya federatsiyasi"]
  },
  {
    "id": 243,
    "q": "243. Insonning qaysi segi organida barmoq izlari kabi unikal naqshlar bor?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Ko'z rangli pardasi (iris) yoki barmoqlar.",
    "a": ["ko'z", "barmoq", "ko'z pardasi"]
  },
  {
    "id": 244,
    "q": "244. Haroratni o'lchaydigan asbob nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800",
    "hint": "💡 Maslahat: Termometr.",
    "a": ["termometr", "gradusnik"]
  },
  {
    "id": 245,
    "q": "245. O'zbekiston gerbida qaysi afsonaviy qush tasvirlangan?",
    "image": "https://images.unsplash.com/photo-1579273166152-d725a4e2b755?w=800",
    "hint": "💡 Maslahat: Humo qushi.",
    "a": ["humo", "humo qushi"]
  },
  {
    "id": 246,
    "q": "246. Qaysi hayvonning yuragi uning boshida joylashgan?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Krevetka (krevetka saratoni).",
    "a": ["krevetka"]
  },
  {
    "id": 247,
    "q": "247. Quyosh sistemasidagi qaysi planetada ulkan xalqalar (uzuklar) bor?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Saturn.",
    "a": ["saturn", "saturn sayyorasi"]
  },
  {
    "id": 248,
    "q": "248. Bir kilogrammda nechta gramm bor?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: 1000 gramm.",
    "a": ["1000", "1000 g", "1000 gramm"]
  },
  {
    "id": 249,
    "q": "249. Qaysi hayvon 'o'rmon shifokori' deyiladi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Qizilishton qushi.",
    "a": ["qizilishton"]
  },
  {
    "id": 250,
    "q": "250. Internetdagi web-saytlarning bosh sahifasi nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Bosh sahifa (Home page).",
    "a": ["bosh sahifa", "home page", "main page"]
  },
  {
    "id": 251,
    "q": "251. Qaysi o'simlikdan shakar olinadi?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Shakarqamish yoki lavlagi.",
    "a": ["lavlagi", "shakarqamish", "shakar lavlagi"]
  },
  {
    "id": 252,
    "q": "252. Dunyodagi eng kichik okean qaysi?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Shimoliy Muz okeani.",
    "a": ["shimoliy muz okeani", "muz okeani"]
  },
  {
    "id": 253,
    "q": "253. Shaxmat taxtasida nechta katak bor?",
    "image": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=800",
    "hint": "💡 Maslahat: 8x8 kataklar.",
    "a": ["64 ta", "64", "64 katak"]
  },
  {
    "id": 254,
    "q": "254. Qaysi daryo dunyoda eng sersuv hisoblanadi?",
    "image": "https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?w=800",
    "hint": "💡 Maslahat: Janubiy Amerikadagi daryo.",
    "a": ["amazonka", "amazonka daryosi"]
  },
  {
    "id": 255,
    "q": "255. Inson tanasida nechta qovurg'a bor?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: 12 juft (24 ta).",
    "a": ["24 ta", "24", "12 juft"]
  },
  {
    "id": 256,
    "q": "256. Kompyuterda o'chirilgan fayllar qayerga tushadi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Korzina (Recycle Bin).",
    "a": ["korzina", "recycle bin", "chiqindi qutisi"]
  },
  {
    "id": 257,
    "q": "257. Qaysi meva limon kabi nordon, lekin yashil rangda bo'ladi?",
    "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800",
    "hint": "💡 Maslahat: Laym.",
    "a": ["laym"]
  },
  {
    "id": 258,
    "q": "258. Qaysi jonivor tik turib uxlay oladi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Ot yoki fil.",
    "a": ["ot", "fil"]
  },
  {
    "id": 259,
    "q": "259. O'zbekistonda eng katta viloyat qaysi?",
    "image": "https://images.unsplash.com/photo-1579273166152-d725a4e2b755?w=800",
    "hint": "💡 Maslahat: Qoraqalpog'iston Respublikasi / Navoiy viloyati.",
    "a": ["navoiy", "qoraqalpog'iston", "navoiy viloyati"]
  },
  {
    "id": 260,
    "q": "260. Atmosferadagi eng ko'p tarqalgan gaz qaysi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Azot (78%).",
    "a": ["azot", "azot gazi"]
  },
  {
    "id": 261,
    "q": "261. Telefon ekranini chizilishdan himoya qiluvchi oyna nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Zashchitnik (Zashchita oynasi).",
    "a": ["zashchitnik", "himoya oynasi", "steklo"]
  },
  {
    "id": 262,
    "q": "262. Avtomobil qancha masofa bosib o'tganini o'lchaydigan asbob nima?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Odometer (Spidometr qismida).",
    "a": ["odometr", "spidometr"]
  },
  {
    "id": 263,
    "q": "263. Qaysi hayvonning homiladorlik davri eng uzun (taxminan 22 oy)?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Fil.",
    "a": ["fil"]
  },
  {
    "id": 264,
    "q": "264. Qaysi sport turida 'strike' va 'spare' tushunchalari bor?",
    "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800",
    "hint": "💡 Maslahat: Bouling.",
    "a": ["bouling", "bowling"]
  },
  {
    "id": 265,
    "q": "265. Qaysi planetaning atrofida eng ko'p yo'ldoshlar bor?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: Saturn yoki Yupiter.",
    "a": ["saturn", "yupiter"]
  },
  {
    "id": 266,
    "q": "266. Bir metrda nechta santimetr bor?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: 100 sm.",
    "a": ["100", "100 sm", "100 santimetr"]
  },
  {
    "id": 267,
    "q": "267. Qaysi hayvon suv ichmaydi, balki suvni terisi orqali shimib oladi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Qurbaqa.",
    "a": ["qurbaqa"]
  },
  {
    "id": 268,
    "q": "268. Internetda ma'lumot qidiruvchi eng mashhur tizim qaysi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Google.",
    "a": ["google", "gugl"]
  },
  {
    "id": 269,
    "q": "269. Dunyodagi eng baland sharshara qaysi?",
    "image": "https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?w=800",
    "hint": "💡 Maslahat: Anxel (Angel).",
    "a": ["anxel", "angel"]
  },
  {
    "id": 270,
    "q": "270. Inson tanasida nechta sezgi a'zosi bor?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Ko'rish, eshitish, hid bilish, ta'm bilish, paypaslash (5 ta).",
    "a": ["5 ta", "5", "beshta"]
  },
  {
    "id": 271,
    "q": "271. Qaysi turdagi xotira kompyuter o'chirilganda tozalanib ketadi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Operativ xotira (RAM).",
    "a": ["ram", "operativ xotira", "operativka"]
  },
  {
    "id": 272,
    "q": "272. Yer yuzidagi eng sovuq joy qayer?",
    "image": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=800",
    "hint": "💡 Maslahat: Antarktida.",
    "a": ["antarktida"]
  },
  {
    "id": 273,
    "q": "273. Qaysi sabzavot tuproq ostida o'sadi va to's-to's tayyorlanadi?",
    "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
    "hint": "💡 Maslahat: Kartoshka.",
    "a": ["kartoshka"]
  },
  {
    "id": 274,
    "q": "274. Inson tanasidagi eng uzun nerv qaysi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Quyimchak (Sedalishniy) nervi.",
    "a": ["sedalishniy", "quyimchak nervi"]
  },
  {
    "id": 275,
    "q": "275. Qaysi davlat 'Lola mamlakati' deb ataladi?",
    "image": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800",
    "hint": "💡 Maslahat: Niderlandiya (Gollandiya).",
    "a": ["niderlandiya", "gollandiya"]
  },
  {
    "id": 276,
    "q": "276. Dasturlashda xatoliklarni topish va tuzatish jarayoni nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Debagging (Debugging).",
    "a": ["debugging", "debagging", "otladka"]
  },
  {
    "id": 277,
    "q": "277. Qaysi qush tuxum bosmaydi, balki boshqa qushlar iniga qo'yib ketadi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Kaklik emas, Kakku.",
    "a": ["kakku", "kakku qushi"]
  },
  {
    "id": 278,
    "q": "278. Qaysi mato tabiiy ravishda ipak qurti orqali olinadi?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: Ipak.",
    "a": ["ipak", "sholk"]
  },
  {
    "id": 279,
    "q": "279. Qaysi organ suyuqlikni filtrlash va siydik hosil qilish uchun javobgar?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Buyrak.",
    "a": ["buyrak", "buyraklar"]
  },
  {
    "id": 280,
    "q": "280. Dunyodagi eng katta dengiz qaysi?",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "hint": "💡 Maslahat: Filippin dengizi (yoki O'rtayer dengizi).",
    "a": ["filippin dengizi", "o'rtayer dengizi"]
  },
  {
    "id": 281,
    "q": "281. Kompyuter tarmog'ida ma'lumotlarni uzatish tezligi nimada o'lchanadi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Mbit/s (Megabit sekundiga).",
    "a": ["mbit/s", "megabit", "kb/s"]
  },
  {
    "id": 282,
    "q": "282. Qaysi faslda kunlar eng uzun bo'ladi?",
    "image": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=800",
    "hint": "💡 Maslahat: Yoz fasli.",
    "a": ["yoz", "yozda", "yoz faslida"]
  },
  {
    "id": 283,
    "q": "283. Avtomobilda tormoz bosilganda orqada yonadigan chiroqlar qanday rangda?",
    "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=800",
    "hint": "💡 Maslahat: Qizil rang.",
    "a": ["qizil", "qizil rangda"]
  },
  {
    "id": 284,
    "q": "284. Qaysi hayvon suv ichmasdan eng uzoq vaqt yashay oladi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Kenguru kalamushi yoki tuya.",
    "a": ["kenguru kalamushi", "tuya"]
  },
  {
    "id": 285,
    "q": "285. Inson tanasida ovqat hazm qilish qaysi organda boshlanadi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Og'iz bo'shlig'i.",
    "a": ["og'iz", "og'iz bo'shlig'i"]
  },
  {
    "id": 286,
    "q": "286. Dunyodagi eng qimmatbaho va noyob metall qaysi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Rodiy yoki kaliforniy.",
    "a": ["rodiy", "kaliforniy", "platina"]
  },
  {
    "id": 287,
    "q": "287. Telefonda Wi-Fi standarti nimani anglatadi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Simsiz internet (Wireless Fidelity).",
    "a": ["simsiz internet", "wireless fidelity"]
  },
  {
    "id": 288,
    "q": "288. Qaysi qush soatiga 300 km dan ortiq tezlikda shung'iy oladi?",
    "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    "hint": "💡 Maslahat: Sapsan lachin (Lochin).",
    "a": ["sapsan", "lochin", "sapsan lochini"]
  },
  {
    "id": 289,
    "q": "289. Inson ko'zi sekundiga nechta kadrni ajrata oladi deb hisoblanadi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Taxminan 24-60 kadr.",
    "a": ["24", "60", "24-60"]
  },
  {
    "id": 290,
    "q": "290. Qaysi qit'ada birorta ham cho'l yo'q?",
    "image": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800",
    "hint": "💡 Maslahat: Yevropa.",
    "a": ["yevropa", "yevropa qit'asi"]
  },
  {
    "id": 291,
    "q": "291. Dasturlashda davriy takrorlanadigan kod bloki nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800",
    "hint": "💡 Maslahat: Tsikl (Loop).",
    "a": ["tsikl", "loop", "sikll"]
  },
  {
    "id": 292,
    "q": "292. Qaysi hayvonning suti pushti rangda bo'ladi?",
    "image": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800",
    "hint": "💡 Maslahat: Begemot (Gippopotam).",
    "a": ["begemot", "gippopotam"]
  },
  {
    "id": 293,
    "q": "293. Dunyodagi eng qadimgi yozuv turi nima deyiladi?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: Muxrsimon / Mixxat yozuvi (Klinopis).",
    "a": ["mixxat", "klinopis", "iyeroglif"]
  },
  {
    "id": 294,
    "q": "294. Qaysi a'zo qondagi shakarni tartibga solish uchun insulin ishlab chiqaradi?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Oshqozon osti bezi.",
    "a": ["oshqozon osti bezi", "podjeludochnaya"]
  },
  {
    "id": 295,
    "q": "295. Dunyodagi eng tez poezdlar qaysi davlatda ishlaydi?",
    "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800",
    "hint": "💡 Maslahat: Xitoy yoki Yaponiya (Maglev).",
    "a": ["xitoy", "yaponiya"]
  },
  {
    "id": 296,
    "q": "296. Yer o'z o'qi atrofida to'liq bir marta aylanishi uchun qancha vaqt ketadi?",
    "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
    "hint": "💡 Maslahat: 24 soat (1 kun).",
    "a": ["24 soat", "1 kun", "bir kun"]
  },
  {
    "id": 297,
    "q": "297. Yuzaki o'lchov birligi bo'lgan 'gektar' nechta kvadrat metrga teng?",
    "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "hint": "💡 Maslahat: 10 000 kv.m.",
    "a": ["10000", "10 000", "10000 kv m"]
  },
  {
    "id": 298,
    "q": "298. Qaysi metall zanglamaydi?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Oltin yoki platina.",
    "a": ["oltin", "platina"]
  },
  {
    "id": 299,
    "q": "299. Inson skeletidagi eng kichik suyak qayerda joylashgan?",
    "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800",
    "hint": "💡 Maslahat: Quloqda (Uzangi suyagi).",
    "a": ["quloqda", "quloq", "uzangi suyagi"]
  },
  {
    "id": 300,
    "q": "300. Python dasturlash tilining ramzi qaysi hayvon?",
    "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
    "hint": "💡 Maslahat: Ilon (Piton).",
    "a": ["ilon", "piton", "python"]
  }
]

# --- KODGA QO'SHILADIGAN JAVOBNI TEKSHIRISH FUNKSIYASI ---

def normalize_text(text: str) -> str:
    """Matndagi tuturuq belgilari, apostroflar va ortiqcha bo'shliqlarni olib tashlaydi."""
    if not text:
        return ""
    text = str(text).lower().strip()
    
    # Apostroflarni olib tashlash (to'g'ri tirnoq sintaksisi bilan)
    text = re.sub(r"[‘`’'\"`]", "", text)
    
    # O' va G' harflarini standartlashtirish
    text = text.replace("o‘", "o").replace("g‘", "g").replace("o'", "o").replace("g'", "g")
    
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
