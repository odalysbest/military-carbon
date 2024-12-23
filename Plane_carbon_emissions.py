#!/usr/bin/env python3

"""
Airplane CO2 Emission Calculator
By: Odalys (Odi) Benitez

This script calculates the CO2 emissions of various planes based on their fuel
capacity, combat range, cruise speed, and mission length. It also compares the
emissions to yearly CO2 emissions from car driving and visualizes the data.
"""

from collections import namedtuple
from matplotlib import pyplot as plt
from pint import UnitRegistry

# Initialize the unit registry from the Pint library for handling units
unit = UnitRegistry()

# Constants
KG_CO2_PER_GAL_JP8 = 9.75 * unit.kg / unit.gal  # CO2 produced per gallon of JP-8 jet fuel
JP8_DENSITY = 6.75 * unit.lb / unit.gal  # Density of JP-8 jet fuel


def calculate_co2_per_hour(fuel_cap, combat_range, cruise_speed):
    """
    Calculate the CO2 emissions in metric tons per hour for a plane.

    Parameters:
    fuel_cap (quantity): The fuel capacity of the plane in gallons.
    combat_range (quantity): The combat range of the plane in miles.
    cruise_speed (quantity): The cruise speed of the plane in miles per hour.

    Returns:
    quantity: CO2 emissions in metric tons per hour.
    """
    return (fuel_cap / (2 * combat_range)) * cruise_speed * KG_CO2_PER_GAL_JP8


# Define plane characteristics using namedtuple for better readability
PlaneCharacteristics = namedtuple('PlaneCharacteristics',
                                  ['name', 'fuel_cap', 'combat_range', 'cruise_speed', 'mission_length'])

# Plane data: fuel capacity, combat range, cruise speed, and mission length
planes = [
    PlaneCharacteristics('B-52', 47_975 * unit.gal, 8_800 * unit.mi, 509 * unit.mi / unit.h, 34 * unit.hr),
    PlaneCharacteristics('B-1', 265_274 * unit.lb / JP8_DENSITY, 3_444 * unit.mi, 647 * unit.mi / unit.h, 12 * unit.hr),
    PlaneCharacteristics('B-2', 167_000 * unit.lb / JP8_DENSITY, 6_900 * unit.mi, 560 * unit.mi / unit.h, 31 * unit.hr),
    PlaneCharacteristics('F-15', 13_455 * unit.lb / JP8_DENSITY, 1_221 * unit.mi, 570 * unit.mi / unit.h, 2 * unit.hr),
    PlaneCharacteristics('F-35', 18_250 * unit.lb / JP8_DENSITY, 770 * unit.mi, 647 * unit.mi / unit.h, 2 * unit.hr)
]

# Define a namedtuple to store the CO2 calculations
CO2Emissions = namedtuple('CO2Emissions', ['co2_per_hour', 'co2_per_mission', 'co2_comparison'])

# Initialize a single dictionary to store all results for each plane
plane_emissions = {}

# Calculate yearly CO2 emissions for an average car
KG_CO2_GAL = 8.9 * unit.kg / unit.gal  # CO2 produced per gallon of gasoline
GALLONS_PER_YEAR_DRIVING = 489 * unit.gal / unit.yr  # Average american fuel consumption per year for registered vehicle
CO2_TONS_YEAR_DRIVING = (KG_CO2_GAL * GALLONS_PER_YEAR_DRIVING).to(unit.metric_ton / unit.yr)

# Calculate CO2 emissions per plane and compare to car emissions
for plane in planes:
    co2_hour = calculate_co2_per_hour(plane.fuel_cap, plane.combat_range, plane.cruise_speed).to(
        unit.metric_ton / unit.hour)
    co2_mission = co2_hour * plane.mission_length
    co2_comparison = co2_mission / CO2_TONS_YEAR_DRIVING

    # Store all results in a namedtuple for each plane
    plane_emissions[plane.name] = CO2Emissions(co2_hour, co2_mission, co2_comparison)

    # Output comparison in terms of months, weeks, or years
    print(f"{plane.name}: ", end='')
    if co2_comparison.m > 1:
        print(co2_comparison)
    elif co2_comparison.m > 1 / 12:
        print(co2_comparison.to(unit.month))
    else:
        print(co2_comparison.to(unit.week))


# Plot CO2 emissions per hour for each plane
def plot_co2_emissions(data, title, ylabel, attribute):
    """
    Plot a bar chart for the CO2 emissions data.

    Parameters:
    data (dict): A dictionary of plane names and their CO2 emission values (either per hour or per mission).
    title (str): Title of the plot.
    ylabel (str): Y-axis label.
    attribute (str): Attribute of the CO2Emissions namedtuple to plot ('co2_per_hour' or 'co2_per_mission').
    """
    plane_names = list(data.keys())
    emissions = [getattr(emission, attribute).m for emission in data.values()]  # Use getattr to access the correct attribute

    plt.bar(plane_names, emissions)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.show()


# Plot CO2 emissions per hour
plot_co2_emissions(plane_emissions, "Metric Ton CO2/hr, per plane", "Metric Ton CO2/hr", 'co2_per_hour')

# Plot CO2 emissions per mission
plot_co2_emissions(plane_emissions, "Metric Ton CO2 per mission, per plane", "Metric Ton CO2 per mission", 'co2_per_mission')
