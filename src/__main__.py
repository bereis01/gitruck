from .html import Html
from .args import ArgParse
from .gitruck import Gitruck

args = ArgParse()
git_url = args.get_url()

gitruck = Gitruck(args.get_url())
truck_factor, top_contributors = gitruck.calculate_truck_factor()

html = Html()
html.add_truck_factor(truck_factor)
html.add_top_contributors(top_contributors)
html.persist()
