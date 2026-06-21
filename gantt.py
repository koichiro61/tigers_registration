import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import japanize_matplotlib


CSV_FILE = "tigers_reg_history.csv"
PNG_FILE = "tigers_gantt.png"


# ==========================
# CSV読み込み
# ==========================

df = pd.read_csv(CSV_FILE)


# ==========================
# 登録・抹消イベント化
# ==========================

# ==========================
# 登録・抹消イベント化
# ==========================

events = {}

for _, row in df.iterrows():

    date = pd.to_datetime(row["日付"])


    # 登録
    if pd.notna(row["登録_名前"]) and row["登録_名前"] != "":

        name = row["登録_名前"]

        events.setdefault(name, []).append(
            ("in", date)
        )


    # 抹消
    if pd.notna(row["抹消_名前"]) and row["抹消_名前"] != "":

        name = row["抹消_名前"]

        events.setdefault(name, []).append(
            ("out", date)
        )

# ==========================
# 登録期間へ変換
# ==========================

intervals = []

last_date = pd.to_datetime(df["日付"].dropna().max())


for player, ev in events.items():

    ev.sort(key=lambda x:x[1])

    start = None

    for kind, date in ev:

        if kind == "in":
            start = date

        elif kind == "out" and start:

            intervals.append(
                [
                    player,
                    start,
                    date
                ]
            )

            start = None


    # 現在登録中の場合
    if start:

        intervals.append(
            [
                player,
                start,
                last_date
            ]
        )


chart = pd.DataFrame(
    intervals,
    columns=[
        "選手",
        "開始",
        "終了"
    ]
)



# ==========================
# 表示順
# ==========================

players = (
    chart.groupby("選手")["開始"]
    .min()
    .sort_values()
    .index
    .tolist()
)



# ==========================
# 色設定
# 同じ選手＝同じ色
# ==========================

cmap = plt.cm.tab20


colors = {}

for i,p in enumerate(players):

    colors[p] = cmap(
        i % 20
    )



# ==========================
# ガントチャート描画
# ==========================

plt.figure(
    figsize=(14, max(8,len(players)*0.3))
)


for y, player in enumerate(players):

    rows = chart[
        chart["選手"] == player
    ]

    for _, r in rows.iterrows():

        plt.barh(
            y,
            (r["終了"] - r["開始"]).days + 1,
            left=mdates.date2num(r["開始"]),
            height=0.6,
            color=colors[player]
        )



plt.yticks(
    range(len(players)),
    players
)


plt.gca().invert_yaxis()


plt.gca().xaxis_date()


plt.gca().xaxis.set_major_locator(
    mdates.WeekdayLocator(interval=1)
)


plt.gca().xaxis.set_major_formatter(
    mdates.DateFormatter("%m/%d")
)


plt.xlabel("日付")

plt.title(
    "阪神 一軍登録期間 ガントチャート"
)
plt.grid(True,linestyle="--", alpha=0.6)

plt.tight_layout()


plt.savefig(
    PNG_FILE,
    dpi=200,
    bbox_inches="tight"
)


plt.close()


print(
    "作成完了:",
    PNG_FILE
)