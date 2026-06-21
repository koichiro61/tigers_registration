# tigers_registration
阪神タイガース公式サイトの一軍登録抹消履歴を読み込んで各行を各選手の出場登録期間選手を表示するガントチャートを作成する。<br/>
公式ページ・一軍登録抹消履歴 https://hanshintigers.jp/game/regist/history.html

makecsv.py
一軍登録抹消履歴ページを scrapeして tigers_reg_history.csv を出力<br/>
サンプル　https://github.com/koichiro61/tigers_registration/blob/dd6de4f1bc4b23f33f4e8aa2dd041aa41cdc4775/tigers_reg_history.csv

gannt.py
tigers_reg_history.csv を読み込んでガントチャート tigers_gantt.png を生成
![サンプル](https://github.com/koichiro61/tigers_registration/blob/dd6de4f1bc4b23f33f4e8aa2dd041aa41cdc4775/tigers_gantt.png "サンプル")

動作検証環境
iPadOS 26.5 / a-shell 2.0.2 / Python Python 3.13.1+

