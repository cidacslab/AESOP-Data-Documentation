
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
                          B = B,
                          baseline_ears = baseline_ears,
                          alpha_ears = alpha_ears,
                          method_ears = method_ears) {
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
          if (all(.x$all_count) != 0) {
            datsts <- sts(
              observed = .x$data_count,
              start = c(min(lubridate::epiyear(.x$t)), 
                        lubridate::epiweek(min(.x$t))), frequency = 52,
              epoch = .x$t,
              epochAsDate = T
            )
            tidy.sts(earsC(datsts, control = control_ears)) %>% 
              mutate(alarm = as.character(alarm))
          } else {
            data.frame(alarm = "No record")
          }
        },
        .before = B - 1,
        .complete = TRUE
      )
    ) %>%
    tidyr::unnest(trend_analysis)
}