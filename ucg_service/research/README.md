Research

Vertica каждый раз ломается при загрузке больших данных, не получилось проверить ее на больших данных

В итоге при 5000 записей в вертике и 1000000 в кликхаусе, вертика в 10 из 10 случаев показывала худшие показатели на чтение(0.04 vs 0.045) и запись (0.06 vs 0.07). Попробовал вставить в вертику меньше данных, чтобы проверить разницу на 1000 и 5000, разница есть, на 1000 записей, вертика быстрее. Судя по прогрессии, плохо понимаю как вертика может пережевывать большие данные.

Итог: Кликхаус мощь, а вертику видимо как то готовить еще сложно надо, нам бы что попроще -> Кликхаус наш кандидат
На кликхаус я нашел больше информации, подозреваю при ошибках в работе с ним, достаточно просто будет гуглить решения. Вертику наверное нужно использовать как готовое решение за деньги, может тогда она станет приятнее.


Архитектура Vertica
![alt text](https://www.vertica.com/docs/9.2.x/HTML/Content/Resources/Images/ConceptsGuide/cluster_storage.png)

Архитектура ClickHouse
![alt text](https://altinity.com/wp-content/uploads/2020/02/12dc1-clickhouse2bmulti-device2bstorage_cr.jpg)