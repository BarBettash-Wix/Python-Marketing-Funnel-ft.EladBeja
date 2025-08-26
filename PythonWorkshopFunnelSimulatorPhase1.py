# uplift - This section handles random bonus conversion rate increases

# Import random module for generating random numbers
import random


def random_uplift(step, min_rate=0, max_rate=0.05, uplift_tracker=None)->float:
    """Generate a random uplift (bonus conversion) for a funnel step"""
    
    # Flip a coin (0 or 1) to decide if uplift happens
    coin = random.randint(0,1)
    
    # If coin is 1, apply uplift
    if coin>0:
        # Generate random uplift between min and max rates
        uplift = random.uniform(min_rate, max_rate)
        
        # If tracking dictionary is provided
        if uplift_tracker is not None:
            # Store the uplift value for this step
            uplift_tracker[step] = uplift
        
        # Return the uplift value to add to conversion rate
        return uplift
    else:
        # If coin is 0, no uplift (return 0)
        return 0


# landing page visits - Calculate how many visitors we can get with our budget
def landing_page_visits(budget:float,cost_per_user:float) -> int:
    """Calculate total landing page visits based on budget and cost per user"""
    
    # Integer division: total budget divided by cost per visitor
    return budget // cost_per_user


# range boundaries - Determine if visitor volume is low, high, or optimal
def position_in_range(page_visits,low_threshold,high_threshold) -> int:
    """Determine if visitor count is above, below, or within optimal range"""
    
    # Too many visitors (server overload scenario)
    if page_visits > high_threshold:
        # Return 1 for "high volume"
        return 1
    
    # Too few visitors (low engagement scenario)
    elif page_visits < low_threshold:
        # Return -1 for "low volume"
        return -1
    else:
        # Visitor count is in the sweet spot
        # Return 0 for "optimal volume"
        return 0


def conversion_rate(conversion_ranges, step, uplift_tracker=None):
    """Generate a random conversion rate within the specified range, plus any uplift"""
    
    # Get lower bound of conversion rate for this step
    step_LB = conversion_ranges[step][0]
    
    # Get upper bound of conversion rate for this step
    step_UB = conversion_ranges[step][1]
    
    # Generate random rate + uplift
    rate = random.uniform(step_LB,step_UB)+random_uplift(step, uplift_tracker=uplift_tracker)
    
    # Return the final conversion rate for this step
    return rate


def funnel(budget, cost_per_user, conversion_ranges, low_threshold, high_threshold,
           neg_effect_low, neg_effect_high, pos_effect, average_revenue_per_paying_user):
    """Main funnel simulation function - processes users through conversion steps"""
    
    # Calculate starting visitor count from budget
    page_visits = landing_page_visits(budget, cost_per_user)
    
    # Define steps in order - the customer journey from visitor to paying user
    steps = ['registered', 'site_created', 'premium', 'premium_no_trial_churn']
    
    # Dictionary to store user count at each step
    num_of_users = {}
    
    # Dictionary to store actual conversion rates used
    applied_rates = {}
    
    # Dictionary to track which steps got uplift bonuses
    uplift_used = {}
    
    # Start with total page visits as current user count
    current_users = page_visits
    
    # Process each step in the funnel
    for step in steps:
        # Get conversion rate for this step
        rate = conversion_rate(conversion_ranges, step, uplift_tracker=uplift_used)
        
        # Store the rate for reporting
        applied_rates[step] = rate
        
        # Calculate how many users convert at this step
        users = rate * current_users
        
        # Apply threshold effects only to registration step
        if step == 'registered':
            # Check if user count is high/low/optimal
            position = position_in_range(users, low_threshold, high_threshold)
            
            # High volume - server overload reduces conversions
            if position == 1:
                # Apply high volume penalty
                users = int(users * (1 - neg_effect_high))
            
            # Low volume - poor engagement reduces conversions
            elif position == -1:
                # Apply low volume penalty
                users = int(users * (1 - neg_effect_low))
            else:
                # Optimal volume - boost conversions
                # Apply optimal volume bonus
                users = int(users * (1 + pos_effect))
        else:
            # For all other steps, just convert to integer
            # Round down to whole users
            users = int(users)
            
        # Store user count for this step
        num_of_users[step] = users
        
        # Update current users for next step in funnel
        current_users = users
    
    # Revenue calculation - final step users are the paying customers
    # Calculate total revenue
    total_revenue = float(current_users * average_revenue_per_paying_user)
    
    # Calculate return on investment
    roi = float((total_revenue - budget) / budget)
    
    # Return all results as a dictionary
    return {
        # User count at each funnel step
        "users_per_step": num_of_users,
        
        # Total revenue generated
        "total_revenue": total_revenue,
        
        # Return on investment (can be negative if losing money)
        "roi": roi,
        
        # Actual conversion rates used
        "applied_rates": applied_rates,
        
        # Which steps got random uplift bonuses
        "uplift_triggered": uplift_used
    }