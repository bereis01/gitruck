from .html import Html
from .args import ArgParse
from .gitruck import Gitruck

# Parses CLI arguments
args = ArgParse()
git_url = args.get_url()

# Executes all operations
gitruck = Gitruck()
gitruck.load_repository_locally(args.get_url())
truck_factor, top_contributors = gitruck.calculate_truck_factor()
contributors_total, contributors_positive, contributors_negative = (
    gitruck.calculate_contributors_per_year()
)
contributions = gitruck.calculate_avg_contributions_per_year()
insertions, deletions = gitruck.calculate_avg_lines_changed()

# Creates the visualization
html = Html()
html.add_logo()
html.add_truck_factor(truck_factor)
html.add_top_contributors(top_contributors)
html.add_contributor_statistics(
    contributors_total, contributors_positive, contributors_negative
)
html.add_contribution_statistics(contributions, insertions, deletions)
html.persist()
