# **************************************
# Function written by Nathan Jones
# **************************************

#------------ Define Imports -----------
import pandas as pd
import copy
import math
from scipy.stats import norm
#---------------------------------------

def gen_large_sample_ci_pop_mean(
        sample: list,
        approx_confidence_level_pct: float) -> list:

    """
    Description:

    This function computes a large-sample confidence interval for the population mean following an approach 
    outlined in "Probability and Statistics for Enginering and the Sciences: Ninth Edition" by Jay L. Devore on 
    page 286.

    The function takes in a list, named sample, holding floats. These floats should be independent and identically
    distributed (IID) from the population for which the population mean is being estimated. The function also takes in
    the approximate confidence level for the confidence interval as a percentage float.

    The function returns a list with 3 entries. The index 0 entry is the lower bound of the confidence interval. The 
    index 1 entry is the mean of the sample. The index 2 entry is the upper bound of the confidence interval.

    Inputs:

        sample (list) =  A list of floats where each value is an IID draw from the population for which the population 
                         mean will be estimated by the confidence interval. The sample size must be > 40.

        approx_confidence_level_pct (float) = The approximate confidence level desired for the confidence interval
                                              expressed as a percentage. For example, if you want a 95% confidence 
                                              interval, provide 95.0.
        
    Outputs:

        out_lst (list)  =  A list where index 0 is the CI lower bound, index 1 is the sampe mean, and index 2 is the CI
                           upper bound.

    Testing:

        Is all the testing for this function automated with pytest (Y/N): Y
        Path to automated testing file for pytest: tests/test_gen_large_sample_ci_pop_mean.py
        Non-pytest testing description and result: N/A
    """

    #------------------ Check User Inputs ---------------------
    # Sample must be a list
    if not isinstance(sample,list):
        raise Exception("sample needs to be a list")
    
    # Sample must contain floats
    for i in sample:
        if not isinstance(i,float):
            raise Exception("sample must contain all floats")
    
    # approx_confidence_level_pct must be a float
    if not isinstance(approx_confidence_level_pct,float):
        raise Exception("approx_confidence_level_pct must be a float")
    
    # The sample size must be > 40 (per Devore p. 286)
    if not len(sample) > 40:
        raise Exception("For this confidence interval, the sample size must be greater than 40")
    #----------------------------------------------------------

    # Copy input list
    wrk_sample = copy.deepcopy(sample)

    # Compute alpha from approx_confidence_level_pct
    alpha = 1.0 - (approx_confidence_level_pct/100.0)

    # Compute sample mean
    sample_mean = float(sum(wrk_sample))/float(len(wrk_sample))

    # Compute sample standard deviation
    run_total = 0.0
    for i in wrk_sample:
        run_total = run_total + (i - sample_mean)**2
    sample_var = run_total/float((len(wrk_sample)-1))
    sample_st_dev = float(math.sqrt(sample_var))

    # Get z value
    z = float(norm.ppf(1.0 - (alpha/2.0)))

    # Compute CI lower and upper bound
    ci_lower_bnd = sample_mean - (z * (sample_st_dev/math.sqrt(float(len(wrk_sample)))))
    ci_upper_bnd = sample_mean + (z * (sample_st_dev/math.sqrt(float(len(wrk_sample)))))

    # Return statement
    return [ci_lower_bnd, sample_mean, ci_upper_bnd]
