# Python Marketing Funnel Simulator

## 🎯 What This Project Does

A **data-driven marketing funnel simulator** that helps businesses optimize their marketing budget and understand customer conversion patterns.

**Input:** Marketing budget, user costs, conversion rates  
**Output:** Revenue projections, ROI analysis, optimal budget recommendations

## 🤔 Why I Built This

**Problem:** Marketing teams need to predict ROI and optimize budgets before spending millions on campaigns.

**Solution:** Built a sophisticated simulator that models real-world scenarios:
- Random conversion rate variations
- Volume-based performance effects (server overload, low engagement)
- Price sensitivity across different funnel steps
- Statistical averaging for reliable predictions

## 🚀 Key Features

### Phase 1: Basic Simulator
- **Core funnel modeling** with 4 steps: Landing → Registration → Site Creation → Premium → Retention
- **Volume threshold effects** (performance drops at high/low volumes)
- **Random uplifts** (50% chance of 5% conversion boost per step)
- **ROI calculation** with realistic business parameters

### Phase 2: Advanced Analytics  
- **📊 Multiple Simulations** - Run N simulations, get averaged results
- **💰 Price Effects** - Model how discounts/increases affect conversion rates
- **⚙️ Configurable Funnels** - Define custom steps for any business model
- **🎯 Budget Optimization** - Find the budget that maximizes ROI

## 📈 Business Impact

**Real Example:** With $20M budget:
- **10% Discount:** ROI improves by ~10%
- **Optimal Budget:** $25M generates highest ROI (-72% vs -75% at $20M)
- **Statistical Confidence:** Average across multiple runs eliminates random variance

## ⚡ Quick Start

```bash
# Run complete simulation with all features
python3 PythonWorkshopFunnelSimulatorPhase2.py
```

**Key Functions:**
- `configurable_funnel()` - Single simulation
- `run_multiple_simulations()` - Statistical averaging  
- `funnel_with_price_change()` - Price sensitivity analysis
- `optimize_budget()` - Find optimal ROI budget

## 💻 Technical Implementation

- **Language:** Pure Python (no external libraries)
- **Architecture:** Modular functions with configurable parameters
- **Testing:** Comprehensive test suite with 100% requirement coverage
- **Reproducibility:** Random seed control for consistent results

## 📊 Results Format

```python
{
    "users_per_step": {"landing_page": 1333333, "registered": 655473, ...},
    "total_revenue": 6420000.0,
    "roi": -0.679,  # Can be negative if costs > revenue
    "applied_rates": {"registered": 0.436, "site_created": 0.475, ...},
    "uplift_triggered": {"registered": True, "premium": False, ...}
}
```

---
*Built for university Data Engineering course - Marketing Analytics project*
