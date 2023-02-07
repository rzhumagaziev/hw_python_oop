class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, 
                 training_type: str, 
                duration: float, 
                distance: float, 
                speed: float, 
                calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP)/self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance()/self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message: str = InfoMessage(
        self.__class__.__name__,
        self.duration,
        self.get_distance(),
        self.get_mean_speed(),
        self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT) 
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_H
            )


class SportsWalking(Training):

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED: float = 0.029
    KMH_TO_SEK: float = 0.278
    SM_IN_M: int = 100
    
    """Тренировка: спортивная ходьба."""
    def __init__(self, 
                action: int, 
                duration: float, 
                weight: float, 
                height: float):

        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_TO_SEK)**2
                   / (self.height / self.SM_IN_M))
                * self.CALORIES_MEAN_SPEED * self.weight)
                * (self.duration * self.MIN_IN_H))
    


class Swimming(Training):

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTI: int = 2

    def __init__(self, 
                 action: int, 
                duration: float, 
                weight: float, 
                length_pool: float, 
                count_pool: int):
        """Тренировка: плавание."""

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Рассчет средней скорости."""
        return (self.length_pool * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        
        """Рассчет количества затраченных калорий."""

        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MEAN_SPEED_MULTI * self.weight * self.duration)

training_classes = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

def read_package(workout_type: str, 
                 data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = training_classes[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info_result = info.get_message()
    print(info_result)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)