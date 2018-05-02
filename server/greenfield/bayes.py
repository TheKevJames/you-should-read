#!/usr/bin/env python
import asyncio

import asyncpg
import numpy


def normal_curve(start, end, count, ratio=0.15):
    center = (start + end) / 2
    scale = (end - start) * ratio

    dist = numpy.random.normal(loc=center, scale=scale, size=count)
    return list(sorted(dist))


def to_range(mid, minimum=1, maximum=10):
    if mid < (maximum + minimum) / 2:
        return (minimum, 2 * mid - minimum)
    return (2 * mid - maximum, maximum)


def fit_curve(source, target, sweight=1, tweight=1):
    for s, t in zip(source, target):
        yield (s * sweight + t * tweight) / (sweight + tweight)


class Media:
    def __init__(self, mid, name, ratings):
        self.mid = mid
        self.name = name
        self.ratings = ratings
        self.computed = 0
        self.computed_computed = 0

    @property
    def rating_count(self):
        return len(self.ratings)

    @property
    def rating_total(self):
        return sum(r.value for r in self.ratings)

    @property
    def rating_total_computed(self):
        return sum(r.computed for r in self.ratings)

    @property
    def rating_average(self):
        try:
            return self.rating_total / self.rating_count
        except ZeroDivisionError:
            return 0

    @property
    def rating_average_computed(self):
        try:
            return self.rating_total_computed / self.rating_count
        except ZeroDivisionError:
            return 0

    def apply(self, prior_count, prior_average):
        numerator = prior_average + self.rating_total
        numerator_computed = prior_average + self.rating_total_computed
        denominator = prior_count + self.rating_count
        self.computed = round(numerator / denominator, 3)
        self.computed_computed = round(numerator_computed / denominator, 3)


class Medias:
    def __init__(self, medias):
        self.medias = medias
        assert self.medias

    @staticmethod
    async def create(ratings):
        conn = await asyncpg.connect(host='localhost', user='postgres',
                                     database='postgres')
        medias = await conn.fetch('SELECT id, name FROM ysr.media')
        return Medias([Media(a, b, ratings.for_mid(a)) for a, b in medias])

    @property
    def average_rating(self):
        total = sum(m.rating_total for m in self.medias)
        count = sum(m.rating_count for m in self.medias)
        return total / count

    @property
    def average_rating_average(self):
        total = sum(m.rating_average for m in self.medias)
        return total / len(self.medias)

    @property
    def average_rating_count(self):
        total = sum(m.rating_count for m in self.medias)
        return total / len(self.medias)

    @property
    def average_rating_total(self):
        total = sum(m.rating_total for m in self.medias)
        return total / len(self.medias)

    @property
    def average_rating_total_average(self):
        return self.average_rating_average * self.average_rating_count

    @property
    def average_rating_computed(self):
        total = sum(m.rating_total_computed for m in self.medias)
        count = sum(m.rating_count for m in self.medias)
        return total / count

    @property
    def average_rating_average_computed(self):
        total = sum(m.rating_average_computed for m in self.medias)
        return total / len(self.medias)

    @property
    def average_rating_total_computed(self):
        total = sum(m.rating_total_computed for m in self.medias)
        return total / len(self.medias)

    @property
    def average_rating_total_average_computed(self):
        return self.average_rating_average_computed * self.average_rating_count

    def apply(self):
        # ar = self.average_rating
        # ara = self.average_rating_average
        arc = self.average_rating_count
        art = self.average_rating_total
        # arta = self.average_rating_total_average

        # print('{:<6}, {:<6}, {:<6}, {:<6}, {:<6}'.format(
        #     round(ar, 4), round(ara, 4), round(arc, 4), round(art, 4),
        #     round(arta, 4)))

        for item in self.medias:
            # # (C, A): expect items to have average rating A with confidence C
            # # eg. after C ratings expect average value A
            # item.apply(3, 5)

            # smooth from expected values and emphasize dupes
            item.apply(arc, art)

            # # stronger smoothing and dupes (ara is more centroid)
            # item.apply(arc, ara)

    def apply_computed(self):
        # ar = self.average_rating_computed
        # ara = self.average_rating_average_computed
        arc = self.average_rating_count
        art = self.average_rating_total_computed
        # arta = self.average_rating_total_average_computed

        # print('{:<6}, {:<6}, {:<6}, {:<6}, {:<6}'.format(
        #     round(ar, 4), round(ara, 4), round(arc, 4), round(art, 4),
        #     round(arta, 4)))

        for item in self.medias:
            # # (C, A): expect items to have average rating A with confidence C
            # # eg. after C ratings expect average value A
            # item.apply(3, 5)

            # smooth from expected values and emphasize dupes
            item.apply(arc, art)

            # # stronger smoothing and dupes (ara is more centroid)
            # item.apply(arc, ara)

    def score(self, out_prefix='std'):
        print('{:37} | Num | Avge. | Bayes | B Off | Norm. | N Off'.format(
            'Item'))
        print('{:37} | --- | ----- | ----- | ----- | ----- | -----'.format(
            '-' * 37))

        medias = list(sorted(self.medias, key=lambda x: -x.rating_average))
        medias_by_c = list(sorted(medias, key=lambda x: -x.computed))
        medias_by_cc = list(sorted(medias, key=lambda x: -x.computed_computed))

        for i, media in enumerate(medias):
            bayes_offset = i - medias_by_c.index(media)
            normal_offset = i - medias_by_cc.index(media)
            avg = round(media.rating_average, 3)
            print(
                '{:37} | {:3} | {:<5} | {:<5} | {:<5} | {:<5} | {:<5}'.format(
                    media.name, media.rating_count, avg, media.computed,
                    bayes_offset, media.computed_computed, normal_offset))

        with open('{}.std.txt'.format(out_prefix), 'w') as f:
            f.write('{:37} | Rating\n'.format('Item'))
            for media in medias:
                f.write('{:37} | {:<6}\n'.format(media.name, round(media.rating_average, 4)))

        with open('{}.computed.txt'.format(out_prefix), 'w') as f:
            f.write('{:37} | Rating\n'.format('Item'))
            for media in medias_by_c:
                f.write('{:37} | {:<6}\n'.format(media.name, round(media.computed, 4)))

        with open('{}.computed_from_computed.txt'.format(out_prefix), 'w') as f:
            f.write('{:37} | Rating\n'.format('Item'))
            for media in medias_by_cc:
                f.write('{:37} | {:<6}\n'.format(media.name, round(media.computed_computed, 4)))

        print()

    def show(self):
        print('{:37} | Avge.    |    {:37} | Avge.'.format('Item', 'Item'))
        print('{:37} | -----    |    {:37} | -----'.format('-' * 37, '-' * 37))

        medias = list(sorted(self.medias, key=lambda x: -x.rating_average))
        medias_sort = list(sorted(medias, key=lambda x: -x.computed_computed))
        # stable sort
        medias = list(sorted(medias_sort, key=lambda x: -x.rating_average))

        for lhs, rhs in zip(medias, medias_sort):
            avg = round(lhs.rating_average, 3)
            avg_sort = round(rhs.computed_computed, 3)
            print('{:37} | {:<5}    |    {:37} | {:<5}'.format(
                lhs.name, avg, rhs.name, avg_sort))


class Rating:
    # pylint: disable=too-few-public-methods
    def __init__(self, uid, mid, value):
        self.uid = uid
        self.mid = mid
        self.value = float(value or 0)
        self.computed = self.value


class Ratings:
    def __init__(self, ratings):
        self.ratings = ratings
        assert self.ratings

    @staticmethod
    async def create():
        conn = await asyncpg.connect(host='localhost', user='postgres',
                                     database='postgres')
        ratings = await conn.fetch('SELECT uid, mid, value FROM ysr.rating')

        return Ratings([Rating(a, b, c) for a, b, c in ratings])

    def for_mid(self, mid):
        return [r for r in self.ratings if r.mid == mid]

    def apply(self):
        # pylint: disable=too-many-locals
        user_rating_counts = []
        user_rating_totals = []
        user_rating_averages = []

        for uid in sorted({r.uid for r in self.ratings}):
            ratings = [r for r in self.ratings if r.uid == uid]
            assert ratings, f'no ratings for {uid}'

            urc = len(ratings)
            urt = sum(r.value for r in ratings)
            ura = urt / urc

            user_rating_totals.append(urt)
            user_rating_counts.append(urc)
            user_rating_averages.append(ura)

        aur = sum(user_rating_averages) / len(user_rating_averages)
        # aurc = sum(user_rating_counts) / len(user_rating_counts)
        # aurt = sum(user_rating_totals) / len(user_rating_totals)
        # aura = aurt / aurc

        # print('{:<6}, {:<6}, {:<6}, {:<6}'.format(
        #     round(aur, 4), round(aura, 4), round(aurc, 4), round(aurt, 4)))

        min_aur, max_aur = to_range(aur)
        # min_aura, max_aura = to_range(aura)

        for uid in sorted({r.uid for r in self.ratings}):
            ratings = [r for r in self.ratings if r.uid == uid]
            ratings = list(sorted(ratings, key=lambda r: r.value))
            assert ratings, f'no ratings for {uid}'

            # # fit user ratings to normal curve
            # curve = normal_curve(1, 10, len(ratings))

            # fit user ratings to average
            curve = normal_curve(min_aur, max_aur, len(ratings))

            # # fit user ratings to average of averages
            # curve = normal_curve(min_aura, max_aura, len(ratings))

            fitted = fit_curve((r.value for r in ratings), curve, sweight=3,
                               tweight=2)
            for rating, value in zip(ratings, fitted):
                rating.computed = round(value, 3)

    def score(self):
        for uid in sorted({r.uid for r in self.ratings}):
            ratings = [r for r in self.ratings if r.uid == uid]
            ratings = list(sorted(ratings, key=lambda r: r.value))
            assert ratings, f'no ratings for {uid}'

            def printable(xs):
                return [float('{}'.format(round(x, 1))) for x in xs]

            print('User:', uid)
            print([r.value for r in ratings])
            print(printable([r.computed for r in ratings]))
            print()


async def main():
    ratings = await Ratings.create()
    medias = await Medias.create(ratings)

    ratings.apply()
    # ratings.score()

    medias.apply()
    # medias.score()

    medias.apply_computed()
    # medias.score(out_prefix='computed')

    medias.show()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
