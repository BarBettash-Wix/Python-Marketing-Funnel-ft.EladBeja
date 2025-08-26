# Funnel Simulator Phase 2

A Python implementation of an advanced marketing funnel simulator with multiple simulations, price effects, configurable steps, and budget optimization.

## Functions Overview

### Core Utility Functions

#### `calculate_average(numbers)`
- **Purpose**: Calculate the average of a list of numbers
- **Parameters**: `numbers` - list of numeric values
- **Returns**: Average value (0 if list is empty)

#### `apply_price_effect(original_rate, price_change, step_sensitivity)`
- **Purpose**: Apply price change effects to conversion rates
- **Parameters**: 
  - `original_rate` - base conversion rate
  - `price_change` - price change percentage (positive = increase, negative = discount)
  - `step_sensitivity` - how sensitive this step is to price changes (0.0 to 1.0)
- **Returns**: Modified conversion rate (clamped between 0.0 and 1.0)

### Configuration Functions

#### `default_funnel_config()`
- **Purpose**: Provides the default funnel configuration matching Phase 1
- **Returns**: Dictionary with step names and conversion rate ranges
- **Steps**: registered → site_created → premium → premium_no_trial_churn

### Main Simulation Functions

#### `configurable_funnel(funnel_config=None, **funnel_params)`
- **Purpose**: Run a single funnel simulation with configurable steps
- **Parameters**: 
  - `funnel_config` - dictionary defining steps and conversion ranges (optional)
  - `**funnel_params` - budget, costs, thresholds, and other simulation parameters
- **Returns**: Dictionary with users_per_step, total_revenue, roi, applied_rates, uplift_triggered
- **Features**: Supports any number of custom steps, applies threshold effects to first step only

#### `run_multiple_simulations(num_simulations, seed_base, **funnel_params)`
- **Purpose**: Run multiple simulations and return averaged results
- **Parameters**:
  - `num_simulations` - number of simulations to run
  - `seed_base` - random seed for reproducibility
  - `**funnel_params` - simulation parameters
- **Returns**: Averaged results across all simulations
- **Features**: Statistical averaging, uplift frequency analysis, reproducible results

#### `funnel_with_price_change(price_change=0.0, funnel_config=None, **funnel_params)`
- **Purpose**: Run simulation with price change effects applied to conversion rates
- **Parameters**:
  - `price_change` - percentage price change (e.g., 0.1 = 10% increase, -0.1 = 10% discount)
  - `funnel_config` - optional custom funnel configuration
  - `**funnel_params` - simulation parameters
- **Returns**: Simulation results with price-adjusted conversion rates
- **Features**: Step-specific price sensitivities, realistic business impact modeling

#### `optimize_budget(budget_list, num_sims_per_budget=1, **other_params)`
- **Purpose**: Find the optimal budget that maximizes ROI
- **Parameters**:
  - `budget_list` - list of budget amounts to test
  - `num_sims_per_budget` - simulations per budget (default: 1)
  - `**other_params` - simulation parameters
- **Returns**: Dictionary with optimal_budget, optimal_roi, budget_analysis, and recommendation
- **Features**: Comprehensive budget analysis, data-driven recommendations

## Usage Example

```python
from PythonWorkshopFunnelSimulatorPhase2 import *

# Basic parameters
params = {
    'budget': 20000000,
    'cost_per_user': 15,
    'low_threshold': 400000,
    'high_threshold': 1200000,
    'neg_effect_low': 0.3,
    'neg_effect_high': 0.2,
    'pos_effect': 0.2,
    'average_revenue_per_paying_user': 120
}

# Single simulation
result = configurable_funnel(**params)

# Multiple simulations with averaging
avg_result = run_multiple_simulations(10, 42, **params)

# Price effect simulation
discount_result = funnel_with_price_change(price_change=-0.1, **params)

# Budget optimization
optimization = optimize_budget([15000000, 20000000, 25000000], **params)
```

## Testing & Running the Code

### Quick Start
```bash
# Run the main script to see all Phase 2 features in action
python3 PythonWorkshopFunnelSimulatorPhase2.py
```

### Manual Testing Examples

#### Test 1: Basic Single Simulation
```python
from PythonWorkshopFunnelSimulatorPhase2 import *

# Test basic functionality
params = {
    'budget': 20000000,
    'cost_per_user': 15,
    'low_threshold': 400000,
    'high_threshold': 1200000,
    'neg_effect_low': 0.3,
    'neg_effect_high': 0.2,
    'pos_effect': 0.2,
    'average_revenue_per_paying_user': 120
}

result = configurable_funnel(**params)
print("Single simulation result:")
print(f"ROI: {result['roi']:.2%}")
print(f"Revenue: ${result['total_revenue']:,.2f}")
print(f"Users per step: {result['users_per_step']}")
```

#### Test 2: Multiple Simulations with Averaging
```python
# Test statistical averaging
avg_result = run_multiple_simulations(5, 42, **params)
print("\nAverage results across 5 simulations:")
print(f"Average ROI: {avg_result['roi']:.2%}")
print(f"Average Revenue: ${avg_result['total_revenue']:,.2f}")
print(f"Uplift triggered: {avg_result['uplift_triggered']}")
```

#### Test 3: Price Effect Testing
```python
# Test price sensitivity
print("\nPrice Effect Testing:")

# 10% discount
discount_result = funnel_with_price_change(price_change=-0.1, **params)
print(f"10% Discount ROI: {discount_result['roi']:.2%}")

# 10% price increase  
increase_result = funnel_with_price_change(price_change=0.1, **params)
print(f"10% Increase ROI: {increase_result['roi']:.2%}")

# No price change (baseline)
baseline_result = funnel_with_price_change(price_change=0.0, **params)
print(f"Baseline ROI: {baseline_result['roi']:.2%}")
```

#### Test 4: Custom Funnel Configuration
```python
# Test configurable funnel steps
custom_funnel = {
    "signup": (0.2, 0.4),
    "activate": (0.5, 0.7),
    "purchase": (0.1, 0.3)
}

custom_result = configurable_funnel(funnel_config=custom_funnel, **params)
print(f"\nCustom funnel steps: {list(custom_result['users_per_step'].keys())}")
print(f"Custom funnel ROI: {custom_result['roi']:.2%}")
```

#### Test 5: Budget Optimization
```python
# Test budget optimization
budgets_to_test = [15000000, 20000000, 25000000, 30000000]
optimization = optimize_budget(budgets_to_test, num_sims_per_budget=3, **params)

print(f"\nBudget Optimization Results:")
print(f"Optimal Budget: ${optimization['optimal_budget']:,}")
print(f"Optimal ROI: {optimization['optimal_roi']:.2%}")
print(f"Recommendation: {optimization['recommendation']}")
```

### Validation Tests

#### Test Utility Functions
```python
# Test helper functions
print("Testing utility functions:")

# Test calculate_average
numbers = [10, 20, 30, 40, 50]
avg = calculate_average(numbers)
print(f"Average of {numbers} = {avg} (Expected: 30)")

# Test apply_price_effect
original_rate = 0.4
price_change = 0.1  # 10% increase
sensitivity = 0.5
new_rate = apply_price_effect(original_rate, price_change, sensitivity)
print(f"Price effect: {original_rate} → {new_rate} (Expected: ~0.38)")

# Test edge cases
empty_avg = calculate_average([])
print(f"Empty list average: {empty_avg} (Expected: 0)")

extreme_rate = apply_price_effect(0.1, 2.0, 1.0)  # Should clamp to 0
print(f"Extreme price effect: {extreme_rate} (Expected: 0.0)")
```

### Expected Output Verification

When running the main script, you should see output demonstrating:
1. **Single simulation** - Basic funnel results with ROI and user counts
2. **Multiple simulations** - Averaged results showing statistical stability
3. **Budget optimization** - Analysis of different budget levels with recommendation

All results should include:
- `users_per_step` dictionary with landing_page and all funnel steps
- `total_revenue` as a float value
- `roi` as a float (can be negative if costs exceed revenue)
- `applied_rates` showing actual conversion rates used
- `uplift_triggered` with boolean values for each step

## Features

- **Multiple Simulations**: Statistical averaging across multiple runs
- **Price Sensitivity**: Realistic price change effects on different funnel steps  
- **Configurable Funnels**: Support for any number of custom steps and conversion ranges
- **Budget Optimization**: Data-driven budget recommendations for maximum ROI
- **Backward Compatibility**: Works with Phase 1 requirements and format
- **Assignment Compliant**: Meets all university assignment requirements

## Output Format

All functions return dictionaries with:
- `users_per_step`: User counts at each funnel step (including landing_page)
- `total_revenue`: Total revenue generated
- `roi`: Return on investment 
- `applied_rates`: Actual conversion rates used
- `uplift_triggered`: Boolean values indicating uplift application
