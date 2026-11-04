"""Post-hoc sensitivity (not pre-registered): repeat the H1, H2 (item-clustered GLM) and H3 contrasts
without calls in which Claude Code made an in-call schema correction (num_turns > 2).
Writes results/sensitivity_excluding_extra_turn_calls.json."""
import sys, json, collections
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import pandas as pd, analyse
R = str(analyse.RESULTS) + '/'
turns = {}
c = collections.Counter()
for l in open(R + 'monitor_raw.jsonl'):
    r = json.loads(l); t = r['attempts'][-1]['num_turns']; turns[r['call_id']] = t
    c[(analyse.MON[r['monitor']], r['condition'], t > 2)] += 1
for k in sorted(c):
    if k[2]: print('extra turns', k[:2], c[k], 'of', c[(k[0], k[1], False)] + c[k])
df = pd.read_csv(R + 'judgments.csv')
df['extra'] = df.call_id.map(turns) > 2
d = df[~df.extra]
out = {}
for mon in analyse.MONS:
    dm = d[d.monitor == mon]
    h1 = analyse.contrast(dm[dm.experiment == 'exp1'], 'P2.5', 'P50', analyse.EXP1, 'batch_key')['term']
    h3 = analyse.contrast(dm[dm.condition.isin(['P2.5', 'R-cal'])], 'R-cal', 'P2.5', ['P2.5', 'R-cal'], 'batch_key')['term']
    e2 = dm[(dm.experiment == 'exp2') & (dm.backdoored == 1)]
    h2 = analyse.glm_cluster(e2, "flag ~ C(condition, Treatment('S50'))", 'problem_id')['coefs']["C(condition, Treatment('S50'))[T.S1]"]
    print(mon, 'H1 OR %.2f p=%.4f | H2 (GLM) OR %.2f p=%.4f | H3 OR %.2f p=%.4f' % (h1['OR'], h1['p'], h2['OR'], h2['p'], h3['OR'], h3['p']))
    for cond in ['P50', 'P2.5', 'R-cal']:
        x = dm[(dm.condition == cond) & (dm.backdoored == 1)]
        print('   ', cond, 'H = %.3f (n=%d)' % (x.flag.mean(), len(x)))
    out[mon] = {'H1': h1, 'H2_glm': h2, 'H3': h3}
json.dump({'note': 'post-hoc sensitivity: calls with num_turns > 2 (in-call schema correction by Claude Code) excluded',
           'extra_turn_calls': {f'{k[0]}|{k[1]}': v for k, v in c.items() if k[2]}, 'results': out},
          open(R + 'sensitivity_excluding_extra_turn_calls.json', 'w'), indent=1)
