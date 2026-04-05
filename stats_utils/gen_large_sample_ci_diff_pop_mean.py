# **************************************
# Function written by Nathan Jones
# **************************************

#------------ Define Imports -----------
import pandas as pd
import copy
import math
from scipy.stats import norm
#---------------------------------------

def gen_large_sample_ci_diff_pop_mean(
        x_sample: list,
        y_sample: list,
        approx_confidence_level: float):
    
    """
    Description:

    This function computes a confidence interval for the difference in population means when leveraged samples
    from those populations are both large. The approach for this function is documented within the book 
    'Probability and Statistics For Engineering and the Sciences: Ninth Edition' by Jay L. Devore on page 369. 
    Dicussion of assumptions is on page 362 and discussion of sample sizes is on page 370.

    The formulation assumes you have two populations of interest, with population means of mu1 and mu2 (Devore p. 
    362). Large random samples, each of size > 40, are taken from these populations (Devore p. 362, 370). The sample 
    from the mu1 population is the x_sample and the sample from the mu2 population is the y_sample (Devore p. 362).
    The samples need to be independent of each other but can be of differerent sizes (Devore p. 362). 

    This function takes in two lists of floats corresponding to x_sample and y_sample. Leveraging these lists and a 
    specified approximate confidence level (e.g., 95.0%), it computes a confidence interval for mu1 - mu2 with the
    desired approximate confidence level.

    The function returns a list with 3 float elements. The index [0] element is the lower bound of the confidence
    interval. The index [1] element is the x_sample mean minus the y-sample mean (i.e., the mid point of the
    confidence interval). Lastly, the index [2] element is the upper bound of the confidence interval.
    
    Inputs:

        x_sample (list) =  A list of floats where each value is an IID draw from the population with mean mu1.
                           The sample size must be > 40.

        y_sample (list) =  A list of floats where each value is an IID draw from the population with mean mu2.
                           The sample size must be > 40.

        approx_confidence_level (float) = The approximate confidence level desired for the confidence interval
                                          expressed as a percentage. For example, if you want a 95% confidence 
                                          interval, provide 95.0.
        
    Outputs:

        out_lst (list)  =  A list of floats where index 0 is the CI lower bound, index 1 is the x_sample mean minus 
                           the y-sample mean, and index 2 is the CI upper bound.

    Testing:

        Is all the testing for this function automated with pytest (Y/N): Y
        Path to automated testing file for pytest: tests/test_gen_large_sample_ci_diff_pop_mean.py
        Non-pytest testing description and result: N/A
    """

    #------------------ Check for Input Errors -----------------------------

    # x_sample needs to be a list
    if not isinstance(x_sample,list):
        raise Exception("x_sample needs to be a list")
    
    # Each entry in x_sample needs to be a float
    for i in x_sample:
        if not isinstance(i,float):
            raise Exception("Each entry in x_sample needs to be a float")
    
    # The sample size for x_sample needs to be > 40
    if not len(x_sample) > 40:
        raise Exception("The sample size for x_sample needs to be > 40")
    
    # y_sample needs to be a list
    if not isinstance(y_sample,list):
        raise Exception("y_sample needs to be a list")
    
    # Each entry in y_sample needs to be a float
    for i in y_sample:
        if not isinstance(i,float):
            raise Exception("Each entry in y_sample needs to be a float")

    # The sample size for y_sample needs to be > 40
    if not len(y_sample) > 40:
        raise Exception("The sample size for y_sample needs to be > 40")
    
    # approx_confidence_level needs to be a float
    if not isinstance(approx_confidence_level,float):
        raise Exception("approx_confidence_level needs to be a float")
    #------------------ End Check for Input Errors -------------------------

    # Make working copies of input lists
    wrk_x_sample = copy.deepcopy(x_sample)
    wrk_y_sample = copy.deepcopy(y_sample)

    # Compute Alpha
    alpha = 1.0 - (approx_confidence_level/100.0)

    # Compute sample sizes
    m = float(len(wrk_x_sample))
    n = float(len(wrk_y_sample))

    # Compute Sample Means
    x_mean = float(sum(wrk_x_sample))/m
    y_mean = float(sum(wrk_y_sample))/n

    # Compute sample variance for x_sample
    run_sum = 0.0
    for i in wrk_x_sample:
        run_sum = run_sum + float(((i - x_mean) ** 2))
    s_1_squared = float(run_sum/(m - 1.0))

    # Compute sample variance for y_sample
    run_sum = 0.0
    for i in wrk_y_sample:
        run_sum = run_sum + float(((i - y_mean) ** 2))
    s_2_squared = float(run_sum/(n - 1.0))

    # Get z value
    z = float(norm.ppf(1.0 - (alpha/2.0)))

    # Get x_sample mean minus y_sample mean
    x_s_mean_minus_y_s_mean = float(x_mean - y_mean)

    # Compute CI lower bound
    ci_lower = float(x_s_mean_minus_y_s_mean - (z * float(math.sqrt((s_1_squared/m) + (s_2_squared/n)))))

    # Compute CI upper bound
    ci_upper = float(x_s_mean_minus_y_s_mean + (z * float(math.sqrt((s_1_squared/m) + (s_2_squared/n)))))

    # Return out_lst
    return [ci_lower, x_s_mean_minus_y_s_mean, ci_upper]
