from PQueue import ArrayDeque
from RepeatingThread import RepeatingThread, get_trigger


class FourLevelFeedbackQueue:

    def __init__(self, max_active_num):
        self._max_active_num = max_active_num
        self._low = FeedbackQueue(4)
        self._medium = FeedbackQueue(3)
        self._high = FeedbackQueue(2)
        self._critical = FeedbackQueue(1)
        self._queue_list = [self._critical, self._high, self._medium, self._low]
        self._priority_map = dict()

    def is_empty(self):
        return self._low.is_empty() and self._medium.is_empty() \
               and self._high.is_empty and self._critical.is_empty

    def __contains__(self, item):
        return self._priority_map.__contains__(item)

    def add_item(self, p_key, minutes, priority_level):
        self._priority_map[p_key] = priority_level
        self._queue_list[priority_level].add_record(p_key, minutes)

    def schedule_next(self):
        if not self._critical.is_empty():
            self._critical.start_next()
        elif not self._high.is_empty():
            self._high.start_next()
        elif not self._medium.is_empty():
            self._medium.start_next()
        elif not self._low.is_empty():
            self._low.start_next()

        for key in self._high.age(self._critical):
            print("Gab {0}".format(key))
            self._priority_map[key] = 0
            print("{0} -> {1}".format(key, self._priority_map[key]))
        for key in self._medium.age(self._high):
            print(key)
            self._priority_map[key] = 1
        for key in self._low.age(self._medium):
            print(key)
            self._priority_map[key] = 2

    def finish_op(self, p_key):
        priority_level = self._priority_map[p_key]
        self._priority_map.pop(p_key)
        self._queue_list[priority_level].terminate(p_key)

    def get_expected_time(self, p_key):
        priority_level = self._priority_map[p_key]
        print("HAG")
        print(priority_level)
        options = self.get_active_ops()
        if options == []:
            options.append(0)
        else:
            options = [self._queue_list[self._priority_map[key]].get_length(key) for key in options]
        for i in range(priority_level):
            print(options)
            options = self._queue_list[i].get_all_delay_options(options)
        # print(total)
        print(options)
        # print("HGH {0}".format(self._queue_list[priority_level].get_delay(p_key, options)))
        # total += self._queue_list[priority_level].get_delay(p_key, active_ops)
        # print(total)
        return self._queue_list[priority_level].get_delay(p_key, options)

    def get_active_ops(self):
        active_ops = []
        for queue in self._queue_list:
            active_ops.extend(queue.active_ops())
            if len(active_ops) == self._max_active_num:
                break
        return active_ops

    def change_max_active_ops(self, delta):
        self._max_active_num += delta


class FeedbackQueue:
    def __init__(self, priority):
        self._deque = ArrayDeque()
        self._total_time = 0
        self._priority = priority
        self._head = 0

    def add_record(self, p_key, minutes):
        print("Adding {0}".format(p_key))
        new_op = _Node(p_key, minutes, self._priority)
        self._deque.add([new_op, None])
        self._total_time += minutes

    def _find_key(self, p_key):
        ind = 0
        for item in self._deque:
            if item[0].get_key() == p_key:
                return ind
            ind += 1
        return -1

    def get_length(self, p_key):
        ind = 0
        for item in self._deque:
            if item[0].get_key() == p_key:
                return item[0].get_operation_time()
            ind += 1
        return -1

    def start_next(self):
        next_op = self._deque[self._head]
        next_op[1] = RepeatingThread(get_trigger(), 2, self._tick, self._head)
        next_op[1].start()
        self._head += 1

    def terminate(self, p_key):
        index = self._find_key(p_key)

        self._deque[index][1].stop()
        next_op = self._deque.remove()
        self._total_time -= next_op[0].get_operation_time()

        for i in range(self._head):
            if self._deque[i][0].is_set():
                self._deque.remove()
            else:
                break

    def is_empty(self):
        return self._deque.is_empty()

    def get_all_delay_options(self, options):
        min_ind = 0
        for i in range(self._deque.size()):
            if self._deque[i][1] is None:
                options[min_ind] += self._deque[i][0].get_operation_time()
                print("Updated options: {0}".format(options))

                min = options[0]
                min_ind = 0
                for m in range(1, len(options)):
                    print("Try out {0}".format(options[m]))
                    if options[m] < min:
                        min = options[m]
                        min_ind = m
        return options

    def get_delay(self, p_key, options):
        index = self._find_key(p_key)
        print("{0} found at {1}".format(p_key, index))

        if self._deque[index][1] is not None:
            return 0

        min_ind = options.index(min(options))
        for i in range(index):
            if self._deque[i][1] is None:
                options[min_ind] += self._deque[i][0].get_operation_time()
                print("Updated options: {0}".format(options))

                min_ind = options.index(min(options))

        return options[min_ind]

    def get_total_time(self):
        return self._total_time

    def active_ops(self):
        active_ops = []
        for node in self._deque:
            if node[1] is not None:
                active_ops.append(node[0].get_key())
            else:
                break
        return active_ops

    def _tick(self, ind):
        node = self._deque[ind][0]
        if node.get_operation_time() > 0:
            delta = -1
            node.set_operation_time(delta)
            self._total_time += delta

    def age(self, next_level):
        if next_level is None:
            return []

        changed = []
        max = self._deque.size()
        for i in range(max):
            print(self._deque[i])
            if self._deque[i][1] is None and self._deque[i][0].age():
                print("Node {0} is aging!".format(i))
                changed.append(i)

        for i in range(len(changed)):
            print("JJJJJ {0}".format(changed))
            temp = changed[i] - i
            print(temp)
            node = self._deque[temp][0]
            changed[i] = self._deque[temp][0].get_key()
            print(temp)

            self._total_time -= node.get_operation_time()
            next_level.add_record(node.get_key(), node.get_operation_time())
            self._deque.force_remove(temp)
        print(changed)
        return changed


class _Node:
    def __init__(self, p_key, minutes, age_time):
        self._key = p_key
        self._op_time = minutes
        self._age = 0
        self._age_inc = age_time

    def get_key(self):
        return self._key

    def get_operation_time(self):
        return self._op_time

    def set_operation_time(self, delta):
        self._op_time += delta

    def age(self):
        self._age = self._age + 1
        print(self._age)
        return self._age % self._age_inc == 0
