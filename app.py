medals = ["🥇","🥈","🥉"]
        results = []
        for friend in tournament.get("friends", []):
            fp = picks.get(friend, [])
            scored = [(n, int(scores.get(n,0))) for n in fp if scores.get(n,0) > 0]
            scored.sort(key=lambda x: x[1])
            if len(scored) >= 2:
                best = scored[:2]
                combined = sum(s for _,s in best)
                label = f"{best[0][0]} ({best[0][1]}) + {best[1][0]} ({best[1][1]})"
            else:
                combined = 9999
                label = "Awaiting scores"
            results.append({
                "Friend": friend,
                "Best 2 golfers": label,
                "Combined strokes": combined,
                "All picks": ", ".join(fp)
            })

        results.sort(key=lambda x: x["Combined strokes"])
        for i, r in enumerate(results):
            r["Pos"] = medals[i] if i < 3 else str(i+1)

        df = pd.DataFrame(results)[["Pos","Friend","Best 2 golfers","Combined strokes","All picks"]]
        df["Combined strokes"] = df["Combined strokes"].replace(9999, "-")
        st.dataframe(df, use_container_width=True, hide_index=True)