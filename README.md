# SafeRoute
Source code for Safe Route.

# v0.2 (12/18/19)
![alt text](https://raw.githubusercontent.com/hty8/SafeRoute/master/SafeRouteDemo.png)
Bu proje, Boğaziçi Üniversitesi'ndeki MIS 463 kodlu Decision Support Systems dersi kapsamında hazırlanmıştır ve Chicago şehrinde değerli yük taşıyan firmalar için tasarlanmış bir uygulamayı içermektedir. 
Kullanıcılar bu uygulama sayesinde varış destinasyonlarına giden rotalar içinden en güvenli olanlarını bulabilir.

Uygulamayı geliştirirken,
Django,
Google Maps API,
Chicago City Data API,
PostGIS,
Postgresql
gibi teknolojiler kullanılmıştır.

Kullanıcı başlangıç ve varış noktalarını seçtiğinde uygulama Google Maps API'ına istek yaparak üç alternatif yol bilgisi almakta, daha sonra ise [Chicago Crime Data](https://data.cityofchicago.org/Public-Safety/Crimes-2019/w98m-zvie)'yı kullanarak bu yolların güvenlik skorlarını hesaplayıp kullanıcıya sunmaktadır.

# Servisin Kurulumu
Kurulum için Docker, makinenizde kurulu olmalıdır. Docker kullanılmadan kurulum için requirements.txt içerisinde lib'ler python 3 için kurulmalıdır. Docker ile kurulum için makinenin terminalinde sırası ile aşağıdakiler yapılmalıdır;

Proje lokale çekilir
```
git clone git@github.com:hty8/SafeRoute.git
```
Projeye gidilir
```
cd SafeRoute
```
Servisi başlatmak için aşağıdaki komut çalıştırılır.
```
docker-compose up --build -d
```
Servis ayağa kalktıktan sonra database içine crime datasının eklenmesi için aşağıdaki komutlar sırasıyla çalıştırılmalıdır.
```
docker exec -it saferoute_db_1 bash
```
```
shp2pgsql -I -s 4326 scores.shp scores | psql -d postgres -U postgres -h db -p 5432
```
```
exit
```
# Servisin Çalıştırılması

Servisi çalıştırmak için aşağıdaki komutlar sırasıyla çalıştırılmalıdır.(eğer farklı bir porttan çıkılacak ise docker üzerinden ilgili port dışarıya açılmalıdır.)
```
docker exec -it saferoute_app_1 bash
```
```
python manage.py runserver 0.0.0.0:8000
```

Browserınızda http://0.0.0.0:8000 adresine giderek uygulamaya erişebilirsiniz.
