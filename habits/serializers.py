from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    RelatedHabitValidator,
    DurationValidator,
    PleasantHabitValidator,
    RewardValidator,
    PeriodicityValidator,
)
from users.serializers import UserSerializer


class HabitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitValidator("related_habit", "reward"),
            DurationValidator("duration"),
            PleasantHabitValidator("related_habit", "pleasant_habit_sign"),
            RewardValidator("reward", "related_habit", "pleasant_habit_sign"),
            PeriodicityValidator("periodicity"),
        ]
