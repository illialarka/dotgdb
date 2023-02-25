from refreshers.breakpoints_refresher import BreakpointsRefresher

supporeted_refreshers = set([
    BreakpointsRefresher()
])


def select_refresher(scopes):
    return [refresher for refresher in supporeted_refreshers if refresher.scope in scopes]
