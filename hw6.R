install.packages("readxl")
library(readxl)

patients <- read_excel("Пациенты.xlsx")
head(patients)

names(patients) <- c("Пол", "Возраст", "Креатинин", "Гемоглобин", "Лейкоциты", "Эритроциты", "Тромбоциты", "СОЭ", "Глюкоза")



## 1. 
str(patients[, c("Возраст", "Глюкоза")])

## 2.
patients$Пол <- factor(patients$Пол, levels = c("м", "ж"))
levels(patients$Пол)

## 3.
patients$возраст_группа_2 <- ifelse(patients$Возраст <= 60, "Молодые", "Старшие")
patients$возраст_группа_2 <- factor(patients$возраст_группа_2, levels = c("Молодые","Старшие"))

## 4.
patients[patients$Возраст > 75, ]

## 5. 
head(patients[, c("Лейкоциты", "Глюкоза")])
summary(patients[, c("Лейкоциты", "Глюкоза")])

## 6. 
aggregate(Глюкоза ~ Пол, data = patients, FUN = mean, na.rm = TRUE)

## 7. 
aggregate(Лейкоциты ~ Пол + возраст_группа_2, data = patients, FUN = mean, na.rm = TRUE)

## 8 он же 9
gluc_stats <- aggregate(Глюкоза ~ Пол, data = patients,
                        FUN = function(x) c(mean = mean(x, na.rm=TRUE),
                                            sd   = sd(x,   na.rm=TRUE),
                                            n    = sum(!is.na(x))))
gluc_stats <- do.call(data.frame, gluc_stats)
names(gluc_stats) <- c("Пол", "Глюкоза_mean", "Глюкоза_sd", "Глюкоза_n")
gluc_stats

## 10. 
boxplot(Глюкоза ~ Пол, data = patients,
        main = "Распределение глюкозы по полу",
        xlab = "Пол", ylab = "Глюкоза")

## 11.
# H0: средний уровень лейкоцитов у мужчин = у женщин
# HA: средние уровни отличаются
tt <- t.test(Лейкоциты ~ Пол, data = patients)
tt
# Если p-value < 0.05, то отклоняем H0 и считаем различия статистически значимыми;
# если p-value >= 0.05, оснований считать различия значимыми нет.

patients_task <- patients
patients_task$Глюкоза[c(3, 15, 45)] <- NA

## 12. 
sum(is.na(patients_task))

## 13.
which(is.na(patients_task$Глюкоза))

## 14. 
patients_no_na <- na.omit(patients_task)
dim(patients_task); dim(patients_no_na)

## 15. 
med_gluc <- median(patients_task$Глюкоза, na.rm = TRUE)
patients_task$Глюкоза[is.na(patients_task$Глюкоза)] <- med_gluc

## 16. 
mean_leuk_by_sex_task <- tapply(patients_task$Лейкоциты, patients_task$Пол, mean, na.rm = TRUE)
mean_leuk_by_sex_no_na <- tapply(patients_no_na$Лейкоциты, patients_no_na$Пол, mean, na.rm = TRUE)
mean_leuk_by_sex_task
mean_leuk_by_sex_no_na

## 17. 
hemo_stats <- aggregate(Гемоглобин ~ возраст_группа_2, data = patients, 
                        FUN = function(x) c(mean = mean(x, na.rm=TRUE),
                                            sd   = sd(x,   na.rm=TRUE)))
final_result <- do.call(data.frame, hemo_stats)
names(final_result) <- c("Возрастная_группа", "Гемоглобин_mean", "Гемоглобин_sd")
final_result

## 18. 
write.csv(final_result, file = "анализ_гемаглобина.csv", row.names = FALSE)