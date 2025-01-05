from deap import base, creator, tools
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from genetic_algorithm import eaSimpleWithElitism


class SolutionService:
    def __init__(self, problem, hard_constraint_penalty=10000):
        """
        Initializes the SolutionService with the given scheduling problem.

        Parameters:
        - problem (DoctorSchedulingProblem): Pre-configured scheduling problem.
        - hard_constraint_penalty (int): Penalty for constraint violations.
        """
        self.problem = problem
        self.hard_constraint_penalty = hard_constraint_penalty
        self.toolbox = base.Toolbox()
        self._setup_genetic_algorithm()

    def _setup_genetic_algorithm(self):
        """Configures the genetic algorithm parameters."""
        # Constants
        POPULATION_SIZE = 900
        P_CROSSOVER = 0.9
        P_MUTATION = 0.3
        MAX_GENERATIONS = 1000
        HALL_OF_FAME_SIZE = 450

        # Random Seed
        RANDOM_SEED = 42
        random.seed(RANDOM_SEED)

        # Fitness definition
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox.register("zeroOrOne", random.randint, 0, 1)
        self.toolbox.register(
            "individualCreator", tools.initRepeat, creator.Individual, self.toolbox.zeroOrOne, len(self.problem)
        )
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.individualCreator)

        # Fitness evaluation
        self.toolbox.register("evaluate", lambda ind: (self.problem.getCost(ind),))
        self.toolbox.register("select", tools.selTournament, tournsize=2)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / len(self.problem))

        # Save constants
        self.params = {
            'population_size': POPULATION_SIZE,
            'p_crossover': P_CROSSOVER,
            'p_mutation': P_MUTATION,
            'max_generations': MAX_GENERATIONS,
            'hall_of_fame_size': HALL_OF_FAME_SIZE
        }

    def run_genetic_algorithm(self):
        """Executes the genetic algorithm and returns the best solution."""
        # Create population
        population = self.toolbox.populationCreator(n=self.params['population_size'])

        # Setup statistics
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min)
        stats.register("avg", np.mean)

        hof = tools.HallOfFame(self.params['hall_of_fame_size'])

        # Run GA
        population, logbook = eaSimpleWithElitism(
            population,
            self.toolbox,
            cxpb=self.params['p_crossover'],
            mutpb=self.params['p_mutation'],
            ngen=self.params['max_generations'],
            stats=stats,
            halloffame=hof,
            verbose=True
        )

        # Process Results
        best = hof.items[0]
        print("-- Best Individual = ", best)
        print("-- Best Fitness = ", best.fitness.values[0])
        self.problem.printScheduleInfo(best)

        # Visualization
        min_fitness, avg_fitness = logbook.select("min", "avg")
        sns.set_style("whitegrid")
        plt.plot(min_fitness, color='red')
        plt.plot(avg_fitness, color='green')
        plt.xlabel('Generation')
        plt.ylabel('Min / Average Fitness')
        plt.title('Min and Average Fitness over Generations')
        plt.show()

        return best
