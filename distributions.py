# reference: https://github.com/stan-dev/stan/releases/download/v2.14.0/stan-reference-2.14.0.pdf
# type high -> type hidden -> types
# type hidden -> type high
distribution_higher_type = {
 "binary" : "discrete",
 "bounded discrete": "discrete",
 "unbounded discrete": "discrete",
 "multivariate discrete": "discrete",
 "unbounded continuous":  "continuous",
 "positive continuous":  "continuous",
 "non-negative continuous":  "continuous",
 "positive lower-bounded":  "continuous",
 "continuous on [0 1]":  "continuous",
 "circular":  "continuous",
 "bounded continuous":  "continuous",
 "unbounded vectors":  "continuous",
 "simplex":  "continuous",
 "correlation matrix":  "continuous",
 "covariance matrix":  "continuous",
}

# types -> type hidden
# sampling statement: type      # stan functions
distribution_type2 = {
  "bernoulli": "binary",        # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "bernoulli_logit": "binary",  # _log
  "binomial": "bounded discrete",      # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "binomial_logit": "bounded discrete", # _log
  "beta_binomial": "bounded discrete",  # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "hypergeometric": "bounded discrete", # _log, _rng
  "categorical": "bounded discrete",    # _log, _rng
  "categorical_logit": "bounded discrete",    # _log, _rng
  "ordered_logistic": "bounded discrete", # _log, _rng, 
  "neg_binomial": "unbounded discrete",   # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "neg_binomial_2": "unbounded discrete", # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "neg_binomial_2_log": "unbounded discrete", # _log, _log_rng, 
  "poisson": "unbounded discrete",        # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "poisson_log": "unbounded discrete",    # _log, _rng
  "multinomial": "multivariate discrete",    # _log, _rng
  "normal": "unbounded continuous",       # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "exp_mod_normal": "unbounded continuous", # _log, _cdf, _ccdf_log, _rng
  "skew_normal": "unbounded continuous",  # _log, _cdf, _cdf_log, _rng
  "student_t": "unbounded continuous",    # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "cauchy": "unbounded continuous",       # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "double_exponential": "unbounded continuous", # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "logistic": "unbounded continuous",     # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "gumbel": "unbounded continuous",       # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "lognormal": "positive continuous",    # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "chi_square": "positive continuous",   # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "inv_chi_square": "positive continuous", # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "scaled_inv_chi_square": "positive continuous",  # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "exponential": "positive continuous",  # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "gamma": "positive continuous",        # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "inv_gamma": "positive continuous",    # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "weibull": "positive continuous",      # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "frechet": "positive continuous",      # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "rayleigh": "non-negative continuous",     # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "wiener": "non-negative continuous",       # _log
  "pareto": "positive lower-bounded",       # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "pareto_type_2": "positive lower-bounded",# _log, _cdf, _cdf_log, _ccdf_log, _rng
  "beta": "continuous on [0 1]",         # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "von_mises": "circular",    # _log, _rng
  "uniform": "bounded continuous",      # _log, _cdf, _cdf_log, _ccdf_log, _rng
  "multi_normal": "unbounded vectors", # _log, _rng
  "multi_normal_prec": "unbounded vectors",  # _log
  "multi_normal_cholesky": "unbounded vectors",  # _log, _rng
  "multi_gp": "unbounded vectors",     # _log
  "multi_gp_cholesky": "unbounded vectors",  # _log
  "multi_student_t": "unbounded vectors",  #_log, _rng
  "gaussian_dlm_obs": "unbounded vectors", # _log
  "dirichlet": "simplex",  # _log, _rng
  "lkj_corr": "correlation matrix",   # _log, _rng
  "lkj_corr_cholesky": "correlation matrix", # _log, _rng
  "wishart": "covariance matrix",    # _log, _rng
  "inv_wishart": "covariance matrix",  # _log, _rng
}
