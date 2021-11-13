from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage(object):
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training(object):
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("<Method must be implemented in a child>")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    MULT_COEF_CALORIE_SPEED: ClassVar[int] = 18
    SUBTRAHEND_COEF_CALORIE_SPEED: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        # Calculation by the formula: (coef_18 * average_speed - coef_20)
        # * weight / M_IN_KM * duration_in_minutes
        average_speed = self.get_mean_speed()
        duration_in_minutes = self.duration * self.MIN_IN_HOUR
        return ((self.MULT_COEF_CALORIE_SPEED * average_speed
                - self.SUBTRAHEND_COEF_CALORIE_SPEED)
                * self.weight / self.M_IN_KM
                * duration_in_minutes)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    MULT_COEF_CALORIE_WEIGH: ClassVar[float] = 0.035
    SQUARE_COEF_CALORIE_SPEED: ClassVar[int] = 2
    MULT_COEF_CALORIE_GENERAL: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при хотьбе."""
        # Calculation by the formula: (coef_0.035 * weight +
        # (average_speed ** coef_2 // height) * coef_0.029 * weight)
        # * duration_in_minutes
        average_speed = self.get_mean_speed()
        duration_in_minutes = self.duration * self.MIN_IN_HOUR
        return ((self.MULT_COEF_CALORIE_WEIGH * self.weight
                + (average_speed ** self.SQUARE_COEF_CALORIE_SPEED
                 // self.height)
                * self.MULT_COEF_CALORIE_GENERAL * self.weight)
                * duration_in_minutes)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float

    LEN_STEP: ClassVar[float] = 1.38
    TERM_COEF_CALORIE_SPEED: ClassVar[float] = 1.1
    MULT_COEF_CALORIE_GENERAL: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при хотьбе."""
        # Calculation by the formula: (average_speed + 1.1) * 2 * weight
        return ((self.get_mean_speed() + self.TERM_COEF_CALORIE_SPEED)
                * self.MULT_COEF_CALORIE_GENERAL * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in workout_type_dict:
        return workout_type_dict[workout_type](*data)
    raise KeyError('A valid training code is required')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
