### Generate T growth data

###########################################################################
myDF <- read.csv("met_data/no_tgrowth/EUC_met_data_amb_avg_co2.csv", skip=4)
myDF[1:30, "tgrow"] <- mean(myDF$tair)
for (i in 31:length(myDF$doy)) {
    myDF[i, "tgrow"] <- mean(myDF$tair[i-30:i])
}

### rows
row1 <- "# EUC daily met forcing"
row2 <- "# Data from 2012-2023"
row3 <- paste("# Created by Mingkai Jiang")

row4 <- as.list(c("#--", "--", "c", "mm", "c","c", "c","c","c","c",
                  "kPa", "kPa", "ppm", "t/ha/year", "t/ha/year", "t/ha/year",
                  "m/s", "m/s", "mj/m2/am", "mj/m2/pm"))
row5 <- as.list(as.character(c("#year", "doy", "tair", "rain", "tsoil", "tam", "tpm", "tmin", "tmax",
                               "tday", "vpd_am", "vpd_pm", "co2", "ndep", "nfix", "pdep", "wind", "pres",
                               "wind_am", "wind_pm", "par_am", "par_pm", "tgrow")))

# write into folder
write.table(row1, "met_data/EUC_met_data_amb_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=F, quote = F)

write.table(row2, "met_data/EUC_met_data_amb_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row3, "met_data/EUC_met_data_amb_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row4, "met_data/EUC_met_data_amb_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row5, "met_data/EUC_met_data_amb_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(myDF, "met_data/EUC_met_data_amb_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)


###########################################################################
myDF <- read.csv("met_data/no_tgrowth/EUC_met_data_amb_var_co2.csv", skip=4)
myDF[1:30, "tgrow"] <- mean(myDF$tair)
for (i in 31:length(myDF$doy)) {
    myDF[i, "tgrow"] <- mean(myDF$tair[i-30:i])
}

### rows
row1 <- "# EUC daily met forcing"
row2 <- "# Data from 2012-2023"
row3 <- paste("# Created by Mingkai Jiang")

row4 <- as.list(c("#--", "--", "c", "mm", "c","c", "c","c","c","c",
                  "kPa", "kPa", "ppm", "t/ha/year", "t/ha/year", "t/ha/year",
                  "m/s", "m/s", "mj/m2/am", "mj/m2/pm"))
row5 <- as.list(as.character(c("#year", "doy", "tair", "rain", "tsoil", "tam", "tpm", "tmin", "tmax",
                               "tday", "vpd_am", "vpd_pm", "co2", "ndep", "nfix", "pdep", "wind", "pres",
                               "wind_am", "wind_pm", "par_am", "par_pm", "tgrow")))

# write into folder
write.table(row1, "met_data/EUC_met_data_amb_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=F, quote = F)

write.table(row2, "met_data/EUC_met_data_amb_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row3, "met_data/EUC_met_data_amb_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row4, "met_data/EUC_met_data_amb_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row5, "met_data/EUC_met_data_amb_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(myDF, "met_data/EUC_met_data_amb_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)


###########################################################################
myDF <- read.csv("met_data/no_tgrowth/EUC_met_data_ele_avg_co2.csv", skip=4)
myDF[1:30, "tgrow"] <- mean(myDF$tair)
for (i in 31:length(myDF$doy)) {
    myDF[i, "tgrow"] <- mean(myDF$tair[i-30:i])
}

### rows
row1 <- "# EUC daily met forcing"
row2 <- "# Data from 2012-2023"
row3 <- paste("# Created by Mingkai Jiang")

row4 <- as.list(c("#--", "--", "c", "mm", "c","c", "c","c","c","c",
                  "kPa", "kPa", "ppm", "t/ha/year", "t/ha/year", "t/ha/year",
                  "m/s", "m/s", "mj/m2/am", "mj/m2/pm"))
row5 <- as.list(as.character(c("#year", "doy", "tair", "rain", "tsoil", "tam", "tpm", "tmin", "tmax",
                               "tday", "vpd_am", "vpd_pm", "co2", "ndep", "nfix", "pdep", "wind", "pres",
                               "wind_am", "wind_pm", "par_am", "par_pm", "tgrow")))

# write into folder
write.table(row1, "met_data/EUC_met_data_ele_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=F, quote = F)

write.table(row2, "met_data/EUC_met_data_ele_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row3, "met_data/EUC_met_data_ele_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row4, "met_data/EUC_met_data_ele_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row5, "met_data/EUC_met_data_ele_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(myDF, "met_data/EUC_met_data_ele_avg_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)


###########################################################################
myDF <- read.csv("met_data/no_tgrowth/EUC_met_data_ele_var_co2.csv", skip=4)
myDF[1:30, "tgrow"] <- mean(myDF$tair)
for (i in 31:length(myDF$doy)) {
    myDF[i, "tgrow"] <- mean(myDF$tair[i-30:i])
}

### rows
row1 <- "# EUC daily met forcing"
row2 <- "# Data from 2012-2023"
row3 <- paste("# Created by Mingkai Jiang")

row4 <- as.list(c("#--", "--", "c", "mm", "c","c", "c","c","c","c",
                  "kPa", "kPa", "ppm", "t/ha/year", "t/ha/year", "t/ha/year",
                  "m/s", "m/s", "mj/m2/am", "mj/m2/pm"))
row5 <- as.list(as.character(c("#year", "doy", "tair", "rain", "tsoil", "tam", "tpm", "tmin", "tmax",
                               "tday", "vpd_am", "vpd_pm", "co2", "ndep", "nfix", "pdep", "wind", "pres",
                               "wind_am", "wind_pm", "par_am", "par_pm", "tgrow")))

# write into folder
write.table(row1, "met_data/EUC_met_data_ele_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=F, quote = F)

write.table(row2, "met_data/EUC_met_data_ele_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row3, "met_data/EUC_met_data_ele_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row4, "met_data/EUC_met_data_ele_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row5, "met_data/EUC_met_data_ele_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(myDF, "met_data/EUC_met_data_ele_var_co2.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)


###########################################################################
myDF <- read.csv("met_data/no_tgrowth/EUC_met_data_equilibrium_50_yrs.csv", skip=4)
myDF[1:30, "tgrow"] <- mean(myDF$tair)
for (i in 31:length(myDF$doy)) {
    myDF[i, "tgrow"] <- mean(myDF$tair[i-30:i])
}

### rows
row1 <- "# EUC daily met forcing"
row2 <- "# Data from 2012-2023"
row3 <- paste("# Created by Mingkai Jiang")

row4 <- as.list(c("#--", "--", "c", "mm", "c","c", "c","c","c","c",
                  "kPa", "kPa", "ppm", "t/ha/year", "t/ha/year", "t/ha/year",
                  "m/s", "m/s", "mj/m2/am", "mj/m2/pm"))
row5 <- as.list(as.character(c("#year", "doy", "tair", "rain", "tsoil", "tam", "tpm", "tmin", "tmax",
                               "tday", "vpd_am", "vpd_pm", "co2", "ndep", "nfix", "pdep", "wind", "pres",
                               "wind_am", "wind_pm", "par_am", "par_pm", "tgrow")))

# write into folder
write.table(row1, "met_data/EUC_met_data_equilibrium_50_yrs.csv",
            col.names=F, row.names=F, sep=",", append=F, quote = F)

write.table(row2, "met_data/EUC_met_data_equilibrium_50_yrs.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row3, "met_data/EUC_met_data_equilibrium_50_yrs.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row4, "met_data/EUC_met_data_equilibrium_50_yrs.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row5, "met_data/EUC_met_data_equilibrium_50_yrs.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(myDF, "met_data/EUC_met_data_equilibrium_50_yrs.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)


###########################################################################
myDF <- read.csv("met_data/no_tgrowth/EUC_met_data_industrial_to_present_1750_2011.csv", skip=4)
myDF[1:30, "tgrow"] <- mean(myDF$tair)
for (i in 31:length(myDF$doy)) {
    myDF[i, "tgrow"] <- mean(myDF$tair[i-30:i])
}

### rows
row1 <- "# EUC daily met forcing"
row2 <- "# Data from 2012-2023"
row3 <- paste("# Created by Mingkai Jiang")

row4 <- as.list(c("#--", "--", "c", "mm", "c","c", "c","c","c","c",
                  "kPa", "kPa", "ppm", "t/ha/year", "t/ha/year", "t/ha/year",
                  "m/s", "m/s", "mj/m2/am", "mj/m2/pm"))
row5 <- as.list(as.character(c("#year", "doy", "tair", "rain", "tsoil", "tam", "tpm", "tmin", "tmax",
                               "tday", "vpd_am", "vpd_pm", "co2", "ndep", "nfix", "pdep", "wind", "pres",
                               "wind_am", "wind_pm", "par_am", "par_pm", "tgrow")))

# write into folder
write.table(row1, "met_data/EUC_met_data_industrial_to_present_1750_2011.csv",
            col.names=F, row.names=F, sep=",", append=F, quote = F)

write.table(row2, "met_data/EUC_met_data_industrial_to_present_1750_2011.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row3, "met_data/EUC_met_data_industrial_to_present_1750_2011.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row4, "met_data/EUC_met_data_industrial_to_present_1750_2011.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(row5, "met_data/EUC_met_data_industrial_to_present_1750_2011.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

write.table(myDF, "met_data/EUC_met_data_industrial_to_present_1750_2011.csv",
            col.names=F, row.names=F, sep=",", append=T, quote=F)

