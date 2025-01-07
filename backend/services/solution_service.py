from deap import base, creator, tools
import random
import os
import calendar
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from services.genetic_algorithm import eaSimpleWithElitism
from repositories.repository import ShiftRepository, ScheduleRepository
from database.models import Schedule,Shift

# Constants for genetic algorithm configuration
POPULATION_SIZE = 900
P_CROSSOVER = 0.9
P_MUTATION = 0.3
MAX_GENERATIONS = 5
HALL_OF_FAME_SIZE = 450
RANDOM_SEED = 42

class SolutionService:
    """
    Service for solving scheduling problems using a genetic algorithm.
    """
    def __init__(self, problem, hard_constraint_penalty=10000):
        """
        Initializes the SolutionService with the given scheduling problem.

        Parameters:
        - problem: The scheduling problem instance.
        - hard_constraint_penalty (int): Penalty for constraint violations.
        """
        self.problem = problem
        self.hard_constraint_penalty = hard_constraint_penalty
        self.toolbox = base.Toolbox()
        self._setup_genetic_algorithm()

    def _setup_genetic_algorithm(self):
        """
        Configures the genetic algorithm parameters and operators.
        """
        random.seed(RANDOM_SEED)

        # Define fitness and individual structure
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        # Register genetic operators
        self.toolbox.register("zeroOrOne", random.randint, 0, 1)
        self.toolbox.register(
            "individualCreator", tools.initRepeat, creator.Individual, self.toolbox.zeroOrOne, len(self.problem)
        )
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.individualCreator)

        self.toolbox.register("evaluate", lambda ind: (self.problem.getCost(ind),))
        self.toolbox.register("select", tools.selTournament, tournsize=2)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / len(self.problem))

    def run_genetic_algorithm(self):
        """
        Executes the genetic algorithm and returns the best solution.

        Returns:
        - best (list): The best solution found by the genetic algorithm.
        """
        population = self.toolbox.populationCreator(n=POPULATION_SIZE)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min)
        stats.register("avg", np.mean)

        hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

        population, logbook = eaSimpleWithElitism(
            population,
            self.toolbox,
            cxpb=P_CROSSOVER,
            mutpb=P_MUTATION,
            ngen=MAX_GENERATIONS,
            stats=stats,
            halloffame=hof,
            verbose=True
        )

        best = hof.items[0]
        print("-- Best Individual = ", best)
        print("-- Best Fitness = ", best.fitness.values[0])
        self.problem.printScheduleInfo(best)

        # # Plot fitness trends
        # min_fitness, avg_fitness = logbook.select("min", "avg")
        # sns.set_style("whitegrid")
        # plt.plot(min_fitness, color='red')
        # plt.plot(avg_fitness, color='green')
        # plt.xlabel('Generation')
        # plt.ylabel('Min / Average Fitness')
        # plt.title('Min and Average Fitness over Generations')

        # # Save plot to 'dev_utils' directory
        # output_dir = 'dev_utils'
        # os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
        # plot_path = os.path.join(output_dir, 'fitness_trends.png')  # File path

        # plt.savefig(plot_path, format='png')  # Save as PNG
        # plt.close()  # Close the plot to free memory
        # print(f"Fitness trends plot saved at: {plot_path}")
        
        return best

    def save_solution_to_db(self, session, month, year, solution):
        """
        Saves the generated solution to the database using the repository layer.

        Parameters:
        - session: Database session.
        - month (str): The month for the schedule.
        - year (int): The year for the schedule.
        - solution (list): The generated solution to save.
        """
        from repositories.repository import ScheduleRepository, ShiftRepository

        # Fetch or create schedule
        try:
            schedule = ScheduleRepository.add_schedule(session, month, year)
        except ValueError:
            schedule = session.query(Schedule).filter_by(month=month, year=year).first()

        # Clear existing shifts via repository
        ShiftRepository.clear_shifts_for_schedule(session, schedule.id)

        # Get the correct year and month dynamically
        schedule_dates = [
            datetime(year, list(calendar.month_name).index(month), day + 1).strftime("%Y-%m-%d")
            for day in range(len(solution))
        ]

        # Initialize shifts list before the loop
        shifts = []

        # Prepare shift data
        for day, date in enumerate(schedule_dates):
            for doctor_idx, assigned in enumerate(solution[day]):
                if assigned == 1:
                    shifts.append({
                        'doctor_id': doctor_idx + 1,
                        'date': date
                    })

        # Save new shifts
        ShiftRepository.save_shifts(session, schedule.id, shifts)
        print("Solution saved successfully!")
