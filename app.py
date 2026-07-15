import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Golf Major Tracker", page_icon="⛳", layout="wide")

def load(file, default):
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
    return default

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

tournament = load("tournament.json", {})
field      = load("field.json", [])
picks      = load("picks.json", {})
scores     = load("scores.json", {})

st.sidebar.title("⛳ Golf Major Tracker")
if tournament.get("tournament"):
    st.sidebar.markdown(f"**{tournament['tournament']}**")
    st.sidebar.markdown(f"{len(tournament.get('friends', []))} players")

page = st.sidebar.radio("", ["🏆 Setup", "⛳ Field & Points", "👥 Friend Picks", "📊 Leaderboard"])

# ── SETUP ────────────────────────────────────────────────────────────────────
if page == "🏆 Setup":
    st.title("🏆 Tournament Setup")
    name = st.text_input("Tournament name", value=tournament.get("tournament", ""))
    friends_text = st.text_area("Friends — one per line", value="\n".join(tournament.get("friends", [])))
    if st.button("Save", type="primary"):
        if name and friends_text.strip():
            friends = [f.strip() for f in friends_text.strip().split("\n") if f.strip()]
            save("tournament.json", {"tournament": name, "friends": friends})
            st.success(f"Saved! {len(friends)} players.")
            st.rerun()

# ── FIELD & POINTS ────────────────────────────────────────────────────────────
elif page == "⛳ Field & Points":
    st.title("⛳ Field & Points")
    st.caption("Add each golfer and assign points 1–10. Higher points = tournament favourite.")

    with st.form("add_golfer", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1: name = st.text_input("Golfer name")
        with c2: pts  = st.number_input("Points", 1, 10, 5)
        with c3:
            st.write("")
            st.write("")
            add = st.form_submit_button("Add")
        if add and name:
            if name in [g["name"] for g in field]:
                st.error("Already in field")
            else:
                field.append({"name": name, "points": pts})
                save("field.json", field)
                st.rerun()

    if field:
        st.subheader(f"{len(field)} golfers in the field")
        df = pd.DataFrame(field).sort_values("points", ascending=False).reset_index(drop=True)
        df.index += 1
        st.dataframe(df, use_container_width=True)
        if st.button("Clear entire field"):
            save("field.json", [])
            st.rerun()
    else:
        st.info("No golfers added yet.")

# ── FRIEND PICKS ──────────────────────────────────────────────────────────────
elif page == "👥 Friend Picks":
    st.title("👥 Friend Picks")
    BUDGET = 16

    if not tournament.get("friends"):
        st.warning("Add friends in Setup first.")
    elif not field:
        st.warning("Add golfers in Field & Points first.")
    else:
        friend = st.selectbox("Select friend", tournament["friends"])
        current = picks.get(friend, [])
        used    = sum(g["points"] for g in field if g["name"] in current)

        c1, c2, c3 = st.columns(3)
        c1.metric("Budget",    f"{BUDGET} pts")
        c2.metric("Used",      f"{used} pts")
        c3.metric("Remaining", f"{BUDGET - used} pts")

        st.divider()
        new_picks = []
        for g in sorted(field, key=lambda x: x["points"], reverse=True):
            checked   = g["name"] in current
            new_total = used - (g["points"] if checked else 0) + (0 if checked else g["points"])
            disabled  = (new_total > BUDGET) and not checked
            if st.checkbox(f"{g['name']}  —  {g['points']} pts", value=checked,
                           disabled=disabled, key=f"{friend}_{g['name']}"):
                new_picks.append(g["name"])

        if st.button("Save picks", type="primary"):
            total = sum(g["points"] for g in field if g["name"] in new_picks)
            if len(new_picks) < 2:
                st.error("Must pick at least 2 golfers.")
            elif total > BUDGET:
                st.error(f"Over budget — {total}/{BUDGET} pts.")
            else:
                picks[friend] = new_picks
                save("picks.json", picks)
                st.success(f"Saved {len(new_picks)} picks for {friend} ({total} pts)")

# ── LEADERBOARD ───────────────────────────────────────────────────────────────
elif page == "📊 Leaderboard":
    st.title("📊 Leaderboard")

    if not picks:
        st.warning("No picks entered yet.")
    else:
        with st.expander("📝 Enter scores (admin only)"):
            picked = sorted(set(n for p in picks.values() for n in p))
            with st.form("scores"):
                cols  = st.columns(3)
                new_s = {}
                for i, name in enumerate(picked):
                    with cols[i % 3]:
                        new_s[name] = st.number_input(name, value=int(scores.get(name, 0)),
                                                       min_value=0, max_value=400)
                if st.form_submit_button("Update scores"):
                    save("scores.json", new_s)
                    scores = new_s
                    st.success("Scores updated!")
                    st.rerun()

        medals = ["🥇", "🥈", "🥉"]
        results = []
        for friend in tournament.get("friends", []):
            friend_picks = picks.get(friend, [])
            scored = [(n, int(scores[n])) for n in friend_picks if scores.get(n, 0) > 0]
            scored.sort(key=lambda x: x[1])
            if len(scored) >= 2:
                best     = scored[:2]
                combined = sum(s for _, s in best)
                label    = f"{best[0][0]} ({best[0][1]}) + {best[1][0]} ({best[1][1]})"
            else:
                combined = 9999
                label    = "Awaiting scores"
            results.append({"Friend": friend, "Best 2": label,
                             "Combined strokes": combined, "Picks": ", ".join(friend_picks)})

        results.sort(key=lambda x: x["Combined strokes"])
        for i, r in enumerate(results):
            r["Pos"] = medals[i] if i < 3 else str(i + 1)

        df = pd.DataFrame(results)[["Pos", "Friend", "Best 2", "Combined strokes", "Picks"]]
        df["Combined strokes"] = df["Combined strokes"].replace(9999, "-")
        st.dataframe(df, use_container_width=True, hide_index=True)