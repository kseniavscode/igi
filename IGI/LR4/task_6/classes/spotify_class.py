from classes.base_class import *
from classes.statistic_mixin import *
class SpotifyClass(BaseClass, StatisticMixin):
    CYAN = '\033[96m'
    RESET = '\033[0m'

    def __init__(self, file_path):
        super().__init__(file_path)
        self.version = "1.0.0"

    def __str__(self):
        
        return f"SpotifyAnalyzer {self.CYAN}v{self.version}{self.RESET}"
    
    def get_popularity(self):
        """Method for getting colum with tracks 2020 and their popularity"""

        return self._df.loc[self._df['released_year'] == 2020, 'streams']
    
    def sliding_average(self, popularity):
        """Considers the sliding average in popularity"""

        return popularity.rolling(window=10).mean()
    
    def load_data(self):
        """Override load data for changing stream"""

        super().load_data()

        if self._df is not None:

            self._df['streams'] = pandas.to_numeric(self._df['streams'], errors='coerce')
            self._df = self._df.dropna(subset=['streams'])

    def analize_danceability(self):
        """How many times danceability average 10% most popular track more then most unpopular tracks"""

        high = self._df['streams'].quantile(0.9)
        low = self._df['streams'].quantile(0.1)

        popular = self._df[self._df['streams'] >= high]
        unpopular = self._df[self._df['streams'] <= low]

        mean_pop = popular['danceability_%'].mean()
        mean_unpop = unpopular['danceability_%'].mean()

        return popular, unpopular, self.calculate_ratio(mean_pop, mean_unpop)