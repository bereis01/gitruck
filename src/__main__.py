from .html import Html
from .args import ArgParse
from .gitruck import Gitruck

args = ArgParse()
gitruck = Gitruck(args.get_url())
html = Html()

html.add_paragraph("Commit distribution")
commit_dist = gitruck.commit_dist()
html.add_image(commit_dist)
html.persist()
