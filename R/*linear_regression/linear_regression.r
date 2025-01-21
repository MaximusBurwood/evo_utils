# Install and load the required package
if (!require("traitdataform")) {
  install.packages("traitdataform")
}
library(traitdataform)

# Load the PanTHERIA dataset (mammalian traits)
data(pantheria)

# Extract relevant columns and clean the data
df <- pantheria[, c("5-1_AdultBodyMass_g", "18-1_LitterSize")]
colnames(df) <- c("body_mass", "litter_size")
df_clean <- na.omit(df)

# Log-transform body mass to reduce skewness
df_clean$log_body_mass <- log(df_clean$body_mass)

# Perform linear regression: Litter Size vs. Log(Body Mass)
model <- lm(litter_size ~ log_body_mass, data = df_clean)

# Print regression summary
summary(model)

# Plot the relationship
plot(
  litter_size ~ log_body_mass,
  data = df_clean,
  xlab = "Log(Body Mass in grams)",
  ylab = "Litter Size",
  main = "Linear Regression of Litter Size vs. Body Mass"
)
abline(model, col = "red")