#!/usr/bin/env python
# coding: utf-8

# <!-- HTML file automatically generated from DocOnce source (https://github.com/doconce/doconce/)
# doconce format html week37.do.txt --no_mako -->
# <!-- dom:TITLE: Week 37: Statistical interpretations and Resampling Methods -->

# # Week 37: Statistical interpretations and Resampling Methods
# **Morten Hjorth-Jensen**, Department of Physics, University of Oslo and Department of Physics and Astronomy and Facility for Rare Isotope Beams, Michigan State University
# 
# Date: **Sep 18, 2023**
# 
# Copyright 1999-2023, Morten Hjorth-Jensen. Released under CC Attribution-NonCommercial 4.0 license
# 
# <!-- todo add link to videos and add link to Van Wieringens notes -->

# ## Plans for week 37
# 
# **Material for the active learning sessions on Tuesday and Wednesday.**
# 
#   * Lecture from last week on calculations of expectation values
# 
#   * Exercise for week 37
# 
#   * Work on project 1
# 
#   * See also additional note on scaling (jupyter-notebook) sent separately. This will be discussed during the first hour of each session. This note is added at the end of these slides.
# 
#   * For more discussions of Ridge regression and calculation of averages, [Wessel van Wieringen's](https://arxiv.org/abs/1509.09169) article is highly recommended.
# 
#   
# **Material for the lecture on Thursday September 7.**
# 
#   * [Video of Lecture](https://youtu.be/YOBBr_toYxc)
# 
#   * [Whiteboard notes](https://github.com/CompPhysics/MachineLearning/blob/master/doc/HandWrittenNotes/2023/NotesSep14.pdf)
# 
#   * Resampling techniques, Bootstrap and cross validation and bias-variance tradeoff
# 
#   * Statistical interpretation of Ridge and Lasso regression
# 
#   * Readings and Videos:
# 
#     * Hastie et al Chapter 7, here we recommend 7.1-7.5 and 7.10 (cross-validation) and 7.11 (bootstrap). 
# 
#     * [Video on cross validation](https://www.youtube.com/watch?v=fSytzGwwBVw)
# 
#     * [Video on Bootstrapping](https://www.youtube.com/watch?v=Xz0x-8-cgaQ)
# 
#     * [Video on bias-variance tradeoff](https://www.youtube.com/watch?v=EuBBz3bI-aA)

# ## Material from last week and relevant for the weekly exercises

# ## Linking the regression analysis with a statistical interpretation
# 
# We will now couple the discussions of ordinary least squares, Ridge
# and Lasso regression with a statistical interpretation, that is we
# move from a linear algebra analysis to a statistical analysis. In
# particular, we will focus on what the regularization terms can result
# in.  We will amongst other things show that the regularization
# parameter can reduce considerably the variance of the parameters
# $\beta$.
# 
# The
# advantage of doing linear regression is that we actually end up with
# analytical expressions for several statistical quantities.  
# Standard least squares and Ridge regression  allow us to
# derive quantities like the variance and other expectation values in a
# rather straightforward way.
# 
# It is assumed that $\varepsilon_i
# \sim \mathcal{N}(0, \sigma^2)$ and the $\varepsilon_{i}$ are
# independent, i.e.:

# $$
# \begin{align*} 
# \mbox{Cov}(\varepsilon_{i_1},
# \varepsilon_{i_2}) & = \left\{ \begin{array}{lcc} \sigma^2 & \mbox{if}
# & i_1 = i_2, \\ 0 & \mbox{if} & i_1 \not= i_2.  \end{array} \right.
# \end{align*}
# $$

# The randomness of $\varepsilon_i$ implies that
# $\mathbf{y}_i$ is also a random variable. In particular,
# $\mathbf{y}_i$ is normally distributed, because $\varepsilon_i \sim
# \mathcal{N}(0, \sigma^2)$ and $\mathbf{X}_{i,\ast} \, \boldsymbol{\beta}$ is a
# non-random scalar. To specify the parameters of the distribution of
# $\mathbf{y}_i$ we need to calculate its first two moments. 
# 
# Recall that $\boldsymbol{X}$ is a matrix of dimensionality $n\times p$. The
# notation above $\mathbf{X}_{i,\ast}$ means that we are looking at the
# row number $i$ and perform a sum over all values $p$.

# ## Assumptions made
# 
# The assumption we have made here can be summarized as (and this is going to be useful when we discuss the bias-variance trade off)
# that there exists a function $f(\boldsymbol{x})$ and  a normal distributed error $\boldsymbol{\varepsilon}\sim \mathcal{N}(0, \sigma^2)$
# which describe our data

# $$
# \boldsymbol{y} = f(\boldsymbol{x})+\boldsymbol{\varepsilon}
# $$

# We approximate this function with our model from the solution of the linear regression equations, that is our
# function $f$ is approximated by $\boldsymbol{\tilde{y}}$ where we want to minimize $(\boldsymbol{y}-\boldsymbol{\tilde{y}})^2$, our MSE, with

# $$
# \boldsymbol{\tilde{y}} = \boldsymbol{X}\boldsymbol{\beta}.
# $$

# ## Expectation value and variance
# 
# We can calculate the expectation value of $\boldsymbol{y}$ for a given element $i$

# $$
# \begin{align*} 
# \mathbb{E}(y_i) & =
# \mathbb{E}(\mathbf{X}_{i, \ast} \, \boldsymbol{\beta}) + \mathbb{E}(\varepsilon_i)
# \, \, \, = \, \, \, \mathbf{X}_{i, \ast} \, \beta, 
# \end{align*}
# $$

# while
# its variance is

# $$
# \begin{align*} \mbox{Var}(y_i) & = \mathbb{E} \{ [y_i
# - \mathbb{E}(y_i)]^2 \} \, \, \, = \, \, \, \mathbb{E} ( y_i^2 ) -
# [\mathbb{E}(y_i)]^2  \\  & = \mathbb{E} [ ( \mathbf{X}_{i, \ast} \,
# \beta + \varepsilon_i )^2] - ( \mathbf{X}_{i, \ast} \, \boldsymbol{\beta})^2 \\ &
# = \mathbb{E} [ ( \mathbf{X}_{i, \ast} \, \boldsymbol{\beta})^2 + 2 \varepsilon_i
# \mathbf{X}_{i, \ast} \, \boldsymbol{\beta} + \varepsilon_i^2 ] - ( \mathbf{X}_{i,
# \ast} \, \beta)^2 \\  & = ( \mathbf{X}_{i, \ast} \, \boldsymbol{\beta})^2 + 2
# \mathbb{E}(\varepsilon_i) \mathbf{X}_{i, \ast} \, \boldsymbol{\beta} +
# \mathbb{E}(\varepsilon_i^2 ) - ( \mathbf{X}_{i, \ast} \, \boldsymbol{\beta})^2 
# \\ & = \mathbb{E}(\varepsilon_i^2 ) \, \, \, = \, \, \,
# \mbox{Var}(\varepsilon_i) \, \, \, = \, \, \, \sigma^2.  
# \end{align*}
# $$

# Hence, $y_i \sim \mathcal{N}( \mathbf{X}_{i, \ast} \, \boldsymbol{\beta}, \sigma^2)$, that is $\boldsymbol{y}$ follows a normal distribution with 
# mean value $\boldsymbol{X}\boldsymbol{\beta}$ and variance $\sigma^2$ (not be confused with the singular values of the SVD).

# ## Expectation value and variance for $\boldsymbol{\beta}$
# 
# With the OLS expressions for the optimal parameters $\boldsymbol{\hat{\beta}}$ we can evaluate the expectation value

# $$
# \mathbb{E}(\boldsymbol{\hat{\beta}}) = \mathbb{E}[ (\mathbf{X}^{\top} \mathbf{X})^{-1}\mathbf{X}^{T} \mathbf{Y}]=(\mathbf{X}^{T} \mathbf{X})^{-1}\mathbf{X}^{T} \mathbb{E}[ \mathbf{Y}]=(\mathbf{X}^{T} \mathbf{X})^{-1} \mathbf{X}^{T}\mathbf{X}\boldsymbol{\beta}=\boldsymbol{\beta}.
# $$

# This means that the estimator of the regression parameters is unbiased.
# 
# We can also calculate the variance
# 
# The variance of the optimal value $\boldsymbol{\hat{\beta}}$ is

# $$
# \begin{eqnarray*}
# \mbox{Var}(\boldsymbol{\hat{\beta}}) & = & \mathbb{E} \{ [\boldsymbol{\beta} - \mathbb{E}(\boldsymbol{\beta})] [\boldsymbol{\beta} - \mathbb{E}(\boldsymbol{\beta})]^{T} \}
# \\
# & = & \mathbb{E} \{ [(\mathbf{X}^{T} \mathbf{X})^{-1} \, \mathbf{X}^{T} \mathbf{y} - \boldsymbol{\beta}] \, [(\mathbf{X}^{T} \mathbf{X})^{-1} \, \mathbf{X}^{T} \mathbf{y} - \boldsymbol{\beta}]^{T} \}
# \\
# % & = & \mathbb{E} \{ [(\mathbf{X}^{T} \mathbf{X})^{-1} \, \mathbf{X}^{T} \mathbf{y}] \, [(\mathbf{X}^{T} \mathbf{X})^{-1} \, \mathbf{X}^{T} \mathbf{y}]^{T} \} - \boldsymbol{\beta} \, \boldsymbol{\beta}^{T}
# % \\
# % & = & \mathbb{E} \{ (\mathbf{X}^{T} \mathbf{X})^{-1} \, \mathbf{X}^{T} \mathbf{y} \, \mathbf{y}^{T} \, \mathbf{X} \, (\mathbf{X}^{T} \mathbf{X})^{-1}  \} - \boldsymbol{\beta} \, \boldsymbol{\beta}^{T}
# % \\
# & = & (\mathbf{X}^{T} \mathbf{X})^{-1} \, \mathbf{X}^{T} \, \mathbb{E} \{ \mathbf{y} \, \mathbf{y}^{T} \} \, \mathbf{X} \, (\mathbf{X}^{T} \mathbf{X})^{-1} - \boldsymbol{\beta} \, \boldsymbol{\beta}^{T}
# \\
# & = & (\mathbf{X}^{T} \mathbf{X})^{-1} \, \mathbf{X}^{T} \, \{ \mathbf{X} \, \boldsymbol{\beta} \, \boldsymbol{\beta}^{T} \,  \mathbf{X}^{T} + \sigma^2 \} \, \mathbf{X} \, (\mathbf{X}^{T} \mathbf{X})^{-1} - \boldsymbol{\beta} \, \boldsymbol{\beta}^{T}
# % \\
# % & = & (\mathbf{X}^T \mathbf{X})^{-1} \, \mathbf{X}^T \, \mathbf{X} \, \boldsymbol{\beta} \, \boldsymbol{\beta}^T \,  \mathbf{X}^T \, \mathbf{X} \, (\mathbf{X}^T % \mathbf{X})^{-1}
# % \\
# % & & + \, \, \sigma^2 \, (\mathbf{X}^T \mathbf{X})^{-1} \, \mathbf{X}^T  \, \mathbf{X} \, (\mathbf{X}^T \mathbf{X})^{-1} - \boldsymbol{\beta} \boldsymbol{\beta}^T
# \\
# & = & \boldsymbol{\beta} \, \boldsymbol{\beta}^{T}  + \sigma^2 \, (\mathbf{X}^{T} \mathbf{X})^{-1} - \boldsymbol{\beta} \, \boldsymbol{\beta}^{T}
# \, \, \, = \, \, \, \sigma^2 \, (\mathbf{X}^{T} \mathbf{X})^{-1},
# \end{eqnarray*}
# $$

# where we have used  that $\mathbb{E} (\mathbf{y} \mathbf{y}^{T}) =
# \mathbf{X} \, \boldsymbol{\beta} \, \boldsymbol{\beta}^{T} \, \mathbf{X}^{T} +
# \sigma^2 \, \mathbf{I}_{nn}$. From $\mbox{Var}(\boldsymbol{\beta}) = \sigma^2
# \, (\mathbf{X}^{T} \mathbf{X})^{-1}$, one obtains an estimate of the
# variance of the estimate of the $j$-th regression coefficient:
# $\boldsymbol{\sigma}^2 (\boldsymbol{\beta}_j ) = \boldsymbol{\sigma}^2 [(\mathbf{X}^{T} \mathbf{X})^{-1}]_{jj} $. This may be used to
# construct a confidence interval for the estimates.
# 
# In a similar way, we can obtain analytical expressions for say the
# expectation values of the parameters $\boldsymbol{\beta}$ and their variance
# when we employ Ridge regression, allowing us again to define a confidence interval. 
# 
# It is rather straightforward to show that

# $$
# \mathbb{E} \big[ \hat{\boldsymbol{\beta}}^{\mathrm{Ridge}} \big]=(\mathbf{X}^{T} \mathbf{X} + \lambda \mathbf{I}_{pp})^{-1} (\mathbf{X}^{\top} \mathbf{X})\boldsymbol{\beta}.
# $$

# We see clearly that 
# $\mathbb{E} \big[ \hat{\boldsymbol{\beta}}^{\mathrm{Ridge}} \big] \not= \hat{\boldsymbol{\beta}}^{\mathrm{OLS}}$ for any $\lambda > 0$.
# 
# We can also compute the variance as

# $$
# \mbox{Var}[\hat{\boldsymbol{\beta}}^{\mathrm{Ridge}}]=\sigma^2[  \mathbf{X}^{T} \mathbf{X} + \lambda \mathbf{I} ]^{-1}  \mathbf{X}^{T} \mathbf{X} \{ [  \mathbf{X}^{\top} \mathbf{X} + \lambda \mathbf{I} ]^{-1}\}^{T},
# $$

# and it is easy to see that if the parameter $\lambda$ goes to infinity then the variance of Ridge parameters $\boldsymbol{\beta}$ goes to zero. 
# 
# With this, we can compute the difference

# $$
# \mbox{Var}[\hat{\boldsymbol{\beta}}^{\mathrm{OLS}}]-\mbox{Var}(\hat{\boldsymbol{\beta}}^{\mathrm{Ridge}})=\sigma^2 [  \mathbf{X}^{T} \mathbf{X} + \lambda \mathbf{I} ]^{-1}[ 2\lambda\mathbf{I} + \lambda^2 (\mathbf{X}^{T} \mathbf{X})^{-1} ] \{ [  \mathbf{X}^{T} \mathbf{X} + \lambda \mathbf{I} ]^{-1}\}^{T}.
# $$

# The difference is non-negative definite since each component of the
# matrix product is non-negative definite. 
# This means the variance we obtain with the standard OLS will always for $\lambda > 0$ be larger than the variance of $\boldsymbol{\beta}$ obtained with the Ridge estimator. This has interesting consequences when we discuss the so-called bias-variance trade-off below. 
# 
# For more discussions of Ridge regression and calculation of averages, [Wessel van Wieringen's](https://arxiv.org/abs/1509.09169) article is highly recommended.

# ## Material for lecture Thursday September 14

# ## Deriving OLS from a probability distribution
# 
# Our basic assumption when we derived the OLS equations was to assume
# that our output is determined by a given continuous function
# $f(\boldsymbol{x})$ and a random noise $\boldsymbol{\epsilon}$ given by the normal
# distribution with zero mean value and an undetermined variance
# $\sigma^2$.
# 
# We found above that the outputs $\boldsymbol{y}$ have a mean value given by
# $\boldsymbol{X}\hat{\boldsymbol{\beta}}$ and variance $\sigma^2$. Since the entries to
# the design matrix are not stochastic variables, we can assume that the
# probability distribution of our targets is also a normal distribution
# but now with mean value $\boldsymbol{X}\hat{\boldsymbol{\beta}}$. This means that a
# single output $y_i$ is given by the Gaussian distribution

# $$
# y_i\sim \mathcal{N}(\boldsymbol{X}_{i,*}\boldsymbol{\beta}, \sigma^2)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp{\left[-\frac{(y_i-\boldsymbol{X}_{i,*}\boldsymbol{\beta})^2}{2\sigma^2}\right]}.
# $$

# ## Independent and Identically Distrubuted (iid)
# 
# We assume now that the various $y_i$ values are stochastically distributed according to the above Gaussian distribution. 
# We define this distribution as

# $$
# p(y_i, \boldsymbol{X}\vert\boldsymbol{\beta})=\frac{1}{\sqrt{2\pi\sigma^2}}\exp{\left[-\frac{(y_i-\boldsymbol{X}_{i,*}\boldsymbol{\beta})^2}{2\sigma^2}\right]},
# $$

# which reads as finding the likelihood of an event $y_i$ with the input variables $\boldsymbol{X}$ given the parameters (to be determined) $\boldsymbol{\beta}$.
# 
# Since these events are assumed to be independent and identicall distributed we can build the probability distribution function (PDF) for all possible event $\boldsymbol{y}$ as the product of the single events, that is we have

# $$
# p(\boldsymbol{y},\boldsymbol{X}\vert\boldsymbol{\beta})=\prod_{i=0}^{n-1}\frac{1}{\sqrt{2\pi\sigma^2}}\exp{\left[-\frac{(y_i-\boldsymbol{X}_{i,*}\boldsymbol{\beta})^2}{2\sigma^2}\right]}=\prod_{i=0}^{n-1}p(y_i,\boldsymbol{X}\vert\boldsymbol{\beta}).
# $$

# We will write this in a more compact form reserving $\boldsymbol{D}$ for the domain of events, including the ouputs (targets) and the inputs. That is
# in case we have a simple one-dimensional input and output case

# $$
# \boldsymbol{D}=[(x_0,y_0), (x_1,y_1),\dots, (x_{n-1},y_{n-1})].
# $$

# In the more general case the various inputs should be replaced by the possible features represented by the input data set $\boldsymbol{X}$. 
# We can now rewrite the above probability as

# $$
# p(\boldsymbol{D}\vert\boldsymbol{\beta})=\prod_{i=0}^{n-1}\frac{1}{\sqrt{2\pi\sigma^2}}\exp{\left[-\frac{(y_i-\boldsymbol{X}_{i,*}\boldsymbol{\beta})^2}{2\sigma^2}\right]}.
# $$

# It is a conditional probability (see below) and reads as the likelihood of a domain of events $\boldsymbol{D}$ given a set of parameters $\boldsymbol{\beta}$.

# ## Maximum Likelihood Estimation (MLE)
# 
# In statistics, maximum likelihood estimation (MLE) is a method of
# estimating the parameters of an assumed probability distribution,
# given some observed data. This is achieved by maximizing a likelihood
# function so that, under the assumed statistical model, the observed
# data is the most probable. 
# 
# We will assume here that our events are given by the above Gaussian
# distribution and we will determine the optimal parameters $\beta$ by
# maximizing the above PDF. However, computing the derivatives of a
# product function is cumbersome and can easily lead to overflow and/or
# underflowproblems, with potentials for loss of numerical precision.
# 
# In practice, it is more convenient to maximize the logarithm of the
# PDF because it is a monotonically increasing function of the argument.
# Alternatively, and this will be our option, we will minimize the
# negative of the logarithm since this is a monotonically decreasing
# function.
# 
# Note also that maximization/minimization of the logarithm of the PDF
# is equivalent to the maximization/minimization of the function itself.

# ## A new Cost Function
# 
# We could now define a new cost function to minimize, namely the negative logarithm of the above PDF

# $$
# C(\boldsymbol{\beta}=-\log{\prod_{i=0}^{n-1}p(y_i,\boldsymbol{X}\vert\boldsymbol{\beta})}=-\sum_{i=0}^{n-1}\log{p(y_i,\boldsymbol{X}\vert\boldsymbol{\beta})},
# $$

# which becomes

# $$
# C(\boldsymbol{\beta}=\frac{n}{2}\log{2\pi\sigma^2}+\frac{\vert\vert (\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\beta})\vert\vert_2^2}{2\sigma^2}.
# $$

# Taking the derivative of the *new* cost function with respect to the parameters $\beta$ we recognize our familiar OLS equation, namely

# $$
# \boldsymbol{X}^T\left(\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\beta}\right) =0,
# $$

# which leads to the well-known OLS equation for the optimal paramters $\beta$

# $$
# \hat{\boldsymbol{\beta}}^{\mathrm{OLS}}=\left(\boldsymbol{X}^T\boldsymbol{X}\right)^{-1}\boldsymbol{X}^T\boldsymbol{y}!
# $$

# Before we make a similar analysis for Ridge and Lasso regression, we need a short reminder on statistics.

# ## More basic Statistics and Bayes' theorem
# 
# A central theorem in statistics is Bayes' theorem. This theorem plays a similar role as the good old Pythagoras' theorem in geometry.
# Bayes' theorem is extremely simple to derive. But to do so we need some basic axioms from statistics.
# 
# Assume we have two domains of events $X=[x_0,x_1,\dots,x_{n-1}]$ and $Y=[y_0,y_1,\dots,y_{n-1}]$.
# 
# We define also the likelihood for $X$ and $Y$ as $p(X)$ and $p(Y)$ respectively.
# The likelihood of a specific event $x_i$ (or $y_i$) is then written as $p(X=x_i)$ or just $p(x_i)=p_i$. 
# 
# **Union of events is given by.**

# $$
# p(X \cup Y)= p(X)+p(Y)-p(X \cap Y).
# $$

# **The product rule (aka joint probability) is given by.**

# $$
# p(X \cup Y)= p(X,Y)= p(X\vert Y)p(Y)=p(Y\vert X)p(X),
# $$

# where we read $p(X\vert Y)$ as the likelihood of obtaining $X$ given $Y$.
# 
# If we have independent events then $p(X,Y)=p(X)p(Y)$.

# ## Marginal Probability
# 
# The marginal probability is defined in terms of only one of the set of variables $X,Y$. For a discrete probability we have

# $$
# p(X)=\sum_{i=0}^{n-1}p(X,Y=y_i)=\sum_{i=0}^{n-1}p(X\vert Y=y_i)p(Y=y_i)=\sum_{i=0}^{n-1}p(X\vert y_i)p(y_i).
# $$

# ## Conditional  Probability
# 
# The conditional  probability, if $p(Y) > 0$, is

# $$
# p(X\vert Y)= \frac{p(X,Y)}{p(Y)}=\frac{p(X,Y)}{\sum_{i=0}^{n-1}p(Y\vert X=x_i)p(x_i)}.
# $$

# ## Bayes' Theorem
# 
# If we combine the conditional probability with the marginal probability and the standard product rule, we have

# $$
# p(X\vert Y)= \frac{p(X,Y)}{p(Y)},
# $$

# which we can rewrite as

# $$
# p(X\vert Y)= \frac{p(X,Y)}{\sum_{i=0}^{n-1}p(Y\vert X=x_i)p(x_i)}=\frac{p(Y\vert X)p(X)}{\sum_{i=0}^{n-1}p(Y\vert X=x_i)p(x_i)},
# $$

# which is Bayes' theorem. It allows us to evaluate the uncertainty in in $X$ after we have observed $Y$. We can easily interchange $X$ with $Y$.

# ## Interpretations of Bayes' Theorem
# 
# The quantity $p(Y\vert X)$ on the right-hand side of the theorem is
# evaluated for the observed data $Y$ and can be viewed as a function of
# the parameter space represented by $X$. This function is not
# necesseraly normalized and is normally called the likelihood function.
# 
# The function $p(X)$ on the right hand side is called the prior while the function on the left hand side is the called the posterior probability. The denominator on the right hand side serves as a normalization factor for the posterior distribution.
# 
# Let us try to illustrate Bayes' theorem through an example.

# ## Example of Usage of Bayes' theorem
# 
# Let us suppose that you are undergoing a series of mammography scans in
# order to rule out possible breast cancer cases.  We define the
# sensitivity for a positive event by the variable $X$. It takes binary
# values with $X=1$ representing a positive event and $X=0$ being a
# negative event. We reserve $Y$ as a classification parameter for
# either a negative or a positive breast cancer confirmation. (Short note on wordings: positive here means having breast cancer, although none of us would consider this being a  positive thing).
# 
# We let $Y=1$ represent the the case of having breast cancer and $Y=0$ as not.
# 
# Let us assume that if you have breast cancer, the test will be positive with a probability of $0.8$, that is we have

# $$
# p(X=1\vert Y=1) =0.8.
# $$

# This obviously sounds  scary since many would conclude that if the test is positive, there is a likelihood of $80\%$ for having cancer.
# It is however not correct, as the following Bayesian analysis shows.

# ## Doing it correctly
# 
# If we look at various national surveys on breast cancer, the general likelihood of developing breast cancer is a very small number.
# Let us assume that the prior probability in the population as a whole is

# $$
# p(Y=1) =0.004.
# $$

# We need also to account for the fact that the test may produce a false positive result (false alarm). Let us here assume that we have

# $$
# p(X=1\vert Y=0) =0.1.
# $$

# Using Bayes' theorem we can then find the posterior probability that the person has breast cancer in case of a positive test, that is we can compute

# $$
# p(Y=1\vert X=1)=\frac{p(X=1\vert Y=1)p(Y=1)}{p(X=1\vert Y=1)p(Y=1)+p(X=1\vert Y=0)p(Y=0)}=\frac{0.8\times 0.004}{0.8\times 0.004+0.1\times 0.996}=0.031.
# $$

# That is, in case of a positive test, there is only a $3\%$ chance of having breast cancer!

# ## Bayes' Theorem and Ridge and Lasso Regression
# 
# Using Bayes' theorem we can gain a better intuition about Ridge and Lasso regression. 
# 
# For ordinary least squares we postulated that the maximum likelihood for the doamin of events $\boldsymbol{D}$ (one-dimensional case)

# $$
# \boldsymbol{D}=[(x_0,y_0), (x_1,y_1),\dots, (x_{n-1},y_{n-1})],
# $$

# is given by

# $$
# p(\boldsymbol{D}\vert\boldsymbol{\beta})=\prod_{i=0}^{n-1}\frac{1}{\sqrt{2\pi\sigma^2}}\exp{\left[-\frac{(y_i-\boldsymbol{X}_{i,*}\boldsymbol{\beta})^2}{2\sigma^2}\right]}.
# $$

# In Bayes' theorem this function plays the role of the so-called likelihood. We could now ask the question what is the posterior probability of a parameter set $\boldsymbol{\beta}$ given a domain of events $\boldsymbol{D}$?  That is, how can we define the posterior probability

# $$
# p(\boldsymbol{\beta}\vert\boldsymbol{D}).
# $$

# Bayes' theorem comes to our rescue here since (omitting the normalization constant)

# $$
# p(\boldsymbol{\beta}\vert\boldsymbol{D})\propto p(\boldsymbol{D}\vert\boldsymbol{\beta})p(\boldsymbol{\beta}).
# $$

# We have a model for $p(\boldsymbol{D}\vert\boldsymbol{\beta})$ but need one for the **prior** $p(\boldsymbol{\beta}$!

# ## Ridge and Bayes
# 
# With the posterior probability defined by a likelihood which we have
# already modeled and an unknown prior, we are now ready to make
# additional models for the prior.
# 
# We can, based on our discussions of the variance of $\boldsymbol{\beta}$ and the mean value, assume that the prior for the values $\boldsymbol{\beta}$ is given by a Gaussian with mean value zero and variance $\tau^2$, that is

# $$
# p(\boldsymbol{\beta})=\prod_{j=0}^{p-1}\exp{\left(-\frac{\beta_j^2}{2\tau^2}\right)}.
# $$

# Our posterior probability becomes then (omitting the normalization factor which is just a constant)

# $$
# p(\boldsymbol{\beta\vert\boldsymbol{D})}=\prod_{i=0}^{n-1}\frac{1}{\sqrt{2\pi\sigma^2}}\exp{\left[-\frac{(y_i-\boldsymbol{X}_{i,*}\boldsymbol{\beta})^2}{2\sigma^2}\right]}\prod_{j=0}^{p-1}\exp{\left(-\frac{\beta_j^2}{2\tau^2}\right)}.
# $$

# We can now optimize this quantity with respect to $\boldsymbol{\beta}$. As we
# did for OLS, this is most conveniently done by taking the negative
# logarithm of the posterior probability. Doing so and leaving out the
# constants terms that do not depend on $\beta$, we have

# $$
# C(\boldsymbol{\beta})=\frac{\vert\vert (\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\beta})\vert\vert_2^2}{2\sigma^2}+\frac{1}{2\tau^2}\vert\vert\boldsymbol{\beta}\vert\vert_2^2,
# $$

# and replacing $1/2\tau^2$ with $\lambda$ we have

# $$
# C(\boldsymbol{\beta})=\frac{\vert\vert (\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\beta})\vert\vert_2^2}{2\sigma^2}+\lambda\vert\vert\boldsymbol{\beta}\vert\vert_2^2,
# $$

# which is our Ridge cost function!  Nice, isn't it?

# ## Lasso and Bayes
# 
# To derive the Lasso cost function, we simply replace the Gaussian prior with an exponential distribution ([Laplace in this case](https://en.wikipedia.org/wiki/Laplace_distribution)) with zero mean value,  that is

# $$
# p(\boldsymbol{\beta})=\prod_{j=0}^{p-1}\exp{\left(-\frac{\vert\beta_j\vert}{\tau}\right)}.
# $$

# Our posterior probability becomes then (omitting the normalization factor which is just a constant)

# $$
# p(\boldsymbol{\beta}\vert\boldsymbol{D})=\prod_{i=0}^{n-1}\frac{1}{\sqrt{2\pi\sigma^2}}\exp{\left[-\frac{(y_i-\boldsymbol{X}_{i,*}\boldsymbol{\beta})^2}{2\sigma^2}\right]}\prod_{j=0}^{p-1}\exp{\left(-\frac{\vert\beta_j\vert}{\tau}\right)}.
# $$

# Taking the negative
# logarithm of the posterior probability and leaving out the
# constants terms that do not depend on $\beta$, we have

# $$
# C(\boldsymbol{\beta}=\frac{\vert\vert (\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\beta})\vert\vert_2^2}{2\sigma^2}+\frac{1}{\tau}\vert\vert\boldsymbol{\beta}\vert\vert_1,
# $$

# and replacing $1/\tau$ with $\lambda$ we have

# $$
# C(\boldsymbol{\beta}=\frac{\vert\vert (\boldsymbol{y}-\boldsymbol{X}\boldsymbol{\beta})\vert\vert_2^2}{2\sigma^2}+\lambda\vert\vert\boldsymbol{\beta}\vert\vert_1,
# $$

# which is our Lasso cost function!

# ## Why resampling methods
# 
# Before we proceed, we need to rethink what we have been doing. In our
# eager to fit the data, we have omitted several important elements in
# our regression analysis. In what follows we will
# 1. look at statistical properties, including a discussion of mean values, variance and the so-called bias-variance tradeoff
# 
# 2. introduce resampling techniques like cross-validation, bootstrapping and jackknife and more
# 
# and discuss how to select a given model (one of the difficult parts in machine learning).

# ## Resampling methods
# Resampling methods are an indispensable tool in modern
# statistics. They involve repeatedly drawing samples from a training
# set and refitting a model of interest on each sample in order to
# obtain additional information about the fitted model. For example, in
# order to estimate the variability of a linear regression fit, we can
# repeatedly draw different samples from the training data, fit a linear
# regression to each new sample, and then examine the extent to which
# the resulting fits differ. Such an approach may allow us to obtain
# information that would not be available from fitting the model only
# once using the original training sample.
# 
# Two resampling methods are often used in Machine Learning analyses,
# 1. The **bootstrap method**
# 
# 2. and **Cross-Validation**
# 
# In addition there are several other methods such as the Jackknife and the Blocking methods. We will discuss in particular
# cross-validation and the bootstrap method.

# ## Resampling approaches can be computationally expensive
# 
# Resampling approaches can be computationally expensive, because they
# involve fitting the same statistical method multiple times using
# different subsets of the training data. However, due to recent
# advances in computing power, the computational requirements of
# resampling methods generally are not prohibitive. In this chapter, we
# discuss two of the most commonly used resampling methods,
# cross-validation and the bootstrap. Both methods are important tools
# in the practical application of many statistical learning
# procedures. For example, cross-validation can be used to estimate the
# test error associated with a given statistical learning method in
# order to evaluate its performance, or to select the appropriate level
# of flexibility. The process of evaluating a model’s performance is
# known as model assessment, whereas the process of selecting the proper
# level of flexibility for a model is known as model selection. The
# bootstrap is widely used.

# ## Why resampling methods ?
# **Statistical analysis.**
# 
# * Our simulations can be treated as *computer experiments*. This is particularly the case for Monte Carlo methods which are widely used in statistical analyses.
# 
# * The results can be analysed with the same statistical tools as we would use when analysing experimental data.
# 
# * As in all experiments, we are looking for expectation values and an estimate of how accurate they are, i.e., possible sources for errors.

# ## Statistical analysis
# 
# * As in other experiments, many numerical  experiments have two classes of errors:
# 
#   * Statistical errors
# 
#   * Systematical errors
# 
# * Statistical errors can be estimated using standard tools from statistics
# 
# * Systematical errors are method specific and must be treated differently from case to case.

# ## Resampling methods
# 
# With all these analytical equations for both the OLS and Ridge
# regression, we will now outline how to assess a given model. This will
# lead to a discussion of the so-called bias-variance tradeoff (see
# below) and so-called resampling methods.
# 
# One of the quantities we have discussed as a way to measure errors is
# the mean-squared error (MSE), mainly used for fitting of continuous
# functions. Another choice is the absolute error.
# 
# In the discussions below we will focus on the MSE and in particular since we will split the data into test and training data,
# we discuss the
# 1. prediction error or simply the **test error** $\mathrm{Err_{Test}}$, where we have a fixed training set and the test error is the MSE arising from the data reserved for testing. We discuss also the 
# 
# 2. training error $\mathrm{Err_{Train}}$, which is the average loss over the training data.
# 
# As our model becomes more and more complex, more of the training data tends to  used. The training may thence adapt to more complicated structures in the data. This may lead to a decrease in the bias (see below for code example) and a slight increase of the variance for the test error.
# For a certain level of complexity the test error will reach minimum, before starting to increase again. The
# training error reaches a saturation.

# ## Resampling methods: Bootstrap
# Bootstrapping is a [non-parametric approach](https://en.wikipedia.org/wiki/Nonparametric_statistics) to statistical inference
# that substitutes computation for more traditional distributional
# assumptions and asymptotic results. Bootstrapping offers a number of
# advantages: 
# 1. The bootstrap is quite general, although there are some cases in which it fails.  
# 
# 2. Because it does not require distributional assumptions (such as normally distributed errors), the bootstrap can provide more accurate inferences when the data are not well behaved or when the sample size is small.  
# 
# 3. It is possible to apply the bootstrap to statistics with sampling distributions that are difficult to derive, even asymptotically. 
# 
# 4. It is relatively simple to apply the bootstrap to complex data-collection plans (such as stratified and clustered samples).
# 
# The textbook by [Davison on the Bootstrap Methods and their Applications](https://www.cambridge.org/core/books/bootstrap-methods-and-their-application/ED2FD043579F27952363566DC09CBD6A) provides many more insights and proofs. In this course we will take a more practical approach and use the results and theorems provided in the literature. For those interested in reading more about the bootstrap methods, we recommend the above text and the one by [Efron and Tibshirani](https://www.routledge.com/An-Introduction-to-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317).
# 
# Before we proceed however, we need to remind ourselves about a central theorem in statistics, namely the so-called **central limit theorem**.

# ## The Central Limit Theorem
# 
# Suppose we have a PDF $p(x)$ from which we generate  a series $N$
# of averages $\mathbb{E}[x_i]$. Each mean value $\mathbb{E}[x_i]$
# is viewed as the average of a specific measurement, e.g., throwing 
# dice 100 times and then taking the average value, or producing a certain
# amount of random numbers. 
# For notational ease, we set $\mathbb{E}[x_i]=x_i$ in the discussion
# which follows. We do the same for $\mathbb{E}[z]=z$.
# 
# If we compute the mean $z$ of $m$ such mean values $x_i$

# $$
# z=\frac{x_1+x_2+\dots+x_m}{m},
# $$

# the question we pose is which is the PDF of the new variable $z$.

# ## Finding the Limit
# 
# The probability of obtaining an average value $z$ is the product of the 
# probabilities of obtaining arbitrary individual mean values $x_i$,
# but with the constraint that the average is $z$. We can express this through
# the following expression

# $$
# \tilde{p}(z)=\int dx_1p(x_1)\int dx_2p(x_2)\dots\int dx_mp(x_m)
#     \delta(z-\frac{x_1+x_2+\dots+x_m}{m}),
# $$

# where the $\delta$-function enbodies the constraint that the mean is $z$.
# All measurements that lead to each individual $x_i$ are expected to
# be independent, which in turn means that we can express $\tilde{p}$ as the 
# product of individual $p(x_i)$.  The independence assumption is important in the derivation of the central limit theorem.

# ## Rewriting the $\delta$-function
# 
# If we use the integral expression for the $\delta$-function

# $$
# \delta(z-\frac{x_1+x_2+\dots+x_m}{m})=\frac{1}{2\pi}\int_{-\infty}^{\infty}
#    dq\exp{\left(iq(z-\frac{x_1+x_2+\dots+x_m}{m})\right)},
# $$

# and inserting $e^{i\mu q-i\mu q}$ where $\mu$ is the mean value
# we arrive at

# $$
# \tilde{p}(z)=\frac{1}{2\pi}\int_{-\infty}^{\infty}
#    dq\exp{\left(iq(z-\mu)\right)}\left[\int_{-\infty}^{\infty}
#    dxp(x)\exp{\left(iq(\mu-x)/m\right)}\right]^m,
# $$

# with the integral over $x$ resulting in

# $$
# \int_{-\infty}^{\infty}dxp(x)\exp{\left(iq(\mu-x)/m\right)}=
#   \int_{-\infty}^{\infty}dxp(x)
#    \left[1+\frac{iq(\mu-x)}{m}-\frac{q^2(\mu-x)^2}{2m^2}+\dots\right].
# $$

# ## Identifying Terms
# 
# The second term on the rhs disappears since this is just the mean and 
# employing the definition of $\sigma^2$ we have

# $$
# \int_{-\infty}^{\infty}dxp(x)e^{\left(iq(\mu-x)/m\right)}=
#   1-\frac{q^2\sigma^2}{2m^2}+\dots,
# $$

# resulting in

# $$
# \left[\int_{-\infty}^{\infty}dxp(x)\exp{\left(iq(\mu-x)/m\right)}\right]^m\approx
#   \left[1-\frac{q^2\sigma^2}{2m^2}+\dots \right]^m,
# $$

# and in the limit $m\rightarrow \infty$ we obtain

# $$
# \tilde{p}(z)=\frac{1}{\sqrt{2\pi}(\sigma/\sqrt{m})}
#     \exp{\left(-\frac{(z-\mu)^2}{2(\sigma/\sqrt{m})^2}\right)},
# $$

# which is the normal distribution with variance
# $\sigma^2_m=\sigma^2/m$, where $\sigma$ is the variance of the PDF $p(x)$
# and $\mu$ is also the mean of the PDF $p(x)$.

# ## Wrapping it up
# 
# Thus, the central limit theorem states that the PDF $\tilde{p}(z)$ of
# the average of $m$ random values corresponding to a PDF $p(x)$ 
# is a normal distribution whose mean is the 
# mean value of the PDF $p(x)$ and whose variance is the variance
# of the PDF $p(x)$ divided by $m$, the number of values used to compute $z$.
# 
# The central limit theorem leads to the well-known expression for the
# standard deviation, given by

# $$
# \sigma_m=
# \frac{\sigma}{\sqrt{m}}.
# $$

# The latter is true only if the average value is known exactly. This is obtained in the limit
# $m\rightarrow \infty$  only. Because the mean and the variance are measured quantities we obtain 
# the familiar expression in statistics (the so-called Bessel correction)

# $$
# \sigma_m\approx 
# \frac{\sigma}{\sqrt{m-1}}.
# $$

# In many cases however the above estimate for the standard deviation,
# in particular if correlations are strong, may be too simplistic. Keep
# in mind that we have assumed that the variables $x$ are independent
# and identically distributed. This is obviously not always the
# case. For example, the random numbers (or better pseudorandom numbers)
# we generate in various calculations do always exhibit some
# correlations.
# 
# The theorem is satisfied by a large class of PDFs. Note however that for a
# finite $m$, it is not always possible to find a closed form /analytic expression for
# $\tilde{p}(x)$.

# ## Confidence Intervals
# 
# Confidence intervals are used in statistics and represent a type of estimate
# computed from the observed data. This gives a range of values for an
# unknown parameter such as the parameters $\boldsymbol{\beta}$ from linear regression.
# 
# With the OLS expressions for the parameters $\boldsymbol{\beta}$ we found 
# $\mathbb{E}(\boldsymbol{\beta}) = \boldsymbol{\beta}$, which means that the estimator of the regression parameters is unbiased.
# 
# We found also that the variance of the estimate of the $j$-th regression coefficient is
# $\boldsymbol{\sigma}^2 (\boldsymbol{\beta}_j ) = \boldsymbol{\sigma}^2 [(\mathbf{X}^{T} \mathbf{X})^{-1}]_{jj} $.
# 
# This quantity will be used to
# construct a confidence interval for the estimates.

# ## Standard Approach based on the Normal Distribution
# 
# We will assume that the parameters $\beta$ follow a normal
# distribution.  We can then define the confidence interval.  Here we will be using as
# shorthands $\mu_{\beta}$ for the above mean value and $\sigma_{\beta}$
# for the standard deviation. We have then a confidence interval

# $$
# \left(\mu_{\beta}\pm \frac{z\sigma_{\beta}}{\sqrt{n}}\right),
# $$

# where $z$ defines the level of certainty (or confidence). For a normal
# distribution typical parameters are $z=2.576$ which corresponds to a
# confidence of $99\%$ while $z=1.96$ corresponds to a confidence of
# $95\%$.  A confidence level of $95\%$ is commonly used and it is
# normally referred to as a *two-sigmas* confidence level, that is we
# approximate $z\approx 2$.
# 
# For more discussions of confidence intervals (and in particular linked with a discussion of the bootstrap method), see chapter 5 of the textbook by [Davison on the Bootstrap Methods and their Applications](https://www.cambridge.org/core/books/bootstrap-methods-and-their-application/ED2FD043579F27952363566DC09CBD6A)
# 
# In this text you will also find an in-depth discussion of the
# Bootstrap method, why it works and various theorems related to it.

# ## Resampling methods: Bootstrap background
# 
# Since $\widehat{\beta} = \widehat{\beta}(\boldsymbol{X})$ is a function of random variables,
# $\widehat{\beta}$ itself must be a random variable. Thus it has
# a pdf, call this function $p(\boldsymbol{t})$. The aim of the bootstrap is to
# estimate $p(\boldsymbol{t})$ by the relative frequency of
# $\widehat{\beta}$. You can think of this as using a histogram
# in the place of $p(\boldsymbol{t})$. If the relative frequency closely
# resembles $p(\vec{t})$, then using numerics, it is straight forward to
# estimate all the interesting parameters of $p(\boldsymbol{t})$ using point
# estimators.

# ## Resampling methods: More Bootstrap background
# 
# In the case that $\widehat{\beta}$ has
# more than one component, and the components are independent, we use the
# same estimator on each component separately.  If the probability
# density function of $X_i$, $p(x)$, had been known, then it would have
# been straightforward to do this by: 
# 1. Drawing lots of numbers from $p(x)$, suppose we call one such set of numbers $(X_1^*, X_2^*, \cdots, X_n^*)$. 
# 
# 2. Then using these numbers, we could compute a replica of $\widehat{\beta}$ called $\widehat{\beta}^*$. 
# 
# By repeated use of the above two points, many
# estimates of $\widehat{\beta}$ can  be obtained. The
# idea is to use the relative frequency of $\widehat{\beta}^*$
# (think of a histogram) as an estimate of $p(\boldsymbol{t})$.

# ## Resampling methods: Bootstrap approach
# 
# But
# unless there is enough information available about the process that
# generated $X_1,X_2,\cdots,X_n$, $p(x)$ is in general
# unknown. Therefore, [Efron in 1979](https://projecteuclid.org/euclid.aos/1176344552)  asked the
# question: What if we replace $p(x)$ by the relative frequency
# of the observation $X_i$?
# 
# If we draw observations in accordance with
# the relative frequency of the observations, will we obtain the same
# result in some asymptotic sense? The answer is yes.

# ## Resampling methods: Bootstrap steps
# 
# The independent bootstrap works like this: 
# 
# 1. Draw with replacement $n$ numbers for the observed variables $\boldsymbol{x} = (x_1,x_2,\cdots,x_n)$. 
# 
# 2. Define a vector $\boldsymbol{x}^*$ containing the values which were drawn from $\boldsymbol{x}$. 
# 
# 3. Using the vector $\boldsymbol{x}^*$ compute $\widehat{\beta}^*$ by evaluating $\widehat \beta$ under the observations $\boldsymbol{x}^*$. 
# 
# 4. Repeat this process $k$ times. 
# 
# When you are done, you can draw a histogram of the relative frequency
# of $\widehat \beta^*$. This is your estimate of the probability
# distribution $p(t)$. Using this probability distribution you can
# estimate any statistics thereof. In principle you never draw the
# histogram of the relative frequency of $\widehat{\beta}^*$. Instead
# you use the estimators corresponding to the statistic of interest. For
# example, if you are interested in estimating the variance of $\widehat
# \beta$, apply the etsimator $\widehat \sigma^2$ to the values
# $\widehat \beta^*$.

# ## Code example for the Bootstrap method
# 
# The following code starts with a Gaussian distribution with mean value
# $\mu =100$ and variance $\sigma=15$. We use this to generate the data
# used in the bootstrap analysis. The bootstrap analysis returns a data
# set after a given number of bootstrap operations (as many as we have
# data points). This data set consists of estimated mean values for each
# bootstrap operation. The histogram generated by the bootstrap method
# shows that the distribution for these mean values is also a Gaussian,
# centered around the mean value $\mu=100$ but with standard deviation
# $\sigma/\sqrt{n}$, where $n$ is the number of bootstrap samples (in
# this case the same as the number of original data points). The value
# of the standard deviation is what we expect from the central limit
# theorem.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
from time import time
from scipy.stats import norm
import matplotlib.pyplot as plt

# Returns mean of bootstrap samples 
# Bootstrap algorithm
def bootstrap(data, datapoints):
    t = np.zeros(datapoints)
    n = len(data)
    # non-parametric bootstrap         
    for i in range(datapoints):
        t[i] = np.mean(data[np.random.randint(0,n,n)])
    # analysis    
    print("Bootstrap Statistics :")
    print("original           bias      std. error")
    print("%8g %8g %14g %15g" % (np.mean(data), np.std(data),np.mean(t),np.std(t)))
    return t

# We set the mean value to 100 and the standard deviation to 15
mu, sigma = 100, 15
datapoints = 10000
# We generate random numbers according to the normal distribution
x = mu + sigma*np.random.randn(datapoints)
# bootstrap returns the data sample                                    
t = bootstrap(x, datapoints)


# We see that our new variance and from that the standard deviation, agrees with the central limit theorem.

# ## Plotting the Histogram

# In[2]:


# the histogram of the bootstrapped data (normalized data if density = True)
n, binsboot, patches = plt.hist(t, 50, density=True, facecolor='red', alpha=0.75)
# add a 'best fit' line  
y = norm.pdf(binsboot, np.mean(t), np.std(t))
lt = plt.plot(binsboot, y, 'b', linewidth=1)
plt.xlabel('x')
plt.ylabel('Probability')
plt.grid(True)
plt.show()


# ## The bias-variance tradeoff
# 
# We will discuss the bias-variance tradeoff in the context of
# continuous predictions such as regression. However, many of the
# intuitions and ideas discussed here also carry over to classification
# tasks. Consider a dataset $\mathcal{D}$ consisting of the data
# $\mathbf{X}_\mathcal{D}=\{(y_j, \boldsymbol{x}_j), j=0\ldots n-1\}$. 
# 
# Let us assume that the true data is generated from a noisy model

# $$
# \boldsymbol{y}=f(\boldsymbol{x}) + \boldsymbol{\epsilon}
# $$

# where $\epsilon$ is normally distributed with mean zero and standard deviation $\sigma^2$.
# 
# In our derivation of the ordinary least squares method we defined then
# an approximation to the function $f$ in terms of the parameters
# $\boldsymbol{\beta}$ and the design matrix $\boldsymbol{X}$ which embody our model,
# that is $\boldsymbol{\tilde{y}}=\boldsymbol{X}\boldsymbol{\beta}$. 
# 
# Thereafter we found the parameters $\boldsymbol{\beta}$ by optimizing the means squared error via the so-called cost function

# $$
# C(\boldsymbol{X},\boldsymbol{\beta}) =\frac{1}{n}\sum_{i=0}^{n-1}(y_i-\tilde{y}_i)^2=\mathbb{E}\left[(\boldsymbol{y}-\boldsymbol{\tilde{y}})^2\right].
# $$

# We can rewrite this as

# $$
# \mathbb{E}\left[(\boldsymbol{y}-\boldsymbol{\tilde{y}})^2\right]=\frac{1}{n}\sum_i(f_i-\mathbb{E}\left[\boldsymbol{\tilde{y}}\right])^2+\frac{1}{n}\sum_i(\tilde{y}_i-\mathbb{E}\left[\boldsymbol{\tilde{y}}\right])^2+\sigma^2.
# $$

# The three terms represent the square of the bias of the learning
# method, which can be thought of as the error caused by the simplifying
# assumptions built into the method. The second term represents the
# variance of the chosen model and finally the last terms is variance of
# the error $\boldsymbol{\epsilon}$.
# 
# To derive this equation, we need to recall that the variance of $\boldsymbol{y}$ and $\boldsymbol{\epsilon}$ are both equal to $\sigma^2$. The mean value of $\boldsymbol{\epsilon}$ is by definition equal to zero. Furthermore, the function $f$ is not a stochastics variable, idem for $\boldsymbol{\tilde{y}}$.
# We use a more compact notation in terms of the expectation value

# $$
# \mathbb{E}\left[(\boldsymbol{y}-\boldsymbol{\tilde{y}})^2\right]=\mathbb{E}\left[(\boldsymbol{f}+\boldsymbol{\epsilon}-\boldsymbol{\tilde{y}})^2\right],
# $$

# and adding and subtracting $\mathbb{E}\left[\boldsymbol{\tilde{y}}\right]$ we get

# $$
# \mathbb{E}\left[(\boldsymbol{y}-\boldsymbol{\tilde{y}})^2\right]=\mathbb{E}\left[(\boldsymbol{f}+\boldsymbol{\epsilon}-\boldsymbol{\tilde{y}}+\mathbb{E}\left[\boldsymbol{\tilde{y}}\right]-\mathbb{E}\left[\boldsymbol{\tilde{y}}\right])^2\right],
# $$

# which, using the abovementioned expectation values can be rewritten as

# $$
# \mathbb{E}\left[(\boldsymbol{y}-\boldsymbol{\tilde{y}})^2\right]=\mathbb{E}\left[(\boldsymbol{y}-\mathbb{E}\left[\boldsymbol{\tilde{y}}\right])^2\right]+\mathrm{Var}\left[\boldsymbol{\tilde{y}}\right]+\sigma^2,
# $$

# that is the rewriting in terms of the so-called bias, the variance of the model $\boldsymbol{\tilde{y}}$ and the variance of $\boldsymbol{\epsilon}$.

# ## A way to Read the Bias-Variance Tradeoff
# 
# <!-- dom:FIGURE: [figures/BiasVariance.png, width=600 frac=0.9] -->
# <!-- begin figure -->
# 
# <img src="figures/BiasVariance.png" width="600"><p style="font-size: 0.9em"><i>Figure 1: </i></p>
# <!-- end figure -->

# ## Example code for Bias-Variance tradeoff

# In[3]:


import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.utils import resample

np.random.seed(2018)

n = 500
n_boostraps = 100
degree = 18  # A quite high value, just to show.
noise = 0.1

# Make data set.
x = np.linspace(-1, 3, n).reshape(-1, 1)
y = np.exp(-x**2) + 1.5 * np.exp(-(x-2)**2) + np.random.normal(0, 0.1, x.shape)

# Hold out some test data that is never used in training.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Combine x transformation and model into one operation.
# Not neccesary, but convenient.
model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression(fit_intercept=False))

# The following (m x n_bootstraps) matrix holds the column vectors y_pred
# for each bootstrap iteration.
y_pred = np.empty((y_test.shape[0], n_boostraps))
for i in range(n_boostraps):
    x_, y_ = resample(x_train, y_train)

    # Evaluate the new model on the same test data each time.
    y_pred[:, i] = model.fit(x_, y_).predict(x_test).ravel()

# Note: Expectations and variances taken w.r.t. different training
# data sets, hence the axis=1. Subsequent means are taken across the test data
# set in order to obtain a total value, but before this we have error/bias/variance
# calculated per data point in the test set.
# Note 2: The use of keepdims=True is important in the calculation of bias as this 
# maintains the column vector form. Dropping this yields very unexpected results.
error = np.mean( np.mean((y_test - y_pred)**2, axis=1, keepdims=True) )
bias = np.mean( (y_test - np.mean(y_pred, axis=1, keepdims=True))**2 )
variance = np.mean( np.var(y_pred, axis=1, keepdims=True) )
print('Error:', error)
print('Bias^2:', bias)
print('Var:', variance)
print('{} >= {} + {} = {}'.format(error, bias, variance, bias+variance))

plt.plot(x[::5, :], y[::5, :], label='f(x)')
plt.scatter(x_test, y_test, label='Data points')
plt.scatter(x_test, np.mean(y_pred, axis=1), label='Pred')
plt.legend()
plt.show()


# ## Understanding what happens

# In[4]:


import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.utils import resample

np.random.seed(2018)

n = 40
n_boostraps = 100
maxdegree = 14


# Make data set.
x = np.linspace(-3, 3, n).reshape(-1, 1)
y = np.exp(-x**2) + 1.5 * np.exp(-(x-2)**2)+ np.random.normal(0, 0.1, x.shape)
error = np.zeros(maxdegree)
bias = np.zeros(maxdegree)
variance = np.zeros(maxdegree)
polydegree = np.zeros(maxdegree)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

for degree in range(maxdegree):
    model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression(fit_intercept=False))
    y_pred = np.empty((y_test.shape[0], n_boostraps))
    for i in range(n_boostraps):
        x_, y_ = resample(x_train, y_train)
        y_pred[:, i] = model.fit(x_, y_).predict(x_test).ravel()

    polydegree[degree] = degree
    error[degree] = np.mean( np.mean((y_test - y_pred)**2, axis=1, keepdims=True) )
    bias[degree] = np.mean( (y_test - np.mean(y_pred, axis=1, keepdims=True))**2 )
    variance[degree] = np.mean( np.var(y_pred, axis=1, keepdims=True) )
    print('Polynomial degree:', degree)
    print('Error:', error[degree])
    print('Bias^2:', bias[degree])
    print('Var:', variance[degree])
    print('{} >= {} + {} = {}'.format(error[degree], bias[degree], variance[degree], bias[degree]+variance[degree]))

plt.plot(polydegree, error, label='Error')
plt.plot(polydegree, bias, label='bias')
plt.plot(polydegree, variance, label='Variance')
plt.legend()
plt.show()


# ## Summing up
# 
# The bias-variance tradeoff summarizes the fundamental tension in
# machine learning, particularly supervised learning, between the
# complexity of a model and the amount of training data needed to train
# it.  Since data is often limited, in practice it is often useful to
# use a less-complex model with higher bias, that is  a model whose asymptotic
# performance is worse than another model because it is easier to
# train and less sensitive to sampling noise arising from having a
# finite-sized training dataset (smaller variance). 
# 
# The above equations tell us that in
# order to minimize the expected test error, we need to select a
# statistical learning method that simultaneously achieves low variance
# and low bias. Note that variance is inherently a nonnegative quantity,
# and squared bias is also nonnegative. Hence, we see that the expected
# test MSE can never lie below $Var(\epsilon)$, the irreducible error.
# 
# What do we mean by the variance and bias of a statistical learning
# method? The variance refers to the amount by which our model would change if we
# estimated it using a different training data set. Since the training
# data are used to fit the statistical learning method, different
# training data sets  will result in a different estimate. But ideally the
# estimate for our model should not vary too much between training
# sets. However, if a method has high variance  then small changes in
# the training data can result in large changes in the model. In general, more
# flexible statistical methods have higher variance.
# 
# You may also find this recent [article](https://www.pnas.org/content/116/32/15849) of interest.

# ## Another Example from Scikit-Learn's Repository

# In[5]:


"""
============================
Underfitting vs. Overfitting
============================

This example demonstrates the problems of underfitting and overfitting and
how we can use linear regression with polynomial features to approximate
nonlinear functions. The plot shows the function that we want to approximate,
which is a part of the cosine function. In addition, the samples from the
real function and the approximations of different models are displayed. The
models have polynomial features of different degrees. We can see that a
linear function (polynomial with degree 1) is not sufficient to fit the
training samples. This is called **underfitting**. A polynomial of degree 4
approximates the true function almost perfectly. However, for higher degrees
the model will **overfit** the training data, i.e. it learns the noise of the
training data.
We evaluate quantitatively **overfitting** / **underfitting** by using
cross-validation. We calculate the mean squared error (MSE) on the validation
set, the higher, the less likely the model generalizes correctly from the
training data.
"""

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score


def true_fun(X):
    return np.cos(1.5 * np.pi * X)

np.random.seed(0)

n_samples = 30
degrees = [1, 4, 15]

X = np.sort(np.random.rand(n_samples))
y = true_fun(X) + np.random.randn(n_samples) * 0.1

plt.figure(figsize=(14, 5))
for i in range(len(degrees)):
    ax = plt.subplot(1, len(degrees), i + 1)
    plt.setp(ax, xticks=(), yticks=())

    polynomial_features = PolynomialFeatures(degree=degrees[i],
                                             include_bias=False)
    linear_regression = LinearRegression()
    pipeline = Pipeline([("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])
    pipeline.fit(X[:, np.newaxis], y)

    # Evaluate the models using crossvalidation
    scores = cross_val_score(pipeline, X[:, np.newaxis], y,
                             scoring="neg_mean_squared_error", cv=10)

    X_test = np.linspace(0, 1, 100)
    plt.plot(X_test, pipeline.predict(X_test[:, np.newaxis]), label="Model")
    plt.plot(X_test, true_fun(X_test), label="True function")
    plt.scatter(X, y, edgecolor='b', s=20, label="Samples")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim((0, 1))
    plt.ylim((-2, 2))
    plt.legend(loc="best")
    plt.title("Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
        degrees[i], -scores.mean(), scores.std()))
plt.show()


# ## Various steps in cross-validation
# 
# When the repetitive splitting of the data set is done randomly,
# samples may accidently end up in a fast majority of the splits in
# either training or test set. Such samples may have an unbalanced
# influence on either model building or prediction evaluation. To avoid
# this $k$-fold cross-validation structures the data splitting. The
# samples are divided into $k$ more or less equally sized exhaustive and
# mutually exclusive subsets. In turn (at each split) one of these
# subsets plays the role of the test set while the union of the
# remaining subsets constitutes the training set. Such a splitting
# warrants a balanced representation of each sample in both training and
# test set over the splits. Still the division into the $k$ subsets
# involves a degree of randomness. This may be fully excluded when
# choosing $k=n$. This particular case is referred to as leave-one-out
# cross-validation (LOOCV).

# ## Cross-validation in brief
# 
# For the various values of $k$
# 
# 1. shuffle the dataset randomly.
# 
# 2. Split the dataset into $k$ groups.
# 
# 3. For each unique group:
# 
# a. Decide which group to use as set for test data
# 
# b. Take the remaining groups as a training data set
# 
# c. Fit a model on the training set and evaluate it on the test set
# 
# d. Retain the evaluation score and discard the model
# 
# 5. Summarize the model using the sample of model evaluation scores

# ## Code Example for Cross-validation and $k$-fold Cross-validation
# 
# The code here uses Ridge regression with cross-validation (CV)  resampling and $k$-fold CV in order to fit a specific polynomial.

# In[6]:


import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import PolynomialFeatures

# A seed just to ensure that the random numbers are the same for every run.
# Useful for eventual debugging.
np.random.seed(3155)

# Generate the data.
nsamples = 100
x = np.random.randn(nsamples)
y = 3*x**2 + np.random.randn(nsamples)

## Cross-validation on Ridge regression using KFold only

# Decide degree on polynomial to fit
poly = PolynomialFeatures(degree = 6)

# Decide which values of lambda to use
nlambdas = 500
lambdas = np.logspace(-3, 5, nlambdas)

# Initialize a KFold instance
k = 5
kfold = KFold(n_splits = k)

# Perform the cross-validation to estimate MSE
scores_KFold = np.zeros((nlambdas, k))

i = 0
for lmb in lambdas:
    ridge = Ridge(alpha = lmb)
    j = 0
    for train_inds, test_inds in kfold.split(x):
        xtrain = x[train_inds]
        ytrain = y[train_inds]

        xtest = x[test_inds]
        ytest = y[test_inds]

        Xtrain = poly.fit_transform(xtrain[:, np.newaxis])
        ridge.fit(Xtrain, ytrain[:, np.newaxis])

        Xtest = poly.fit_transform(xtest[:, np.newaxis])
        ypred = ridge.predict(Xtest)

        scores_KFold[i,j] = np.sum((ypred - ytest[:, np.newaxis])**2)/np.size(ypred)

        j += 1
    i += 1


estimated_mse_KFold = np.mean(scores_KFold, axis = 1)

## Cross-validation using cross_val_score from sklearn along with KFold

# kfold is an instance initialized above as:
# kfold = KFold(n_splits = k)

estimated_mse_sklearn = np.zeros(nlambdas)
i = 0
for lmb in lambdas:
    ridge = Ridge(alpha = lmb)

    X = poly.fit_transform(x[:, np.newaxis])
    estimated_mse_folds = cross_val_score(ridge, X, y[:, np.newaxis], scoring='neg_mean_squared_error', cv=kfold)

    # cross_val_score return an array containing the estimated negative mse for every fold.
    # we have to the the mean of every array in order to get an estimate of the mse of the model
    estimated_mse_sklearn[i] = np.mean(-estimated_mse_folds)

    i += 1

## Plot and compare the slightly different ways to perform cross-validation

plt.figure()

plt.plot(np.log10(lambdas), estimated_mse_sklearn, label = 'cross_val_score')
plt.plot(np.log10(lambdas), estimated_mse_KFold, 'r--', label = 'KFold')

plt.xlabel('log10(lambda)')
plt.ylabel('mse')

plt.legend()

plt.show()


# ## More examples on bootstrap and cross-validation and errors

# In[7]:


# Common imports
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.metrics import mean_squared_error
# Where to save the figures and data files
PROJECT_ROOT_DIR = "Results"
FIGURE_ID = "Results/FigureFiles"
DATA_ID = "DataFiles/"

if not os.path.exists(PROJECT_ROOT_DIR):
    os.mkdir(PROJECT_ROOT_DIR)

if not os.path.exists(FIGURE_ID):
    os.makedirs(FIGURE_ID)

if not os.path.exists(DATA_ID):
    os.makedirs(DATA_ID)

def image_path(fig_id):
    return os.path.join(FIGURE_ID, fig_id)

def data_path(dat_id):
    return os.path.join(DATA_ID, dat_id)

def save_fig(fig_id):
    plt.savefig(image_path(fig_id) + ".png", format='png')

infile = open(data_path("EoS.csv"),'r')

# Read the EoS data as  csv file and organize the data into two arrays with density and energies
EoS = pd.read_csv(infile, names=('Density', 'Energy'))
EoS['Energy'] = pd.to_numeric(EoS['Energy'], errors='coerce')
EoS = EoS.dropna()
Energies = EoS['Energy']
Density = EoS['Density']
#  The design matrix now as function of various polytrops

Maxpolydegree = 30
X = np.zeros((len(Density),Maxpolydegree))
X[:,0] = 1.0
testerror = np.zeros(Maxpolydegree)
trainingerror = np.zeros(Maxpolydegree)
polynomial = np.zeros(Maxpolydegree)

trials = 100
for polydegree in range(1, Maxpolydegree):
    polynomial[polydegree] = polydegree
    for degree in range(polydegree):
        X[:,degree] = Density**(degree/3.0)

# loop over trials in order to estimate the expectation value of the MSE
    testerror[polydegree] = 0.0
    trainingerror[polydegree] = 0.0
    for samples in range(trials):
        x_train, x_test, y_train, y_test = train_test_split(X, Energies, test_size=0.2)
        model = LinearRegression(fit_intercept=False).fit(x_train, y_train)
        ypred = model.predict(x_train)
        ytilde = model.predict(x_test)
        testerror[polydegree] += mean_squared_error(y_test, ytilde)
        trainingerror[polydegree] += mean_squared_error(y_train, ypred) 

    testerror[polydegree] /= trials
    trainingerror[polydegree] /= trials
    print("Degree of polynomial: %3d"% polynomial[polydegree])
    print("Mean squared error on training data: %.8f" % trainingerror[polydegree])
    print("Mean squared error on test data: %.8f" % testerror[polydegree])

plt.plot(polynomial, np.log10(trainingerror), label='Training Error')
plt.plot(polynomial, np.log10(testerror), label='Test Error')
plt.xlabel('Polynomial degree')
plt.ylabel('log10[MSE]')
plt.legend()
plt.show()


# Note that we kept the intercept column in the fitting here. This means that we need to set the **intercept** in the call to the **Scikit-Learn** function as **False**. Alternatively, we could have set up the design matrix $X$ without the first column of ones.

# ## The same example but now with cross-validation
# 
# In this example we keep the intercept column again but add cross-validation in order to estimate the best possible value of the means squared error.

# In[8]:


# Common imports
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


# Where to save the figures and data files
PROJECT_ROOT_DIR = "Results"
FIGURE_ID = "Results/FigureFiles"
DATA_ID = "DataFiles/"

if not os.path.exists(PROJECT_ROOT_DIR):
    os.mkdir(PROJECT_ROOT_DIR)

if not os.path.exists(FIGURE_ID):
    os.makedirs(FIGURE_ID)

if not os.path.exists(DATA_ID):
    os.makedirs(DATA_ID)

def image_path(fig_id):
    return os.path.join(FIGURE_ID, fig_id)

def data_path(dat_id):
    return os.path.join(DATA_ID, dat_id)

def save_fig(fig_id):
    plt.savefig(image_path(fig_id) + ".png", format='png')

infile = open(data_path("EoS.csv"),'r')

# Read the EoS data as  csv file and organize the data into two arrays with density and energies
EoS = pd.read_csv(infile, names=('Density', 'Energy'))
EoS['Energy'] = pd.to_numeric(EoS['Energy'], errors='coerce')
EoS = EoS.dropna()
Energies = EoS['Energy']
Density = EoS['Density']
#  The design matrix now as function of various polytrops

Maxpolydegree = 30
X = np.zeros((len(Density),Maxpolydegree))
X[:,0] = 1.0
estimated_mse_sklearn = np.zeros(Maxpolydegree)
polynomial = np.zeros(Maxpolydegree)
k =5
kfold = KFold(n_splits = k)

for polydegree in range(1, Maxpolydegree):
    polynomial[polydegree] = polydegree
    for degree in range(polydegree):
        X[:,degree] = Density**(degree/3.0)
        OLS = LinearRegression(fit_intercept=False)
# loop over trials in order to estimate the expectation value of the MSE
    estimated_mse_folds = cross_val_score(OLS, X, Energies, scoring='neg_mean_squared_error', cv=kfold)
#[:, np.newaxis]
    estimated_mse_sklearn[polydegree] = np.mean(-estimated_mse_folds)

plt.plot(polynomial, np.log10(estimated_mse_sklearn), label='Test Error')
plt.xlabel('Polynomial degree')
plt.ylabel('log10[MSE]')
plt.legend()
plt.show()


# ## Notes on scaling with examples
# 
# The programs here use both ordinrary least squares (OLS) and Ridge
# regression with one value only for the hyperparameter $\lambda$. The
# first example has no scaling and includes the intercept as well and we
# are trying to fit a second-order polynomial. The second code takes out
# the intercept and subtracts the mean values of each column of the
# design matrix and the mean value of the outputs.
# 
# The third and final code uses **Scikit-Learn** as library in order to
# calculate the optimal parameters for OLS and Ridge regression. Note
# that it is highly recommended to not include the intercept in Ridge
# and Lasso regression, in order to avoid penalizing the optimization by
# the intercept. The second and third codes do thus not include the
# intercept. In the second code we do the scaling ourselves while the
# last code uses the standard scaler option included in **Scikit-Learn**, known as centering (where
# we subtract the mean values).

# In[9]:


import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def MSE(y_data,y_model):
    n = np.size(y_model)
    return np.sum((y_data-y_model)**2)/n

def OLS_fit_beta(X, y):
    return np.linalg.pinv(X.T @ X) @ X.T @ y

def Ridge_fit_beta(X, y,L,d):
    I = np.eye(d,d)
    return np.linalg.pinv(X.T @ X + L*I) @ X.T @ y

# Same random numbers for each test.
np.random.seed(2018)
n = 100
d = 3
# hyperparameter lambda
Lambda = 0.01

# Make data set, simple second-order polynomial
x = np.linspace(-3, 3, n)
y = 2.0 + 0.5*x + 5.0*(x**2)+ np.random.randn(n)

# The design matrix X includes the intercept and no scaling is made
X = np.zeros((len(x), d))
for p in range(d):     
    X[:, p] = x ** (p) 


#Split data, no scaling is used and we include the intercept
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


#Calculate beta, own code
beta_OLS = OLS_fit_beta(X_train, y_train)
beta_Ridge = Ridge_fit_beta(X_train, y_train,Lambda,d)
print(beta_OLS)
print(beta_Ridge)
#predict value
ytilde_test_OLS = X_test @ beta_OLS
ytilde_test_Ridge = X_test @ beta_Ridge

#Calculate MSE
print("  ")
print("test MSE of OLS:")
print(MSE(y_test,ytilde_test_OLS))
print("  ")
print("test MSE of Ridge")
print(MSE(y_test,ytilde_test_Ridge))

plt.scatter(x,y,label='Data')
plt.plot(x, X @ beta_OLS,'*', label="OLS_Fit")
plt.plot(x, X @ beta_Ridge, label="Ridge_Fit")
plt.grid()
plt.legend()
plt.show()


# In this example we do not include the intercept and we scale the data by subtracting the mean values. This follows the discussion in the [lecture material](https://compphysics.github.io/MachineLearning/doc/LectureNotes/_build/html/chapter3.html#more-on-rescaling-data).
# see also the weekly slides [for week 36](https://compphysics.github.io/MachineLearning/doc/pub/week36/html/._week36-bs029.html).
# It is recommended whrn we use Ridge and Lasso regression to not include the intercept in the optimization process.
# 
# Before we discuss the code, we repeat some of the basic math from the slides of week 36.
# 
# Let us try to understand what this may imply mathematically when we
# subtract the mean values, also known as *zero centering* or simply *centering*. For
# simplicity, we will focus on  ordinary regression, as done in the above example.
# 
# The cost/loss function  for regression is

# $$
# C(\beta_0, \beta_1, ... , \beta_{p-1}) = \frac{1}{n}\sum_{i=0}^{n} \left(y_i - \beta_0 - \sum_{j=1}^{p-1} X_{ij}\beta_j\right)^2,.
# $$

# Recall also that we use the squared value. This expression can lead to an
# increased penalty for higher differences between predicted and
# output/target values.
# 
# What we have done is to single out the $\beta_0$ term in the
# definition of the mean squared error (MSE).  The design matrix $X$
# does in this case not contain any intercept column.  When we take the
# derivative with respect to $\beta_0$, we want the derivative to obey

# $$
# \frac{\partial C}{\partial \beta_j} = 0,
# $$

# for all $j$. For $\beta_0$ we have

# $$
# \frac{\partial C}{\partial \beta_0} = -\frac{2}{n}\sum_{i=0}^{n-1} \left(y_i - \beta_0 - \sum_{j=1}^{p-1} X_{ij} \beta_j\right).
# $$

# Multiplying away the constant $2/n$, we obtain

# $$
# \sum_{i=0}^{n-1} \beta_0 = \sum_{i=0}^{n-1}y_i - \sum_{i=0}^{n-1} \sum_{j=1}^{p-1} X_{ij} \beta_j.
# $$

# Let us specialize first to the case where we have only two parameters $\beta_0$ and $\beta_1$.
# Our result for $\beta_0$ simplifies then to

# $$
# n\beta_0 = \sum_{i=0}^{n-1}y_i - \sum_{i=0}^{n-1} X_{i1} \beta_1.
# $$

# We obtain then

# $$
# \beta_0 = \frac{1}{n}\sum_{i=0}^{n-1}y_i - \beta_1\frac{1}{n}\sum_{i=0}^{n-1} X_{i1}.
# $$

# If we define

# $$
# \mu_{\boldsymbol{x}_1}=\frac{1}{n}\sum_{i=0}^{n-1} X_{i1},
# $$

# and the mean value of the outputs as

# $$
# \mu_y=\frac{1}{n}\sum_{i=0}^{n-1}y_i,
# $$

# we have

# $$
# \beta_0 = \mu_y - \beta_1\mu_{\boldsymbol{x}_1}.
# $$

# In the general case with more parameters than $\beta_0$ and $\beta_1$, we have

# $$
# \beta_0 = \frac{1}{n}\sum_{i=0}^{n-1}y_i - \frac{1}{n}\sum_{i=0}^{n-1}\sum_{j=1}^{p-1} X_{ij}\beta_j.
# $$

# We can rewrite the latter equation as

# $$
# \beta_0 = \frac{1}{n}\sum_{i=0}^{n-1}y_i - \sum_{j=1}^{p-1} \mu_{\boldsymbol{x}_j}\beta_j,
# $$

# where we have defined

# $$
# \mu_{\boldsymbol{x}_j}=\frac{1}{n}\sum_{i=0}^{n-1} X_{ij},
# $$

# the mean value for all elements of the column vector $\boldsymbol{x}_j$.
# 
# Replacing $y_i$ with $y_i - y_i - \overline{\boldsymbol{y}}$ and centering also our design matrix results in a cost function (in vector-matrix disguise)

# $$
# C(\boldsymbol{\beta}) = (\boldsymbol{\tilde{y}} - \tilde{X}\boldsymbol{\beta})^T(\boldsymbol{\tilde{y}} - \tilde{X}\boldsymbol{\beta}).
# $$

# If we minimize with respect to $\boldsymbol{\beta}$ we have then

# $$
# \hat{\boldsymbol{\beta}} = (\tilde{X}^T\tilde{X})^{-1}\tilde{X}^T\boldsymbol{\tilde{y}},
# $$

# where $\boldsymbol{\tilde{y}} = \boldsymbol{y} - \overline{\boldsymbol{y}}$
# and $\tilde{X}_{ij} = X_{ij} - \frac{1}{n}\sum_{k=0}^{n-1}X_{kj}$.
# 
# For Ridge regression we need to add $\lambda \boldsymbol{\beta}^T\boldsymbol{\beta}$ to the cost function and get then

# $$
# \hat{\boldsymbol{\beta}} = (\tilde{X}^T\tilde{X} + \lambda I)^{-1}\tilde{X}^T\boldsymbol{\tilde{y}}.
# $$

# Now we try to implement this.

# In[10]:



np.random.seed(2018)
n = 100
# we do not include the intercept
d = 2
Lambda = 0.01

# Make data set.
x = np.linspace(-3, 3, n)
y = 2.0 + 0.5*x + 5.0*(x**2)+ np.random.randn(n)

#Design matrix X does not include the intercept. 
X = np.zeros((len(x), d))
for p in range(d):     
    X[:, p] = x ** (p+1)


#Split data in train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scale data by subtracting mean value,own implementation
#For our own implementation, we will need to deal with the intercept by centering the design matrix and the target variable
X_train_mean = np.mean(X_train,axis=0)
#Center by removing mean from each feature
X_train_scaled = X_train - X_train_mean
X_test_scaled = X_test - X_train_mean
#The model intercept (called y_scaler) is given by the mean of the target variable (IF X is centered, note)
y_scaler = np.mean(y_train)
y_train_scaled = y_train - y_scaler


#Calculate beta
beta_OLS = OLS_fit_beta(X_train_scaled, y_train_scaled)
beta_Ridge = Ridge_fit_beta(X_train_scaled, y_train_scaled,Lambda,d)
print(beta_OLS)
print(beta_Ridge)
# calculate intercepts and print them
interceptOLS = y_scaler - X_train_mean @ beta_OLS
interceptRidge = y_scaler - X_train_mean @ beta_Ridge
print(interceptOLS)
print(interceptRidge)

#predict value with intercept
ytilde_test_OLS = X_test_scaled @ beta_OLS+y_scaler
ytilde_test_Ridge = X_test_scaled @ beta_Ridge+y_scaler


#Calculate MSE

print("  ")
print("test MSE of OLS:")
print(MSE(y_test,ytilde_test_OLS))
print("  ")
print("test MSE of Ridge")
print(MSE(y_test,ytilde_test_Ridge))

plt.scatter(x,y,label='Data')
plt.plot(x, X @ beta_OLS+interceptOLS,'*', label="OLS_Fit")
plt.plot(x, X @ beta_Ridge+interceptRidge, label="Ridge_Fit")
plt.grid()
plt.legend()
plt.show()


# Finally, instead of using our own function we repeat the same example
# using the **standardscaler** functionality of the library
# **Scikit-Learn**.  Here we limit ourselves to Ridge regression only.

# In[11]:


from sklearn import linear_model
np.random.seed(2018)
n = 10
d = 2
Lambda = 0.01

# Make data set.
x = np.linspace(-3, 3, n)
y = 2.0 + 0.5*x + 5.0*(x**2)+ np.random.randn(n)

# Design matrix X does not include the intercept. 
X = np.zeros((n, d))
for p in range(d):     
    X[:, p] = x ** (p+1)

#Split data in train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Scale data by subtracting mean value of the input using scikit-learn
scaler = StandardScaler(with_std=False)
scaler.fit(X_train)
X_train_mean = np.mean(X_train,axis=0)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
# We scale also the output, here by our own code
y_scaler = np.mean(y_train)
y_train_scaled = y_train - y_scaler
y_test_scaled = y_test- y_scaler

#Calculate beta
OLS = LinearRegression()
betaOLS=OLS.fit(X_train_scaled,y_train_scaled)
ypredictOLS = OLS.predict(X_test_scaled)
linear_model.Ridge(Lambda)
RegRidge.fit(X_train_scaled,y_train_scaled)
ypredictRidge = RegRidge.predict(X_test_scaled)
betaOLS = OLS.coef_
betaRidge = RegRidge.coef_
print(betaOLS)
print(betaRidge)
interceptOLS = np.mean(y_train) - X_train_mean @ betaOLS
interceptRidge = y_scaler - X_train_mean @ betaRidge
print(interceptOLS)
print(interceptRidge)
#predict value 
ytilde_test_Ridge = X_test_scaled @ betaRidge+y_scaler
ytilde_test_OLS = X_test_scaled @ betaOLS+y_scaler

#Calculate MSE
print("  ")
print("test MSE of OLS")
print(MSE(y_test,ytilde_test_OLS))
print("  ")
print("test MSE of Ridge")
print(MSE(y_test,ytilde_test_Ridge))
plt.scatter(x,y,label='Data')
plt.plot(x, X @ RegRidge.coef_ + RegRidge.intercept_ , label="Ridge_Fit")
plt.grid()
plt.legend()
plt.show()

