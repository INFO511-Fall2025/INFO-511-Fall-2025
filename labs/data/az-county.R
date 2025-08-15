library(tidycensus)
library(tidyverse)
library(tigris)
library(sf)

# Load your Census API key
census_api_key("CENSUS_API_KEY", install = TRUE)

# Get the decennial census data for Arizona counties
az_county_raw <- get_decennial(
  geography = "county",
  variables = "P1_001N",
  year = 2020,
  state = "AZ",
  geometry = TRUE,
  keep_geo_vars = TRUE
)

# Process the data
az_county <- az_county_raw |>
  mutate(
    land_area_mi2 = ALAND / 2589988.11,
    density = value / land_area_mi2
  ) |> # m2 ÷ 2,589,988.11 = mi2
  rename(
    county = NAME.x,
    state_abb = STUSPS,
    state_name = STATE_NAME,
    land_area_m2 = ALAND,
    population = value
  ) |>
  select(county, state_abb, state_name, land_area_m2, land_area_mi2, population, density) |>
  st_drop_geometry()

# Display the processed data
print(az_county)

# Save the data to a CSV file
write_csv(az_county, file = "az-county.csv")
