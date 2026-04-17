import re
class ColorOutputMixin():

    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

    def print_pretty(self):
        part = []
        for k,x in self.__dict__.items():
            clear_k = re.sub(r"^\_", "", k)
            format_x = f"{x:<15}"
            colored = f"{self.CYAN}{clear_k}{self.RESET} : {self.BLUE}{format_x}{self.RESET}"
            part.append(colored)
        return "|".join(part)

    def __str__(self):
        return self.print_pretty()
        
