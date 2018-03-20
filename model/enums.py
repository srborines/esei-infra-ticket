# (c) 2018 Baltasar MIT License <baltasarq@gmail.com>
# Implements an enum, missing in Python 2.7


class Enum:
    def __init__(self, values, start=None, default=None):
        """Creates a new Enum by accepting a dictionary
        pairing strings and values.

        :param start: The value of the first element, 0 by default.
        :param default: The default value, the first one by default.
        :param values: A dict in the form {'Orange': 1, 'Lemon': 2} (start ignored)
                        Or a list in the form ['Orange', 'Lemons']
        """
        assert len(values) > 0, "Enum.create(values): 'values' at least one element needed"

        if isinstance(values, list):
            self._start = start if start else 0
            order = self.start
            self.values = dict(zip(range(self.start, self.start + len(values)), values))
            for v in values:
                self.__dict__[Enum.from_value_to_constant(v)] = order
                order += 1
        elif isinstance(values, dict):
            self.values = dict(zip(values.values(), values.keys()))
            self._start = self.values.keys()[0]
            for k in values:
                self.__dict__[Enum.from_value_to_constant(k)] = values[k]

        self._default = default if default else self.start

    @property
    def start(self):
        return self._start

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    def ranged_get(self, x):
        """Returns the value if contained in this enum,
            or the minimum value if less or equal than start,
            or the maximum value if greater or equal than max.

        :param x: The value to take.
        :return: x, or the closest value to x, being min() or max(),
                    or the default, provided it is in the middle.
        """
        toret = x

        if x not in self.values:
            biggest = self.max()

            if x <= self.start:
                toret = self.start
            elif x >= biggest:
                toret = biggest
            else:
                toret = self.default

        return toret

    def get_or_default(self, x):
        """Returns the given value if corresponds to a contained value,
            or the default value if not found.

            :param x: The value to check its existence.
            :return: The given x, if it is part of this enum.
            """
        toret = x

        if x not in self.values:
            toret = self.default

        return toret

    def value_from_str(self, s):
        """Returns the corresponding value, given the name of the constant.

            :param s: The name of the constant, as a string.
            :return: The integer value, or throws KeyError if not found."""
        return self.__dict__[Enum.from_value_to_constant(s)]

    def __contains__(self, item):
        """Returns whether this enumerator contains the given item.

            :param item: Can be an integer or a string.
            :return: True if it is contained, False otherwise.
        """
        toret = False

        if isinstance(item, int):
            toret = item in self.values.keys()
        elif isinstance(item, str):
            try:
                toret = True if self.value_from_str(item) else False
            except KeyError:
                toret = False

        return toret

    def add(self, x):
        """Adds a new value to the enumeration.

            :param x: The new value, which takes the ordinal max plus one,
                        or a tuple (value, ordinal)
        """
        if isinstance(x, tuple):
            k = x[0]
            v = x[1]
        else:
            k = x
            v = self.max() + 1

        assert k, "Enum.add(): Key cannot be None"

        k = k.strip()
        assert k, "Enum.add(): Key cannot be empty"

        self.values[v] = k
        self.__dict__[Enum.from_value_to_constant(k)] = v
        return self

    def max(self):
        return self.values.keys()[-1]

    def min(self):
        return self.values.keys()[0]

    def __iadd__(self, x):
        return self.add(x)

    def __len__(self):
        return len(self.values.keys())

    @staticmethod
    def from_value_to_constant(s):
        """Converts 'LEMMON' or 'lemmon' to Lemon, or 'Won't fix' to WontFix

            :param s: The string with the value.
            :return: A string with the name of the constant."""
        toret = ""
        s = s.strip().lower()
        mays = True

        for ch in s:
            if ch.isalpha():
                if mays:
                    toret += ch.upper()
                    mays = False
                else:
                    toret += ch

            if ch.isspace() or ch == '-':
                mays = True

        return toret[0].upper() + toret[1:]
