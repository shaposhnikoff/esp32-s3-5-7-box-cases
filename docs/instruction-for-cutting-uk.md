# Інструкція для майстерні: акрилові корпуси

Потрібно виготовити **три окремі пробні корпуси** з литого акрилу номінальною товщиною **3 мм**: для Raspberry Pi 4 Model B, екрана Waveshare 5″ та екрана Waveshare 7B. Кожен корпус складається із шести деталей. Усі розміри у файлах — у міліметрах.

Для лазерного різання використовуйте **DXF**. Окремі **SVG** містять ті самі деталі. **PDF** призначені для друку паперових шаблонів і перевірки посадки; друкуйте їх у масштабі **100%**, без припасування до сторінки, та перевіряйте контрольну лінію 50 мм. Спочатку виріжте пробний зразок з’єднання з фактичного акрилу та перевірте входження зубців у пази.

## 1. Raspberry Pi 4 Model B

Корпус 110 × 86 × 40 мм. Потрібні нижня та верхня панелі, а також чотири бічні стінки: для живлення/HDMI/AV, USB/Ethernet, microSD і GPIO. У верхній панелі є отвір для доступу до роз’ємів. У бічних стінках передбачені отвори для портів.

**Файли для різання й перевірки:**

- [DXF — усі шість деталей](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/prototype-cut-sheet.dxf)
- [PDF — усі деталі на одному аркуші A4, масштаб 1:1](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/a4-cut-layout.pdf)
- [PDF — шість окремих шаблонів A4, масштаб 1:1](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/a4-fit-templates.pdf)
- [SVG — нижня панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/bottom.svg)
- [SVG — верхня панель з отвором](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/top-open-gpio.svg)
- [SVG — стінка живлення/HDMI/AV](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/power-hdmi-av.svg)
- [SVG — стінка USB/Ethernet](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/usb-ethernet.svg)
- [SVG — стінка microSD](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/microsd-side.svg)
- [SVG — стінка GPIO](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/gpio-side.svg)
- [DXF пробного з’єднання](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/fit-coupon.dxf) · [PDF пробного з’єднання](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/fit-coupon.pdf) · [SVG пазів](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/fit-slots.svg) · [SVG зубця](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/Raspberry/V4/output/fit-tab.svg)

## 2. Екран Waveshare 5″

Потрібні лицьова, задня, верхня й нижня панелі та ліва й права стінки. Габарит лицьової панелі — 160 × 115 мм; отвір під металеву частину екрана — **121,7 × 80,6 мм**. Кольоровий край екрана має залишатися на лицьовому акрилі для кріплення двосторонньою стрічкою.

- [DXF — усі шість деталей](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/prototype-cut-sheet.dxf)
- [PDF — лицьова панель 1:1](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/front-panel-1to1.pdf)
- [PDF — шість шаблонів A4, масштаб 1:1](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/a4-fit-templates.pdf)
- [SVG — лицьова панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/front.svg)
- [SVG — задня панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/rear.svg)
- [SVG — верхня панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/top.svg)
- [SVG — нижня панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/bottom.svg)
- [SVG — ліва стінка](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/left.svg)
- [SVG — права стінка](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-5b/right.svg)

## 3. Екран Waveshare 7B

Також потрібно шість деталей: лицьова, задня, верхня й нижня панелі та дві бічні стінки. Габарит лицьової панелі — 224 × 140 мм; отвір під металеву частину екрана — **168,3 × 102,8 мм**. Кольоровий край залишається на акрилі для кріплення двосторонньою стрічкою.

- [DXF — усі шість деталей](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/prototype-cut-sheet.dxf)
- [PDF — лицьова панель 1:1](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/front-panel-1to1.pdf)
- [PDF — шість шаблонів A4, масштаб 1:1](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/a4-fit-templates.pdf)
- [SVG — лицьова панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/front.svg)
- [SVG — задня панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/rear.svg)
- [SVG — верхня панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/top.svg)
- [SVG — нижня панель](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/bottom.svg)
- [SVG — ліва стінка](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/left.svg)
- [SVG — права стінка](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/waveshare-7b/right.svg)

**Спільний пробний зразок з’єднання для корпусів екранів:** [DXF](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/fit-coupon/fit-coupon.dxf) · [PDF](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/fit-coupon/fit-coupon.pdf) · [SVG пазів](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/fit-coupon/slot-gauge.svg) · [SVG зубця](https://github.com/shaposhnikoff/esp32-s3-5-7-box-cases/blob/main/output/finger-joint/fit-coupon/tab-gauge.svg).

## Перед виготовленням повних комплектів

1. Роздрукувати PDF у масштабі 1:1 та прикласти реальні плати й екрани до паперових шаблонів.
2. Вирізати пробні з’єднання з тієї самої партії акрилу й перевірити посадку без надмірного зусилля.
3. Узгодити розміри й розташування отворів для кабелів. У корпусах екранів отвори для роз’ємів у бічних стінках поки **не передбачені**.
4. Після перевірки зробити один пробний комплект кожного корпусу; фінальний розкрій погодити за результатом примірки.
