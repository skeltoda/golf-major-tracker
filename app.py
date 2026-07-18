import streamlit as st
import pandas as pd
import json, os, requests, io
from datetime import datetime

st.set_page_config(page_title="Golf Major Tracker", page_icon="⛳", layout="wide")

# ── SUPABASE HELPERS ──────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def db_get(key):
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/app_data?key=eq.{key}&select=value",
            headers=HEADERS, timeout=5
        )
        data = r.json()
        if data:
            return json.loads(data[0]["value"])
        return None
    except:
        return None

def db_set(key, value):
    try:
        requests.patch(
            f"{SUPABASE_URL}/rest/v1/app_data?key=eq.{key}",
            headers=HEADERS,
            json={"value": json.dumps(value)},
            timeout=5
        )
    except:
        pass

PAR = 70
HEADER_IMG = "https://i.postimg.cc/RhN53Hrs/IMG-5175.jpg"

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

def fmt_par(score):
    if score == 0: return "E"
    return f"{score:+d}"

def show_header():
    st.markdown(f"""
    <div style="width:100%;margin-bottom:24px;border-radius:12px;overflow:hidden;max-height:200px">
        <img src="{HEADER_IMG}" style="width:100%;object-fit:cover;object-position:center 60%">
    </div>
    """, unsafe_allow_html=True)

# ── LOAD DATA FROM SUPABASE ───────────────────────────────────────────────────
tournament  = db_get("tournament") or {}
field       = db_get("field") or []
picks       = db_get("picks") or {}
scores      = db_get("scores") or {}
last_updated = db_get("last_updated") or {}
cut = db_get("cut") or {}

st.sidebar.title("⛳ Golf Major Tracker")
if tournament.get("tournament"):
    st.sidebar.markdown(f"**{tournament['tournament']}**")
    st.sidebar.markdown(f"{len(tournament.get('friends', []))} players · 16pt budget")

page = st.sidebar.radio("Navigate", ["📊 Leaderboard", "📝 Score Updates", "🏆 Setup", "⛳ Field & Points", "👥 Friend Picks"])

# ── LEADERBOARD ───────────────────────────────────────────────────────────────
if page == "📊 Leaderboard":
    show_header()
    st.title("📊 Leaderboard")
    if not picks:
        st.warning("No picks entered yet.")
    else:
        if last_updated.get("time"):
            updated_time = datetime.strptime(last_updated["time"], "%Y-%m-%d %H:%M:%S")
            diff = datetime.utcnow() - updated_time
            mins = int(diff.total_seconds() // 60)
            if mins < 1:
                time_str = "just now"
            elif mins < 60:
                time_str = f"{mins} minutes ago"
            else:
                hours = mins // 60
                time_str = f"{hours}h {mins % 60}m ago"
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};border-radius:12px;padding:14px 18px;margin-bottom:10px">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;flex-wrap:wrap">
                    <span style="font-size:22px">{pos}</span>
                    <span style="font-size:18px;font-weight:600;{name_style}">{r['friend']}</span>
                    <span style="font-size:18px;font-weight:700;color:{score_color}">{r['par_label']}</span>
                    {elim_badge}
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:6px">{picks_html}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#FEF3C7;border:1px solid #F59E0B;border-radius:10px;padding:12px 16px;margin-bottom:16px">
                <p style="margin:0;font-size:14px;font-weight:700;color:#92400E">⏱️ Scores not yet updated</p>
                <p style="margin:4px 0 0;font-size:13px;color:#92400E">Go to <b>📝 Score Updates</b> in the left sidebar to enter the latest scores.</p>
            </div>
            """, unsafe_allow_html=True)

        st.caption(f"Royal Birkdale · Par {PAR} · ⭐ = counting · ☆ = not counting · all scores relative to par")

        medals = ["🥇", "🥈", "🥉"]
        results = []
        for friend in tournament.get("friends", []):
            fp = picks.get(friend, [])
            pick_scores = [(n, int(scores.get(n, 0)), cut.get(n, False)) for n in fp]
            active = [(n, s) for n, s, mc in pick_scores if not mc]
            active.sort(key=lambda x: x[1])
            eliminated = len(active) < 2
            if not eliminated:
                contributing = [active[0][0], active[1][0]]
                combined_par = active[0][1] + active[1][1]
                par_label = f"{combined_par:+d}" if combined_par != 0 else "E"
            else:
                contributing = []
                combined_par = 9999
                par_label = "N/A"
            results.append({
                "friend": friend,
                "par_label": par_label,
                "combined_par": combined_par,
                "pick_scores": pick_scores,
                "contributing": contributing,
                "eliminated": eliminated,
                "active_count": len(active),
            })

        results.sort(key=lambda x: (1 if x["eliminated"] else 0, x["combined_par"]))

        active_pos = 0
        for r in results:
            if r["eliminated"]:
                pos = "💀"
                bg = "#FFF1F1"
                border = "#FCA5A5"
            else:
                pos = medals[active_pos] if active_pos < 3 else f"{active_pos + 1}."
                bg = "#F0FDF4" if active_pos == 0 else "#FAFAFA"
                border = "#E2E8F0"
                active_pos += 1

            name_style = "text-decoration:line-through;color:#94A3B8;" if r["eliminated"] else "color:#0F172A;"
            elim_badge = '<span style="background:#FEE2E2;color:#991B1B;font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;margin-left:8px">ELIMINATED — fewer than 2 active players</span>' if r["eliminated"] else ""
            score_color = "#94A3B8" if r["eliminated"] else ("#16A34A" if r["combined_par"] < 0 else "#DC2626" if r["combined_par"] > 0 else "#0F172A")

            picks_html = ""
            for n, s, mc in r["pick_scores"]:
                if mc:
                    picks_html += f'<span style="background:#FEE2E2;color:#94A3B8;padding:4px 10px;border-radius:20px;font-size:12px;text-decoration:line-through">✂️ {n} (CUT)</span>'
                elif n in r["contributing"]:
                    picks_html += f'<span style="background:#D1FAE5;color:#065F46;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:600">⭐ {n} ({fmt_par(s)})</span>'
                else:
                    picks_html += f'<span style="background:#F1F5F9;color:#94A3B8;padding:4px 10px;border-radius:20px;font-size:12px">☆ {n} ({fmt_par(s)})</span>'

            st.markdown(f"""<div style="background:#FEF3C7;border:1px solid #F59E0B;border-radius:10px;padding:12px 16px;margin-bottom:16px">
                <p style="margin:0;font-size:14px;font-weight:700;color:#92400E">⏱️ Scores last updated: {time_str}</p>
                <p style="margin:4px 0 0;font-size:13px;color:#92400E">To refresh the leaderboard, go to <b>📝 Score Updates</b> in the left sidebar and confirm the latest scores.</p>
            </div>""", unsafe_allow_html=True)
        st.divider()
# ── SCORE UPDATES ─────────────────────────────────────────────────────────────
elif page == "📝 Score Updates":
    show_header()
    st.title("📝 Score Updates")
    st.caption("Update scores here — leaderboard updates immediately")
    st.markdown("📺 **Live scores:** [theopen.com/leaderboard](https://www.theopen.com/leaderboard)")
    st.divider()

    if not picks:
        st.warning("No picks entered yet.")
    else:
        cut = db_get("cut") or {}
        picked = sorted(set(n for p in picks.values() for n in p))
        st.subheader(f"{len(picked)} players in the competition")

        with st.form("score_update_form"):
            new_s = {}
            cols = st.columns(3)
            for i, name in enumerate(picked):
                with cols[i % 3]:
                    current = int(scores.get(name, 0))
                    new_s[name] = st.number_input(
                        f"{name}  ({fmt_par(current)})",
                        value=current,
                        min_value=-30,
                        max_value=30,
                        key=f"su_{name}"
                    )
                    cut[name] = st.checkbox("❌ Missed cut", value=cut.get(name, False), key=f"cut_{name}")

            st.write("")
            c1, c2 = st.columns(2)
            with c1:
                save_btn = st.form_submit_button("💾 Save & Update Leaderboard", type="primary", use_container_width=True)
            with c2:
                confirm_btn = st.form_submit_button("✅ No Changes", use_container_width=True)

            if save_btn:
                db_set("scores", new_s)
                db_set("cut", cut)
                db_set("last_updated", {"time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")})
                st.success("✅ Scores saved! Leaderboard updated.")
                st.rerun()

            if confirm_btn:
                db_set("last_updated", {"time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")})
                st.success("✅ Confirmed — no changes.")
                st.rerun()

# ── SETUP ─────────────────────────────────────────────────────────────────────
elif page == "🏆 Setup":
    show_header()
    st.title("🏆 Tournament Setup")
    pin = st.text_input("Enter admin PIN", type="password")
    if pin != st.secrets["ADMIN_PIN"]:
        st.warning("Admin access only.")
        st.stop()
    name = st.text_input("Tournament name", value=tournament.get("tournament", "The 154th Open"))
    friends_text = st.text_area("Friends — one per line", value="\n".join(tournament.get("friends", [])))
    if st.button("Save", type="primary"):
        if name and friends_text.strip():
            friends = [f.strip() for f in friends_text.strip().split("\n") if f.strip()]
            db_set("tournament", {"tournament": name, "friends": friends})
            st.success(f"Saved! {len(friends)} players.")
            st.rerun()

# ── FIELD & POINTS ─────────────────────────────────────────────────────────────
elif page == "⛳ Field & Points":
    show_header()
    st.title("⛳ Field & Points")
    pin = st.text_input("Enter admin PIN", type="password")
    if pin != st.secrets["ADMIN_PIN"]:
        st.warning("Admin access only.")
        st.stop()
    if not field:
        st.info(f"Ready to load {len(FIELD_CLEAN)} players with points from bookmaker odds.")
        if st.button("📥 Load field", type="primary"):
            db_set("field", FIELD_CLEAN)
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
            with c1: selected = st.selectbox("Player", [p["name"] for p in field])
            with c2: new_pts = st.number_input("Points", 1, 10, 1)
            with c3:
                st.write("")
                st.write("")
                submitted = st.form_submit_button("Update")
            if submitted:
                for p in field:
                    if p["name"] == selected:
                        p["points"] = new_pts
                db_set("field", field)
                st.success(f"Updated {selected} to {new_pts} pts")
                st.rerun()
        st.divider()
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ Reset field"):
            db_set("field", [])
            st.rerun()

# ── FRIEND PICKS ──────────────────────────────────────────────────────────────
elif page == "👥 Friend Picks":
    show_header()
    st.title("👥 Friend Picks")
    pin = st.text_input("Enter admin PIN", type="password")
    if pin != st.secrets["ADMIN_PIN"]:
        st.warning("Admin access only.")
        st.stop()
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
                db_set("picks", picks)
                st.success(f"Saved {len(new_picks)} picks for {friend} ({total} pts)")