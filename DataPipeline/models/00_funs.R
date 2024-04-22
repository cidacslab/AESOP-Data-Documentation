#' classify ears 
#'
#' @param df 
#' @param t 
#' @param data_count 
#' @param all_count 
#' @param B 
#' @param baseline_ears 
#' @param alpha_ears 
#' @param method_ears 
#'
#' @return
#' @export
#'
#' @examples
classify_ears <- function(df,
                          t = date,
                          data_count = dataCount,
                          all_count = allCount,
                          B = 12,
                          baseline_ears = 8,
                          alpha_ears = 0.05,
                          method_ears = "C2") {
  control_ears <- list(
    method = method_ears,
    alpha = alpha_ears,
    baseline = baseline_ears
  )
  grouping <- group_vars(df)
  all_count <- enquo(all_count)
  t <- enquo(t)
  data_count <- enquo(data_count)
  df %>%
    mutate(
      t = lubridate::as_date(!!t),
      data_count = as.numeric(!!data_count),
      all_count = as.numeric(!!all_count)
    ) %>%
    mutate(
      trend_analysis = slider::slide(
        .x = tibble(t, data_count, all_count),
        .f = function(.x) {
          if (all(.x$all_count!= 0)) {
            datsts <- sts(
              observed = .x$data_count,
              start = c(min(lubridate::epiyear(.x$t)), lubridate::epiweek(min(.x$t))), frequency = 52,
              epoch = .x$t,
              epochAsDate = T
            )
            tidy.sts(earsC(datsts, control = control_ears)) |> mutate(alarm = as.character(alarm))
          } else {
            data.frame(alarm = "No data")
          }
        },
        .before = B - 1,
        .complete = TRUE
      )
    ) %>%
    tidyr::unnest(trend_analysis)
}



#' classify_trend
#'
#' @param df 
#' @param t 
#' @param data_count 
#' @param all_count 
#' @param B 
#'
#' @return
#' @export
#'
#' @examples
classify_trend <- function(df, t = date, data_count = dataCount, all_count = allCount, B = 12) {
  
  
  grouping <- group_vars(df)
  all_count <- enquo(all_count)
  t <- enquo(t)
  data_count <- enquo(data_count)
  df %>%
    mutate(
      t = lubridate::as_date(!!t),
      data_count = as.numeric(!!data_count),
      all_count = as.numeric(!!all_count)
    ) %>%
    mutate(
      trend_analysis = slider::slide(
        .x = tibble(t, data_count, all_count),
        .f = function(.x) {
          if (any(.x$all_count==0)) {
            data.frame(neg = NA, pos = NA)
          } else {
            update(mod,
                   newdata = .x,
                   backend = "cmdstanr",
                   cores=2) %>%
              tidy_draws(b_t) |> 
              summarise(neg=mean(b_t<0),
                        pos=mean(b_t>0))
          }
        },
        .before = B - 1,
        .complete = TRUE
      )
    ) %>%
    tidyr::unnest(trend_analysis) %>%
    ungroup() 
}





#' glm_model_fun
#'
#' @param df 
#' @param week_length number of weeks in the output
#' @param disease which numbers use
#' @param formula formula to pass in the nb model
#'
#' @return dataframe with upperbound (proportion of encounters)
#' @export
#'
#' @examples
#' The function define a arbitrary cutoff - The total of encounters of the 
#' current week must be greater than the historical 5%
glm_model_fun <- function(df, 
                          week_length,
                          disease,
                          formula) {
  tryCatch(
    {
      condition <- df |> slice_max(n = week_length, order_by = week_no) |> pull(atend_totais) >
        df |>
        summarise(p5 = quantile(atend_totais, 0.05)) |>
        pull(p5)
      mod <- MASS::glm.nb(as.formula(formula), data = df |> slice_max(n = nrow(df) - week_length, order_by = week_no))
      predicted <- predict(mod, newdata = df |> slice_max(n = week_length, order_by = week_no), se.fit = T, type = "response")
      yhat <- predicted$fit
      dispersion <- mod$theta
      alarm <- ifelse(df |> slice_max(n = week_length, order_by = week_no) |> pull({{disease}}) >
                        qnbinom(1 - alpha, size = dispersion, mu = yhat) &
                        df |>
                        slice_max(n = week_length, order_by = week_no) |>
                        pull(atend_ivas) > 5, 1, 0)
      data.frame(
        week = df |> slice_max(n = week_length, order_by = week_no) |> pull(week),
        observerd = df |> slice_max(n = week_length, order_by = week_no) |> pull({{disease}}), alarm = alarm,
        upperbound = qnbinom(1 - alpha, size = dispersion, mu = yhat),
        error = if_else(condition,"No error","Partial data")
      )
    },
    error = function(e) {
      data.frame(
        week = df |> slice_max(n = week_length, order_by = week_no) |> pull(week),
        observerd = df |> slice_max(n = week_length, order_by = week_no) |> pull({{disease}}),
        error = "Fit Problem"
      )
    }
  )
}




