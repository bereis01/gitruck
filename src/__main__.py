from .html import Html
from .args import ArgParse
from .gitruck import Gitruck

args = ArgParse()
gitruck = Gitruck(args.get_url())
html = Html()

html.add_paragraph(args.get_url())
html.persist()