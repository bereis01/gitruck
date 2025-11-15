from .html import Html
from .args import ArgParse
from .gitruck import Gitruck

args = ArgParse()
gitruck = Gitruck(args.get_url())
html = Html()

truck_factor = gitruck.calculate_truck_factor()
html.add_truck_factor(truck_factor)

html.persist()
