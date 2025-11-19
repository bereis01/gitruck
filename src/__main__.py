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

# Creates the visualization
html = Html()
html.add_logo()
html.add_truck_factor(truck_factor)
html.add_top_contributors(top_contributors)
html.persist()
