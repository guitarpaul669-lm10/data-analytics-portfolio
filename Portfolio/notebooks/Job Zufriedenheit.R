install.packages(c("tidyverse", "haven", "Hmisc", "dplyr", "car", "psych", "plm", "lmtest"))

#load packages
library(tidyverse)
library(haven)
library(Hmisc)
library(dplyr)
library(car)
library(psych)
library(plm)
library(lmtest)

#Data
soep <- "Z:/Seminardaten/soep-teaching-v37/"

d <- read_dta(paste0(soep,"pequiv.dta"))
e <- read_dta(paste0(soep, "pl.dta"))
f <- read_dta(paste0(soep, "pgen.dta"))

##Variablen

d <- d %>% 
  select(residence = l11101_ew,
         education = d11109,
         age = d11101,
         syear= syear,
         gender= d11102ll,
         pid = pid)


e <- e %>%
  select(gründlich_arb = plh0212, #Big Five
         kommunikativ = plh0213,
         grob_zu_anderen = plh0214,
         originell = plh0215,
         sorgen = plh0216,
         verzeihen = plh0217,
         faul = plh0218,
         gesellig = plh0219,
         künstlerisch = plh0220,
         nervös = plh0221,
         effiziente_arb_weise = plh0222,
         zurückhaltend = plh0223,
         freundlich_Umgang = plh0224,
         phantasievoll = plh0225,
         stress_umgang =plh0226, 
         sat_work = plh0173,          #Satisfaction
         sat_income = plh0176,
         sat_freetime = plh0178,
         sat_life = plh0182,
         isco = p_isco08,             #isco
         syear= syear,                #Formales
         pid = pid)

f <- f %>% 
  select(bruttoverdienst = pglabgro,
         wochenstunden = pgvebzeit ,
         tenure = pgerwzeit,
         syear= syear,
         pid = pid)


#syear 
d <- d %>% filter(syear>=2005 & syear<=2019 ) 
e <- e %>% filter(syear>=2005 & syear <= 2019 )
f <- f %>% filter(syear>=2005 & syear <= 2019 )
h <- left_join(d,e, by = c("pid", "syear")) #zur Überführung von 3 zu 1 Datensatz
g <- left_join(h,f, by=c("pid", "syear"))


#age
g$age[g$age < 18] <- NA

#gender
g$gender[g$gender<0] <- NA
table(g$gender, useNA = "ifany")
g$female <- ifelse(g$gender == 2, yes = 1, no = 0)
table(g$female, useNA = "ifany")                   

#region
table(g$residence)
g$residence[g$residence<0]<- NA
g$West <- ifelse(g$residence == 21, yes = 1, no = 0)
table(g$West, useNA = "ifany")

#education
g$education[g$education<0] <- NA
table(g$education, useNA = "ifany")



##Big Five

#Extraversion (kommunikativ, gesellig, zur?ckhaltend (reversed))

g$kommunikativ[g$kommunikativ<0] <- NA
g$gesellig[g$gesellig<0] <- NA
g$zurückhaltend[g$zurückhaltend<0] <- NA
#reverse von zur?ckhaltend

g$r_zurückhaltend<- recode(g$zurückhaltend, "1=7; 2=6;3=5;5=3;7=1")


#Openess (orginell, k?nstlerisch, phantasievoll)

g$originell[g$originell<0] <- NA
g$künstlerisch[g$künstlerisch<0] <- NA
g$phantasievoll[g$phantasievoll<0] <- NA

#Conscientiousness (gr?ndl_arb, effiziente_arb_weise, faul (reversed))

g$gründlich_arb[g$gründlich_arb<0] <- NA
g$effiziente_arb_weise[g$effiziente_arb_weise<0] <- NA
g$faul[g$faul<0] <- NA

#reverse von faul
g$r_faul<- recode(g$faul, "1=7; 2=6;3=5;5=3;7=1")

#Agreeableness (freundlich, verzeihen, grob_zu_anderen (reversed))
g$freundlich_Umgang[g$freundlich_Umgang<0] <- NA
g$verzeihen[g$verzeihen<0] <- NA
g$grob_zu_anderen[g$grob_zu_anderen<0] <- NA

#reverse von grob zu anderen
g$r_grob_zu_anderen<- recode(g$grob_zu_anderen, "1=7; 2=6;3=5;5=3;7=1")

#Neuroticism (sorgen, nerv?s, stress_umgang)
g$sorgen[g$sorgen<0] <- NA
g$nervös[g$nervös<0] <- NA
g$stress_umgang[g$stress_umgang<0] <- NA

#Skalen f?r die Big Five

g$Extraversion <- rowMeans(subset(g, select = c(kommunikativ, gesellig, r_zurückhaltend)), na.rm = TRUE) 

g$openess <- rowMeans(subset(g, select = c(originell, künstlerisch, phantasievoll)), na.rm = TRUE)

g$conscientiousness <- rowMeans(subset(g, select = c(gründlich_arb,effiziente_arb_weise, r_faul)), na.rm = TRUE)

g$agreeableness <- rowMeans(subset(g, select = c(freundlich_Umgang,verzeihen,r_grob_zu_anderen)), na.rm = TRUE)

g$neuroticism <- rowMeans(subset(g, select = c(sorgen,nervös,stress_umgang)), na.rm = TRUE)

#fill
g <- g %>%
  group_by(pid) %>%
  fill(Extraversion, openess, neuroticism, agreeableness, conscientiousness, .direction = "up")

#Job-Satisfaction

g$sat_work[g$sat_work<0]<- NA
g$sat_income[g$sat_income<0]<- NA
g$sat_freetime[g$sat_freetime<0]<- NA

g$sat_life[g$sat_life<0]<- NA

g$sat_scale <- rowMeans(subset(g, select = c(sat_work, sat_income, sat_freetime )), na.rm = TRUE)



#Job-Produktivität 

g$bruttoverdienst[g$bruttoverdienst<=0]<-NA
g$wochenstunden[g$wochenstunden<=0]<-NA

stundenlohn <- g$bruttoverdienst/(4* g$wochenstunden)
g <- cbind(g,stundenlohn)
names(g)[41] <- "stundenlohn"
g$stundenlohn[g$stundenlohn<=0]<- NA
g$log_stundenlohn <- log(g$stundenlohn)

g$tenure[g$tenure<=0]<- NA



#Berufsgruppen 
g$isco[g$isco<0]<-NA
 


g<- na.omit(g)




#Berufgruppen-Datens?tze

g_soldaten <- g %>%
  filter(isco>=0 & isco<1000)

g_führungskräfte <- g %>%
  filter(isco>=1000 & isco<2000)

g_akademiker <- g %>%
  filter(isco>=2000 & isco<3000)

g_techniker <- g %>%
  filter(isco>=3000 & isco<4000)

g_bürokräfte <- g %>%
  filter(isco>=4000 & isco<5000)

g_dienstleistung <- g %>%
  filter(isco>=5000 & isco<6000)

g_landwirtschaft <- g %>%
  filter(isco>=6000 & isco<7000)

g_handwerk <- g %>%
  filter(isco>=7000 & isco<8000)

g_montierer <- g %>%
  filter(isco>=8000 & isco<9000)

g_hilfsarbeiter <- g %>%
  filter(isco>=9000 & isco<10000)


#Berufshauptgruppen - Akademiker, F?hrungskr?fte, Handwerk und technik, Dienstleistung/B?ro 
g_handwerk_all <- rbind(g_handwerk, g_montierer, g_landwirtschaft)


#Männer und Frauen Subset

g_maenner <- subset(g, female == 0)
g_frauen <- subset(g, female == 1)



#Regressionen 


g <- pdata.frame(g, index = c("pid", "syear"))








#Regressionsergebnisse 


###Alle Job-Produktitvität
#random effects

modell_1 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "random")
summary(modell_1)

#pooling

modell_2 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "pooling")
summary(modell_2)

##Frauen

#Random
modell_3 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_frauen, model = "random")
summary(modell_3)

#pooling
modell_4 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_frauen, model = "pooling")
summary(modell_4)

##Männer
#Random
modell_5 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_maenner, model = "random")
summary(modell_5)
#pooling
modell_6 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_maenner, model = "pooling")
summary(modell_6)

###Satisfaction 

##All
#Random
modell_7<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "random")
summary(modell_7)

modell_8 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "random" )
summary(modell_8)

#pooling
modell_56<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "pooling")
summary(modell_56)

modell_57 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "pooling" )
summary(modell_57)

##Frauen
#Random
modell_9 <- plm(sat_work ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_frauen, model = "random" )
summary(modell_9)

modell_10 <- plm(sat_scale ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_frauen, model = "random" )
summary(modell_10)

#Pooling
modell_58 <- plm(sat_work ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_frauen, model = "pooling" )
summary(modell_58)

modell_59 <- plm(sat_scale ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_frauen, model = "pooling" )
summary(modell_59)

##Männer
#Random
modell_11 <- plm(sat_work ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_maenner, model = "random" )
summary(modell_11)

modell_12 <- plm(sat_scale ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_maenner, model = "random" )
summary(modell_12)

#pooling

modell_60 <- plm(sat_work ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_maenner, model = "pooling" )
summary(modell_60)

modell_61 <- plm(sat_scale ~ age + I(age^2) + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_maenner, model = "pooling" )
summary(modell_61)


##Tenure-Interaktionen 
modell_13 <- plm(log_stundenlohn~ age + I(age^2) + education + female + West + tenure*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g, model = "random")
summary(modell_13)
#pooled
modell_63 <- plm(log_stundenlohn~ age + I(age^2) + education + female + West + tenure*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g, model = "pooling")
summary(modell_63)

#Frau
modell_14 <- plm(log_stundenlohn~ age + I(age^2) + education + West + tenure*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g, model = "random")
summary(modell_14)
#Mann
modell_15 <- plm(log_stundenlohn~ age + I(age^2) + education + West + tenure*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g, model = "random")
summary(modell_15)

##Age Interaktionen  
#All
modell_41 <- plm(log_stundenlohn~  I(age^2) + education + female + West + tenure + age*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g, model = "random")
summary(modell_41)

#pooled
modell_64 <- plm(log_stundenlohn~  I(age^2) + education + female + West + tenure + age*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g, model = "pooling")
summary(modell_64)

#Frau
modell_42 <- plm(log_stundenlohn~ I(age^2) + education + West + tenure + age*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g_frauen, model = "random")
summary(modell_42)
#Mann
modell_43 <- plm(log_stundenlohn~ I(age^2) + education + West  + tenure + age*(Extraversion + openess + neuroticism + agreeableness + conscientiousness), data = g_maenner, model = "random")
summary(modell_43)




###Berufsgruppen

##Akademiker
g_akademiker <- pdata.frame(g_akademiker, index = c("pid", "syear"))

#Lohn

#Random effects
modell_16<- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_akademiker, model = "random")
summary(modell_16)
#pooled
modell_17 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_akademiker, model = "pooling")
summary(modell_17)

#Satisfaction

#Random effects

modell_18<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "random")
summary(modell_18)

modell_19 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "random" )
summary(modell_19)

#pooled
modell_20<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "pooling")
summary(modell_20)

modell_21 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "pooling" )
summary(modell_21)

##Dienstleisung
g_dienstleistung <- pdata.frame(g_dienstleistung, index = c("pid", "syear"))

#Lohn
#Random effects
modell_22<- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_dienstleistung, model = "random")
summary(modell_22)
#pooled
modell_23 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_dienstleistung, model = "pooling")
summary(modell_23)

#Satisfaction

#Random effects
modell_24<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_dienstleistung, model = "random")
summary(modell_24)

modell_25 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_dienstleistung, model = "random" )
summary(modell_25)

#pooled
modell_26<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_dienstleistung, model = "pooling")
summary(modell_26)

modell_27 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_dienstleistung, model = "pooling" )
summary(modell_27)



##Führungskräfte
g_führungskräfte <- pdata.frame(g_führungskräfte, index = c("pid", "syear"))

#Lohn
#Random effects
modell_28<- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_führungskräfte, model = "random")
summary(modell_28)
#pooled
modell_29 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_führungskräfte, model = "pooling")
summary(modell_29)

#Satisfaction

#Random effects

modell_30<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_führungskräfte, model = "random")
summary(modell_30)

modell_31 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_führungskräfte, model = "random" )
summary(modell_31)
#pooled

modell_32<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_führungskräfte, model = "pooling")
summary(modell_32)

modell_33 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_führungskräfte, model = "pooling" )
summary(modell_33)

##Handwerk_all
g_handwerk_all <- pdata.frame(g_handwerk_all, index = c("pid", "syear"))

#Lohn
#Random effects
modell_34<- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_handwerk_all, model = "random")
summary(modell_34)
#pooled
modell_35 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_handwerk_all, model = "pooling")
summary(modell_35)

#Satisfaction

#Random effects

modell_36<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_handwerk_all, model = "random")
summary(modell_36)

modell_37 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_handwerk_all, model = "random" )
summary(modell_37)
#pooled

modell_38<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_handwerk_all, model = "pooling")
summary(modell_38)

modell_39 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_handwerk_all, model = "pooling" )
summary(modell_39)

##büro
g_bürokräfte <- pdata.frame(g_bürokräfte, index = c("pid", "syear"))

#Lohn
#Random effects
modell_44<- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_bürokräfte, model = "random")
summary(modell_44)
#pooled
modell_45 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_bürokräfte, model = "pooling")
summary(modell_45)

#Satisfaction

#Random effects

modell_46<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_bürokräfte, model = "random")
summary(modell_46)

modell_47 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_bürokräfte, model = "random" )
summary(modell_47)

#pooled
modell_48<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_bürokräfte, model = "pooling")
summary(modell_48)

modell_49 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_bürokräfte, model = "pooling" )
summary(modell_49)

##techniker
g_techniker <- pdata.frame(g_techniker, index = c("pid", "syear"))

#Lohn
#Random effects
modell_50<- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_techniker, model = "random")
summary(modell_50)
#pooled
modell_51 <- plm(log_stundenlohn~ age + I(age^2) + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_techniker, model = "pooling")
summary(modell_51)

#Satisfaction

#Random effects
modell_52<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_techniker, model = "random")
summary(modell_52)

modell_53 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_techniker, model = "random" )
summary(modell_53)

#pooled

modell_54<- plm(sat_work~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_techniker, model = "pooling")
summary(modell_54)

modell_55 <- plm(sat_scale ~ age + I(age^2) + female + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g_techniker, model = "pooling" )
summary(modell_55)


### nur Big Five
#Random
modell_40 <- plm(log_stundenlohn~ Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "random")
summary(modell_40)
#pooling
modell_62 <- plm(log_stundenlohn~ Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "pooling")
summary(modell_62)




##Output
library(stargazer)
stargazer(modell_40, modell_1, modell_3, modell_5, modell_13, modell_41,title = "Regressionsergebnisse Job-Produktivität", style = "default", decimal.mark = ",", out = "Job-Produktivität_1.html")

stargazer(modell_7, modell_9, modell_11,modell_8, modell_10, modell_12, title = "Regressionsergebnisse Job-Satisfaction", style = "default", decimal.mark = ",", out = "Job-Satisfaction_1.html")

stargazer(modell_16, modell_22, modell_28,modell_34, modell_44, modell_50, title = "Regressionsergebnisse Job-Produktivität Berufsbereiche",label = "tab:modelle", column.labels = c("Akademiker", "Dienstleistende","Führungskräfte", "Handwerker", "Büro", "Techniker"), style = "default", decimal.mark = ",", out = "Job-Produktivität_2.html")

stargazer(modell_18, modell_24, modell_30,modell_36, modell_46, modell_52, title = "Regressionsergebnisse Job-Satisfaction Berufsbereiche",label = "tab:modelle", column.labels = c("Akademiker", "Dienstleistende","Führungskräfte", "Handwerker", "Büro", "Techniker"), style = "default", decimal.mark = ",", out = "Job-Satisfaction_2.html")

stargazer(modell_19, modell_25, modell_31,modell_37, modell_47, modell_53, title = "Regressionsergebnisse Job-Satisfaction Berufsbereiche",label = "tab:modelle", column.labels = c("Akademiker", "Dienstleistende","Führungskräfte", "Handwerker", "Büro", "Techniker"), style = "default", decimal.mark = ",", out = "Job-Satisfaction_3.html")

#Pooled
stargazer(modell_62, modell_2, modell_4, modell_6,modell_63, modell_64, title = "Regressionsergebnisse Job-Produktivität (Pooled)", style = "default", decimal.mark = ",", out = "Job-Produktivität_pol.html")

stargazer(modell_56, modell_58, modell_60,modell_57, modell_59, modell_61, title = "Regressionsergebnisse Job-Satisfaction (Pooled)", style = "default", decimal.mark = ",", out = "Job-Satisfaction_pol.html")

stargazer(modell_17, modell_23, modell_29,modell_35, modell_45, modell_51, title = "Regressionsergebnisse Job-Produktivität Berufsbereiche (Pooled)",label = "tab:modelle", column.labels = c("Akademiker", "Dienstleistende","Führungskräfte", "Handwerker", "Büro", "Techniker"), style = "default", decimal.mark = ",", out = "Job-Produktivität_pol_1.html")

stargazer(modell_20, modell_26, modell_32,modell_38, modell_58, modell_54, title = "Regressionsergebnisse Job-Satisfaction Berufsbereiche (Pooled)",label = "tab:modelle", column.labels = c("Akademiker", "Dienstleistende","Führungskräfte", "Handwerker", "Büro", "Techniker"), style = "default", decimal.mark = ",", out = "Job-Satisfaction_pol_1.html")

stargazer(modell_21, modell_27, modell_33,modell_39, modell_49, modell_55, title = "Regressionsergebnisse Job-Satisfaction Berufsbereiche (Pooled)",label = "tab:modelle", column.labels = c("Akademiker", "Dienstleistende","Führungskräfte", "Handwerker", "Büro", "Techniker"), style = "default", decimal.mark = ",", out = "Job-Satisfaction_pol_2.html")

#Deskriptive Statistik

summary(g, "table")






###Regressionsdiagnostik

##Varianzinflationsfaktoren


vif(modell_1)
1/vif(modell_1)
#Neues Modell ohne Age^2
modell_a <- plm(log_stundenlohn~ age + tenure + education + female + West + Extraversion + openess + neuroticism + agreeableness + conscientiousness, data = g, model = "random")
vif(modell_a)
1/vif(modell_a)

#Normalverteilung der abhängigen Variable
residuals <- resid(modell_1)  # Residuen

hist(residuals, main="Histogramm der abhängigen Variable", xlab="Werte von y", ylab="Häufigkeit")

#Adison-Darling Test
library(nortest)
ad.test(residuals)


#Homo-/Heteroskedaszitität

residuals <- resid(modell_1)  # Residuen 
predicted <- fitted(modell_1)  # Vorhergesagte Werte

# Streudiagramm der Residuen gegenüber den vorhergesagten Werten 
ggplot(data = data.frame(predicted, residuals), aes(x = predicted, y = residuals)) +
  geom_point() +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  labs(title = "Streudiagramm der Residuen",
       x = "Vorhergesagte Werte", y = "Residuen")

