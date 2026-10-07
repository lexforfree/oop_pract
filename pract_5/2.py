# Почему здесь UnboundLocalError / NameError и как исправить?


class Counter:
    count = 0

    def increment(self):
        count += 1

    def show(self):
        print(count)


counter = Counter()

counter.increment()
counter.increment()
counter.show()