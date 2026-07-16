import streamlit as st
import pandas as pd
import json, os, requests

st.set_page_config(page_title="Golf Major Tracker", page_icon="⛳", layout="wide")

def load(file, default):
    if os.path.exists(file):
        with open(file) as f: return json.load(f)
    return default

def save(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=2)

PAR = 70

OPEN_FIELD = [
    {"name":"Scottie Scheffler","points":10},
    {"name":"Rory McIlroy","points":10},
    {"name":"Tommy Fleetwood","points":8},
    {"name":"Matt Fitzpatrick","points":8},
    {"name":"Jon Rahm","points":7},
    {"name":"Viktor Hovland","points":7},
    {"name":"Xander Schauffele","points":7},
    {"name":"Chris Gotterup","points":7},
    {"name":"Wyndham Clark","points":6},
    {"name":"Tyrrell Hatton","points":6},
    {"name":"Collin Morikawa","points":6},
    {"name":"Ludvig Aberg","points":6},
    {"name":"Min Woo Lee","points":6},
    {"name":"Robert MacIntyre","points":6},
    {"name":"Shane Lowry","points":6},
    {"name":"Brooks Koepka","points":6},
    {"name":"Cameron Smith","points":5},
    {"name":"Justin Rose","points":5},
    {"name":"Sam Burns","points":5},
    {"name":"Justin Thomas","points":5},
    {"name":"Patrick Cantlay","points":5},
    {"name":"Bryson DeChambeau","points":5},
    {"name":"Jason Day","points":4},
    {"name":"Aaron Rai","points":4},
    {"name":"Sahith Theegala","points":4},
    {"name":"Max Homa","points":4},
    {"name":"Tom Kim","points":3},
    {"name":"Sepp Straka","points":3},
    {"name":"Adam Scott","points":3},
    {"name":"Rasmus Hojgaard","points":3},
    {"name":"Nicolai Hojgaard","points":3},
    {"name":"Hideki Matsuyama","points":3},
    {"name":"Jordan Spieth","points":2},
    {"name":"Si Woo Kim","points":2},
    {"name":"Harris English","points":2},
    {"name":"Russell Henley","points":2},
    {"name":"Patrick Reed","points":2},
    {"name":"Akshay Bhatia","points":2},
    {"name":"Alex Noren","points":2},
    {"name":"Billy Horschel","points":1},
    {"name":"Daniel Berger","points":1},
    {"name":"Eugenio Chacarra","points":1},
    {"name":"Haotong Li","points":1},
    {"name":"Matt McCarty","points":1},
    {"name":"Max Greyserman","points":1},
    {"name":"Nico Echavarria","points":1},
    {"name":"Cameron Young","points":1},
    {"name":"JT Poston","points":1},
    {"name":"Laurie Canter","points":1},
    {"name":"David Puig","points":1},
    {"name":"Eric Cole","points":1},
    {"name":"Kazuma Kobori","points":1},
    {"name":"JJ Spaun","points":1},
    {"name":"Andrew Novak","points":1},
    {"name":"Tom McKibbin","points":1},
    {"name":"Ryo Hisatsune","points":1},
    {"name":"Bud Cauley","points":1},
    {"name":"Harry Hall","points":1},
    {"name":"Kristoffer Reitan","points":1},
    {"name":"Joakim Lagergren","points":1},
    {"name":"Naoyuki Kataoka","points":1},
    {"name":"Adrien Saddier","points":1},
    {"name":"Jacob Bridgeman","points":1},
    {"name":"Kota Kaneko","points":1},
    {"name":"Casey Jarvis","points":1},
    {"name":"Jiho Yang","points":1},
    {"name":"Alistair Docherty","points":1},
    {"name":"Caleb Surratt","points":1},
    {"name":"Stuart Grehan","points":1},
    {"name":"Pierceson Coody","points":1},
    {"name":"Sam Stevens","points":1},
    {"name":"Peter Uihlein","points":1},
    {"name":"Tom Sloman","points":1},
    {"name":"Michael Thorbjornsen","points":1},
    {"name":"Ben Griffin","points":1},
    {"name":"Daniel Hillier","points":1},
    {"name":"Jeongwoo Ham","points":1},
    {"name":"Mason Howell","points":1},
    {"name":"Cameron John","points":1},
    {"name":"Kazuki Higa","points":1},
    {"name":"Joe Dean","points":1},
    {"name":"Dan Bradbury","points":1},
    {"name":"Daniel Brown","points":1},
    {"name":"Angel Ayora","points":1},
    {"name":"Tiger Christensen","points":1},
    {"name":"Shaun Norris","points":1},
    {"name":"Jayden Schaper","points":1},
    {"name":"Marcus Plunkett","points":1},
    {"name":"Ren Yonezawa","points":1},
    {"name":"Jackson Suber","points":1},
    {"name":"Alex Smalley","points":1},
    {"name":"Maverick McNealy","points":1},
    {"name":"Alex Fitzpatrick","points":1},
    {"name":"Aldrich Potgieter","points":1},
    {"name":"Jose Luis Ballester Barrio","points":1},
    {"name":"Martin Couvra","points":1},
    {"name":"Johnny Keefer","points":1},
    {"name":"Brian Harman","points":1},
    {"name":"Ryan Gerard","points":1},
    {"name":"Lev Grinberg","points":1},
    {"name":"Bernd Wiesberger","points":1},
    {"name":"Henrik Stenson","points":1},
    {"name":"Jake Knapp","points":1},
    {"name":"Keita Nakajima","points":1},
    {"name":"Jack Buchanan","points":1},
    {"name":"Jack McDonald","points":1},
    {"name":"David Howard","points":1},
    {"name":"Michael Hollick","points":1},
    {"name":"Rasmus Neergaard Petersen","points":1},
    {"name":"Scott Vincent","points":1},
    {"name":"Matt Wallace","points":1},
    {"name":"Kurt Kitayama","points":1},
    {"name":"Joaquin Niemann","points":1},
    {"name":"Gary Woodland","points":1},
    {"name":"Sungjae Im","points":1},
    {"name":"Keith Mitchell","points":1},
    {"name":"Corey Conners","points":1},
    {"name":"Andy Sullivan","points":1},
    {"name":"Victor Perez","points":1},
    {"name":"Nick Taylor","points":1},
    {"name":"Ryan Fox","points":1},
    {"name":"Sam Bairstow","points":1},
    {"name":"Matthew Jordan","points":1},
    {"name":"Padraig Harrington","points":1},
    {"name":"Francesco Molinari","points":1},
    {"name":"Rickie Fowler","points":1},
    {"name":"Fifa Laopakdee","points":1},
    {"name":"Antoine Rozner","points":1},
    {"name":"Francesco Laporta","points":1},
    {"name":"Michael Kim","points":1},
    {"name":"Jesper Svensson","points":1},
    {"name":"Sami Valimaki","points":1},
    {"name":"Austen Truslow","points":1},
    {"name":"Tim Wiedemeyer","points":1},
    {"name":"MJ Daffue","points":1},
    {"name":"Michael Brennan","points":1},
    {"name":"Travis Smyth","points":1},
    {"name":"James Nicholas","points":1},
    {"name":"Mateo Pulcini","points":1},
    {"name":"Nevill Ruiter","points":1},
    {"name":"Frederic Lacroix","points":1},
    {"name":"Keegan Bradley","points":1},
    {"name":"Matthew Baldwin","points":1},
    {"name":"Matthew Southgate","points":1},
    {"name":"Hennie Du Plessis","points":1},
    {"name":"Darren Clarke","points":1},
    {"name":"Stewart Cink","points":1},
    {"name":"David Duval","points":1},
    {"name":"Baard Bjoernevik Skogen","points":1},
    {"name":"Alejandro De Castro Piera","points":1},
    {"name":"Jordan Smith","points":1},
]

seen = set()
FIELD_CLEAN = []
for p in OPEN_FIELD:
    if p["name"] not in seen:
        seen.add(p["name"])
        FIELD_CLEAN.append(p)

def fmt_par(strokes):
    diff = strokes - PAR
    if diff == 0: return "E"
    return f"{diff:+d}"

def fetch_live_scores():
    try:
        api_key = st.secrets["GOLF_API_KEY"]
        headers = {"x-apisports-key": api_key}
        url = "https://v1.golf.api-sports.io/tournaments?season=2026"
        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()
        tournament_id = None
        for t in data.get("response", []):
            name = t.get("name", "").lower()
            if "open" in name and "championship" in name:
                tournament_id = t.get("id")
                break
        if not tournament_id:
            return {}, "Could not find The Open"
        lb_url = f"https://v1.golf.api-sports.io/leaderboards?tournament={tournament_id}&season=2026"
        r2 = requests.get(lb_url, headers=headers, timeout=5)
        lb_data = r2.json()
        scores = {}
        for player in lb_data.get("response", []):
            name = player.get("player", {}).get("name", "")
            total = player.get("scores", {}).get("total", None)
            if name and total is not None:
                strokes = PAR * 4 + int(total)
                scores[name] = strokes
        if scores:
            return scores, None
        return {}, "No scores available yet"
    except Exception as e:
        return {}, str(e)

tournament = load("tournament.json", {})
field = load("field.json", [])
picks = load("picks.json", {})
scores = load("scores.json", {})

st.sidebar.title("⛳ Golf Major Tracker")
if tournament.get("tournament"):
    st.sidebar.markdown(f"**{tournament['tournament']}**")
    st.sidebar.markdown(f"{len(tournament.get('friends', []))} players · 16pt budget")

page = st.sidebar.radio("Navigate", ["🏆 Setup", "⛳ Field & Points", "👥 Friend Picks", "📊 Leaderboard", "🏌️ Live Leaderboard"])

if page == "🏆 Setup":
    st.title("🏆 Tournament Setup")
    name = st.text_input("Tournament name", value=tournament.get("tournament", "The 154th Open"))
    friends_text = st.text_area("Friends — one per line", value="\n".join(tournament.get("friends", [])))
    if st.button("Save", type="primary"):
        if name and friends_text.strip():
            friends = [f.strip() for f in friends_text.strip().split("\n") if f.strip()]
            save("tournament.json", {"tournament": name, "friends": friends})
            st.success(f"Saved! {len(friends)} players.")
            st.rerun()

elif page == "⛳ Field & Points":
    st.title("⛳ Field & Points")
    if not field:
        st.info(f"Ready to load {len(FIELD_CLEAN)} players with points from bookmaker odds.")
        if st.button("📥 Load field", type="primary"):
            save("field.json", FIELD_CLEAN)
            st.success("Field loaded!")
            st.rerun()
    else:
        st.success(f"✅ {len(field)} players loaded")
        df = pd.DataFrame(field).sort_values("points", ascending=False).reset_index(drop=True)
        df.index += 1
        pts_counts = df["points"].value_counts().sort_index(ascending=False).head(8)
        cols = st.columns(len(pts_counts))
        for i, (pts, count) in enumerate(pts_counts.items()):
            cols[i].metric(f"{pts} pts", f"{count} players")
        st.divider()
        st.subheader("Override a player's points")
        with st.form("override"):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                selected = st.selectbox("Player", [p["name"] for p in field])
            with c2:
                new_pts = st.number_input("Points", 1, 10, 1)
            with c3:
                st.write("")
                st.write("")
                submitted = st.form_submit_button("Update")
            if submitted:
                for p in field:
                    if p["name"] == selected:
                        p["points"] = new_pts
                save("field.json", field)
                st.success(f"Updated {selected} to {new_pts} pts")
                st.rerun()
        st.divider()
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ Reset field"):
            save("field.json", [])
            st.rerun()

elif page == "👥 Friend Picks":
    st.title("👥 Friend Picks")
    BUDGET = 16
    if not tournament.get("friends"):
        st.warning("Add friends in Setup first.")
    elif not field:
        st.warning("Load the field in Field & Points first.")
    else:
        friend = st.selectbox("Select friend", tournament["friends"])
        current = picks.get(friend, [])
        used = sum(p["points"] for p in field if p["name"] in current)
        remaining = BUDGET - used
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Budget", f"{BUDGET} pts")
        c2.metric("Used", f"{used} pts")
        c3.metric("Remaining", f"{remaining} pts")
        c4.metric("Picks", len(current))
        if len(current) >= 2:
            st.success(f"✅ Valid — {len(current)} golfers, {used} pts used")
        st.divider()
        search = st.text_input("🔍 Search player")
        new_picks = []
        field_sorted = sorted(field, key=lambda x: x["points"], reverse=True)
        filtered = [g for g in field_sorted if search.lower() in g["name"].lower()] if search else field_sorted
        for g in filtered:
            checked = g["name"] in current
            new_total = used - (g["points"] if checked else 0) + (0 if checked else g["points"])
            disabled = (new_total > BUDGET) and not checked
            if st.checkbox(f"{g['name']}  —  {g['points']} pts", value=checked,
                           disabled=disabled, key=f"{friend}_{g['name']}"):
                new_picks.append(g["name"])
        if st.button("💾 Save picks", type="primary"):
            total = sum(p["points"] for p in field if p["name"] in new_picks)
            if len(new_picks) < 2:
                st.error("Must pick at least 2 golfers.")
            elif total > BUDGET:
                st.error(f"Over budget — {total}/{BUDGET} pts.")
            else:
                picks[friend] = new_picks
                save("picks.json", picks)
                st.success(f"Saved {len(new_picks)} picks for {friend} ({total} pts)")

elif page == "📊 Leaderboard":
    st.title("📊 Leaderboard")
    if not picks:
        st.warning("No picks entered yet.")
    else:
        st.caption(f"Royal Birkdale · Par {PAR} · Live scores update when tournament starts 17 July")
        if st.button("🔄 Refresh"):
            st.rerun()
        live, error = fetch_live_scores()
        if live:
            scores.update(live)
            save("scores.json", scores)
            st.success(f"✅ Live scores — {len(live)} players")
        else:
            st.info(f"⏳ {error or 'Awaiting tournament start'}")
            with st.expander("📝 Enter scores manually (total strokes e.g. 68)"):
                picked = sorted(set(n for p in picks.values() for n in p))
                with st.form("scores_form"):
                    cols = st.columns(3)
                    new_s = {}
                    for i, name in enumerate(picked):
                        with cols[i % 3]:
                            new_s[name] = st.number_input(
                                name, value=int(scores.get(name, 0)),
                                min_value=0, max_value=400)
                    if st.form_submit_button("Update scores"):
                        save("scores.json", new_s)
                        scores = new_s
                        st.success("Updated!")
                        st.rerun()
        medals = ["🥇", "🥈", "🥉"]
        results = []
        for friend in tournament.get("friends", []):
            fp = picks.get(friend, [])
            scored = [(n, int(scores.get(n, PAR))) for n in fp]
            scored.sort(key=lambda x: x[1])
            if len(scored) >= 2:
                best = scored[:2]
                combined_strokes = sum(s for _, s in best)
                combined_par = combined_strokes - (PAR * 2)
                par_label = f"{combined_par:+d}" if combined_par != 0 else "E"
                label = f"{best[0][0]} ({fmt_par(best[0][1])}) + {best[1][0]} ({fmt_par(best[1][1])})"
            else:
                combined_par = 9999
                par_label = "-"
                label = "Awaiting scores"
            results.append({
                "Friend": friend,
                "Best 2 golfers": label,
                "Score": par_label,
                "Sort": combined_par,
                "All picks": ", ".join(fp)
            })
        results.sort(key=lambda x: x["Sort"])
        for i, r in enumerate(results):
            r["Pos"] = medals[i] if i < 3 else str(i + 1)
        df = pd.DataFrame(results)[["Pos", "Friend", "Best 2 golfers", "Score", "All picks"]]
        st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "🏌️ Live Leaderboard":
    st.title("🏌️ The 154th Open — Live Leaderboard")
    st.caption("Royal Birkdale · Par 70 · Auto-updates during the tournament")

    if st.button("🔄 Refresh"):
        st.rerun()

    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/golf/leaderboard?league=pga"
        r = requests.get(url, timeout=5)
        data = r.json()

        leaderboard = []
        found = False

        for event in data.get("events", []):
            ename = event.get("name", "").lower()
            if "open" in ename or "birkdale" in ename:
                found = True
                for comp in event.get("competitions", []):
                    for p in comp.get("competitors", []):
                        name = p.get("athlete", {}).get("displayName", "")
                        pos = p.get("status", {}).get("position", {}).get("displayName", "-")
                        score = p.get("score", {}).get("displayValue", "-")
                        today = p.get("linescores", [{}])[-1].get("displayValue", "-") if p.get("linescores") else "-"
                        thru = p.get("status", {}).get("thru", {}).get("displayValue", "-")
                        made_cut = p.get("status", {}).get("type", {}).get("id", "") != "5"
                        if name:
                            leaderboard.append({
                                "Pos": pos,
                                "Player": name,
                                "Score": score,
                                "Today": today,
                                "Thru": thru,
                            })

        if leaderboard:
            df = pd.DataFrame(leaderboard)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("⏳ Tournament leaderboard not available yet — check back Thursday 17 July when play begins.")

    except Exception as e:
        st.info("⏳ Tournament not yet started — leaderboard will appear here once play begins on Thursday 17 July.")