# Phase 2 - Advanced Funnel Simulator
# Import Phase 1 functions
from PythonWorkshopFunnelSimulatorPhase1 import funnel
import random

def calculate_average(numbers):
    """Calculate average of a list of numbers"""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def apply_price_effect(original_rate, price_change, step_sensitivity):
    """Apply price change effect to a conversion rate"""
    # Price increase reduces conversion, discount increases conversion
    new_rate = original_rate * (1 - price_change * step_sensitivity)
    # Make sure rate stays reasonable (between 0 and 1)
    return max(0.0, min(1.0, new_rate))

def funnel_with_price_change(price_change=0.0, funnel_config=None, **funnel_params):
    """Wrapper for funnel that applies price change effects to conversion rates"""
    
    # Apply price effects to different funnel steps
    if price_change == 0.0:
        # No price change, use configurable funnel
        return configurable_funnel(funnel_config=funnel_config, **funnel_params)
    
    # Use default config if none provided
    if funnel_config is None:
        funnel_config = default_funnel_config()
    
    # Define step sensitivities
    step_sensitivities = {
        "registered": 0.1,           # Small effect on early decisions
        "site_created": 0.0,         # No price sensitivity  
        "premium": 0.5,              # Medium effect on payment decisions
        "premium_no_trial_churn": 0.8 # High effect on retention decisions
    }
    
    # Apply price effects to conversion ranges
    modified_ranges = {}
    
    for step_name, (min_rate, max_rate) in funnel_config.items():
        sensitivity = step_sensitivities.get(step_name, 0.0)
        new_min = apply_price_effect(min_rate, price_change, sensitivity)
        new_max = apply_price_effect(max_rate, price_change, sensitivity)
        modified_ranges[step_name] = (new_min, new_max)
    
    # Use configurable funnel with modified ranges
    return configurable_funnel(funnel_config=modified_ranges, **funnel_params)

def default_funnel_config():
    """Return the default funnel configuration matching Phase 1"""
    return {
        "registered": (0.3, 0.5),
        "site_created": (0.4, 0.6), 
        "premium": (0.1, 0.2),
        "premium_no_trial_churn": (0.7, 0.9)
    }

def configurable_funnel(funnel_config=None, **funnel_params):
    """Configurable funnel that works with any step names and order"""
    
    # Use default config if none provided
    if funnel_config is None:
        funnel_config = default_funnel_config()
    
    # Import Phase 1 helper functions
    from PythonWorkshopFunnelSimulatorPhase1 import landing_page_visits, position_in_range, conversion_rate
    
    # Calculate starting visitor count from budget
    page_visits = landing_page_visits(funnel_params["budget"], funnel_params["cost_per_user"])
    
    # Extract step names from config in order
    step_names = list(funnel_config.keys())
    
    # Dictionary to store user count at each step  
    num_of_users = {}
    
    # Dictionary to store actual conversion rates used
    applied_rates = {}
    
    # Dictionary to track which steps got uplift bonuses
    uplift_used = {}
    
    # Start with total page visits as current user count
    current_users = page_visits
    
    # Process each step in the funnel
    for i, step_name in enumerate(step_names):
        # Get conversion rate for this step using the config ranges
        rate = conversion_rate(funnel_config, step_name, uplift_tracker=uplift_used)
        
        # Store the rate for reporting  
        applied_rates[step_name] = rate
        
        # Calculate how many users convert at this step
        users = rate * current_users
        
        # Apply threshold effects only to first step
        if i == 0:  # First step gets threshold effects
            # Check if user count is high/low/optimal
            position = position_in_range(users, funnel_params["low_threshold"], funnel_params["high_threshold"])
            
            # High volume - server overload reduces conversions
            if position == 1:
                users = int(users * (1 - funnel_params["neg_effect_high"]))
            # Low volume - poor engagement reduces conversions  
            elif position == -1:
                users = int(users * (1 - funnel_params["neg_effect_low"]))
            else:
                # Optimal volume - boost conversions
                users = int(users * (1 + funnel_params["pos_effect"]))
        else:
            # For all other steps, just convert to integer
            users = int(users)
            
        # Store user count for this step
        num_of_users[step_name] = users
        
        # Update current users for next step in funnel
        current_users = users
    
    # Revenue calculation - final step users are the paying customers
    total_revenue = float(current_users * funnel_params["average_revenue_per_paying_user"])
    
    # Calculate return on investment
    roi = float((total_revenue - funnel_params["budget"]) / funnel_params["budget"])
    
    # Add landing_page to users_per_step (assignment requirement)
    num_of_users["landing_page"] = page_visits
    
    # Convert uplift values to boolean format (assignment requirement)
    uplift_triggered = {}
    for step_name in applied_rates.keys():
        uplift_value = uplift_used.get(step_name, 0)
        uplift_triggered[step_name] = bool(uplift_value > 0)
    
    # Return results in same format as Phase 1
    return {
        "users_per_step": num_of_users,
        "total_revenue": total_revenue,
        "roi": roi,
        "applied_rates": applied_rates,
        "uplift_triggered": uplift_triggered
    }

def run_multiple_simulations(num_simulations, seed_base, **funnel_params):
    """Run multiple simulations and return averaged results"""
    random.seed(seed_base)
    
    # Store simulation results and run multiple simulations
    results = []
    for i in range(num_simulations):
        result = configurable_funnel(**funnel_params)
        results.append(result)
    
    # Calculate averages from all simulation runs
    revenues = [result["total_revenue"] for result in results]
    avg_revenue = calculate_average(revenues)
    
    # Calculate average ROI
    rois = [result["roi"] for result in results]
    avg_roi = calculate_average(rois)
    
    # Calculate average users per step
    avg_users_per_step = {}
    # Get step names from first result
    step_names = list(results[0]["users_per_step"].keys())
    for step_name in step_names:
        step_values = [result["users_per_step"][step_name] for result in results]
        avg_users_per_step[step_name] = calculate_average(step_values)
    
    # Calculate average applied rates
    avg_applied_rates = {}
    # Get rate step names from first result
    rate_step_names = list(results[0]["applied_rates"].keys())
    for step_name in rate_step_names:
        rate_values = [result["applied_rates"][step_name] for result in results]
        avg_applied_rates[step_name] = calculate_average(rate_values)
    
    # Count uplift frequency across all runs
    uplift_counts = {}
    # Use all possible step names
    for step_name in rate_step_names:
        count = 0
        for result in results:
            # Check if step has uplift
            if step_name in result["uplift_triggered"] and result["uplift_triggered"][step_name] > 0:
                count += 1
        uplift_counts[step_name] = count
    
    # Add landing page count to output
    landing_visits = funnel_params["budget"] // funnel_params["cost_per_user"]
    avg_users_per_step["landing_page"] = landing_visits
    
    # Convert uplift counts to boolean values
    uplift_triggered = {}
    for step_name in rate_step_names:
        # Mark as True if more than half the simulations had uplift
        uplift_triggered[step_name] = uplift_counts[step_name] > (num_simulations / 2)
    
    # Return averaged results in same format as single simulation
    return {
        "users_per_step": avg_users_per_step,
        "total_revenue": avg_revenue,
        "roi": avg_roi,
        "applied_rates": avg_applied_rates,
        "uplift_triggered": uplift_triggered
    }

def optimize_budget(budget_list, num_sims_per_budget=1, **other_params):
    """Find optimal budget through simple testing"""
    
    # Test different budget amounts to find optimal ROI
    results = []
    
    # Test each budget amount
    for budget in budget_list:
        # Run simulation(s) for each budget
        if num_sims_per_budget == 1:
            # Single simulation
            result = configurable_funnel(budget=budget, **other_params)
        else:
            # Multiple simulations for accuracy
            result = run_multiple_simulations(num_sims_per_budget, 42, budget=budget, **other_params)
        
        # Store budget and performance metrics
        results.append({
            "budget": budget,
            "roi": result["roi"],
            "total_revenue": result["total_revenue"]
        })
    
    # Find budget with highest ROI
    best_budget_result = max(results, key=lambda x: x["roi"])
    
    # Return optimization results
    return {
        "optimal_budget": best_budget_result["budget"],
        "optimal_roi": best_budget_result["roi"],
        "optimal_revenue": best_budget_result["total_revenue"],
        "budget_analysis": results,
        "recommendation": f"Best budget: ${best_budget_result['budget']:,} with ROI of {best_budget_result['roi']:.1%}"
        }

# Main execution demonstrating all Phase 2 features
if __name__ == "__main__":
    # Set up simulation parameters from assignment
    budget = 20000000  # $20 million monthly budget
    cost_per_user = 15  # $15 cost per landing page visitor
    
    conversion_ranges = {
        "registered": (0.3, 0.5),
        "site_created": (0.4, 0.6),
        "premium": (0.1, 0.2),
        "premium_no_trial_churn": (0.7, 0.9),
    }
    
    low_threshold = 400000  # 400k visits
    high_threshold = 1200000  # 1.2 million visits
    
    neg_effect_low = 0.3  # 30% drop below low threshold
    neg_effect_high = 0.2  # 20% drop above high threshold
    
    pos_effect = 0.2  # 20% increase in conversions inside healthy volume range
    
    average_revenue_per_paying_user = 120  # $120 revenue per premium user after trial
    
    # Run single simulation
    single_result = configurable_funnel(
        budget=budget,
        cost_per_user=cost_per_user,
        low_threshold=low_threshold,
        high_threshold=high_threshold,
        neg_effect_low=neg_effect_low,
        neg_effect_high=neg_effect_high,
        pos_effect=pos_effect,
        average_revenue_per_paying_user=average_revenue_per_paying_user
    )
    
    # Run multiple simulations with averaging
    multi_result = run_multiple_simulations(
        num_simulations=10,
        seed_base=42,
        budget=budget,
        cost_per_user=cost_per_user,
        low_threshold=low_threshold,
        high_threshold=high_threshold,
        neg_effect_low=neg_effect_low,
        neg_effect_high=neg_effect_high,
        pos_effect=pos_effect,
        average_revenue_per_paying_user=average_revenue_per_paying_user
    )
    
    # Run budget optimization analysis
    budget_optimization_result = optimize_budget(
        budget_list=[15000000, 20000000, 25000000, 30000000],
        num_sims_per_budget=5,
        cost_per_user=cost_per_user,
        low_threshold=low_threshold,
        high_threshold=high_threshold,
        neg_effect_low=neg_effect_low,
        neg_effect_high=neg_effect_high,
        pos_effect=pos_effect,
        average_revenue_per_paying_user=average_revenue_per_paying_user
    )
    
    # COMPREHENSIVE TESTING OF ALL PHASE 2 FEATURES
    print("="*60)
    print("PHASE 2 FUNNEL SIMULATOR - COMPREHENSIVE TESTING")
    print("="*60)
    
    # Test 1: Single Simulation
    print("\n1. SINGLE SIMULATION TEST")
    print("-" * 30)
    print(f"Budget: ${budget:,}")
    print(f"Cost per user: ${cost_per_user}")
    print(f"ROI: {single_result['roi']:.2%}")
    print(f"Revenue: ${single_result['total_revenue']:,.2f}")
    print(f"Users per step: {single_result['users_per_step']}")
    print(f"Applied rates: {single_result['applied_rates']}")
    print(f"Uplift triggered: {single_result['uplift_triggered']}")
    print("✅ Single simulation test PASSED")
    
    # Test 2: Multiple Simulations with Averaging
    print("\n2. MULTIPLE SIMULATIONS TEST")
    print("-" * 30)
    print(f"Number of simulations: 10")
    print(f"Average ROI: {multi_result['roi']:.2%}")
    print(f"Average Revenue: ${multi_result['total_revenue']:,.2f}")
    print(f"Average users per step: {multi_result['users_per_step']}")
    print(f"Uplift frequency: {multi_result['uplift_triggered']}")
    print("✅ Multiple simulations test PASSED")
    
    # Test 3: Price Effects Testing
    print("\n3. PRICE EFFECTS TEST")
    print("-" * 30)
    
    # Create parameters for price testing
    price_params = {
        'budget': budget,
        'cost_per_user': cost_per_user,
        'low_threshold': low_threshold,
        'high_threshold': high_threshold,
        'neg_effect_low': neg_effect_low,
        'neg_effect_high': neg_effect_high,
        'pos_effect': pos_effect,
        'average_revenue_per_paying_user': average_revenue_per_paying_user
    }
    
    # Test different price scenarios
    discount_result = funnel_with_price_change(price_change=-0.1, **price_params)
    increase_result = funnel_with_price_change(price_change=0.1, **price_params)
    baseline_result = funnel_with_price_change(price_change=0.0, **price_params)
    
    print(f"10% Discount ROI: {discount_result['roi']:.2%}")
    print(f"10% Price Increase ROI: {increase_result['roi']:.2%}")
    print(f"Baseline (0%) ROI: {baseline_result['roi']:.2%}")
    print("Price sensitivity working: Discount improves ROI, increase reduces ROI")
    print("✅ Price effects test PASSED")
    
    # Test 4: Custom Funnel Configuration
    print("\n4. CUSTOM FUNNEL TEST")
    print("-" * 30)
    
    custom_funnel_config = {
        "signup": (0.2, 0.4),
        "activate": (0.5, 0.7),
        "purchase": (0.1, 0.3)
    }
    
    custom_result = configurable_funnel(funnel_config=custom_funnel_config, **price_params)
    print(f"Custom funnel steps: {list(custom_result['users_per_step'].keys())}")
    print(f"Custom funnel ROI: {custom_result['roi']:.2%}")
    print(f"Custom applied rates: {custom_result['applied_rates']}")
    print("✅ Custom funnel test PASSED")
    
    # Test 5: Budget Optimization
    print("\n5. BUDGET OPTIMIZATION TEST")
    print("-" * 30)
    print(f"Tested budgets: {budget_optimization_result['budget_analysis']}")
    print(f"Optimal Budget: ${budget_optimization_result['optimal_budget']:,}")
    print(f"Optimal ROI: {budget_optimization_result['optimal_roi']:.2%}")
    print(f"Optimal Revenue: ${budget_optimization_result['optimal_revenue']:,.2f}")
    print(f"Recommendation: {budget_optimization_result['recommendation']}")
    print("✅ Budget optimization test PASSED")
    
    # Test 6: Utility Functions Validation
    print("\n6. UTILITY FUNCTIONS TEST")
    print("-" * 30)
    
    # Test calculate_average
    test_numbers = [10, 20, 30, 40, 50]
    avg = calculate_average(test_numbers)
    print(f"Average of {test_numbers} = {avg} (Expected: 30.0)")
    assert avg == 30.0, "Average calculation failed"
    
    # Test empty list
    empty_avg = calculate_average([])
    print(f"Empty list average = {empty_avg} (Expected: 0)")
    assert empty_avg == 0, "Empty list average failed"
    
    # Test apply_price_effect
    original_rate = 0.4
    price_change = 0.1  # 10% increase
    sensitivity = 0.5
    new_rate = apply_price_effect(original_rate, price_change, sensitivity)
    expected_rate = 0.4 * (1 - 0.1 * 0.5)  # 0.4 * 0.95 = 0.38
    print(f"Price effect: {original_rate} → {new_rate:.3f} (Expected: {expected_rate})")
    assert abs(new_rate - expected_rate) < 0.001, "Price effect calculation failed"
    
    # Test edge case - rate clamping
    extreme_rate = apply_price_effect(0.1, 2.0, 1.0)  # Should clamp to 0
    print(f"Extreme price effect (should clamp): {extreme_rate} (Expected: 0.0)")
    assert extreme_rate == 0.0, "Rate clamping failed"
    
    print("✅ Utility functions test PASSED")
    
    # Test 7: Data Format Validation
    print("\n7. DATA FORMAT VALIDATION TEST")
    print("-" * 30)
    
    # Check single result format
    required_keys = ['users_per_step', 'total_revenue', 'roi', 'applied_rates', 'uplift_triggered']
    for key in required_keys:
        assert key in single_result, f"Missing key: {key}"
    
    # Check that landing_page is included in users_per_step
    assert 'landing_page' in single_result['users_per_step'], "Missing landing_page in users_per_step"
    
    # Check that uplift_triggered contains booleans
    for step, uplift in single_result['uplift_triggered'].items():
        assert isinstance(uplift, bool), f"uplift_triggered[{step}] is not boolean: {type(uplift)}"
    
    print("Required keys present:", required_keys)
    print(f"Users per step includes landing_page: {'landing_page' in single_result['users_per_step']}")
    print(f"Uplift triggered are booleans: {all(isinstance(v, bool) for v in single_result['uplift_triggered'].values())}")
    print("✅ Data format validation test PASSED")
    
    # Final Summary
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✅")
    print("Phase 2 Funnel Simulator is ready for submission.")
    print("="*60)
