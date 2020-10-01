def collect_titles(badges):
    titles = []
    for badge in badges:
        titles.append(badge.badges.title)
    return set(titles)


def collect_badges(user):
    badge = user.reward_set.all()
    titles = collect_titles(badges=badge)

    rewards = []
    count = []
    for title in titles:
        rewards.append(user.reward_set.filter(badges__title=title).first())
        count.append(user.reward_set.filter(badges__title=title).count())

    return rewards, count


