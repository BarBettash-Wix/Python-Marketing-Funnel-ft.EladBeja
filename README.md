# Funnel Simulator - Phase 2

Phase 2 extends the basic funnel simulator with advanced analytics: multiple simulations, price effects, configurable funnels, and budget optimization.

## Phase 2 Functions

### 1. Multiple Simulations - `run_multiple_simulations()`

Runs N simulations and calculates averaged results for statistical reliability.

```python
def run_multiple_simulations(num_simulations, seed_base, **funnel_params):
    random.seed(seed_base)  # Reproducibility
    results = []
    for i in range(num_simulations):
        result = configurable_funnel(**funnel_params)
        results.append(result)
    
    # Calculate averages
    avg_revenue = calculate_average([r["total_revenue"] for r in results])
    avg_roi = calculate_average([r["roi"] for r in results])
    # ... more averaging logic
```

**How it calculates:** Collects results from N runs, then calculates `sum(values) / len(values)` for each metric.

### 2. Price Effects - `funnel_with_price_change()`

Adjusts conversion rates based on price changes with step-specific sensitivities.

```python
def funnel_with_price_change(price_change=0.0, funnel_config=None, **funnel_params):
    # Define sensitivities for each step
    step_sensitivities = {
        "registered": 0.1,           # Low sensitivity (early funnel)
        "site_created": 0.0,         # No price effect
        "premium": 0.5,              # Medium (payment step)
        "premium_no_trial_churn": 0.8 # High (retention sensitive)
    }
    
    # Apply price effects using apply_price_effect()
    for step_name, (min_rate, max_rate) in funnel_config.items():
        sensitivity = step_sensitivities.get(step_name, 0.0)
        new_min = apply_price_effect(min_rate, price_change, sensitivity)
        new_max = apply_price_effect(max_rate, price_change, sensitivity)
```

**How it calculates:** `new_rate = original_rate * (1 - price_change * sensitivity)`
- Price increase (+0.1) reduces conversion rates
- Discount (-0.1) improves conversion rates

### 3. Configurable Funnels - `configurable_funnel()`

Runs simulation with custom funnel steps and conversion ranges.

```python
def configurable_funnel(funnel_config=None, **funnel_params):
    if funnel_config is None:
        funnel_config = default_funnel_config()  # Use Phase 1 defaults
    
    step_names = list(funnel_config.keys())
    current_users = landing_page_visits(budget, cost_per_user)
    
    for i, step_name in enumerate(step_names):
        rate = conversion_rate(funnel_config, step_name, uplift_tracker)
        users = rate * current_users
        
        # Apply threshold effects only to first step
        if i == 0:
            position = position_in_range(users, low_threshold, high_threshold)
            if position == 1: users *= (1 - neg_effect_high)    # Server overload
            elif position == -1: users *= (1 - neg_effect_low)  # Low engagement
            else: users *= (1 + pos_effect)                     # Optimal range
```

**How it works:** Processes steps dynamically from `funnel_config` dictionary instead of hardcoded steps.

### 4. Budget Optimization - `optimize_budget()`

Tests multiple budgets and finds the one with highest ROI.

```python
def optimize_budget(budget_list, num_sims_per_budget=1, **other_params):
    results = []
    for budget in budget_list:
        if num_sims_per_budget == 1:
            result = configurable_funnel(budget=budget, **other_params)
        else:
            result = run_multiple_simulations(num_sims_per_budget, 42, 
                                            budget=budget, **other_params)
        
        results.append({"budget": budget, "roi": result["roi"]})
    
    # Find maximum ROI
    best = max(results, key=lambda x: x["roi"])
    return {"optimal_budget": best["budget"], "optimal_roi": best["roi"]}
```

**How it calculates:** Compares ROI across all budget options using `max(results, key=lambda x: x["roi"])`.

## Usage

```python
# Multiple simulations
avg_result = run_multiple_simulations(10, 42, budget=20000000, cost_per_user=15, ...)

# Price effects  
discount_result = funnel_with_price_change(price_change=-0.1, budget=20000000, ...)

# Custom funnel
custom_config = {"signup": (0.2, 0.4), "purchase": (0.1, 0.3)}
custom_result = configurable_funnel(funnel_config=custom_config, budget=20000000, ...)

# Budget optimization
optimization = optimize_budget([15000000, 20000000, 25000000], num_sims_per_budget=5, ...)
```

## Helper Functions

### `calculate_average(numbers)`
```python
def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)
```

### `apply_price_effect(original_rate, price_change, step_sensitivity)`
```python
def apply_price_effect(original_rate, price_change, step_sensitivity):
    new_rate = original_rate * (1 - price_change * step_sensitivity)
    return max(0.0, min(1.0, new_rate))  # Clamp between 0-1
```

## Run Tests
```bash
python3 PythonWorkshopFunnelSimulatorPhase2.py  # Comprehensive testing
```
