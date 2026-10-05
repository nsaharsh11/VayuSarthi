# Validation comparison

**simulated; scenario-based**

Each cell is mean [95% percentile bootstrap CI] from paired scenarios.
Post-hoc v2 design corrections: v1 results were seen. The corrected rules were frozen before this rerun.
Stress settings and training-derived B1 interval are unchanged; neutral paired ages use its scale.
AOG includes grounded waiting and maintenance; healthy future-slot waiting is excluded.
Repair multipliers are assumed. Ties are retained. AOG is censored at the horizon.

## benign; horizon 40 days; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 12.63 [12.325, 12.97] | 2.925 [2.84, 3] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0.205 [0.129875, 0.29] | 0.05 [0.02, 0.080125] | 0 [0, 0] | 2.735 [2.67, 2.795] | 9.64 [9.375, 9.93] |
| B1 | 45.125 [41.8092, 48.4254] | 1.675 [1.56, 1.795] | 208.675 [202.009, 215.423] | 3.38 [3.135, 3.63] | 0 [0, 0] | 0 [0, 0] | 35.435 [32.0299, 38.7601] | 0 [0, 0] | 0 [0, 0] | 0.065 [0.025, 0.11] | 9.625 [9.49, 9.76] |
| B2-K0 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B2 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B3 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B4 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B4b | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.00166667 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.00166667 | 0 | 0 | 0 |
| B2-K0 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B2 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B3 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B4 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B4b | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |

B2: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B3: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4b: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.00166667 [0, 0.00416667]
B3/B4B share of differing weeks: 0.00166667 [0, 0.00416667]
B4/B4B share of differing weeks: 0.00166667 [0, 0.00416667]

## benign; horizon 40 days; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 13.82 [13.485, 14.1851] | 2.925 [2.84, 3] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0.205 [0.129875, 0.29] | 0.02 [0, 0.04] | 0 [0, 0] | 2.765 [2.705, 2.82] | 10.83 [10.535, 11.15] |
| B1 | 45.435 [42.1347, 48.7302] | 1.675 [1.56, 1.795] | 208.675 [202.009, 215.423] | 3.37 [3.13, 3.62012] | 0 [0, 0] | 0 [0, 0] | 35.435 [32.0299, 38.7601] | 0 [0, 0] | 0 [0, 0] | 0.065 [0.025, 0.11] | 9.935 [9.735, 10.135] |
| B2-K0 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B2 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B3 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B4 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B4b | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.00166667 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.00166667 | 0 | 0 | 0 |
| B2-K0 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B2 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B3 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B4 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B4b | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |

B2: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B3: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4b: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.00166667 [0, 0.00416667]
B3/B4B share of differing weeks: 0.00166667 [0, 0.00416667]
B4/B4B share of differing weeks: 0.00166667 [0, 0.00416667]

## benign; horizon 40 days; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 17.055 [16.6749, 17.4701] | 2.925 [2.84, 3] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0.205 [0.129875, 0.29] | 0.005 [0, 0.015] | 0 [0, 0] | 2.78 [2.72, 2.835] | 14.065 [13.715, 14.435] |
| B1 | 46.365 [43.1195, 49.6556] | 1.675 [1.56, 1.795] | 208.675 [202.009, 215.423] | 3.37 [3.13, 3.62012] | 0 [0, 0] | 0 [0, 0] | 35.435 [32.0299, 38.7601] | 0 [0, 0] | 0 [0, 0] | 0.065 [0.025, 0.11] | 10.865 [10.46, 11.265] |
| B2-K0 | 9.41 [9.26, 9.58013] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 0 [0, 0] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B2 | 9.41 [9.26, 9.58013] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B3 | 9.41 [9.26, 9.58013] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B4 | 9.41 [9.26, 9.58013] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B4b | 9.41 [9.26, 9.58013] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.00166667 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.00166667 | 0 | 0 | 0 |
| B2-K0 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B2 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B3 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B4 | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |
| B4b | 200/1200 (0.166667) | 0.00166667 | 0 | 0 | 0 |

B2: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B3: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4b: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.00166667 [0, 0.00416667]
B3/B4B share of differing weeks: 0.00166667 [0, 0.00416667]
B4/B4B share of differing weeks: 0.00166667 [0, 0.00416667]

## benign; horizon 80 days; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 198.535 [197.575, 199.55] | 9.695 [9.62988, 9.755] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 180.535 [179.575, 181.55] | 0.115 [0.075, 0.16] | 0 [0, 0] | 2.885 [2.84, 2.925] | 15 [15, 15] |
| B1 | 273.095 [267.66, 278.291] | 4.57 [4.37988, 4.765] | 213.095 [206.959, 218.889] | 3.63 [3.38, 3.895] | 0 [0, 0] | 0 [0, 0] | 263.555 [258.16, 268.74] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.54 [9.42, 9.66] |
| B2-K0 | 201.875 [201.375, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B2 | 201.875 [201.375, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B3 | 201.875 [201.375, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B4 | 201.875 [201.375, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B4b | 201.875 [201.375, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.487083 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.487083 | 0 | 0 | 0 |
| B2-K0 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B2 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B3 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B4 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B4b | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]
B3/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]
B4/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]

## benign; horizon 80 days; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 201.535 [200.575, 202.55] | 9.695 [9.62988, 9.755] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 180.535 [179.575, 181.55] | 0.065 [0.035, 0.1] | 0 [0, 0] | 2.935 [2.9, 2.965] | 18 [18, 18] |
| B1 | 273.365 [267.915, 278.542] | 4.57 [4.37988, 4.765] | 213.095 [206.959, 218.889] | 3.62 [3.37, 3.88] | 0 [0, 0] | 0 [0, 0] | 263.555 [258.16, 268.74] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.81 [9.63, 9.99] |
| B2-K0 | 201.88 [201.38, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B2 | 201.88 [201.38, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B3 | 201.88 [201.38, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B4 | 201.88 [201.38, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B4b | 201.88 [201.38, 202.435] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.487083 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.487083 | 0 | 0 | 0 |
| B2-K0 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B2 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B3 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B4 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B4b | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]
B3/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]
B4/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]

## benign; horizon 80 days; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 210.535 [209.575, 211.55] | 9.695 [9.62988, 9.755] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 180.535 [179.575, 181.55] | 0.005 [0, 0.015] | 0 [0, 0] | 2.995 [2.985, 3] | 27 [27, 27] |
| B1 | 274.175 [268.745, 279.41] | 4.57 [4.37988, 4.765] | 213.095 [206.959, 218.889] | 3.62 [3.37, 3.88] | 0 [0, 0] | 0 [0, 0] | 263.555 [258.16, 268.74] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 10.62 [10.26, 10.98] |
| B2-K0 | 201.895 [201.385, 202.455] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 0 [0, 0] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B2 | 201.895 [201.385, 202.455] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B3 | 201.895 [201.385, 202.455] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B4 | 201.895 [201.385, 202.455] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B4b | 201.895 [201.385, 202.455] | 2.2 [2.035, 2.37] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 12 [12, 12] | 192.865 [192.365, 193.425] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.487083 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.487083 | 0 | 0 | 0 |
| B2-K0 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B2 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B3 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B4 | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |
| B4b | 1400/2400 (0.583333) | 0.487083 | 0 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]
B3/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]
B4/B4B share of differing weeks: 0.487083 [0.480417, 0.492917]

## moderate; horizon 40 days; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 13.57 [12.9199, 14.2451] | 2.775 [2.66, 2.895] | 0 [0, 0] | 0.735 [0.53, 0.965] | 0 [0, 0] | 0 [0, 0] | 2.12 [1.66987, 2.62] | 0.78 [0.63, 0.95] | 0 [0, 0] | 1.775 [1.695, 1.85] | 8.895 [8.61, 9.19] |
| B1 | 72.53 [67.7687, 77.0459] | 1.645 [1.53487, 1.76012] | 170.862 [162.636, 178.86] | 13.72 [13.105, 14.3651] | 0 [0, 0] | 0 [0, 0] | 64.065 [59.2395, 68.6308] | 0.005 [0, 0.015] | 0 [0, 0] | 0.005 [0, 0.015] | 8.455 [8.255, 8.66] |
| B2-K0 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 0 [0, 0] | 3.73 [3.19488, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |
| B2 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 6 [6, 6] | 3.73 [3.19488, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |
| B3 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 6 [6, 6] | 3.73 [3.19488, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |
| B4 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 6 [6, 6] | 3.73 [3.19488, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |
| B4b | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 6 [6, 6] | 3.73 [3.19488, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.294167 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.294167 | 0 | 0 | 0 |
| B2-K0 | 401/1200 (0.334167) | 0.294167 | 0 | 0 | 0 |
| B2 | 401/1200 (0.334167) | 0.294167 | 0 | 0 | 0 |
| B3 | 401/1200 (0.334167) | 0.294167 | 0 | 0 | 0 |
| B4 | 401/1200 (0.334167) | 0.294167 | 0 | 0 | 0 |
| B4b | 401/1200 (0.334167) | 0.294167 | 0 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.286667 [0.275833, 0.2975]
B2/B4 share of differing weeks: 0.286667 [0.275833, 0.2975]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.294167 [0.284167, 0.305]
B3/B4B share of differing weeks: 0.025 [0.0166667, 0.0341667]
B4/B4B share of differing weeks: 0.025 [0.0166667, 0.0341667]

## moderate; horizon 40 days; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 14.935 [14.2498, 15.66] | 2.775 [2.66, 2.895] | 0 [0, 0] | 0.645 [0.46, 0.855] | 0 [0, 0] | 0 [0, 0] | 2.12 [1.66987, 2.62] | 0.91 [0.735, 1.10512] | 0 [0, 0] | 1.755 [1.675, 1.83] | 10.15 [9.82, 10.4801] |
| B1 | 72.715 [67.9781, 77.2002] | 1.645 [1.53487, 1.76012] | 170.862 [162.636, 178.86] | 13.73 [13.1099, 14.3752] | 0 [0, 0] | 0 [0, 0] | 64.065 [59.2395, 68.6308] | 0.01 [0, 0.03] | 0 [0, 0] | 0.005 [0, 0.015] | 8.635 [8.405, 8.87] |
| B2-K0 | 12.65 [12, 13.3101] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.97] | 0 [0, 0] | 0 [0, 0] | 3.72 [3.185, 4.28] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19013] |
| B2 | 12.65 [12, 13.3101] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.97] | 0 [0, 0] | 6 [6, 6] | 3.72 [3.185, 4.28] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19013] |
| B3 | 12.65 [12, 13.3101] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.97] | 0 [0, 0] | 6 [6, 6] | 3.72 [3.185, 4.28] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19013] |
| B4 | 12.65 [12, 13.3101] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.97] | 0 [0, 0] | 6 [6, 6] | 3.72 [3.185, 4.28] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19013] |
| B4b | 12.635 [11.9999, 13.2851] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.46 [9.97, 10.96] | 0.08 [0, 0.2] | 5.99 [5.975, 6] | 3.72 [3.185, 4.28] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19013] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | -0.005 [-0.015, 0] | 199/200 |
| Intervention cost (man-hours) | 0.08 [0, 0.2] | 198/200 |
| Unused intervention weeks (weeks) | -0.01 [-0.025, 0] | 198/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 198/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | -0.005 [-0.015, 0] | 199/200 |
| Intervention cost (man-hours) | 0.08 [0, 0.2] | 198/200 |
| Unused intervention weeks (weeks) | -0.01 [-0.025, 0] | 198/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 198/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.295 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.295 | 0 | 0 | 0 |
| B2-K0 | 401/1200 (0.334167) | 0.295 | 0 | 0 | 0 |
| B2 | 401/1200 (0.334167) | 0.295 | 0 | 0 | 0 |
| B3 | 401/1200 (0.334167) | 0.295 | 0 | 0 | 0 |
| B4 | 401/1200 (0.334167) | 0.295 | 0 | 0 | 0 |
| B4b | 401/1200 (0.334167) | 0.295 | 0 | 2 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.289167 [0.278333, 0.3]
B2/B4 share of differing weeks: 0.289167 [0.278333, 0.3]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.295 [0.285, 0.305833]
B3/B4B share of differing weeks: 0.025 [0.0166667, 0.0341667]
B4/B4B share of differing weeks: 0.025 [0.0166667, 0.0341667]

## moderate; horizon 40 days; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 18.56 [17.775, 19.395] | 2.775 [2.66, 2.895] | 0 [0, 0] | 0.51 [0.35, 0.695] | 0 [0, 0] | 0 [0, 0] | 2.12 [1.66987, 2.62] | 1.355 [1.135, 1.62] | 0 [0, 0] | 1.67 [1.59, 1.74012] | 13.415 [13, 13.835] |
| B1 | 73.295 [68.615, 77.8003] | 1.645 [1.53487, 1.76012] | 170.882 [162.643, 178.87] | 13.91 [13.26, 14.585] | 0 [0, 0] | 0 [0, 0] | 64.065 [59.2395, 68.6308] | 0.115 [0.04, 0.2] | 0 [0, 0] | 0.005 [0, 0.015] | 9.11 [8.775, 9.465] |
| B2-K0 | 13.45 [12.6549, 14.2751] | 0.805 [0.694875, 0.920125] | 39.7823 [37.0063, 42.5366] | 10.49 [10, 11.0001] | 0 [0, 0] | 0 [0, 0] | 3.72 [3.185, 4.28] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 9.6 [9.19988, 10.0351] |
| B2 | 13.45 [12.6549, 14.2751] | 0.805 [0.694875, 0.920125] | 39.9471 [37.1516, 42.6863] | 10.54 [10.0449, 11.0552] | 0.24 [0.08, 0.44] | 5.97 [5.945, 5.99] | 3.72 [3.185, 4.28] | 0.09 [0.025, 0.18] | 0 [0, 0] | 0 [0, 0] | 9.64 [9.225, 10.075] |
| B3 | 13.45 [12.6549, 14.2751] | 0.805 [0.694875, 0.920125] | 39.7823 [37.0063, 42.5366] | 10.49 [10, 11.0001] | 0 [0, 0] | 6 [6, 6] | 3.72 [3.185, 4.28] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 9.6 [9.19988, 10.0351] |
| B4 | 13.45 [12.6549, 14.2751] | 0.805 [0.694875, 0.920125] | 39.7823 [37.0063, 42.5366] | 10.49 [10, 11.0001] | 0 [0, 0] | 6 [6, 6] | 3.72 [3.185, 4.28] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 9.6 [9.19988, 10.0351] |
| B4b | 13.45 [12.6549, 14.2751] | 0.805 [0.694875, 0.920125] | 39.7823 [37.0063, 42.5366] | 10.49 [10, 11.0001] | 0 [0, 0] | 6 [6, 6] | 3.72 [3.185, 4.28] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 9.6 [9.19988, 10.0351] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | -0.164784 [-0.416281, -0.0149682] | 196/200 |
| Plan churn (changed placements) | -0.05 [-0.11, -0.005] | 194/200 |
| Intervention cost (man-hours) | -0.24 [-0.44, -0.08] | 194/200 |
| Unused intervention weeks (weeks) | 0.03 [0.01, 0.055] | 194/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0.04 [0.005, 0.08] | 196/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | -0.04 [-0.08, -0.005] | 196/200 |

Combined ties (all_reported_metrics): 194/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0.164784 [0.0149682, 0.416281] | 196/200 |
| Plan churn (changed placements) | 0.05 [0.005, 0.11] | 194/200 |

Combined ties (outcomes_only): 194/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.2975 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.2975 | 0 | 0 | 0 |
| B2-K0 | 401/1200 (0.334167) | 0.2975 | 0 | 0 | 0 |
| B2 | 401/1200 (0.334167) | 0.2975 | 0 | 6 | 0 |
| B3 | 401/1200 (0.334167) | 0.2975 | 0 | 0 | 0 |
| B4 | 401/1200 (0.334167) | 0.2975 | 0 | 0 | 0 |
| B4b | 401/1200 (0.334167) | 0.2975 | 0 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.2925 [0.281667, 0.302521]
B2/B4 share of differing weeks: 0.2925 [0.281667, 0.302521]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.2975 [0.2875, 0.3075]
B3/B4B share of differing weeks: 0.0233333 [0.015, 0.0316667]
B4/B4B share of differing weeks: 0.0233333 [0.015, 0.0316667]

## moderate; horizon 80 days; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 197.635 [195.795, 199.611] | 9.515 [9.44, 9.585] | 0 [0, 0] | 0.91 [0.695, 1.15] | 0 [0, 0] | 0 [0, 0] | 178.62 [176.805, 180.6] | 1.98 [1.685, 2.25] | 0 [0, 0] | 2.035 [1.95, 2.12] | 15 [15, 15] |
| B1 | 299.545 [292.705, 306.175] | 4.565 [4.375, 4.765] | 179.215 [170.984, 187.058] | 14.345 [13.705, 14.9951] | 0 [0, 0] | 0 [0, 0] | 289.97 [283.143, 296.64] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 9.57 [9.43, 9.72025] |
| B2-K0 | 210.495 [209.285, 211.84] | 2.75 [2.565, 2.945] | 41.3375 [38.6476, 44.0185] | 10.565 [10.0549, 11.085] | 0 [0, 0] | 0 [0, 0] | 200.33 [199.195, 201.625] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 10.16 [9.98, 10.35] |
| B2 | 210.495 [209.285, 211.84] | 2.75 [2.565, 2.945] | 41.3375 [38.6476, 44.0185] | 10.565 [10.0549, 11.085] | 0 [0, 0] | 12 [12, 12] | 200.33 [199.195, 201.625] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 10.16 [9.98, 10.35] |
| B3 | 210.495 [209.285, 211.84] | 2.75 [2.565, 2.945] | 41.3375 [38.6476, 44.0185] | 10.565 [10.0549, 11.085] | 0 [0, 0] | 12 [12, 12] | 200.33 [199.195, 201.625] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 10.16 [9.98, 10.35] |
| B4 | 210.495 [209.285, 211.84] | 2.75 [2.565, 2.945] | 41.3375 [38.6476, 44.0185] | 10.565 [10.0549, 11.085] | 0 [0, 0] | 12 [12, 12] | 200.33 [199.195, 201.625] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 10.16 [9.98, 10.35] |
| B4b | 210.495 [209.285, 211.84] | 2.75 [2.565, 2.945] | 41.3375 [38.6476, 44.0185] | 10.565 [10.0549, 11.085] | 0 [0, 0] | 12 [12, 12] | 200.33 [199.195, 201.625] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 10.16 [9.98, 10.35] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.631667 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.631667 | 0 | 0 | 0 |
| B2-K0 | 1601/2400 (0.667083) | 0.631667 | 0 | 0 | 0 |
| B2 | 1601/2400 (0.667083) | 0.631667 | 0 | 0 | 0 |
| B3 | 1601/2400 (0.667083) | 0.631667 | 0 | 0 | 0 |
| B4 | 1601/2400 (0.667083) | 0.631667 | 0 | 0 | 0 |
| B4b | 1601/2400 (0.667083) | 0.631667 | 0 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.143333 [0.137917, 0.14875]
B2/B4 share of differing weeks: 0.143333 [0.137917, 0.14875]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.631667 [0.62375, 0.639583]
B3/B4B share of differing weeks: 0.497083 [0.489583, 0.50375]
B4/B4B share of differing weeks: 0.497083 [0.489583, 0.50375]

## moderate; horizon 80 days; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 201.305 [199.455, 203.3] | 9.515 [9.44, 9.585] | 0 [0, 0] | 0.89 [0.695, 1.11] | 0 [0, 0] | 0 [0, 0] | 178.62 [176.805, 180.6] | 2.72 [2.365, 3.04013] | 0 [0, 0] | 1.965 [1.885, 2.04013] | 18 [18, 18] |
| B1 | 299.835 [293.044, 306.43] | 4.565 [4.375, 4.765] | 179.215 [170.984, 187.058] | 14.36 [13.72, 15.01] | 0 [0, 0] | 0 [0, 0] | 289.97 [283.143, 296.64] | 0.01 [0, 0.03] | 0 [0, 0] | 0 [0, 0] | 9.855 [9.645, 10.0804] |
| B2-K0 | 211.095 [209.825, 212.47] | 2.75 [2.565, 2.945] | 41.2532 [38.5222, 43.9247] | 10.575 [10.07, 11.095] | 0 [0, 0] | 0 [0, 0] | 200.32 [199.19, 201.605] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 10.755 [10.485, 11.04] |
| B2 | 211.095 [209.825, 212.47] | 2.75 [2.565, 2.945] | 41.2532 [38.5222, 43.9247] | 10.575 [10.07, 11.095] | 0 [0, 0] | 12 [12, 12] | 200.32 [199.19, 201.605] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 10.755 [10.485, 11.04] |
| B3 | 211.095 [209.825, 212.47] | 2.75 [2.565, 2.945] | 41.2532 [38.5222, 43.9247] | 10.575 [10.07, 11.095] | 0 [0, 0] | 12 [12, 12] | 200.32 [199.19, 201.605] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 10.755 [10.485, 11.04] |
| B4 | 211.095 [209.825, 212.47] | 2.75 [2.565, 2.945] | 41.2532 [38.5222, 43.9247] | 10.575 [10.07, 11.095] | 0 [0, 0] | 12 [12, 12] | 200.32 [199.19, 201.605] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 10.755 [10.485, 11.04] |
| B4b | 211.08 [209.81, 212.46] | 2.75 [2.565, 2.945] | 41.2532 [38.5222, 43.9247] | 10.57 [10.065, 11.0851] | 0.08 [0, 0.2] | 11.99 [11.975, 12] | 200.32 [199.19, 201.605] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 10.755 [10.485, 11.04] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | -0.005 [-0.015, 0] | 199/200 |
| Intervention cost (man-hours) | 0.08 [0, 0.2] | 198/200 |
| Unused intervention weeks (weeks) | -0.01 [-0.025, 0] | 198/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 198/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | -0.005 [-0.015, 0] | 199/200 |
| Intervention cost (man-hours) | 0.08 [0, 0.2] | 198/200 |
| Unused intervention weeks (weeks) | -0.01 [-0.025, 0] | 198/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 198/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |

Combined ties (outcomes_only): 200/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.632083 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.632083 | 0 | 0 | 0 |
| B2-K0 | 1601/2400 (0.667083) | 0.632083 | 0 | 0 | 0 |
| B2 | 1601/2400 (0.667083) | 0.632083 | 0 | 0 | 0 |
| B3 | 1601/2400 (0.667083) | 0.632083 | 0 | 0 | 0 |
| B4 | 1601/2400 (0.667083) | 0.632083 | 0 | 0 | 0 |
| B4b | 1601/2400 (0.667083) | 0.632083 | 0 | 2 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.144583 [0.139167, 0.15]
B2/B4 share of differing weeks: 0.144583 [0.139167, 0.15]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.632083 [0.624156, 0.64]
B3/B4B share of differing weeks: 0.497083 [0.489583, 0.50375]
B4/B4B share of differing weeks: 0.497083 [0.489583, 0.50375]

## moderate; horizon 80 days; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 212.98 [211.095, 215.07] | 9.515 [9.44, 9.585] | 0 [0, 0] | 1.04 [0.875, 1.23012] | 0 [0, 0] | 0 [0, 0] | 178.62 [176.805, 180.6] | 5.57 [5.08, 6.04512] | 0 [0, 0] | 1.79 [1.71, 1.865] | 27 [27, 27] |
| B1 | 300.785 [294.06, 307.19] | 4.565 [4.375, 4.765] | 179.236 [170.978, 187.02] | 14.545 [13.8999, 15.235] | 0 [0, 0] | 0 [0, 0] | 289.97 [283.143, 296.64] | 0.105 [0.035, 0.19] | 0 [0, 0] | 0 [0, 0] | 10.71 [10.29, 11.1608] |
| B2-K0 | 212.99 [211.549, 214.535] | 2.75 [2.565, 2.945] | 41.0019 [38.2518, 43.6732] | 10.6 [10.09, 11.13] | 0 [0, 0] | 0 [0, 0] | 200.32 [199.19, 201.605] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 12.54 [11.97, 13.11] |
| B2 | 212.92 [211.48, 214.46] | 2.75 [2.565, 2.945] | 41.1485 [38.4073, 43.8382] | 10.65 [10.135, 11.19] | 0.24 [0.08, 0.44] | 11.97 [11.945, 11.99] | 200.32 [199.19, 201.605] | 0.09 [0.025, 0.18] | 0 [0, 0] | 0 [0, 0] | 12.51 [11.97, 13.08] |
| B3 | 212.99 [211.549, 214.535] | 2.75 [2.565, 2.945] | 41.0019 [38.2518, 43.6732] | 10.6 [10.09, 11.13] | 0 [0, 0] | 12 [12, 12] | 200.32 [199.19, 201.605] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 12.54 [11.97, 13.11] |
| B4 | 212.99 [211.549, 214.535] | 2.75 [2.565, 2.945] | 41.0019 [38.2518, 43.6732] | 10.6 [10.09, 11.13] | 0 [0, 0] | 12 [12, 12] | 200.32 [199.19, 201.605] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 12.54 [11.97, 13.11] |
| B4b | 212.99 [211.549, 214.535] | 2.75 [2.565, 2.945] | 41.0019 [38.2518, 43.6732] | 10.6 [10.09, 11.13] | 0 [0, 0] | 12 [12, 12] | 200.32 [199.19, 201.605] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 12.54 [11.97, 13.11] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0.07 [0.005, 0.165] | 196/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | -0.146586 [-0.394853, 0] | 197/200 |
| Plan churn (changed placements) | -0.05 [-0.11, -0.005] | 194/200 |
| Intervention cost (man-hours) | -0.24 [-0.44, -0.08] | 194/200 |
| Unused intervention weeks (weeks) | 0.03 [0.01, 0.055] | 194/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0.04 [0.005, 0.08] | 196/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0.03 [0, 0.09] | 199/200 |

Combined ties (all_reported_metrics): 194/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -0.07 [-0.165, -0.005] | 196/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0.146586 [0, 0.394853] | 197/200 |
| Plan churn (changed placements) | 0.05 [0.005, 0.11] | 194/200 |

Combined ties (outcomes_only): 194/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.633333 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.633333 | 0 | 0 | 0 |
| B2-K0 | 1601/2400 (0.667083) | 0.633333 | 0 | 0 | 0 |
| B2 | 1601/2400 (0.667083) | 0.633333 | 0 | 6 | 0 |
| B3 | 1601/2400 (0.667083) | 0.633333 | 0 | 0 | 0 |
| B4 | 1601/2400 (0.667083) | 0.633333 | 0 | 0 | 0 |
| B4b | 1601/2400 (0.667083) | 0.633333 | 0 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.147083 [0.141667, 0.1525]
B2/B4 share of differing weeks: 0.147083 [0.141667, 0.1525]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.633333 [0.625, 0.64126]
B3/B4B share of differing weeks: 0.49625 [0.489167, 0.5025]
B4/B4B share of differing weeks: 0.49625 [0.489167, 0.5025]

## stressed; horizon 40 days; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 31.22 [28.8749, 33.5654] | 2.88 [2.725, 3.03] | 0 [0, 0] | 8.17 [7.265, 9.12012] | 0 [0, 0] | 0 [0, 0] | 26.995 [24.5648, 29.4405] | 0 [0, 0] | 0 [0, 0] | 0.14 [0.095, 0.185] | 4.085 [3.845, 4.315] |
| B1 | 102.895 [97.3438, 108.276] | 1.865 [1.74, 2] | 65.7922 [59.9312, 71.226] | 11.96 [11.055, 12.905] | 0 [0, 0] | 0 [0, 0] | 100.24 [94.5998, 105.71] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 2.655 [2.51, 2.79] |
| B2-K0 | 39.725 [37.7897, 41.7301] | 1.78 [1.625, 1.94512] | 10.5052 [8.6159, 12.6255] | 10.775 [9.90987, 11.675] | 0 [0, 0] | 0 [0, 0] | 36.63 [34.67, 38.6803] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.095 [2.9, 3.29] |
| B2 | 36.03 [33.9696, 38.1854] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.505 [3.35, 3.65] |
| B3 | 36.03 [33.9696, 38.1854] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.505 [3.35, 3.65] |
| B4 | 36.03 [33.9696, 38.1854] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.505 [3.35, 3.65] |
| B4b | 36.03 [33.9696, 38.1854] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.505 [3.35, 3.65] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -3.695 [-3.97, -3.415] | 38/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.621178 [0.173231, 1.25948] | 182/200 |
| Plan churn (changed placements) | 0.8 [0.73, 0.865] | 42/200 |

Combined ties (outcomes_only): 33/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.466667 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.466667 | 0 | 0 | 0 |
| B2-K0 | 605/1200 (0.504167) | 0.466667 | 0 | 0 | 0 |
| B2 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B3 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B4 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B4b | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.219167 [0.195833, 0.244167]
B2/B4 share of differing weeks: 0.219167 [0.195833, 0.244167]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.353333 [0.334146, 0.3725]
B3/B4B share of differing weeks: 0.408333 [0.395833, 0.421667]
B4/B4B share of differing weeks: 0.408333 [0.395833, 0.421667]

## stressed; horizon 40 days; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 31.865 [29.53, 34.2054] | 2.88 [2.725, 3.03] | 0 [0, 0] | 8.17 [7.265, 9.12012] | 0 [0, 0] | 0 [0, 0] | 26.995 [24.5648, 29.4405] | 0 [0, 0] | 0 [0, 0] | 0.14 [0.095, 0.185] | 4.73 [4.44487, 5.01] |
| B1 | 102.925 [97.3789, 108.291] | 1.865 [1.74, 2] | 65.7922 [59.9312, 71.226] | 11.96 [11.055, 12.905] | 0 [0, 0] | 0 [0, 0] | 100.24 [94.5998, 105.71] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 2.685 [2.53, 2.83] |
| B2-K0 | 39.93 [38, 41.9551] | 1.78 [1.625, 1.94512] | 10.5052 [8.6159, 12.6255] | 10.775 [9.90987, 11.675] | 0 [0, 0] | 0 [0, 0] | 36.63 [34.67, 38.6803] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.3 [3.065, 3.54013] |
| B2 | 36.295 [34.2146, 38.48] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.77 [3.56, 3.97] |
| B3 | 36.295 [34.2146, 38.48] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.77 [3.56, 3.97] |
| B4 | 36.295 [34.2146, 38.48] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.77 [3.56, 3.97] |
| B4b | 36.295 [34.2146, 38.48] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.77 [3.56, 3.97] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -3.635 [-3.92, -3.35] | 41/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.621178 [0.173231, 1.25948] | 182/200 |
| Plan churn (changed placements) | 0.8 [0.73, 0.865] | 42/200 |

Combined ties (outcomes_only): 33/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.466667 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.466667 | 0 | 0 | 0 |
| B2-K0 | 605/1200 (0.504167) | 0.466667 | 0 | 0 | 0 |
| B2 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B3 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B4 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B4b | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.219167 [0.195833, 0.244167]
B2/B4 share of differing weeks: 0.219167 [0.195833, 0.244167]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.353333 [0.334146, 0.3725]
B3/B4B share of differing weeks: 0.408333 [0.395833, 0.421667]
B4/B4B share of differing weeks: 0.408333 [0.395833, 0.421667]

## stressed; horizon 40 days; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 33.495 [31.2347, 35.8051] | 2.88 [2.725, 3.03] | 0 [0, 0] | 8.17 [7.265, 9.12012] | 0 [0, 0] | 0 [0, 0] | 26.995 [24.5648, 29.4405] | 0 [0, 0] | 0 [0, 0] | 0.14 [0.095, 0.185] | 6.36 [5.89975, 6.79512] |
| B1 | 103.015 [97.4843, 108.361] | 1.865 [1.74, 2] | 65.7922 [59.9312, 71.226] | 11.96 [11.055, 12.905] | 0 [0, 0] | 0 [0, 0] | 100.24 [94.5998, 105.71] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 2.775 [2.585, 2.97] |
| B2-K0 | 40.46 [38.4846, 42.5055] | 1.78 [1.625, 1.94512] | 10.5052 [8.6159, 12.6255] | 10.775 [9.90987, 11.675] | 0 [0, 0] | 0 [0, 0] | 36.63 [34.67, 38.6803] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.83 [3.465, 4.2] |
| B2 | 36.985 [34.8548, 39.2251] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 4.46 [4.10487, 4.81513] |
| B3 | 36.985 [34.8548, 39.2251] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 4.46 [4.10487, 4.81513] |
| B4 | 36.985 [34.8548, 39.2251] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 4.46 [4.10487, 4.81513] |
| B4b | 36.985 [34.8548, 39.2251] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 4.46 [4.10487, 4.81513] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -3.475 [-3.775, -3.165] | 47/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.621178 [0.173231, 1.25948] | 182/200 |
| Plan churn (changed placements) | 0.8 [0.73, 0.865] | 42/200 |

Combined ties (outcomes_only): 34/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.466667 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.466667 | 0 | 0 | 0 |
| B2-K0 | 605/1200 (0.504167) | 0.466667 | 0 | 0 | 0 |
| B2 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B3 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B4 | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |
| B4b | 565/1200 (0.470833) | 0.466667 | 167 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.219167 [0.195833, 0.244167]
B2/B4 share of differing weeks: 0.219167 [0.195833, 0.244167]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.353333 [0.334146, 0.3725]
B3/B4B share of differing weeks: 0.408333 [0.395833, 0.421667]
B4/B4B share of differing weeks: 0.408333 [0.395833, 0.421667]

## stressed; horizon 80 days; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 271.13 [266.779, 275.835] | 9.375 [9.295, 9.455] | 0 [0, 0] | 20.905 [19.6698, 22.1851] | 0 [0, 0] | 0 [0, 0] | 261.855 [257.495, 266.591] | 0 [0, 0] | 0 [0, 0] | 0.145 [0.1, 0.19] | 9.13 [8.91, 9.335] |
| B1 | 399.12 [391.414, 406.787] | 4.48 [4.27, 4.69] | 113.903 [106.114, 121.06] | 26.34 [25.0646, 27.6051] | 0 [0, 0] | 0 [0, 0] | 393.41 [385.693, 401.112] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 5.71 [5.58, 5.83] |
| B2-K0 | 316.34 [313.53, 319.475] | 3.385 [3.17488, 3.595] | 20.3708 [17.6874, 23.2293] | 27.54 [26.3046, 28.79] | 0 [0, 0] | 0 [0, 0] | 309.48 [306.65, 312.505] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 6.86 [6.62, 7.095] |
| B2 | 312.175 [309.264, 315.276] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 6.83 [6.595, 7.07] |
| B3 | 312.175 [309.264, 315.276] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 6.83 [6.595, 7.07] |
| B4 | 312.175 [309.264, 315.276] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 6.83 [6.595, 7.07] |
| B4b | 312.175 [309.264, 315.276] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 6.83 [6.595, 7.07] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -4.165 [-4.42, -3.90488] | 33/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.334054 [-0.0818134, 0.975177] | 186/200 |
| Plan churn (changed placements) | 0.775 [0.7, 0.84] | 35/200 |

Combined ties (outcomes_only): 33/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.733333 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.733333 | 0 | 0 | 0 |
| B2-K0 | 1805/2400 (0.752083) | 0.733333 | 0 | 0 | 0 |
| B2 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B3 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B4 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B4b | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.613333 [0.600823, 0.62626]
B2/B4 share of differing weeks: 0.613333 [0.600823, 0.62626]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.668333 [0.656667, 0.679167]
B3/B4B share of differing weeks: 0.69125 [0.6825, 0.7]
B4/B4B share of differing weeks: 0.69125 [0.6825, 0.7]

## stressed; horizon 80 days; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 272.795 [268.454, 277.495] | 9.375 [9.295, 9.455] | 0 [0, 0] | 20.905 [19.6698, 22.1851] | 0 [0, 0] | 0 [0, 0] | 261.855 [257.495, 266.591] | 0 [0, 0] | 0 [0, 0] | 0.145 [0.1, 0.19] | 10.795 [10.525, 11.05] |
| B1 | 399.155 [391.45, 406.817] | 4.48 [4.27, 4.69] | 113.903 [106.114, 121.06] | 26.34 [25.0646, 27.6051] | 0 [0, 0] | 0 [0, 0] | 393.41 [385.693, 401.112] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 5.745 [5.61, 5.87012] |
| B2-K0 | 316.925 [314.07, 320.06] | 3.385 [3.17488, 3.595] | 20.3708 [17.6874, 23.2293] | 27.54 [26.3046, 28.79] | 0 [0, 0] | 0 [0, 0] | 309.48 [306.65, 312.505] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 7.445 [7.13, 7.76] |
| B2 | 312.745 [309.823, 315.906] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 7.4 [7.08488, 7.72] |
| B3 | 312.745 [309.823, 315.906] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 7.4 [7.08488, 7.72] |
| B4 | 312.745 [309.823, 315.906] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 7.4 [7.08488, 7.72] |
| B4b | 312.745 [309.823, 315.906] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 7.4 [7.08488, 7.72] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -4.18 [-4.445, -3.91487] | 33/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.334054 [-0.0818134, 0.975177] | 186/200 |
| Plan churn (changed placements) | 0.775 [0.7, 0.84] | 35/200 |

Combined ties (outcomes_only): 33/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.733333 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.733333 | 0 | 0 | 0 |
| B2-K0 | 1805/2400 (0.752083) | 0.733333 | 0 | 0 | 0 |
| B2 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B3 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B4 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B4b | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.613333 [0.600823, 0.62626]
B2/B4 share of differing weeks: 0.613333 [0.600823, 0.62626]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.668333 [0.656667, 0.679167]
B3/B4B share of differing weeks: 0.69125 [0.6825, 0.7]
B4/B4B share of differing weeks: 0.69125 [0.6825, 0.7]

## stressed; horizon 80 days; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 277.56 [273.265, 282.265] | 9.375 [9.295, 9.455] | 0 [0, 0] | 20.905 [19.6698, 22.1851] | 0 [0, 0] | 0 [0, 0] | 261.855 [257.495, 266.591] | 0 [0, 0] | 0 [0, 0] | 0.145 [0.1, 0.19] | 15.56 [15.1399, 15.9651] |
| B1 | 399.26 [391.618, 406.907] | 4.48 [4.27, 4.69] | 113.903 [106.114, 121.06] | 26.34 [25.0646, 27.6051] | 0 [0, 0] | 0 [0, 0] | 393.41 [385.693, 401.112] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 5.85 [5.675, 6.035] |
| B2-K0 | 318.635 [315.69, 321.81] | 3.385 [3.17488, 3.595] | 20.3708 [17.6874, 23.2293] | 27.54 [26.3046, 28.79] | 0 [0, 0] | 0 [0, 0] | 309.48 [306.65, 312.505] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.155 [8.59475, 9.74] |
| B2 | 314.41 [311.35, 317.695] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.065 [8.49987, 9.65012] |
| B3 | 314.41 [311.35, 317.695] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.065 [8.49987, 9.65012] |
| B4 | 314.41 [311.35, 317.695] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.065 [8.49987, 9.65012] |
| B4b | 314.41 [311.35, 317.695] | 3.38 [3.165, 3.59] | 20.7049 [18.0571, 23.4465] | 28.315 [27.06, 29.5701] | 6.68 [6.24, 7.08] | 11.165 [11.115, 11.22] | 305.345 [302.465, 308.41] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.065 [8.49987, 9.65012] |

### B4 minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B3 minus B2 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B4 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B4b minus B3 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0 [0, 0] | 200/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 0 [0, 0] | 200/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |

Combined ties (all_reported_metrics): 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -4.225 [-4.52013, -3.925] | 33/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.334054 [-0.0818134, 0.975177] | 186/200 |
| Plan churn (changed placements) | 0.775 [0.7, 0.84] | 35/200 |

Combined ties (outcomes_only): 33/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/2400 (0) | 0.733333 | 0 | 0 | 0 |
| B1 | 0/2400 (0) | 0.733333 | 0 | 0 | 0 |
| B2-K0 | 1805/2400 (0.752083) | 0.733333 | 0 | 0 | 0 |
| B2 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B3 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B4 | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |
| B4b | 1765/2400 (0.735417) | 0.733333 | 167 | 0 | 0 |

B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B4b: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.613333 [0.600823, 0.62626]
B2/B4 share of differing weeks: 0.613333 [0.600823, 0.62626]
B3/B4 share of differing weeks: 0 [0, 0]
B2/B4B share of differing weeks: 0.668333 [0.656667, 0.679167]
B3/B4B share of differing weeks: 0.69125 [0.6825, 0.7]
B4/B4B share of differing weeks: 0.69125 [0.6825, 0.7]
