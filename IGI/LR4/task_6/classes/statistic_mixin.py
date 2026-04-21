
class StatisticMixin():
    def calculate_ratio(self, mean, lower_mean):
        """Method for finding how many times chosen mean more than b like lower mean"""
        if lower_mean == 0:
            return 0
        return round(mean / lower_mean, 2)