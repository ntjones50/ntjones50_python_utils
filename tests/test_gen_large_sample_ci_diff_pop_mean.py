# ***************************************************************
# Function written by Nathan Jones
# Pytest tests for stats_utils/gen_large_sample_ci_diff_pop_mean.py
# Test 1 and Test 2 initially passed testing
# ***************************************************************

# Imports
import sys
import os
import pytest

#--------------- Import user defined functions -------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "stats_utils")))
from gen_large_sample_ci_diff_pop_mean import gen_large_sample_ci_diff_pop_mean
#-----------------------------------------------------------

def test_gen_large_sample_ci_diff_pop_mean():

    #------------------- Test User Input Checks -----------------------
    test_lst_1 = [1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,1.1,2.2,3.3,4.4,5.5,6.6,
                  4.4,3.3,4.4,5.5,6.6,7.7,8.8,5.5,4.4,3.3,2.3,4.4,5.5,6.6,7.7,
                  2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,1.1,2.2,3.3,4.4,55.5]
    
    test_lst_2 = [1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,1.1,2.2,3.3,4.4,5.5,6.6,
                  4.4,3.3,4.4,5.5,6.6,7.7,8.8,5.5,4.4,3.3,2.3,4.4,5.5,6.6,7.7,
                  2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,1.1,2.2,3.3,4.4,55.5]
    
    test_lst_hasint = [1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,1.1,2.2,3.3,4.4,5.5,6.6,
                       4.4,3.3,4.4,5.5,8,7.7,8.8,5.5,4.4,3.3,2.3,4.4,5.5,6.6,7.7,
                       2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,1.1,2.2,3.3,4.4,55.5]

    # x_sample needs to be a list
    with pytest.raises(Exception) as e:
        gen_large_sample_ci_diff_pop_mean(x_sample = 'test_lst_1',
                                          y_sample = test_lst_2,
                                          approx_confidence_level = 95.0)
    assert str(e.value) == "x_sample needs to be a list"

    # Each entry in x_sample needs to be a float
    with pytest.raises(Exception) as e:
        gen_large_sample_ci_diff_pop_mean(x_sample = test_lst_hasint,
                                          y_sample = test_lst_2,
                                          approx_confidence_level = 95.0)
    assert str(e.value) == "Each entry in x_sample needs to be a float"

    # The sample size for x_sample needs to be > 40
    with pytest.raises(Exception) as e:
        gen_large_sample_ci_diff_pop_mean(x_sample = [1.1,2.2,3.3],
                                          y_sample = test_lst_2,
                                          approx_confidence_level = 95.0)
    assert str(e.value) == "The sample size for x_sample needs to be > 40"

    # y_sample needs to be a list
    with pytest.raises(Exception) as e:
        gen_large_sample_ci_diff_pop_mean(x_sample = test_lst_1,
                                          y_sample = 'test_lst_2',
                                          approx_confidence_level = 95.0)
    assert str(e.value) == "y_sample needs to be a list"

    # Each entry in y_sample needs to be a float
    with pytest.raises(Exception) as e:
        gen_large_sample_ci_diff_pop_mean(x_sample = test_lst_1,
                                          y_sample = test_lst_hasint,
                                          approx_confidence_level = 95.0)
    assert str(e.value) == "Each entry in y_sample needs to be a float"

    # The sample size for y_sample needs to be > 40
    with pytest.raises(Exception) as e:
        gen_large_sample_ci_diff_pop_mean(x_sample = test_lst_1,
                                          y_sample = [1.1,2.2],
                                          approx_confidence_level = 95.0)
    assert str(e.value) == "The sample size for y_sample needs to be > 40"

    # approx_confidence_level needs to be a float  
    with pytest.raises(Exception) as e:
        gen_large_sample_ci_diff_pop_mean(x_sample = test_lst_1,
                                          y_sample = test_lst_2,
                                          approx_confidence_level = 95)
    assert str(e.value) == "approx_confidence_level needs to be a float"
    #------------------- End Test User Input Checks -------------------

    #-------------------- Test 1 --------------------------
    in_x_sample = [0.196969047,1.30467259,2.16146859,-2.716994332,-2.955219834,-2.278700518,-2.088966847,
                   1.498285929,3.935278773,3.384111628,4.455593925,3.264338491,-1.383744629,-4.464827731,
                   2.08062363,0.82466982,3.482947787,0.701699258,-4.141825562,-4.948879368,-3.796567567,
                   0.296265988,-4.415207525,2.359981832,2.646518445,-3.215985752,3.010658375,0.149145932,
                   -3.257938968,-3.210793725,4.824246714,-2.110715376,3.733420368,-1.270234851,-0.015001049,
                   1.748432509,3.308789268,3.871409785,2.480016041,-1.010347699,-3.023908078,-0.739959089,
                   1.40761911,-3.978603294]
    
    in_y_sample = [12.73884688,10.10308935,7.593248599,12.49621146,-4.632821675,0.513639469,4.818165686,
                   12.7492707,2.270063987,8.681735659,9.144157186,-1.514839275,0.717341943,0.193547159,
                   -4.023069375,6.064535258,-4.228797348,1.329696436,6.258816554,10.61423681,12.72334142,
                   -1.414605708,14.34517766,-1.76799657,6.590269514,-2.165017902,-1.025954874,13.17510629,
                   1.279379309,11.92886818,8.812497101,0.853836259,10.44829516,1.104368452,13.91332183,
                   6.250496902,3.675567256,-0.904431152,-3.780332463,14.80868929,10.47824649,11.83638723,
                   -1.269551793,-2.474539077]
    
    comp_lst = gen_large_sample_ci_diff_pop_mean(x_sample = in_x_sample,
                                                 y_sample = in_y_sample,
                                                 approx_confidence_level = 97.0)

    # Test Lower Bound
    assert comp_lst[0] == pytest.approx(-7.177189045)

    # Test mid point
    assert comp_lst[1] == pytest.approx(-4.936494369)

    # Test Upper Bound
    assert comp_lst[2] == pytest.approx(-2.695799692)
    #-------------------- End Test 1 ----------------------

    #-------------------- Test 2 --------------------------
    in_x_sample_2 = [2.722488323,2.683631821,0.286438742,1.140882749,4.883284686,1.971998369,4.18060009,
                     1.069422005,-4.814228911,-2.310235241,-4.547016059,-0.456948567,-1.519341882,
                     -3.679234972,-2.663836187,-2.633298984,1.31467649,-3.883545194,-1.898859356,4.761609098,
                     4.058673029,-0.440162763,4.186376939,3.665047557,1.875394631,3.008578122,0.744447239,
                     3.991569679,-0.174324058,-2.569831091,-3.654679977,3.990309784,0.440459014,3.74984236,
                     1.052198989,-3.16444841,-2.773081905,2.992275482,-3.332180994,-2.016206277,-4.069831728,
                     3.425620348,-4.275110631,-0.609854815]
    
    in_y_sample_2 = [-7.638946881,-6.615488406,-6.253317606,-8.722979763,-6.283579537,-9.481951511,-5.518634178,
                     -5.708132555,-6.077149761,-8.336229076,-5.42252321,-5.519066993,-6.589610587,-5.661595605,
                     -9.862080784,-5.007898138,-8.195414951,-7.236813978,-9.950035796,-9.692853298,-5.635396657,
                     -6.693656494,-5.582867406,-7.055995478,-8.433904215,-9.907360217,-8.222928072,-8.257757696,
                     -5.538841282,-6.702953408,-6.549694223,-8.973808655,-7.5218414,-7.748042126,-8.309248327,
                     -8.052956788,-7.23325789,-8.189747321,-5.496705456,-5.171980262,-7.503310086,-6.309825516,
                     -9.056466788,-6.412038256,-7.07227927,-7.576823442,-8.689829752,-6.999547337,-7.451127179]
    
    out_lst_2 = gen_large_sample_ci_diff_pop_mean(x_sample = in_x_sample_2,
                                                  y_sample = in_y_sample_2,
                                                  approx_confidence_level = 75.0)

    # Test Lower Bound
    assert out_lst_2[0] == pytest.approx(6.843666592)

    # Test mid point
    assert out_lst_2[1] == pytest.approx(7.42033698)

    # Test Upper Bound
    assert out_lst_2[2] == pytest.approx(7.997007368)
    #-------------------- End Test 2 ----------------------