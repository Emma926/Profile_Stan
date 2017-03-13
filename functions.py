# reference: https://github.com/stan-dev/stan/releases/download/v2.14.0/stan-reference-2.14.0.pdf
# distribution functions include both reference 2.14 and 2.8.

# we can only extract computation type from the names
# to determine the data type, need to track the arguments' data type

# split based on complexity of computation
# read value
# basic computation: the functional units that CPUs have, e.g. +-*/
# complex computation: log, power, etc
function_type = {
  "arithmetic": "basic", # all types
  "logical": "basic",       # all types
  "absolute": "basic",
  "integer":  "basic",
  "real": "basic",
  "integer bound": "basic",
  "const": "read",
  "special value": "read",
  "log probability": "complex",
  "round": "basic",
  "power": "complex",
  "log": "complex",
  "trigonometric": "complex",
  "link": "complex",
  "prob": "complex",
  "composed": "complex",
  "log_sum_exp":"complex",
  "reduction": "basic",
  "size": "read",
  "array size": "read",
  "array sort": "basic",
  "matrix size": "read",
  "elementwise": "basic",
  "transpose": "basic",
  "dot": "basic",
  "specialized": "complex",
  "replicate": "basic",
  "matrix": "basic",
  "sparse matrix": "basic",
  "matrix sort": "basic",
  "matrix slicing": "basic",
  "matrix concat": "basic",
  "matrix special": "basic",
  "linear algebra": "basic",
  "mixed": "basic",
  "ODE solver": "complex",
  "distribution functions": "complex"
}

functions = {
  "+": "arithmetic", 
  "-": "arithmetic", 
  "*": "arithmetic", 
  "/": "arithmetic", 
  "\\": "arithmetic", # matrix left division 
  "%": "arithmetic",
  "abs": "absolute", 
  "int_step": "integer", 
  "min": "integer bound",
  "max": "integer bound",
  "pi": "const",
  "e": "const",
  "sqrt2": "const",
  "log2": "const",
  "log10": "const",
  "not_a_number": "special value",
  "positive_infinity": "special value",
  "negative_infinity": "special value",
  "machine_precision": "special value",
  "target": "log probability",   # returns the current value of the log probability accumulator
  "get_lp": "log probability",
  "<": "logical",
  "<=": "logical",
  ">": "logical",
  ">=": "logical",
  "==": "logical",
  "!=": "logical",
  "!": "logical",
  "&&": "logical",
  "||": "logical",
  "step": "logical", 
  "is_inf": "logical", 
  "is_nan": "logical",
  "^": "arithmetic",
  "fabs": "absolute",
  "fdim": "real",
  "fmin": "real",
  "fmax": "real",
  "fmod": "real",
  "floor": "round", 
  "ceil": "round",
  "round": "round",
  "trunc": "round",
  "sqrt": "power",
  "cbrt": "power",
  "square": "power",
  "exp": "power",
  "exp2": "power",
  "log": "log",
  "log2": "log",
  "log10": "log",
  "pow": "power",
  "inv": "power",
  "inv_sqrt": "power",
  "inv_square": "power",
  "hypot": "trigonometric",
  "cos": "trigonometric",
  "sin": "trigonometric",
  "tan": "trigonometric",
  "acos": "trigonometric",
  "asin": "trigonometric",
  "atan": "trigonometric",
  "atan2": "trigonometric",
  "cosh": "trigonometric",
  "sinh": "trigonometric",
  "tanh": "trigonometric",
  "acosh": "trigonometric",
  "asinh": "trigonometric",
  "atanh": "trigonometric",
  "logit": "link", 
  "inv_logit": "link",
  "inv_cloglog": "link",
  "erf": "prob", 
  "erfc": "prob",
  "Phi": "prob",
  "inv_Phi": "prob",
  "Phi_approx": "prob",
  "binary_log_loss": "prob",
  "owens_t": "prob",
  "inc_beta": "prob",
  "lbeta": "prob",
  "tgamma": "prob",
  "lgamma": "prob",
  "digamma": "prob",
  "trigamma": "prob",
  "lmgamma": "prob",
  "gamma_p": "prob",
  "gamma_q": "prob",
  "binomial_coefficient_log": "prob",
  "choose": "prob",
  "bessel_first_kind": "prob",
  "bessel_second_kind": "prob",
  "modified_bessel_first_kind": "prob",
  "modified_bessel_second_kind": "prob",
  "falling_factorial": "prob",
  "lchoose": "prob",
  "log_falling_factorial": "prob",
  "rising_factorial": "prob",
  "log_rising_factorial": "prob",
  "expml": "composed", 
  "fma": "composed",
  "multiply_log": "composed",
  "lmultiply": "composed",
  "loglp": "composed",
  "loglm": "composed",
  "log1p_exp": "composed",
  "log1m_exp": "composed",
  "log_diff_exp": "composed",
  "log_mix": "composed",
  "log_sum_exp": "log_sum_exp",
  "log_inv_logit": "composed",
  "log1m_inv_logit": "composed",
  "min": "reduction",
  "max": "reduction",
  "sum": "reduction",
  "prod": "reduction",
  #"log_sum_exp": "reduction",
  "mean": "reduction",
  "variance": "reduction",
  "sd": "reduction",
  "distance": "reduction",
  "squared_distance": "reduction",
  "dims": "array size",
  "num_elements": "size",
  "size": "array size",
  "rep_array": "array rep", 
  "sort_asc": "array sort",
  "sort_desc": "array sort",
  "sort_indices_asc": "array sort",
  "sort_indices_desc": "array sort",
  "rank": "array sort",
  "rows": "matrix size",
  "cols": "martix size",
  ".*": "elementwise",
  "./": "elementwise",
  "'": 'transpose',
  "dot_product": "dot",
  "columns_dot_product": "dot",
  "rows_dot_product": "dot",
  "dot_self": "dot",
  "columns_dot_self": "dot",
  "rows_dot_self": "dot",
  "tcrossprod": "specialized",
  "crossprod": "specialized",
  "quad_form": "specialized",
  "quad_form_diag": "specialized",
  "quad_form_sym": "specialized",
  "trace_quad_form": "specialized",
  "trace_gen_quad_form": "specialized",
  "multiply_lower_tri_self_transpose": "specialized",
  "diag_pre_multiply": "specialized",
  "diag_post_multiply": "specialized",
  "rep_vector": "replicate",
  "rep_row_vector": "replicate",
  "rep_matrix": "replicate",
  "diagonal": "matrix",
  "diag_matrix": "matrix",
  "col": "matrix slicing",
  "row": "matrix slicing",
  "block": "matrx slicing",
  "sub_col": "matrix slicing",
  "sub_row": "matrix slicing",
  "head": "matrix slicing",
  "tail": "matrix slicing",
  "segment": "matrix slicing",
  "append_col": "matrix concat",
  "append_row": "matrix concat",
  "softmax": "matrix special",
  "log_softmax": "matrix special",
  "cumulative_sum": "matrix special",
  "cov_exp_quad": "matrix special",
  "mdivide_left_tri_low": "linear algebra",
  "mdivide_right_tri_low": "linear algebra",
  "mdivide_left_spd": "linear algebra",
  "mdivide_right_spd": "linear algebra",
  "matrix_exp": "linear algebra",
  "trace": "linear algebra",
  "determinant": "linear algebra",
  "log_determinant": "linear algebra",
  "inverse": "linear algebra",
  "inverse_spd": "linear algebra",
  "eigenvalues_sym": "linear algebra",
  "eigenvectors_sym": "linear algebra",
  "qr_Q": "linear algebra",
  "qr_R": "linear algebra",
  "cholesky_decompose": "linear algebra",
  "singular_values": "linear algebra",
  "sort_asc": "matrix sort",
  "sort_desc": "matrix sort",
  "sort_indices_asc": "matrix sort",
  "sort_indices_desc" : "matrix sort",
  "rank": "matrix sort",
  "csr_extract_w": "parse matrix",
  "csr_extract_v": "parse matrix",
  "csr_extract_u": "parse matrix",
  "csr_to_dense_matrix": "parse matrix",
  "csr_matrix_times_vector" : "parse matrix",
  "to_matrix": "mixed",
  "to_vector": "mixed",
  "to_row_vector": "mixed",
  "to_array_2d": "mixed",
  "to_array_1d": "mixed",
  "integrate_ode_rk45": "ODE solver",
  "integrate_ode": "ODE solver",
  "integrate_ode_bdf": "ODE solver",


  # functions from distributions
  "bernoulli_log": "distribution functions",
  "bernoulli_lpmf": "distribution functions",
"bernoulli_cdf": "distribution functions",
"bernoulli_lcdf": "distribution functions",
"bernoulli_lccdf": "distribution functions",
"bernoulli_cdf_log": "distribution functions",
"bernoulli_ccdf_log": "distribution functions",
"bernoulli_rng": "distribution functions",
"bernoulli_logit_log": "distribution functions",
"bernoulli_logit_lpmf": "distribution functions",
"bernoulli_logit_rng": "distribution functions",
"binomial_log": "distribution functions",
"binomial_lpmf": "distribution functions",
"binomial_cdf": "distribution functions",
"binomial_lcdf": "distribution functions",
"binomial_lccdf": "distribution functions",
"binomial_cdf_log": "distribution functions",
"binomial_ccdf_log": "distribution functions",
"binomial_rng": "distribution functions",
"binomial_logit_log": "distribution functions",
"binomial_logit_lpmf": "distribution functions",
"beta_binomial_log": "distribution functions",
"beta_binomial_lpmf": "distribution functions",
"beta_binomial_cdf": "distribution functions",
"beta_binomial_lcdf": "distribution functions",
"beta_binomial_lccdf": "distribution functions",
"beta_binomial_cdf_log": "distribution functions",
"beta_binomial_ccdf_log": "distribution functions",
"beta_binomial_rng": "distribution functions",
"hypergeometric_log": "distribution functions",
"hypergeometric_lpmf": "distribution functions",
"hypergeometric_rng": "distribution functions",
"categorical_log": "distribution functions",
"categorical_lpmf": "distribution functions",
"categorical_rng": "distribution functions",
"categorical_logit_log": "distribution functions",
"categorical_logit_lpmf": "distribution functions",
"categorical_logit_rng": "distribution functions",
"ordered_logistic_log": "distribution functions",
"ordered_logistic_lpmf": "distribution functions",
"ordered_logistic_rng,": "distribution functions",
"neg_binomial_log": "distribution functions",
"neg_binomial_lpmf": "distribution functions",
"neg_binomial_cdf": "distribution functions",
"neg_binomial_lcdf": "distribution functions",
"neg_binomial_lccdf": "distribution functions",
"neg_binomial_cdf_log": "distribution functions",
"neg_binomial_ccdf_log": "distribution functions",
"neg_binomial_rng": "distribution functions",
"neg_binomial_2_log": "distribution functions",
"neg_binomial_2_lpmf": "distribution functions",
"neg_binomial_2_cdf": "distribution functions",
"neg_binomial_2_lcdf": "distribution functions",
"neg_binomial_2_lccdf": "distribution functions",
"neg_binomial_2_cdf_log": "distribution functions",
"neg_binomial_2_ccdf_log": "distribution functions",
"neg_binomial_2_rng": "distribution functions",
"neg_binomial_2_log_log": "distribution functions",
"neg_binomial_2_log_lpmf": "distribution functions",
"neg_binomial_2_log_rng,": "distribution functions",
"poisson_log": "distribution functions",
"poisson_lpmf": "distribution functions",
"poisson_cdf": "distribution functions",
"poisson_lcdf": "distribution functions",
"poisson_lccdf": "distribution functions",
"poisson_cdf_log": "distribution functions",
"poisson_ccdf_log": "distribution functions",
"poisson_rng": "distribution functions",
"poisson_log_log": "distribution functions",
"poisson_log_lpmf": "distribution functions",
"poisson_log_rng": "distribution functions",
"multinomial_log": "distribution functions",
"multinomial_lpmf": "distribution functions",
"multinomial_rng": "distribution functions",
"normal_log": "distribution functions",
"normal_lpdf": "distribution functions",
"normal_cdf": "distribution functions",
"normal_lcdf": "distribution functions",
"normal_lccdf": "distribution functions",
"normal_cdf_log": "distribution functions",
"normal_ccdf_log": "distribution functions",
"normal_rng": "distribution functions",
"exp_mod_normal_log": "distribution functions",
"exp_mod_normal_lpdf": "distribution functions",
"exp_mod_normal_cdf": "distribution functions",
"exp_mod_normal_lcdf": "distribution functions",
"exp_mod_normal_lccdf": "distribution functions",
"exp_mod_normal_ccdf_log": "distribution functions",
"exp_mod_normal_rng": "distribution functions",
"skew_normal_log": "distribution functions",
"skew_normal_lpdf": "distribution functions",
"skew_normal_cdf": "distribution functions",
"skew_normal_lcdf": "distribution functions",
"skew_normal_lccdf": "distribution functions",
"skew_normal_cdf_log": "distribution functions",
"skew_normal_rng": "distribution functions",
"student_t_log": "distribution functions",
"student_t_lpdf": "distribution functions",
"student_t_cdf": "distribution functions",
"student_t_lcdf": "distribution functions",
"student_t_lccdf": "distribution functions",
"student_t_cdf_log": "distribution functions",
"student_t_ccdf_log": "distribution functions",
"student_t_rng": "distribution functions",
"cauchy_log": "distribution functions",
"cauchy_lpdf": "distribution functions",
"cauchy_cdf": "distribution functions",
"cauchy_lcdf": "distribution functions",
"cauchy_lccdf": "distribution functions",
"cauchy_cdf_log": "distribution functions",
"cauchy_ccdf_log": "distribution functions",
"cauchy_rng": "distribution functions",
"double_exponential_log": "distribution functions",
"double_exponential_lpdf": "distribution functions",
"double_exponential_cdf": "distribution functions",
"double_exponential_lcdf": "distribution functions",
"double_exponential_lccdf": "distribution functions",
"double_exponential_cdf_log": "distribution functions",
"double_exponential_ccdf_log": "distribution functions",
"double_exponential_rng": "distribution functions",
"logistic_log": "distribution functions",
"logistic_lpdf": "distribution functions",
"logistic_cdf": "distribution functions",
"logistic_lcdf": "distribution functions",
"logistic_lccdf": "distribution functions",
"logistic_cdf_log": "distribution functions",
"logistic_ccdf_log": "distribution functions",
"logistic_rng": "distribution functions",
"gumbel_log": "distribution functions",
"gumbel_lpdf": "distribution functions",
"gumbel_cdf": "distribution functions",
"gumbel_lcdf": "distribution functions",
"gumbel_lccdf": "distribution functions",
"gumbel_cdf_log": "distribution functions",
"gumbel_ccdf_log": "distribution functions",
"gumbel_rng": "distribution functions",
"lognormal_log": "distribution functions",
"lognormal_lpdf": "distribution functions",
"lognormal_cdf": "distribution functions",
"lognormal_lcdf": "distribution functions",
"lognormal_lccdf": "distribution functions",
"lognormal_cdf_log": "distribution functions",
"lognormal_ccdf_log": "distribution functions",
"lognormal_rng": "distribution functions",
"chi_square_log": "distribution functions",
"chi_square_lpdf": "distribution functions",
"chi_square_cdf": "distribution functions",
"chi_square_lcdf": "distribution functions",
"chi_square_lccdf": "distribution functions",
"chi_square_cdf_log": "distribution functions",
"chi_square_ccdf_log": "distribution functions",
"chi_square_rng": "distribution functions",
"inv_chi_square_log": "distribution functions",
"inv_chi_square_lpdf": "distribution functions",
"inv_chi_square_cdf": "distribution functions",
"inv_chi_square_lcdf": "distribution functions",
"inv_chi_square_lccdf": "distribution functions",
"inv_chi_square_cdf_log": "distribution functions",
"inv_chi_square_ccdf_log": "distribution functions",
"inv_chi_square_rng": "distribution functions",
"scaled_inv_chi_square_log": "distribution functions",
"scaled_inv_chi_square_lpdf": "distribution functions",
"scaled_inv_chi_square_cdf": "distribution functions",
"scaled_inv_chi_square_lcdf": "distribution functions",
"scaled_inv_chi_square_lccdf": "distribution functions",
"scaled_inv_chi_square_cdf_log": "distribution functions",
"scaled_inv_chi_square_ccdf_log": "distribution functions",
"scaled_inv_chi_square_rng": "distribution functions",
"exponential_log": "distribution functions",
"exponential_lpdf": "distribution functions",
"exponential_cdf": "distribution functions",
"exponential_lcdf": "distribution functions",
"exponential_lccdf": "distribution functions",
"exponential_cdf_log": "distribution functions",
"exponential_ccdf_log": "distribution functions",
"exponential_rng": "distribution functions",
"gamma_log": "distribution functions",
"gamma_lpdf": "distribution functions",
"gamma_cdf": "distribution functions",
"gamma_lcdf": "distribution functions",
"gamma_lccdf": "distribution functions",
"gamma_cdf_log": "distribution functions",
"gamma_ccdf_log": "distribution functions",
"gamma_rng": "distribution functions",
"inv_gamma_log": "distribution functions",
"inv_gamma_lpdf": "distribution functions",
"inv_gamma_cdf": "distribution functions",
"inv_gamma_lcdf": "distribution functions",
"inv_gamma_lccdf": "distribution functions",
"inv_gamma_cdf_log": "distribution functions",
"inv_gamma_ccdf_log": "distribution functions",
"inv_gamma_rng": "distribution functions",
"weibull_log": "distribution functions",
"weibull_lpdf": "distribution functions",
"weibull_cdf": "distribution functions",
"weibull_lcdf": "distribution functions",
"weibull_lccdf": "distribution functions",
"weibull_cdf_log": "distribution functions",
"weibull_ccdf_log": "distribution functions",
"weibull_rng": "distribution functions",
"frechet_log": "distribution functions",
"frechet_lpdf": "distribution functions",
"frechet_cdf": "distribution functions",
"frechet_lcdf": "distribution functions",
"frechet_lccdf": "distribution functions",
"frechet_cdf_log": "distribution functions",
"frechet_ccdf_log": "distribution functions",
"frechet_rng": "distribution functions",
"rayleigh_log": "distribution functions",
"rayleigh_lpdf": "distribution functions",
"rayleigh_cdf": "distribution functions",
"rayleigh_lcdf": "distribution functions",
"rayleigh_lccdf": "distribution functions",
"rayleigh_cdf_log": "distribution functions",
"rayleigh_ccdf_log": "distribution functions",
"rayleigh_rng": "distribution functions",
"wiener_log": "distribution functions",
"wiener_lpdf": "distribution functions",
"pareto_log": "distribution functions",
"pareto_lpdf": "distribution functions",
"pareto_cdf": "distribution functions",
"pareto_lcdf": "distribution functions",
"pareto_lccdf": "distribution functions",
"pareto_cdf_log": "distribution functions",
"pareto_ccdf_log": "distribution functions",
"pareto_rng": "distribution functions",
"pareto_type_2_log": "distribution functions",
"pareto_type_2_lpdf": "distribution functions",
"pareto_type_2_cdf": "distribution functions",
"pareto_type_2_lcdf": "distribution functions",
"pareto_type_2_lccdf": "distribution functions",
"pareto_type_2_cdf_log": "distribution functions",
"pareto_type_2_ccdf_log": "distribution functions",
"pareto_type_2_rng": "distribution functions",
"beta_log": "distribution functions",
"beta_lpdf": "distribution functions",
"beta_cdf": "distribution functions",
"beta_lcdf": "distribution functions",
"beta_lccdf": "distribution functions",
"beta_cdf_log": "distribution functions",
"beta_ccdf_log": "distribution functions",
"beta_rng": "distribution functions",
"von_mises_log": "distribution functions",
"von_mises_lpdf": "distribution functions",
"von_mises_rng": "distribution functions",
"uniform_log": "distribution functions",
"uniform_lpdf": "distribution functions",
"uniform_cdf": "distribution functions",
"uniform_lcdf": "distribution functions",
"uniform_lccdf": "distribution functions",
"uniform_cdf_log": "distribution functions",
"uniform_ccdf_log": "distribution functions",
"uniform_rng": "distribution functions",
"multi_normal_log": "distribution functions",
"multi_normal_lpdf": "distribution functions",
"multi_normal_rng": "distribution functions",
"multi_normal_prec_log": "distribution functions",
"multi_normal_prec_lpdf": "distribution functions",
"multi_normal_cholesky_log": "distribution functions",
"multi_normal_cholesky_lpdf": "distribution functions",
"multi_normal_cholesky_rng": "distribution functions",
"multi_gp_log": "distribution functions",
"multi_gp_lpdf": "distribution functions",
"multi_gp_cholesky_log": "distribution functions",
"multi_student_t_log": "distribution functions",
"multi_student_t_lpdf": "distribution functions",
"multi_student_t_rng": "distribution functions",
"gaussian_dlm_obs_log": "distribution functions",
"gaussian_dlm_obs_lpdf": "distribution functions",
"dirichlet_log": "distribution functions",
"dirichlet_lpdf": "distribution functions",
"dirichlet_rng": "distribution functions",
"lkj_corr_log": "distribution functions",
"lkj_corr_lpdf": "distribution functions",
"lkj_corr_rng": "distribution functions",
"lkj_corr_cholesky_log": "distribution functions",
"lkj_corr_cholesky_lpdf": "distribution functions",
"lkj_corr_cholesky_rng": "distribution functions",
"wishart_log": "distribution functions",
"wishart_lpdf": "distribution functions",
"wishart_rng": "distribution functions",
"inv_wishart_rng": "distribution functions",
"inv_wishart_log": "distribution functions",
"inv_wishart_lpdf": "distribution functions",
}
  
