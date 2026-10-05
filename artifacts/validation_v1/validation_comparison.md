# Validation comparison

**simulated; scenario-based**

Each cell is mean [95% percentile bootstrap CI] from paired scenarios.
Stress settings and training-derived B1 interval were frozen before comparison.
AOG includes grounded waiting and maintenance; healthy future-slot waiting is excluded.
Repair multipliers are assumed. Ties are retained. AOG is censored at the horizon.

## benign; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 12.63 [12.325, 12.97] | 2.925 [2.84, 3] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0.205 [0.129875, 0.29] | 0.05 [0.02, 0.080125] | 0 [0, 0] | 2.735 [2.67, 2.795] | 9.64 [9.375, 9.93] |
| B1 | 314.95 [314.765, 315.13] | 0 [0, 0] | 307.92 [306.5, 309.352] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 305.95 [305.765, 306.13] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9 [9, 9] |
| B2-K0 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B2 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B3 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |
| B4 | 9.39 [9.25, 9.55] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.01 [9, 9.03] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | -7.76581e-12 [-4.53929e-11, 3.02907e-11] | 0/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 6 [6, 6] | 0/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0 | 0 | 0 | 0 |
| B2-K0 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B2 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B3 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B4 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
B2: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B3: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]

## benign; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 13.82 [13.485, 14.1851] | 2.925 [2.84, 3] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0.205 [0.129875, 0.29] | 0.02 [0, 0.04] | 0 [0, 0] | 2.765 [2.705, 2.82] | 10.83 [10.535, 11.15] |
| B1 | 314.95 [314.765, 315.13] | 0 [0, 0] | 307.92 [306.5, 309.352] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 305.95 [305.765, 306.13] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9 [9, 9] |
| B2-K0 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B2 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B3 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |
| B4 | 9.395 [9.255, 9.56] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.95 [2.765, 3.13] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.015 [9, 9.045] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | -7.76581e-12 [-4.53929e-11, 3.02907e-11] | 0/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 6 [6, 6] | 0/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0 | 0 | 0 | 0 |
| B2-K0 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B2 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B3 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B4 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
B2: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B3: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]

## benign; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 17.055 [16.6749, 17.4701] | 2.925 [2.84, 3] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0.205 [0.129875, 0.29] | 0.005 [0, 0.015] | 0 [0, 0] | 2.78 [2.72, 2.835] | 14.065 [13.715, 14.435] |
| B1 | 314.95 [314.765, 315.13] | 0 [0, 0] | 307.92 [306.5, 309.352] | 2.95 [2.765, 3.13] | 0 [0, 0] | 0 [0, 0] | 305.95 [305.765, 306.13] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9 [9, 9] |
| B2-K0 | 9.41 [9.26, 9.58012] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 0 [0, 0] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B2 | 9.41 [9.26, 9.58012] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B3 | 9.41 [9.26, 9.58012] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |
| B4 | 9.41 [9.26, 9.58012] | 0.195 [0.14, 0.255] | 142.697 [141.021, 144.237] | 2.955 [2.77, 3.13512] | 0 [0, 0] | 6 [6, 6] | 0.38 [0.24, 0.535125] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 9.03 [9, 9.09] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | -7.76581e-12 [-4.53929e-11, 3.02907e-11] | 0/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 6 [6, 6] | 0/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0 | 0 | 0 | 0 |
| B2-K0 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B2 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B3 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
| B4 | 200/1200 (0.166667) | 0 | 0 | 0 | 0 |
B2: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B3: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B4: Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.
B2/B3 share of differing weeks: 0 [0, 0]
B2/B4 share of differing weeks: 0 [0, 0]
B3/B4 share of differing weeks: 0 [0, 0]

## moderate; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 13.57 [12.9199, 14.2451] | 2.775 [2.66, 2.895] | 0 [0, 0] | 0.735 [0.53, 0.965] | 0 [0, 0] | 0 [0, 0] | 2.12 [1.66987, 2.62] | 0.78 [0.63, 0.95] | 0 [0, 0] | 1.775 [1.695, 1.85] | 8.895 [8.61, 9.19] |
| B1 | 354.225 [353.79, 354.66] | 0.005 [0, 0.015] | 293.025 [287.141, 298.828] | 10.195 [9.705, 10.6901] | 0 [0, 0] | 0 [0, 0] | 346.195 [345.705, 346.69] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 8.03 [7.86, 8.19] |
| B2-K0 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 0 [0, 0] | 3.73 [3.19487, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |
| B2 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 6 [6, 6] | 3.73 [3.19487, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |
| B3 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 6 [6, 6] | 3.73 [3.19487, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |
| B4 | 12.37 [11.77, 12.98] | 0.805 [0.694875, 0.920125] | 40.1433 [37.33, 42.7854] | 10.455 [9.96, 10.96] | 0 [0, 0] | 6 [6, 6] | 3.73 [3.19487, 4.29012] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.635 [8.415, 8.86] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | 0 [0, 0] | 200/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 5.52004e-13 [-3.27723e-12, 4.33985e-12] | 3/200 |
| Plan churn (changed placements) | 0 [0, 0] | 200/200 |
| Intervention cost (man-hours) | 0 [0, 0] | 200/200 |
| Unused intervention weeks (weeks) | 6 [6, 6] | 0/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.286667 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.286667 | 0 | 0 | 0 |
| B2-K0 | 401/1200 (0.334167) | 0.286667 | 0 | 0 | 0 |
| B2 | 401/1200 (0.334167) | 0.286667 | 0 | 0 | 0 |
| B3 | 401/1200 (0.334167) | 0.286667 | 0 | 0 | 0 |
| B4 | 401/1200 (0.334167) | 0.286667 | 0 | 0 | 0 |
B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.286667 [0.275833, 0.2975]
B2/B4 share of differing weeks: 0.286667 [0.275833, 0.2975]
B3/B4 share of differing weeks: 0 [0, 0]

## moderate; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 14.935 [14.2498, 15.66] | 2.775 [2.66, 2.895] | 0 [0, 0] | 0.645 [0.46, 0.855] | 0 [0, 0] | 0 [0, 0] | 2.12 [1.66987, 2.62] | 0.91 [0.735, 1.10512] | 0 [0, 0] | 1.755 [1.675, 1.83] | 10.15 [9.82, 10.4801] |
| B1 | 354.225 [353.79, 354.66] | 0.005 [0, 0.015] | 293.025 [287.141, 298.828] | 10.195 [9.705, 10.6901] | 0 [0, 0] | 0 [0, 0] | 346.195 [345.705, 346.69] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 8.03 [7.86, 8.19] |
| B2-K0 | 12.65 [12, 13.3101] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.97] | 0 [0, 0] | 0 [0, 0] | 3.72 [3.185, 4.28] | 0.02 [0, 0.05] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19012] |
| B2 | 12.635 [11.9999, 13.2851] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.9651] | 0.12 [0, 0.28] | 5.985 [5.965, 6] | 3.72 [3.185, 4.28] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19012] |
| B3 | 12.635 [11.9999, 13.2851] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.9651] | 0.12 [0, 0.28] | 5.985 [5.965, 6] | 3.72 [3.185, 4.28] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19012] |
| B4 | 12.635 [11.9999, 13.2851] | 0.805 [0.694875, 0.920125] | 40.0591 [37.2584, 42.7231] | 10.465 [9.975, 10.9651] | 0.12 [0, 0.28] | 5.985 [5.965, 6] | 3.72 [3.185, 4.28] | 0.005 [0, 0.015] | 0 [0, 0] | 0 [0, 0] | 8.91 [8.65, 9.19012] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 5.98713e-13 [-3.24506e-12, 4.37674e-12] | 4/200 |
| Plan churn (changed placements) | 0 [-0.015, 0.015] | 198/200 |
| Intervention cost (man-hours) | 0.12 [0, 0.28] | 197/200 |
| Unused intervention weeks (weeks) | 5.985 [5.965, 6] | 0/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | -0.015 [-0.04, 0] | 198/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0 [0, 0] | 200/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.2875 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.2875 | 0 | 0 | 0 |
| B2-K0 | 401/1200 (0.334167) | 0.2875 | 0 | 0 | 0 |
| B2 | 401/1200 (0.334167) | 0.2875 | 0 | 3 | 0 |
| B3 | 401/1200 (0.334167) | 0.2875 | 0 | 3 | 0 |
| B4 | 401/1200 (0.334167) | 0.2875 | 0 | 3 | 0 |
B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.2875 [0.276667, 0.298333]
B2/B4 share of differing weeks: 0.2875 [0.276667, 0.298333]
B3/B4 share of differing weeks: 0 [0, 0]

## moderate; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 18.56 [17.775, 19.395] | 2.775 [2.66, 2.895] | 0 [0, 0] | 0.51 [0.35, 0.695] | 0 [0, 0] | 0 [0, 0] | 2.12 [1.66987, 2.62] | 1.355 [1.135, 1.62] | 0 [0, 0] | 1.67 [1.59, 1.74012] | 13.415 [13, 13.835] |
| B1 | 354.225 [353.79, 354.66] | 0.005 [0, 0.015] | 293.025 [287.141, 298.828] | 10.195 [9.705, 10.6901] | 0 [0, 0] | 0 [0, 0] | 346.195 [345.705, 346.69] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 8.03 [7.86, 8.19] |
| B2-K0 | 13.45 [12.6549, 14.2751] | 0.805 [0.694875, 0.920125] | 39.7823 [37.0063, 42.5366] | 10.49 [10, 11.0001] | 0 [0, 0] | 0 [0, 0] | 3.72 [3.185, 4.28] | 0.13 [0.055, 0.22] | 0 [0, 0] | 0 [0, 0] | 9.6 [9.19987, 10.0351] |
| B2 | 13.43 [12.6349, 14.2401] | 0.805 [0.694875, 0.920125] | 39.9993 [37.2071, 42.7081] | 10.56 [10.065, 11.0853] | 0.4 [0.2, 0.64] | 5.95 [5.92, 5.975] | 3.72 [3.185, 4.28] | 0.035 [0, 0.09] | 0 [0, 0] | 0 [0, 0] | 9.675 [9.25, 10.125] |
| B3 | 13.43 [12.6349, 14.2401] | 0.805 [0.694875, 0.920125] | 39.9993 [37.2071, 42.7081] | 10.56 [10.065, 11.0853] | 0.4 [0.2, 0.64] | 5.95 [5.92, 5.975] | 3.72 [3.185, 4.28] | 0.035 [0, 0.09] | 0 [0, 0] | 0 [0, 0] | 9.675 [9.25, 10.125] |
| B4 | 13.43 [12.6349, 14.2401] | 0.805 [0.694875, 0.920125] | 39.9993 [37.2071, 42.7081] | 10.56 [10.065, 11.0853] | 0.4 [0.2, 0.64] | 5.95 [5.92, 5.975] | 3.72 [3.185, 4.28] | 0.035 [0, 0.09] | 0 [0, 0] | 0 [0, 0] | 9.675 [9.25, 10.125] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -0.02 [-0.05, 0] | 198/200 |
| Unplanned failures (failures) | 0 [0, 0] | 200/200 |
| Wasted life at removal (flight cycles) | 0.216929 [0.0254384, 0.499145] | 4/200 |
| Plan churn (changed placements) | 0.07 [0.005, 0.15] | 193/200 |
| Intervention cost (man-hours) | 0.4 [0.2, 0.64] | 190/200 |
| Unused intervention weeks (weeks) | 5.95 [5.92, 5.975] | 0/200 |
| Grounded waiting for spare (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for bay (aircraft-days) | -0.095 [-0.175, -0.03] | 193/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0.075 [0.025, 0.135] | 193/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.289167 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.289167 | 0 | 0 | 0 |
| B2-K0 | 401/1200 (0.334167) | 0.289167 | 0 | 0 | 0 |
| B2 | 401/1200 (0.334167) | 0.289167 | 0 | 10 | 0 |
| B3 | 401/1200 (0.334167) | 0.289167 | 0 | 10 | 0 |
| B4 | 401/1200 (0.334167) | 0.289167 | 0 | 10 | 0 |
B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.289167 [0.278333, 0.299167]
B2/B4 share of differing weeks: 0.289167 [0.278333, 0.299167]
B3/B4 share of differing weeks: 0 [0, 0]

## stressed; assumed repair 1.5x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 31.22 [28.8749, 33.5654] | 2.88 [2.725, 3.03] | 0 [0, 0] | 8.17 [7.265, 9.12012] | 0 [0, 0] | 0 [0, 0] | 26.995 [24.5648, 29.4405] | 0 [0, 0] | 0 [0, 0] | 0.14 [0.095, 0.185] | 4.085 [3.845, 4.315] |
| B1 | 383.135 [382.35, 383.93] | 0.07 [0.035, 0.105] | 88.8589 [83.9028, 93.5633] | 10.54 [9.68975, 11.4051] | 0 [0, 0] | 0 [0, 0] | 380.54 [379.69, 381.405] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 2.595 [2.465, 2.72] |
| B2-K0 | 39.725 [37.7897, 41.7301] | 1.78 [1.625, 1.94512] | 10.5052 [8.6159, 12.6255] | 10.775 [9.90987, 11.675] | 0 [0, 0] | 0 [0, 0] | 36.63 [34.67, 38.6803] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.095 [2.9, 3.29] |
| B2 | 36.03 [33.9696, 38.1854] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.505 [3.35, 3.65] |
| B3 | 36.03 [33.9696, 38.1854] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.505 [3.35, 3.65] |
| B4 | 36.03 [33.9696, 38.1854] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.505 [3.35, 3.65] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -3.695 [-3.97, -3.415] | 38/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.621178 [0.173231, 1.25948] | 71/200 |
| Plan churn (changed placements) | 0.8 [0.73, 0.865] | 42/200 |
| Intervention cost (man-hours) | 6.68 [6.24, 7.08] | 33/200 |
| Unused intervention weeks (weeks) | 5.165 [5.115, 5.22] | 0/200 |
| Grounded waiting for spare (aircraft-days) | -4.105 [-4.35, -3.84] | 33/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0.41 [0.269875, 0.56] | 166/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.219167 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.219167 | 0 | 0 | 0 |
| B2-K0 | 605/1200 (0.504167) | 0.219167 | 0 | 0 | 0 |
| B2 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
| B3 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
| B4 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.219167 [0.195833, 0.244167]
B2/B4 share of differing weeks: 0.219167 [0.195833, 0.244167]
B3/B4 share of differing weeks: 0 [0, 0]

## stressed; assumed repair 2x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 31.865 [29.53, 34.2054] | 2.88 [2.725, 3.03] | 0 [0, 0] | 8.17 [7.265, 9.12012] | 0 [0, 0] | 0 [0, 0] | 26.995 [24.5648, 29.4405] | 0 [0, 0] | 0 [0, 0] | 0.14 [0.095, 0.185] | 4.73 [4.44488, 5.01] |
| B1 | 383.135 [382.35, 383.93] | 0.07 [0.035, 0.105] | 88.8589 [83.9028, 93.5633] | 10.54 [9.68975, 11.4051] | 0 [0, 0] | 0 [0, 0] | 380.54 [379.69, 381.405] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 2.595 [2.465, 2.72] |
| B2-K0 | 39.93 [38, 41.9551] | 1.78 [1.625, 1.94512] | 10.5052 [8.6159, 12.6255] | 10.775 [9.90987, 11.675] | 0 [0, 0] | 0 [0, 0] | 36.63 [34.67, 38.6803] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.3 [3.065, 3.54012] |
| B2 | 36.295 [34.2146, 38.48] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.77 [3.56, 3.97] |
| B3 | 36.295 [34.2146, 38.48] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.77 [3.56, 3.97] |
| B4 | 36.295 [34.2146, 38.48] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.77 [3.56, 3.97] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -3.635 [-3.92, -3.35] | 41/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.621178 [0.173231, 1.25948] | 71/200 |
| Plan churn (changed placements) | 0.8 [0.73, 0.865] | 42/200 |
| Intervention cost (man-hours) | 6.68 [6.24, 7.08] | 33/200 |
| Unused intervention weeks (weeks) | 5.165 [5.115, 5.22] | 0/200 |
| Grounded waiting for spare (aircraft-days) | -4.105 [-4.35, -3.84] | 33/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0.47 [0.31, 0.64] | 163/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.219167 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.219167 | 0 | 0 | 0 |
| B2-K0 | 605/1200 (0.504167) | 0.219167 | 0 | 0 | 0 |
| B2 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
| B3 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
| B4 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.219167 [0.195833, 0.244167]
B2/B4 share of differing weeks: 0.219167 [0.195833, 0.244167]
B3/B4 share of differing weeks: 0 [0, 0]

## stressed; assumed repair 3x

| Policy | Aircraft-days unserviceable (AOG) (aircraft-days) | Unplanned failures (failures) | Wasted life at removal (flight cycles) | Plan churn (changed placements) | Intervention cost (man-hours) | Unused intervention weeks (weeks) | Grounded waiting for spare (aircraft-days) | Grounded waiting for bay (aircraft-days) | Grounded waiting for crew (aircraft-days) | Grounded waiting for permitted slot (aircraft-days) | Induction or repair duration (aircraft-days) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0 | 33.495 [31.2347, 35.8051] | 2.88 [2.725, 3.03] | 0 [0, 0] | 8.17 [7.265, 9.12012] | 0 [0, 0] | 0 [0, 0] | 26.995 [24.5648, 29.4405] | 0 [0, 0] | 0 [0, 0] | 0.14 [0.095, 0.185] | 6.36 [5.89975, 6.79512] |
| B1 | 383.135 [382.35, 383.93] | 0.07 [0.035, 0.105] | 88.8589 [83.9028, 93.5633] | 10.54 [9.68975, 11.4051] | 0 [0, 0] | 0 [0, 0] | 380.54 [379.69, 381.405] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 2.595 [2.465, 2.72] |
| B2-K0 | 40.46 [38.4846, 42.5055] | 1.78 [1.625, 1.94512] | 10.5052 [8.6159, 12.6255] | 10.775 [9.90987, 11.675] | 0 [0, 0] | 0 [0, 0] | 36.63 [34.67, 38.6803] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 3.83 [3.465, 4.2] |
| B2 | 36.985 [34.8547, 39.2251] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 4.46 [4.10488, 4.81513] |
| B3 | 36.985 [34.8547, 39.2251] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 4.46 [4.10488, 4.81513] |
| B4 | 36.985 [34.8547, 39.2251] | 1.775 [1.625, 1.94] | 11.1264 [9.22229, 13.2962] | 11.575 [10.7099, 12.4552] | 6.68 [6.24, 7.08] | 5.165 [5.115, 5.22] | 32.525 [30.4744, 34.68] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 4.46 [4.10488, 4.81513] |

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
All outcomes tied: 200/200

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
All outcomes tied: 200/200

### B2 minus B2-K0 (paired)

| Outcome | Mean difference [95% CI] | Exact scenario ties |
| --- | --- | --- |
| Aircraft-days unserviceable (AOG) (aircraft-days) | -3.475 [-3.775, -3.165] | 47/200 |
| Unplanned failures (failures) | -0.005 [-0.015, 0] | 199/200 |
| Wasted life at removal (flight cycles) | 0.621178 [0.173231, 1.25948] | 71/200 |
| Plan churn (changed placements) | 0.8 [0.73, 0.865] | 42/200 |
| Intervention cost (man-hours) | 6.68 [6.24, 7.08] | 33/200 |
| Unused intervention weeks (weeks) | 5.165 [5.115, 5.22] | 0/200 |
| Grounded waiting for spare (aircraft-days) | -4.105 [-4.35, -3.84] | 33/200 |
| Grounded waiting for bay (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for crew (aircraft-days) | 0 [0, 0] | 200/200 |
| Grounded waiting for permitted slot (aircraft-days) | 0 [0, 0] | 200/200 |
| Induction or repair duration (aircraft-days) | 0.63 [0.419875, 0.845] | 158/200 |
All outcomes tied: 0/200

### Chosen-tail differences

| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4 choice difference share | Expedites | Crew shifts | Bays |
| --- | --- | --- | --- | --- | --- |
| B0 | 0/1200 (0) | 0.219167 | 0 | 0 | 0 |
| B1 | 0/1200 (0) | 0.219167 | 0 | 0 | 0 |
| B2-K0 | 605/1200 (0.504167) | 0.219167 | 0 | 0 | 0 |
| B2 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
| B3 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
| B4 | 565/1200 (0.470833) | 0.219167 | 167 | 0 | 0 |
B2: Opportunity share is descriptive; ties do not establish policy equivalence.
B3: Opportunity share is descriptive; ties do not establish policy equivalence.
B4: Opportunity share is descriptive; ties do not establish policy equivalence.
B2/B3 share of differing weeks: 0.219167 [0.195833, 0.244167]
B2/B4 share of differing weeks: 0.219167 [0.195833, 0.244167]
B3/B4 share of differing weeks: 0 [0, 0]
