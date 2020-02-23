import numpy as np
import arviz as az
import pymc3 as pm
import time
start_time = time.time()
np.random.seed(42)

true_m = 0.5
true_b = -1.3
true_logs = np.log(0.3)
x = np.sort(np.random.uniform(0, 5, 20000))
y = true_b + true_m * x + np.exp(true_logs) * np.random.randn(len(x))

with pm.Model() as model:
    m = pm.Uniform("m", lower=-5, upper=5)
    b = pm.Uniform("b", lower=-5, upper=5)
    logs = pm.Uniform("logs", lower=-5, upper=5)
    pm.Normal("obs", mu=m*x+b, sd=pm.math.exp(logs), observed=y)

    print("Getting trace...")
    trace = pm.sample(draws=1000, tune=1000, chains=15)
    print("Getting posterior_predictive...")
    posterior_predictive = pm.sample_posterior_predictive(trace)

    print("Getting idata...")
    idata = az.from_pymc3(
        trace=trace, posterior_predictive=posterior_predictive
    )

print("--- %s seconds ---" % (time.time() - start_time))
