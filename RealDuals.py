from typing import Self, List, Tuple, Set
import matplotlib.pyplot as plt
import math 

def main():
    number: RealDual = RealDual(1, 1)
    print(number.sin())

class RealDual:

    def __init__(self, real: float, dual: float):
        self._real: float = real
        self._dual: float = dual

    @property
    def real(self) -> float:
        return self._real
    
    @property
    def dual(self) -> float:
        return self._dual

    @staticmethod
    def check(maybe_dual_number: Self | any) -> Self:
        if isinstance(maybe_dual_number, RealDual):
            return maybe_dual_number
        elif isinstance(maybe_dual_number, float) or isinstance(maybe_dual_number, int):
            return RealDual(float(maybe_dual_number), 0)
        # elif isinstance(maybe_dual_number, complex):
        #     return RealDual(maybe_dual_number, 0)
        else:
            raise ValueError("Not a dual number")

    def __neg__(self) -> Self:
        return RealDual(-self.real, -self.dual)

    def __pos__(self) -> Self:
        return RealDual(self.real, self.dual)
    
    def conjugate(self) -> Self:
        return RealDual(self.real, -self.dual)
    
    def reciprocate(self) -> Self:
        if self.real == 0:
            raise ZeroDivisionError("division by RealDual with zero real component")
        return self.conjugate() * (1 / self.real ** 2)

    def __add__(self, other: Self | any) -> Self:
        other: Self = RealDual.check(other)
        return RealDual(self.real + other.real, self.dual + other.dual)
    
    __radd__ = __add__
    
    def __mul__(self, other: Self | any) -> Self:
        other: Self = RealDual.check(other)
        return RealDual(self.real * other.real, other.real * self.dual + self.real * other.dual)
    
    __rmul__ = __mul__

    def __truediv__(self, denominator: Self | any) -> Self:
        denominator: Self = RealDual.check(denominator)
        return self * denominator.reciprocate()

    def __rtruediv__(self, numerator: Self | any) -> Self:
        numerator: Self = RealDual.check(numerator)
        return numerator / self

    def __pow__(self, power: Self | any) -> Self:
        power: Self = RealDual.check(power)
        if self.real > 0:
            return RealDual(self.real ** power.real, self.real ** (power.real - 1) * power.real * self.dual + self.real ** power.real * power.dual * math.log(self.real))
        elif self.real < 0:
            if power.dual == 0 and power.real.is_integer():
                if power.real < 0 and self.real == 0:
                    raise ValueError("Cannot reciprocate a dual number with zero real component")
                return RealDual(self.real ** power.real, self.real ** (power.real - 1) * power.real * self.dual)
        raise ValueError(f"{self:s} ** {power:s} cannot be performed")

    def __rpow__(self, base: Self | any) -> Self:
        base: Self = RealDual.check(base)
        return base ** self

    def exp(self, base: Self | any = math.e) -> Self:
        base: Self = RealDual.check(base)
        return base ** self
    
    def sin(self) -> Self:
        return RealDual(math.sin(self.real), self.dual * math.cos(self.real))
    
    def cos(self) -> Self:
        return RealDual(math.cos(self.real), -self.dual * math.sin(self.real))

    def __eq__(self, other: Self | any) -> bool:
        other = RealDual.check(other)
        return self.real == other.real and self.dual == other.dual
    
    def __neq__(self, other: Self | any) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"Dual({self._real}, {self._dual})" 
    
    def __str__(self) -> str:
        if self.dual == 1:
            return f"{self._real} + ε"
        return f"{self._real} + {self._dual}ε"

if __name__ == "__main__":
    main()