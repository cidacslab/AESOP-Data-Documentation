ssa <- aps |> filter(co_ibge==292740)
library(slider)
tt1 <- slide(ssa, ~.x , .before = Inf, .after=52, .complete=T)
tt2 <- slide(ssa, ~.x , .before = Inf)